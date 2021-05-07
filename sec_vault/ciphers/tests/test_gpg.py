#! /usr/bin/env python3

# This test simulates the scenario where the message is signed using
# sender's gpg key and is decrypted by recipient's gpg key

import os
import pytest
import gnupg
import time
import random
import string
import ciphers.gpg as gpg

GPGBINARY = os.environ.get('GPGBINARY', 'gpg')
keys_dir = "pytest_keys"
if not os.path.isdir(keys_dir): os.mkdir(keys_dir)
gpg_obj = gnupg.GPG(gpgbinary=GPGBINARY, gnupghome=keys_dir)

@pytest.fixture
def key_data():
    global gpg_obj
    gen_email = lambda: "{}@test".format("".join(
        [random.choice(string.ascii_lowercase) for i in range(random.randint(6,10))]
        ))
    gen_passphrase = lambda: "".join(
                [random.choice(string.printable) for i in range(random.randint(30,50))]
                    ).strip().lstrip()
    credential_pair = {
        "sender": {
            "name_email": gen_email(),
            "passphrase": gen_passphrase()
        },
        "recipient": {
            "name_email": gen_email(),
            "passphrase": gen_passphrase()
        }
    }
    result_pair = {}
    for credential in credential_pair:
        key_input = gpg_obj.gen_key_input(**credential_pair[credential])
        result_pair.update({ credential: gpg_obj.gen_key(key_input)})
    return {
        "credential_pair": credential_pair,
        "result_pair": result_pair
    }

def test_cipher(key_data, monkeypatch):
    test_message = "sec-vault: test_gpg"
    credential_pair = key_data['credential_pair']
    result_pair = key_data['result_pair']
    gpg_encryptor = gpg.Encryptor(
        arg_params = {
            "recipients": [result_pair['recipient'].fingerprint],
            "sign": result_pair['sender'].fingerprint,
            'passphrase': credential_pair['sender']['passphrase'],
            "symmetric": False
        })
    gpg_decryptor = gpg.Decryptor(
        arg_params= {
            "passphrase": credential_pair['recipient']['passphrase']
        })
    monkeypatch.setattr(gpg_encryptor, "cipher", gpg_obj)
    monkeypatch.setattr(gpg_decryptor, "cipher", gpg_obj)
    cipher_text = gpg_encryptor.encrypt(test_message)
    assert cipher_text != test_message
    plain_text = gpg_decryptor.decrypt(cipher_text)
    assert plain_text == test_message
