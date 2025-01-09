import os
print("Текущий рабочий каталог:", os.getcwd())

def feistel_encrypt(L0, R0, key, rounds, f):
    L, R = L0, R0
    for i in range(rounds):
        L, R = R, L ^ f(R, key[i])
    return L, R

def feistel_decrypt(Ln, Rn, key, rounds, f):
    L, R = Ln, Rn
    for i in range(rounds - 1, -1, -1):
        L, R = R ^ f(L, key[i]), L
    return L, R

def unit_function(vi):
    return vi

def multiplication_function(vi, x):
    return vi * x

def read_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def main():
    # Имена файлов
    input_text_file = 'D:\Учеба\Магистратура\Защита информации в сети Интернет\Лаба 2\input.txt'
    key_file = 'D:\Учеба\Магистратура\Защита информации в сети Интернет\Лаба 2\key.txt'
    encrypted_file = 'D:\Учеба\Магистратура\Защита информации в сети Интернет\Лаба 2\encrypted.txt'
    decrypted_file = 'D:\Учеба\Магистратура\Защита информации в сети Интернет\Лаба 2\decrypted.txt'
    
    # Чтение текста и ключа из файлов
    text = read_file(input_text_file).strip()
    key = list(map(int, read_file(key_file).strip().split()))

    # Инициализация значений L0 и R0
    L0 = int.from_bytes(text.encode(), 'big') >> (len(text) * 4)
    R0 = int.from_bytes(text.encode(), 'big') & ((1 << (len(text) * 4)) - 1)

    # Выбор функции
    func_type = input("Выберите функцию (1 - Единичная, 2 - Множение): ")
    if func_type == '1':
        f = unit_function
        def wrapped_f(vi, ki):
            return f(vi)
    elif func_type == '2':
        multiplier = int(input("Введите множитель: "))
        f = lambda vi, x: multiplication_function(vi, multiplier)
        def wrapped_f(vi, ki):
            return f(vi, ki)
    else:
        print("Неверный ввод.")
        return

    # Шифрование
    Ln, Rn = feistel_encrypt(L0, R0, key, len(key), wrapped_f)
    encrypted_text = f"{Ln} {Rn}"
    write_file(encrypted_file, encrypted_text)

    # Дешифрование
    L0_dec, R0_dec = feistel_decrypt(Ln, Rn, key, len(key), wrapped_f)
    decrypted_text = (L0_dec << (len(text) * 4)) | R0_dec
    decrypted_text = decrypted_text.to_bytes((decrypted_text.bit_length() + 7) // 8, 'big').decode()
    write_file(decrypted_file, decrypted_text)

if __name__ == "__main__":
    main()
    