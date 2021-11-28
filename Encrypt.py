import os
import pickle

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pad


class Encrypt:
    file = ""
    key_direct = ""
    encrypt_file = ""

    def __init__(self, file, key_direct, encrypt_file):
        self.file = file
        self.key_direct = key_direct
        self.encrypt_file = encrypt_file

    def Encode(self):
        f = open(self.key_direct + '\\encrypt_sym.txt', "rb")
        encrypt_sym_key = f.read()
        f.close()
        f = open(self.key_direct + '\\private.pem', "rb")
        private_key = serialization.load_pem_private_key(f.read(), password=None)
        f.close()
        sym_key = private_key.decrypt(encrypt_sym_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                    algorithm=hashes.SHA256(), label=None))
        f = open(self.file, "r")
        output_text = f.read()
        f.close()
        padder = pad.ANSIX923(8).padder()
        text = bytes(output_text, 'UTF-8')
        padded_text = padder.update(text) + padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.Blowfish(sym_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text)
        setting = {}
        setting['text'] = c_text
        setting['iv'] = iv
        f = open(self.encrypt_file, "wb")
        pickle.dump(setting, f)
        f.close()
