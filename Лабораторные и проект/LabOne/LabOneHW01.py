# Напишем мини-стратегическую игру, в которой игроку предлагается управлять городом (SimCity видели когда-нибудь?)
# У нас есть собственно класс "город", внутри города есть постройки разных типов, которые мы, как градоправитель, строим.
# Также у города есть атрибуты: уровень счастья жителей, уровень экологии, образования, миграции и так далее (на что вашей фантазии хватит).
# Постройки к этим атрибутам добавляют и прибавляют баллы. Можно завести тип постройки, которая на каждом ходе игры приносит в городской бюджет деньги (налоговая служба?.. заводы?).
# Постройки необходимо реализовать с помощью наследования, у некоторых построек могут быть свои методы, например, больница может устраивать медосмотры и вакцинации и поднимать этим уровень благосостояния жителей, а на заводе с рандомной вероятностью может случиться авария, которая понизит экологию.
# Не забудьте реализовать головной класс "игра", в котором будет метод play, можно в нем хранить и городской бюджет.

import random

class Building:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def effect(self, city):
        pass

class Factory(Building):
    def __init__(self, cost, income, ecology_impact):
        super().__init__(name="Завод", cost=cost)
        self.income = income  # Доход от завода
        self.ecology_impact = ecology_impact  # Влияние на экологию

    def effect(self, city):
        city.budget += self.income
        city.ecology += self.ecology_impact

        # Случайная вероятность аварии
        if random.random() < 0.1:  # 10% вероятность аварии
            city.ecology -= 10
            print(f"⚠️ На заводе произошла авария! Экология города ухудшилась.")


class School(Building):
    def __init__(self, cost, education_bonus):
        super().__init__(name="School", cost=cost)
        self.education_bonus = education_bonus  # Бонус к уровню образования

    def effect(self, city):
        city.education += self.education_bonus


class Hospital(Building):
    def __init__(self, cost, happiness_bonus):
        super().__init__(name="Hospital", cost=cost)
        self.happiness_bonus = happiness_bonus  # Бонус к счастью жителей

    def effect(self, city):
        city.happiness += self.happiness_bonus

        if random.random() < 0.5:  # 50% вероятность
            city.happiness += 2
            print(f"🏥 Проведен медицинский осмотр! Счастье жителей увеличилось.")


class City:
    def __init__(self, name):
        self.name = name
        self.budget = 1000  # Стартовый бюджет
        self.ecology = 50  # Уровень экологии
        self.education = 50  # Уровень образования
        self.happiness = 50  # Уровень счастья
        self.buildings = []  # Постройки в городе

    def build(self, building):
        # Постройка нового города
        if self.budget >= building.cost:
            self.budget -= building.cost
            self.buildings.append(building)
            print(f"🏗️ Построено новое здание: {building.name}")
        else:
            print(f"❌ Недостаточно денег для постройки {building.name} (нужно {building.cost}$)")

    def next_turn(self):
        print(f"\n🌆 Состояние города {self.name}:")
        print(f"- Бюджет: {self.budget}$")
        print(f"- Экология: {self.ecology}")
        print(f"- Образование: {self.education}")
        print(f"- Счастье: {self.happiness}")

        for building in self.buildings:
            building.effect(self)

        # Проверка общего состояние города
        if self.ecology <= 0:
            print("💀 Экология в критическом состоянии. Жители покидают ваш город. Вы проиграли.")
            return False
        if self.happiness <= 0:
            print("😢 Жители несчастны и покидают ваш город. Вы проиграли.")
            return False

        return True


class Game:
    def __init__(self):
        self.city = City(name="New City")

    def play(self):
        print("Добро пожаловать в игру по управлению городом!")

        running = True
        while running:
            print("\nЧто вы хотите построить?")
            print("1. Завод (500$, до +200$ дохода, -5 экологии)")
            print("2. Школа (300$, +3 к образованию)")
            print("3. Больница (400$, +5 к счастью)")
            print("4. Пропустить ход")
            choice = input("> ")

            if choice == "1":
                self.city.build(Factory(cost=500, income=random.randint(100, 200), ecology_impact=-5))
            elif choice == "2":
                self.city.build(School(cost=300, education_bonus=3))
            elif choice == "3":
                self.city.build(Hospital(cost=400, happiness_bonus=5))
            elif choice == "4":
                print("⏩ Ход пропущен.")
            else:
                print("❌ Неверный выбор!")

            # Переход к следующему ходу
            running = self.city.next_turn()

        print("Игра завершена. Спасибо за игру!")

# Запуск игры
new_game = Game()
new_game.play()