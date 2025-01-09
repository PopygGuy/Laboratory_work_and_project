import random

class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.mana = 50
        self.attack_power = 10
        self.inventory = ["Целебное зелье"] * 3  # Рюкзак персонажа, по умолчанию 3 зелья

# Метод использования целебного зелья
    def heal(self):
        if "Целебное зелье" in self.inventory:
            self.health += 30
            self.inventory.remove("Целебное зелье")
            print(f"{self.name} выпивает зелье и восстанавливает здоровье (+30).")
        else:
            print("❌ В рюкзаке нет зелий.")

# Метод использования лириумного зелья(мана)
    def use_mana_potion(self):
        print("❌ Только волшебники могут использовать лириумное зелье!")

    def greet(self):
        print(f"Привет! Я {self.name}, готов к приключениям!")

    # Проверка, жив ли герой
    def is_alive(self):
        return self.health > 0

class Wizard(Character):
    def __init__(self, name):
        super().__init__(name)
        self.health = 100 * 1.0
        self.mana = 50 * 1.5
        self.attack_power = 8
        self.inventory += ["Лириумное зелье"] * 5  # Добавляется 5 зелий в рюкзак волшебника

    def use_mana_potion(self):
        if "Лириумное зелье" in self.inventory:
            self.mana += 50
            self.inventory.remove("Лириумное зелье")
            print(f"{self.name} выпивает лириумное зелье и восстанавливает ману (+50 к Мане).")
        else:
            print("❌ В рюкзаке нет лириумных зелий.")

    # Нанесение магического урона
    def attack(self, target):
        if self.mana >= 10:
            damage = self.attack_power * 1.5 + random.randint(-3, 3)
            target.health -= damage
            self.mana -= 10
            print(f"{self.name} наносит магический удар! Урон: {int(damage)}") # вывод урона до целого числа
        else:
            print(f"{self.name} пытается выполнить магический удар, но у него закончилась мана!")

    def greet(self):
        print(f"Я {self.name}, мудрый волшебник. Я обрушу на ваши головы безбожный огненный дождь!")


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name)
        self.health = 100 * 1.5
        self.mana = 50 * 1.0
        self.attack_power = 12

    # Нанесение физического урона
    def attack(self, target):
        damage = self.attack_power * 1.2 + random.randint(-5, 5)
        target.health -= damage
        print(f"{self.name} наносит мощный физический удар! Урон: {int(damage)}")

    def greet(self):
        print(f"Я {self.name}, грозный боец. Я сломаю всем хребты!")


class Monster:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    # Атака монстра
    def attack(self, target):
        damage = self.attack_power + random.randint(-2, 2)
        target.health -= damage
        print(f"{self.name} атакует {target.name}! Урон: {int(damage)}")

    # Проверка, жив ли монстр
    def is_alive(self):
        return self.health > 0


class Game:
    def __init__(self):
        # Создаем главного героя
        print("Добро пожаловать в игру!")
        name = input("Введите имя вашего персонажа: ")
        print("Выберите класс персонажа:")
        print("1. Волшебник")
        print("2. Воин")

        choice = input("> ")
        if choice == "1":
            self.hero = Wizard(name)
        elif choice == "2":
            self.hero = Warrior(name)
        else:
            print("Неверный выбор, вы будете играть за воина.")
            self.hero = Warrior(name)

        self.monster = Monster(name="Гоблин", health=100, attack_power=6)
        self.hero.greet()

    def play(self):
        print("\nВаше приключение начинается!")
        print("В любую минуту вы можете ввести E (англ.), чтобы выйти из игры.")

        while self.hero.is_alive() and self.monster.is_alive():
            print("\n--- Ваш ход ---")
            print("1. Атаковать")
            print("2. Выпить целебное зелье")
            print("3. Выпить лириумное зелье (для мага)")
            print("4. Посмотреть состояние")
            print("E. Выйти из игры")

            action = input("> ")

            if action == "E":  # По нажатию происходит выход
                print("Спасибо за игру. До новых встреч!")
                break
            if action == "1":
                self.hero.attack(self.monster)
            elif action == "2":
                self.hero.heal()
            elif action == "3":
                self.hero.use_mana_potion()
            elif action == "4":
                print(
                    f"{self.hero.name} (Здоровье: {self.hero.health}, Мана: {self.hero.mana}), Рюкзак: {self.hero.inventory}")
                print(f"{self.monster.name} (Здоровье: {self.monster.health})")
                continue
            else:
                print("❌ Неверный выбор!")
                continue

            # Ход монстра
            if self.monster.is_alive():
                print("\n--- Ход противника ---")
                self.monster.attack(self.hero)

        # Проверяем исход боя
        if self.hero.is_alive() and not self.monster.is_alive():
            print(f"\n🎉 {self.hero.name} победил {self.monster.name}!")
        elif not self.hero.is_alive():
            print(f"\n💀 {self.hero.name} был побежден. Конец игры.")

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.play()