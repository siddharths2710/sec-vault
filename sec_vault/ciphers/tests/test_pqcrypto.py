import pytest
import ciphers.pqcrypto as pqcrypto

CONFIG_FIELDS = ("mlkem_private_key", "x25519_private_key", "mldsa_private_key")

def _arg_params(encryptor):
    """Extracts the key material the cipher factory flushes into the config"""
    attributes = vars(encryptor)
    return {field: attributes["_Encryptor__{}".format(field)]
            for field in CONFIG_FIELDS}

def test_cipher():
    test_message = "test: ML-KEM-768 + ML-DSA-65"
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    cipher_text = enc.encrypt(test_message)
    dec = pqcrypto.Decryptor(cipher_params={}, arg_params=_arg_params(enc))
    plain_text = dec.decrypt(cipher_text)
    assert plain_text == test_message

def test_envelope_format():
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    cipher_text = enc.encrypt("[]")
    assert cipher_text.startswith(pqcrypto.SUITE_MAGIC)
    assert len(cipher_text) > pqcrypto.HEADER_SIZE + pqcrypto.SIGNATURE_SIZE

def test_fresh_envelope_per_message():
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    assert enc.encrypt("[]") != enc.encrypt("[]")

def test_config_provided_keys():
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    same_keys = pqcrypto.Encryptor(cipher_params={}, arg_params=_arg_params(enc))
    assert _arg_params(same_keys) == _arg_params(enc)
    dec = pqcrypto.Decryptor(cipher_params={}, arg_params=_arg_params(same_keys))
    assert dec.decrypt(same_keys.encrypt("bytes in the vault")) == "bytes in the vault"

def test_key_sizes():
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    mlkem_key = pqcrypto._load_mlkem_key(_arg_params(enc)["mlkem_private_key"])
    assert len(mlkem_key.public_key().public_bytes_raw()) == 1184
    mldsa_key = pqcrypto._load_mldsa_key(_arg_params(enc)["mldsa_private_key"])
    assert len(mldsa_key.public_key().public_bytes_raw()) == 1952

@pytest.mark.parametrize("offset", [
    len(pqcrypto.SUITE_MAGIC),                      # ML-KEM ciphertext
    pqcrypto.HEADER_SIZE - pqcrypto.NONCE_SIZE,     # nonce
    pqcrypto.HEADER_SIZE + 4,                       # AES-GCM ciphertext
])
def test_tampered_envelope_rejected(offset):
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    dec = pqcrypto.Decryptor(cipher_params={}, arg_params=_arg_params(enc))
    cipher_text = bytearray(enc.encrypt("vault contents"))
    cipher_text[offset] ^= 0x01
    with pytest.raises(Exception, match="signature verification failed"):
        dec.decrypt(bytes(cipher_text))

def test_unsigned_envelope_rejected():
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    dec = pqcrypto.Decryptor(cipher_params={}, arg_params=_arg_params(enc))
    cipher_text = enc.encrypt("vault contents")
    with pytest.raises(Exception):
        dec.decrypt(cipher_text[:-pqcrypto.SIGNATURE_SIZE])

def test_foreign_suite_envelope_rejected():
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    dec = pqcrypto.Decryptor(cipher_params={}, arg_params=_arg_params(enc))
    cipher_text = b"not-a-pqc-envelope" + enc.encrypt("vault contents")
    with pytest.raises(Exception, match="pqcrypto"):
        dec.decrypt(cipher_text)

def test_foreign_keys_rejected():
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    other = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    cipher_text = enc.encrypt("vault contents")
    dec = pqcrypto.Decryptor(cipher_params={}, arg_params=_arg_params(other))
    with pytest.raises(Exception):
        dec.decrypt(cipher_text)

def test_invalid_key_material_rejected():
    enc = pqcrypto.Encryptor(cipher_params={}, arg_params={})
    arg_params = _arg_params(enc)
    arg_params["mlkem_private_key"] = "not-a-key"
    with pytest.raises(Exception, match="mlkem_private_key"):
        pqcrypto.Decryptor(cipher_params={}, arg_params=arg_params)

def test_decryption_requires_key_material():
    with pytest.raises(Exception, match="missing"):
        pqcrypto.Decryptor(cipher_params={}, arg_params={})
