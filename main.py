from Decrypt import Decrypt
from Encrypt import Encrypt
from KeyGenerator import check_size, KeyGenerator

print("Введите директорию, в которой будут сохранены ключи: ")
key_direct = input()
print("Введите длину ключа: ")
size = check_size()
KeyGenerator(key_direct, size).Generate()
print("Введите путь к тексту, который нужно зашифровать: ")
file = input()
print("\nВведите путь, в который хотите сохранить зашифрованный текст: ")
encrypt_file = input()
Encrypt(file, key_direct, encrypt_file).Encode()
print("\nВведите путь, в который хотите сохранить расшифрованный текст: ")
decrypt_file = input()
Decrypt(encrypt_file, key_direct, decrypt_file).Decode()
"""
https://ru.wikipedia.org/wiki/Blowfish
"""