import base64
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Функция генерации случайного DES ключа
def generate_des_key():
    return get_random_bytes(8)  # DES ключ длиной 64 бита (8 байт)

# Функция шифрования открытого текста
def encrypt_text(plaintext, des_key):
    cipher = DES.new(des_key, DES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
    return cipher.iv + ct_bytes  # Возвращаем IV + зашифрованный текст

# Функция генерации RSA ключей
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# Функция шифрования DES ключа с помощью RSA
def encrypt_key_with_rsa(des_key, public_key):
    ciphertext = public_key.encrypt(
        des_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# Основная функция для шифрования
def main_encrypt():
    # Получаем текст для шифрования
    plaintext = input("Введите текст для шифрования: ")

    # Генерируем ключ для DES
    des_key = generate_des_key()

    # Шифруем текст
    encrypted_text = encrypt_text(plaintext, des_key)

    # Генерируем пару ключей RSA
    private_key, public_key = generate_rsa_key_pair()

    # Шифруем DES ключ с помощью RSA
    encrypted_des_key = encrypt_key_with_rsa(des_key, public_key)

    # Кодируем зашифрованные данные в формате Base64 для текстового представления
    encrypted_text_b64 = base64.b64encode(encrypted_text)
    encrypted_des_key_b64 = base64.b64encode(encrypted_des_key)

    # Сохранение зашифрованного текста и ключи в текстовые файлы
    with open("encrypted_text.txt", "wb") as f:
        f.write(encrypted_text_b64)

    with open("encrypted_key.txt", "wb") as f:
        f.write(encrypted_des_key_b64)

    # Сохранение открытого ключа RSA
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    # Сохранение закрытого ключа RSA в файле
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Сохранение в исходный текст в файл
    with open("original_text.txt", "w") as f:
        f.write(plaintext)

    print("Текст зашифрован и сохранен в файл, а ключ DES зашифрован и тоже сохранен.")
    print("Исходный текст сохранен в 'original_text.txt'.")

# Функция дешифрования DES ключа
def decrypt_key_with_rsa(encrypted_key, private_key):
    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Функция дешифрования текста
def decrypt_text(encrypted_text, des_key):
    iv = encrypted_text[:8]  # Первые 8 байт - это IV
    cipher = DES.new(des_key, DES.MODE_CBC, iv)
    decrypted_padded_text = cipher.decrypt(encrypted_text[8:])  # Убираем IV
    return unpad(decrypted_padded_text, DES.block_size).decode()

# Основная функция для дешифрования
def main_decrypt():
    # Загружаем закрытый ключ RSA
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Прочтение зашифрованного ключа DES и декодирока из Base64
    with open("encrypted_key.txt", "rb") as f:
        encrypted_des_key_b64 = f.read()
    encrypted_des_key = base64.b64decode(encrypted_des_key_b64)

    # Дешифровка ключа DES
    des_key = decrypt_key_with_rsa(encrypted_des_key, private_key)

    # Прочтение зашифрованного текста и декодирока из Base64
    with open("encrypted_text.txt", "rb") as f:
        encrypted_text_b64 = f.read()
    encrypted_text = base64.b64decode(encrypted_text_b64)

    # Дешифровка текста
    decrypted_text = decrypt_text(encrypted_text, des_key)

    # Сохрание расшифрованного текст в файл
    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted_text)

    print("Дешифрованный текст:", decrypted_text)
    print("Расшифрованный текст сохранен в 'decrypted_text.txt'.")

# Выбор функции для запуска шифровки и дешифроки
if __name__ == "__main__":
    while True:
        action = input(
            "Введите 'за-шифр' для шифрования, 'де-шифр' для дешифрования или 'выход' для завершения: ").strip().lower()

        if action == 'за-шифр':
            main_encrypt()
        elif action == 'де-шифр':
            main_decrypt()
        elif action == 'выход':
            print("Завершение программы.")
            break  # Выход из цикла
        else:
            print("Неверная команда. Попробуйте снова.")