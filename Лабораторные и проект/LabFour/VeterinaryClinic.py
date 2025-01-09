import pickle
import re

class NameDescriptor:
    """Дескриптор для проверки имени."""

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str) or not value.isalpha():
            raise ValueError("Имя должно быть строкой, содержащей только буквы.")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class PhoneDescriptor:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not re.match(r"^\+?[\d\s-]{10,15}$", value):
            raise ValueError("Телефон должен быть строкой в формате +1234567890.")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class AgeDescriptor:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int) or value < 0 or value > 30:
            raise ValueError("Возраст питомца должен быть целым числом от 0 до 30.")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Pet:
    name = NameDescriptor()
    age = AgeDescriptor()

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.current_appointment = None
        self.appointments = {}

    def add_appointment(self, date, comment=None):
        if comment:
            self.appointments[date] = comment
        else:
            self.current_appointment = date

    def complete_appointment(self, comment):
        if self.current_appointment is None:
            raise ValueError("Нет текущего приема для завершения.")
        self.appointments[self.current_appointment] = comment
        self.current_appointment = None


class Client:
    name = NameDescriptor()
    phone = PhoneDescriptor()

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)


class Database:
    def __init__(self):
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def find_client_by_name(self, name):
        for client in self.clients:
            if client.name == name:
                return client
        return None

    def find_client_by_phone(self, phone):
        for client in self.clients:
            if client.phone == phone:
                return client
        return None

    def save(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(filename):
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return Database()


def main():
    # Загрузка базы данных
    db = Database.load("vet_database.pkl")

    while True:
        print("\n--- Ветеринарная клиника ---")
        print("1. Добавить клиента")
        print("2. Найти клиента (по имени или телефону)")
        print("3. Добавить питомца клиенту")
        print("4. Просмотреть приемы питомца")
        print("5. Назначить прием питомцу")
        print("6. Завершить прием питомца")
        print("7. Сохранить и выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Введите имя клиента: ")
            phone = input("Введите телефон клиента: ")
            try:
                client = Client(name, phone)
                db.add_client(client)
                print(f"Клиент {name} добавлен.")
            except ValueError as e:
                print("Ошибка:", e)

        elif choice == "2":
            search_type = input("Искать по (имя/телефон): ")
            if search_type == "имя":
                name = input("Введите имя клиента: ")
                client = db.find_client_by_name(name)
            elif search_type == "телефон":
                phone = input("Введите телефон клиента: ")
                client = db.find_client_by_phone(phone)
            else:
                print("Неверный тип поиска!")
                continue
            if client:
                print(f"Найден клиент: {client.name}, {client.phone}")
                print("Питомцы:", [pet.name for pet in client.pets])
            else:
                print("Клиент не найден.")

        elif choice == "3":
            name = input("Введите имя клиента: ")
            client = db.find_client_by_name(name)
            if not client:
                print("Клиент не найден.")
                continue
            pet_name = input("Введите имя питомца: ")
            pet_age = int(input("Введите возраст питомца: "))
            try:
                pet = Pet(pet_name, pet_age)
                client.add_pet(pet)
                print(f"Питомец {pet_name} добавлен.")
            except ValueError as e:
                print("Ошибка:", e)

        elif choice == "4":
            name = input("Введите имя клиента: ")
            client = db.find_client_by_name(name)
            if not client:
                print("Клиент не найден.")
                continue
            pet_name = input("Введите имя питомца: ")
            pet = next((p for p in client.pets if p.name == pet_name), None)
            if not pet:
                print("Питомец не найден.")
                continue
            print(f"Текущий прием: {pet.current_appointment}")
            print("Прошлые приемы:")
            for date, comment in pet.appointments.items():
                print(f"- {date}: {comment}")

        elif choice == "5":
            name = input("Введите имя клиента: ")
            client = db.find_client_by_name(name)
            if not client:
                print("Клиент не найден.")
                continue
            pet_name = input("Введите имя питомца: ")
            pet = next((p for p in client.pets if p.name == pet_name), None)
            if not pet:
                print("Питомец не найден.")
                continue
            date = input("Введите дату приема: ")
            pet.add_appointment(date)
            print(f"Прием назначен на {date}.")

        elif choice == "6":
            name = input("Введите имя клиента: ")
            client = db.find_client_by_name(name)
            if not client:
                print("Клиент не найден.")
                continue
            pet_name = input("Введите имя питомца: ")
            pet = next((p for p in client.pets if p.name == pet_name), None)
            if not pet:
                print("Питомец не найден.")
                continue
            comment = input("Введите комментарий ветврача: ")
            try:
                pet.complete_appointment(comment)
                print("Прием завершен.")
            except ValueError as e:
                print("Ошибка:", e)

        elif choice == "7":
            db.save("vet_database.pkl")
            print("База данных сохранена. До свидания!")
            break

        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()