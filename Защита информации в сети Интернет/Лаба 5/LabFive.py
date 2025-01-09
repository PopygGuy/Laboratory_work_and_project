from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

import os
import random

def generate_large_prime(min_value):
    """Генерирует случайное простое число больше min_value."""
    while True:
        candidate = random.randint(min_value + 1, min_value * 10)  # Генерируем случайное число
        if is_prime(candidate):  # Проверяем, является ли оно простым
            return candidate

def is_prime(num):
    """Проверка на простоту числа."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def get_prime_input(prompt):
    """Запрашивает ввод от пользователя и проверяет, является ли число простым и больше 2128."""
    while True:
        try:
            num = int(input(prompt))
            if num >= 2128 and is_prime(num):
                return num  # Возвращает простое число
            else:
                print("Ошибка: число должно быть простым и больше 2128. Попробуйте снова.")
        except ValueError:
            print("Ошибка: введите корректное целое число.")

# Вызов функции для получения простого числа
p = get_prime_input("Введите простое число p (больше 2128): ")
q = get_prime_input("Введите простое число q (больше 2128): ")

def generate_keys():
    # Генерируем открытый и закрытый ключи RSA с использованием p и q
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
# Сохраняем ключи в файлы
    with open('private_key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    with open('public_key.pem', 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

    print(f"Сгенерированы простые числа p: {p}, q: {q}. Ключи успешно сгенерированы и сохранены.")

def encrypt_file(input_file, output_file):
    with open('public_key.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Сохраняем зашифрованный текст в шестнадцатеричном формате (hex)
    with open(output_file, 'wb') as f:
        f.write(ciphertext.hex().encode())  # Кодируем как hex для безопасного хранения

    print("Файл успешно зашифрован.")


def decrypt_file(input_file, output_file):
    with open('private_key.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

    with open(input_file, 'rb') as f:
        hex_ciphertext = f.read().decode()  # Декодируем как текст
        ciphertext = bytes.fromhex(hex_ciphertext)  # Преобразуем обратно в байты из hex

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_file, 'wb') as f:
        f.write(plaintext)

    print("Файл успешно расшифрован.")

if __name__ == "__main__":
    user_text = input("Введите текст, который нужно зашифровать: ")
    with open('input.txt', 'w', encoding='utf-8') as f:
        f.write(user_text)

    generate_keys()
    encrypt_file('input.txt', 'encrypted.txt')
    decrypt_file('encrypted.txt', 'decrypted.txt')
    print("Процесс завершен.")