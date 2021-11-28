import pickle

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as pad


class Decrypt:
    encrypt_file = ""
    key_direct = ""
    decrypt_file = ""

    def __init__(self, encrypt_file, key_direct, decrypt_file):
        self.encrypt_file = encrypt_file
        self.key_direct = key_direct
        self.decrypt_file = decrypt_file

    def Decode(self):
        f = open(self.key_direct + '/encrypt_sym.txt', "rb")
        encrypt_sym_key = f.read()
        f.close()
        f = open(self.key_direct + '/private.pem', "rb")
        private_key = serialization.load_pem_private_key(f.read(), password=None)
        f.close()
        sym_key = private_key.decrypt(encrypt_sym_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                    algorithm=hashes.SHA256(), label=None))
        f = open(self.encrypt_file, "rb")
        data = pickle.load(f)
        f.close()
        text_to_decrypt = data['text']
        iv = data["iv"]
        cipher = Cipher(algorithms.Blowfish(sym_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(text_to_decrypt) + decryptor.finalize()
        unpadder = pad.ANSIX923(8).unpadder()
        unpadded_dc_text = unpadder.update(dc_text)
        f = open(self.decrypt_file, "w")
        f.write(str(unpadded_dc_text)[2:-1])
        f.close()
