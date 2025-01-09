from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

# Функция для генерации ключа
def generate_key(file_path):
    key = os.urandom(8)  # Длина ключа DES: 8 байт
    with open(file_path, 'wb') as key_file:
        key_file.write(key)

# Загрузка ключа из файла
def load_key(file_path):
    with open(file_path, 'rb') as key_file:
        return key_file.read()

# Шифрование файла
def encrypt_file(input_file, key_file, output_file):
    key = load_key(key_file)
    cipher = DES.new(key, DES.MODE_ECB)  # Используем режим ECB

    with open(input_file, 'rb') as f:  # Читаем файл в бинарном режиме
        plaintext = f.read()

    # Шифруем данные
    ciphertext = cipher.encrypt(pad(plaintext, DES.block_size))

    # Сохраняем зашифрованный результат
    with open(output_file, 'wb') as f:
        f.write(ciphertext)

# Расшифровка файла
def decrypt_file(input_file, key_file, output_file):
    key = load_key(key_file)
    cipher = DES.new(key, DES.MODE_ECB)

    with open(input_file, 'rb') as f:  # Читаем зашифрованные данные в бинарном режиме
        ciphertext = f.read()

    # Расшифровываем данные
    plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)

    # Сохраняем расшифрованный результат
    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Основная программа
if __name__ == "__main__":
    # Получаем текст от пользователя
    user_text = input("Введите текст, который нужно зашифровать: ")

    # Сохраняем введенный текст в исходный файл
    with open('plaintext.txt', 'w', encoding='utf-8') as f:
        f.write(user_text)

    # Генерация ключа
    generate_key('key.bin')

    # Шифрование
    encrypt_file('plaintext.txt', 'key.bin', 'encrypted.txt')

    # Расшифровка
    decrypt_file('encrypted.txt', 'key.bin', 'decrypted.txt')

    print("Текст успешно зашифрован и расшифрован.")
    print("Исходный текст сохранен в 'plaintext.txt', зашифрованный текст в 'encrypted.txt', а расшифрованный текст в 'decrypted.txt'.")