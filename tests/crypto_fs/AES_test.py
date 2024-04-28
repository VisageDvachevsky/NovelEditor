from app.crypto_fs.AES import AES
from app.crypto_fs.utility import random_key


def test_key_size():
    bit_size = 256
    byte_size = bit_size / 8
    assert AES.key_size == byte_size


def test_encrypt_decrypt():
    test_message = "Test message"
    aes = AES(random_key())
    encrypted_message = aes.encrypt(test_message.encode())
    decrypted_message = aes.decrypt(encrypted_message).decode()
    assert test_message == decrypted_message


def test_immutability():
    test_message = "Test message"
    key = random_key()
    aes_r = AES(key)
    aes_l = AES(key)

    encrypted_message_r = aes_r.encrypt(test_message.encode())
    encrypted_message_l = aes_l.encrypt(test_message.encode())

    decrypted_message_rl = aes_l.decrypt(encrypted_message_r).decode()
    decrypted_message_lr = aes_r.decrypt(encrypted_message_l).decode()

    assert decrypted_message_rl == test_message
    assert decrypted_message_lr == test_message
