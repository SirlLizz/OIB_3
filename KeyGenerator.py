import os

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import algorithms


def check_size() -> int:
    while True:
        length = input()
        if int(length) >= 4 and int(length) <=56:
            break
        print("Ключ некорректен, повторите ввод(4<_<56): ")

    return int(length)


class KeyGenerator:
    key_directory = ""
    size = 0

    def __init__(self, key_directory, size):
        self.key_directory = key_directory
        self.size = size

    def Generate(self) -> None:
        sym_key = algorithms.Blowfish(os.urandom(self.size))
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_key = key
        public_key = key.public_key()
        f = open(self.key_directory + "\\public.pem", "wb")
        f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PublicFormat.SubjectPublicKeyInfo))
        f.close()
        f = open(self.key_directory + '\\private.pem', "wb")
        f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                          format=serialization.PrivateFormat.TraditionalOpenSSL,
                                          encryption_algorithm=serialization.NoEncryption()))
        f.close()
        encrypt_sym_key = public_key.encrypt(sym_key.key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                       algorithm=hashes.SHA256(), label=None))
        f = open(self.key_directory + '\\encrypt_sym.txt', "wb")
        f.write(encrypt_sym_key)
        f.close()
