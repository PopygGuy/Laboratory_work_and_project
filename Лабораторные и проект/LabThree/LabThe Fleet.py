class Weapon:
    def __init__(self, name, damage, condition=100):
        self.name = name
        self.damage = damage
        self.condition = condition

    def attack(self):
        if self.condition <= 0:
            print(f"Оружие {self.name} в неисправном состоянии и не может атаковать.")
            return 0
        print(f"Оружие {self.name} атакует! Урон: {self.damage}")
        return self.damage

class CrewMember:
    def __init__(self, name):
        self.name = name

    def perform_task(self):
        pass  # У каждого члена экипажа будет своя задача

class Pilot(CrewMember):
    def __init__(self, name):
        super().__init__(name)

    def perform_attack(self, weapons):
        print(f"Пилот {self.name} начинает атаку!")
        total_damage = 0
        for weapon in weapons:
            total_damage += weapon.attack()
        return total_damage

class Engineer(CrewMember):
    def __init__(self, name):
        super().__init__(name)

    def repair(self, ship):
        print(f"Инженер {self.name} чинит {ship.name}. Прочность восстановлена до 100%.")
        ship.integrity = 100

class Ship:
    def __init__(self, name, ship_type, pilot, engineer, integrity=100):
        self.name = name
        self.ship_type = ship_type
        self.integrity = integrity
        self.pilot = pilot
        self.engineer = engineer
        self.weapons = []

    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def attack(self):
        if self.integrity <= 0:
            print(f"Корабль {self.name} повреждён и не может атаковать.")
            return
        print(f"{self.name} начинает атаку!")
        total_damage = self.pilot.perform_attack(self.weapons)
        print(f"Общий урон {self.name}: {total_damage}")

    def repair(self):
        if self.integrity < 100:
            self.engineer.repair(self)
        else:
            print(f"{self.name} не нуждается в ремонте.")

    def defend(self):
        print(f"{self.name} готовится к защите!")

class Fleet:
    def __init__(self):
        self.ships = []

    def add_ship(self, ship):
        self.ships.append(ship)

    def attack_all(self):
        for ship in self.ships:
            ship.attack()

    def repair_all(self):
        for ship in self.ships:
            ship.repair()

    def defend_all(self):
        for ship in self.ships:
            ship.defend()

if __name__ == "__main__":
    # Определение оружия
    laser = Weapon("Laser Cannon", 50)
    missile = Weapon("Missile Launcher", 100)

    # Создание экипажа
    pilot1 = Pilot("John Doe")
    engineer1 = Engineer("Jane Smith")
    pilot2 = Pilot("Han Solo")
    engineer2 = Engineer("Chewbacca")

    # Создание кораблей
    ship1 = Ship("USS Enterprise", "battlecruiser", pilot1, engineer1)
    ship2 = Ship("Falcon", "frigate", pilot2, engineer2)

    # Добавление вооружения к кораблям
    ship1.add_weapon(laser)
    ship2.add_weapon(missile)

    # Создание флота
    fleet = Fleet()
    fleet.add_ship(ship1)
    fleet.add_ship(ship2)

    # Атака флотом
    print("Флот атакует!")
    fleet.attack_all()

    # Ремонт флота
    print("\nФлот выполняет ремонт!")
    fleet.repair_all()