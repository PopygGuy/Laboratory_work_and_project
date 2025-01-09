#### Задача 1 (10 баллов).
# Представим себе, что мы хотим открыть музыкальный магазин и заведовать всеми его делами. Напишем программу, которая будет визуализировать наши мечты. Наверное, в первую очередь нам понадобится класс для самого магазина. У магазина есть счет, склад, возможность продавать инструменты и покупать их (может быть, что-то еще - что придумаете). Потом, нужен, конечно, класс для музыкального инструмента. Попробуйте реализовать музыкальные инструменты с помощью наследования: можно создать некий абстрактный класс "инструмент", а от него будут наследовать классы "гитара", "пианино" и так далее - при этом у гитар и пианино могут быть свои разные характеристики, н-р, у гитары количество струн, тип порожка и так далее. Можно и более подробную иерархию, если будете успевать (например, инструменты бывают электрическими и акустическими). Наконец, можно создать класс "покупатель", у которого будет кошелек.
# Наконец, неплохо бы не забыть написать некий код, который будет приводить наши классы в движение: имитировать рабочий день магазина (можно в цикле), с рандомной вероятностью посещение покупателей, давать нашему владельцу-пользователю возможность решить, не пора ли закупить новые инструменты или, может быть, затеять рекламную кампанию.
# Фантазия всячески поощряется, могу за нее поставить дополнительные баллы.

import random
class MusicalInstrument:
    # Класс для музыкального инструмента
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __str__(self):
        return f"{self.name} - {self.price}$"

class Guitar(MusicalInstrument):
    # Класс гитары
    def __init__(self, price, string_count, bridge_type):
        super().__init__("Гитара", price)
        self.string_count = string_count
        self.bridge_type = bridge_type

    def __str__(self):
        return f"{self.name} (Струнные: {self.string_count}, Порожек: {self.bridge_type}) - {self.price}$"

class Piano(MusicalInstrument):
    # Класс пианино
    def __init__(self, price, piano_type):
        super().__init__("Пианино", price)
        self.piano_type = piano_type

    def __str__(self):
        return f"{self.name} (Тип: {self.piano_type}) - {self.price}$"

class Shop:
    # Класс магазина
    def __init__(self, balance):
        self.balance = balance
        self.stock = []

    def add_instrument(self, instrument):
        # Добавление инструмента на склад
        self.stock.append(instrument)

    def sell_instrument(self, instrument, customer):
        # Продажа инструмента покупателю
        if instrument in self.stock:
            if customer.wallet >= instrument.price:
                customer.wallet -= instrument.price
                self.balance += instrument.price
                self.stock.remove(instrument)
                print(f"{customer.name} купил {instrument}")
            else:
                print(f"{customer.name} не хватает денег на {instrument}")
        else:
            print(f"{instrument.name} отсутствует на складе")

    def buy_instrument(self, instrument):
        # Закупка нового инструмента магазином
        if self.balance >= instrument.price:
            self.balance -= instrument.price
            self.stock.append(instrument)
            print(f"Закуплен новый {instrument}")
        else:
            print(f"Не хватает денег на закупку {instrument}")

    def display_stock(self):
        # Показать склад магазина
        print("Ассортимент магазина:")
        for instrument in self.stock:
            print(f" - {instrument}")
        print()

class Customer:
    # Класс покупателя
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = wallet

    def __str__(self):
        return f"{self.name} (Деньги: {self.wallet}$)"


# Имитируем рабочий день магазина
def simulate_shop_day():
    shop = Shop(balance=1000)  # Начальный баланс магазина

    # Добавляем стартовые инструменты на склад
    shop.add_instrument(Guitar(price=200, string_count=6, bridge_type="Fixed"))
    shop.add_instrument(Guitar(price=300, string_count=7, bridge_type="Floating"))
    shop.add_instrument(Piano(price=1000, piano_type="Grand"))

    # Список покупателей
    possible_customers = [
        Customer("Алексей", 500),
        Customer("Мария", 120),
        Customer("Дмитрий", 1500),
        Customer("Ольга", 800),
    ]

    for hour in range(1, 9):  # Рабочие часы с 1 до 8
        print(f"\nЧас {hour}:")
        shop.display_stock()

        # Вероятность прихода покупателя (50% шанс)
        if random.random() < 0.5:
            customer = random.choice(possible_customers)
            print(f"Пришел покупатель: {customer}")

            # Покупатель случайно выбирает инструмент
            if shop.stock:
                instrument = random.choice(shop.stock)
                shop.sell_instrument(instrument, customer)
            else:
                print("Магазин пуст, нечего купить!")
        else:
            print("Никто не пришел.")

        # Случайная закупка магазина (30% шанс)
        if random.random() < 0.3:
            new_guitar = Guitar(price=250, string_count=6, bridge_type="Fixed")
            shop.buy_instrument(new_guitar)

    print("\nРабочий день завершен!")
    print(f"Баланс магазина: {shop.balance}$")
    shop.display_stock()


# Запуск симуляции
simulate_shop_day()