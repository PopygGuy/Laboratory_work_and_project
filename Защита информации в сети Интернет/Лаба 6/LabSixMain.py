import base64
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
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

# Основная функция
def main():
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

    # Сохраняем зашифрованный текст и ключи в текстовые файлы
    with open("encrypted_text.txt", "wb") as f:
        f.write(encrypted_text_b64)

    with open("encrypted_key.txt", "wb") as f:
        f.write(encrypted_des_key_b64)

    # Сохраняем открытый ключ RSA
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    # Сохраняем закрытый ключ RSA в файле
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    print("Текст зашифрован и сохранен в файл, а ключ DES зашифрован и также сохранен.")

# Запуск основной функции
if __name__ == "__main__":
    main()