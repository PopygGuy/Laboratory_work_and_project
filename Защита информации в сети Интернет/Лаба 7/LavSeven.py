import hashlib

class NHash:
    def __init__(self, stages=1):
        """Инициализация N-hash с указанным количеством этапов."""
        self.stages = stages

    def compute_hash(self, input_data):
        """Вычисляет хэш сообщения."""
        result = input_data

        # Применяем хэширование на заданное количество этапов
        for _ in range(self.stages):
            result = self._intermediate_hash(result)

        return result

    def _intermediate_hash(self, text):
        """Скрытый метод для промежуточного хэширования."""
        # Используем SHA-256 как основной алгоритм
        text_bytes = text.encode('utf-8')
        hash_object = hashlib.sha256()
        hash_object.update(text_bytes)
        return hash_object.hexdigest()

if __name__ == "__main__":
    if __name__ == "__main__":
        while True:
            stages_input = input("Введите количество этапов для хэширования: ")
            try:
                stages = int(stages_input)
                if stages <= 0:
                    print("Ошибка: количество этапов должно быть положительным целым числом.")
                else:
                    break  # Выход из цикла, если введено правильное число
            except ValueError:
                print("Ошибка: количество этапов должно быть целым числом.")

    message = input("Введите сообщение для хэширования: ")

    hasher = NHash(stages=stages)  # Указываем количество этапов
    hash_value = hasher.compute_hash(message)

    print(f"Хэш сообщения: {hash_value}")

    # Сохраняем хэш и исходный текст в файл
    with open("hash_output.txt", "w", encoding='utf-8') as file:
        file.write(f"Исходное сообщение: {message}\n")
        file.write(f"Хэш сообщения: {hash_value}\n")

    print("Хэш и исходное сообщение сохранены в файле 'hash_output.txt'.")