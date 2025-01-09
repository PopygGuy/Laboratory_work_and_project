import hashlib

class SHA:
    def __init__(self):
        self.hasher = hashlib.sha256()  # Инициализируем SHA-256 хэш-объект

    def update(self, data):
        self.hasher.update(data)

    def compute_hash(self):
        return self.hasher.hexdigest()

def pad_message(message):
    original_byte_length = len(message)
    original_bit_length = original_byte_length * 8  # Длина в битах
    padded_message = message + b'\x80'  # Добавляем 1 в конец

    # Дополняем нулями до ближайшего кратного 128
    while (len(padded_message) * 8 + 64) % 128 != 0:
        padded_message += b'\x00'  # Добавляем нули

    # Добавление 64-битное представление длины оригинального сообщения
    padded_message += original_bit_length.to_bytes(8, byteorder='big')

    return padded_message

def main():
    # Ввод текста от пользователя
    user_input = input("Введите текст для хеширования: ").strip()  # Получаем строку и убираем лишние пробелы

    # Кодирование введенного сообщения в байты для хеширования
    user_input_encoded = user_input.encode('utf-8')

    padded_message = pad_message(user_input_encoded)

    # Создаем экземпляр класса SHA и вычисляем хэш
    sha_instance = SHA()
    sha_instance.update(padded_message)
    hash_value = sha_instance.compute_hash()

    # Сохраняем исходное сообщение в отдельный файл
    with open("original_message.txt", 'w', encoding='utf-8') as file:
        file.write(user_input)  # Сохраняем исходное сообщение

    # Сохраняем хэш в отдельный файл
    with open("hashed_message.txt", 'w', encoding='utf-8') as file:
        file.write(hash_value)  # Сохраняем хэш отдельно

    print("Исходное сообщение сохранено в 'original_message.txt', а хэш - в 'hashed_message.txt'.")

if __name__ == "__main__":
    main()