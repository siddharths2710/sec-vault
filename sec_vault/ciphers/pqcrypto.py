"""Post-quantum cipher suite based on ML-KEM (FIPS 203) and ML-DSA (FIPS 204).

The vault is a long-lived blob of secrets, so both confidentiality and
authenticity have to survive a cryptographically relevant quantum computer:

  * confidentiality: ML-KEM-768 encapsulated against the vault key, combined
    with an ephemeral X25519 exchange (hybrid key establishment) and used to
    derive a per-message AES-256-GCM key through HKDF-SHA256. The classical
    half keeps the vault safe even if ML-KEM is broken.
  * authenticity: ML-DSA-65 signs the whole envelope, so a vault file tampered
    with outside of this tool is rejected before anything is decrypted.

Each cipher text is a self-describing envelope:

    b"PQC1" | ML-KEM ciphertext | X25519 ephemeral public key | nonce
            | AES-256-GCM ciphertext | ML-DSA-65 signature

The signature covers every preceding byte of the envelope. Key material is
kept in the cipher config as base64 (seed form for ML-KEM/ML-DSA), matching the
way the other suites persist their parameters.
"""
import os
import base64

from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa, mlkem, x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import (
    Encoding, NoEncryption, PrivateFormat, PublicFormat
)

from . import cipher

SUITE_MAGIC = b"PQC1"
SIGN_CONTEXT = b"sec-vault/pqcrypto/v1"
KDF_INFO = b"sec-vault/pqcrypto/v1/mlkem768+x25519"

KEM_CIPHERTEXT_SIZE = 1088
X25519_PUBLIC_KEY_SIZE = 32
NONCE_SIZE = 12
SIGNATURE_SIZE = 3309
HEADER_SIZE = len(SUITE_MAGIC) + KEM_CIPHERTEXT_SIZE \
              + X25519_PUBLIC_KEY_SIZE + NONCE_SIZE

MLKEM_SEED_SIZE = 64
MLDSA_SEED_SIZE = 32
X25519_PRIVATE_KEY_SIZE = 32


def _encode_key(raw_bytes: bytes) -> str:
    return base64.b64encode(raw_bytes).decode('ascii')


def _decode_key(value, expected_size: int, name: str) -> bytes:
    """Decodes base64 key material, tolerating raw bytes from *_bytes configs"""
    if value is None:
        raise Exception("missing {} in cipher config".format(name))
    encoded = value if isinstance(value, bytes) else value.encode('ascii')
    candidates = [encoded]
    try:
        candidates.insert(0, base64.b64decode(encoded, validate=True))
    except Exception:
        pass
    for raw in candidates:
        if len(raw) == expected_size:
            return raw
    raise Exception("{} must be {} bytes, got {}".format(
        name, expected_size, len(encoded)))


def _load_mlkem_key(value):
    if value is None:
        return mlkem.MLKEM768PrivateKey.generate()
    return mlkem.MLKEM768PrivateKey.from_seed_bytes(
        _decode_key(value, MLKEM_SEED_SIZE, "mlkem_private_key"))


def _load_x25519_key(value):
    if value is None:
        return x25519.X25519PrivateKey.generate()
    return x25519.X25519PrivateKey.from_private_bytes(
        _decode_key(value, X25519_PRIVATE_KEY_SIZE, "x25519_private_key"))


def _load_mldsa_key(value):
    if value is None:
        return mldsa.MLDSA65PrivateKey.generate()
    return mldsa.MLDSA65PrivateKey.from_seed_bytes(
        _decode_key(value, MLDSA_SEED_SIZE, "mldsa_private_key"))


def _derive_key(mlkem_secret: bytes, x25519_secret: bytes) -> bytes:
    """Hybrid combiner: concatenate both shared secrets and run them through
    HKDF-SHA256 so that the derived key is safe as long as either half holds."""
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=KDF_INFO
    ).derive(mlkem_secret + x25519_secret)


class Encryptor(cipher.Encryptor):
    """Encryptor for the post-quantum hybrid suite.

    Key material is dunder-prefixed so that the cipher factory can flush it
    into the config file for later decryption.
    """
    def __init__(self, cipher_params: dict = {}, arg_params: dict = {}, **kwargs):
        """Initializer for the post-quantum primitives

        :param cipher_params: parameters consumed by the base cipher library
        :type dict
        :param arg_params: key material and encoding for the suite
        :type dict
        """
        self.__encoding = arg_params.get("encoding", "utf-8")
        try:
            self._kem_key = _load_mlkem_key(arg_params.get("mlkem_private_key"))
            self._x25519_key = _load_x25519_key(arg_params.get("x25519_private_key"))
            self._mldsa_key = _load_mldsa_key(arg_params.get("mldsa_private_key"))
        except UnsupportedAlgorithm as exception_obj:
            raise Exception(
                "the installed cryptography backend does not support ML-KEM/ML-DSA, "
                "upgrade to cryptography>=47 with an OpenSSL 3.5+ or AWS-LC backend"
            ) from exception_obj
        self.__mlkem_private_key = _encode_key(self._kem_key.private_bytes_raw())
        self.__x25519_private_key = _encode_key(self._x25519_key.private_bytes(
            Encoding.Raw, PrivateFormat.Raw, NoEncryption()))
        self.__mldsa_private_key = _encode_key(self._mldsa_key.private_bytes_raw())

    def encrypt(self, plain_text: str):
        """Encrypts a single message using hybrid ML-KEM-768 + X25519 key
        establishment, AES-256-GCM and an ML-DSA-65 signature

        :param plain_text: input message for encryption
        :type str
        :returns: signed cipher envelope for secure storage
        :rtype bytes
        """
        mlkem_secret, kem_cipher_text = self._kem_key.public_key().encapsulate()
        ephemeral_key = x25519.X25519PrivateKey.generate()
        ephemeral_public = ephemeral_key.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw)
        x25519_secret = ephemeral_key.exchange(self._x25519_key.public_key())
        key = _derive_key(mlkem_secret, x25519_secret)
        nonce = os.urandom(NONCE_SIZE)
        header = SUITE_MAGIC + kem_cipher_text + ephemeral_public + nonce
        cipher_text = AESGCM(key).encrypt(
            nonce, plain_text.encode(self.__encoding), header)
        payload = header + cipher_text
        return payload + self._mldsa_key.sign(payload, context=SIGN_CONTEXT)


class Decryptor(cipher.Decryptor):
    """Decryptor for the post-quantum hybrid suite"""
    def __init__(self, cipher_params: dict = {}, arg_params: dict = {}, **kwargs):
        """Initializer for the post-quantum primitives

        :param cipher_params: parameters consumed by the base cipher library
        :type dict
        :param arg_params: key material and encoding for the suite
        :type dict
        """
        self.__encoding = arg_params.get("encoding", "utf-8")
        missing = [field for field in ("mlkem_private_key", "x25519_private_key",
                                       "mldsa_private_key")
                   if arg_params.get(field) is None]
        if missing:
            raise Exception("missing {} in cipher config for decryption".format(
                ", ".join(missing)))
        try:
            self._kem_key = _load_mlkem_key(arg_params.get("mlkem_private_key"))
            self._x25519_key = _load_x25519_key(arg_params.get("x25519_private_key"))
            self._mldsa_key = _load_mldsa_key(arg_params.get("mldsa_private_key"))
        except UnsupportedAlgorithm as exception_obj:
            raise Exception(
                "the installed cryptography backend does not support ML-KEM/ML-DSA, "
                "upgrade to cryptography>=47 with an OpenSSL 3.5+ or AWS-LC backend"
            ) from exception_obj
        self._mldsa_public_key = self._mldsa_key.public_key()

    def decrypt(self, cipher_text):
        """Verifies and decrypts a signed post-quantum envelope

        :param cipher_text: signed envelope produced by this suite
        :type bytes
        :returns: decrypted plain text
        :rtype str
        """
        envelope = bytes(cipher_text)
        if len(envelope) <= HEADER_SIZE + SIGNATURE_SIZE:
            raise Exception("truncated post-quantum vault envelope")
        if envelope[:len(SUITE_MAGIC)] != SUITE_MAGIC:
            raise Exception(
                "vault was not encrypted with the pqcrypto suite")
        payload, signature = envelope[:-SIGNATURE_SIZE], envelope[-SIGNATURE_SIZE:]
        try:
            self._mldsa_public_key.verify(signature, payload, context=SIGN_CONTEXT)
        except InvalidSignature as exception_obj:
            raise Exception(
                "ML-DSA signature verification failed: vault contents were "
                "modified or the config holds a different signing key"
            ) from exception_obj
        offset = len(SUITE_MAGIC)
        kem_cipher_text = payload[offset:offset + KEM_CIPHERTEXT_SIZE]
        offset += KEM_CIPHERTEXT_SIZE
        ephemeral_public = payload[offset:offset + X25519_PUBLIC_KEY_SIZE]
        offset += X25519_PUBLIC_KEY_SIZE
        nonce = payload[offset:offset + NONCE_SIZE]
        offset += NONCE_SIZE
        aes_cipher_text = payload[offset:]
        mlkem_secret = self._kem_key.decapsulate(kem_cipher_text)
        x25519_secret = self._x25519_key.exchange(
            x25519.X25519PublicKey.from_public_bytes(ephemeral_public))
        key = _derive_key(mlkem_secret, x25519_secret)
        plain_text = AESGCM(key).decrypt(nonce, aes_cipher_text, payload[:offset])
        return plain_text.decode(self.__encoding)


if __name__ != "__main__":
    CIPHER_PKG = {}
    CIPHER_ARGS = {}
