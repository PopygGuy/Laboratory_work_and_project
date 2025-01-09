from abc import ABC, abstractmethod

class Worker(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def work(self, task):
        pass

class Linguist(Worker):
    def work(self, task):
        print(f"Лингвист {self.name} выполняет лингвистическую задачу: {task}")

class Programmer(Worker):
    def work(self, task):
        print(f"Программист {self.name} пишет код для задачи: {task}")

class CompLingWorker(Worker):
    def work(self, task):
        print(f"Компьютерный лингвист {self.name} анализирует данные для задачи: {task}")

class Boss(ABC):
    def __init__(self, name):
        self.name = name
        self.subordinates = []

    def add_subordinate(self, worker):
        self.subordinates.append(worker)

    def assign_task(self, task):
        print(f"Босс {self.name} раздаёт задачу '{task}' своим подчинённым...")
        for subordinate in self.subordinates:
            subordinate.work(task)

class LinguistBoss(Boss):
    pass  # Унаследует всё от Boss

class ProgrammerBoss(Boss):
    pass  # Унаследует всё от Boss

class CompLingBoss(Boss):
    pass  # Унаследует всё от Boss


class MainDepartment:
    def __init__(self):
        self.linguist_boss = None
        self.programmer_boss = None
        self.cl_boss = None

    def set_bosses(self, linguist_boss, programmer_boss, cl_boss):
        self.linguist_boss = linguist_boss
        self.programmer_boss = programmer_boss
        self.cl_boss = cl_boss

    def issue_task(self, department, task):
        print(f"\nГлавный отдел распределяет задачу '{task}' в подотдел '{department}'.")
        if department == 'linguist':
            if self.linguist_boss:
                self.linguist_boss.assign_task(task)
            else:
                print("Подотдел лингвистов не имеет босса!")
        elif department == 'programmer':
            if self.programmer_boss:
                self.programmer_boss.assign_task(task)
            else:
                print("Подотдел программистов не имеет босса!")
        elif department == 'comp_ling':
            if self.cl_boss:
                self.cl_boss.assign_task(task)
            else:
                print("Подотдел компьютерных лингвистов не имеет босса!")
        else:
            print("Неизвестный подотдел!")


if __name__ == "__main__":
    # Создание сотрудников
    linguist1 = Linguist("Ирина")
    linguist2 = Linguist("Сергей")

    programmer1 = Programmer("Андрей")
    programmer2 = Programmer("Мария")

    cl_worker1 = CompLingWorker("Алексей")
    cl_worker2 = CompLingWorker("Ольга")

    # Создание боссов
    linguist_boss = LinguistBoss("лингвистов")
    programmer_boss = ProgrammerBoss("программистов")
    cl_boss = CompLingBoss("компьютерных лингвистов")

    # Назначение подчинённых боссам
    linguist_boss.add_subordinate(linguist1)
    linguist_boss.add_subordinate(linguist2)

    programmer_boss.add_subordinate(programmer1)
    programmer_boss.add_subordinate(programmer2)

    cl_boss.add_subordinate(cl_worker1)
    cl_boss.add_subordinate(cl_worker2)

    # Создание главного отдела и назначение боссов
    main_dept = MainDepartment()
    main_dept.set_bosses(linguist_boss, programmer_boss, cl_boss)

    # Выдача задач
    main_dept.issue_task('linguist', "Исправить грамматические ошибки")
    main_dept.issue_task('programmer', "Разработать новый парсер текста")
    main_dept.issue_task('comp_ling', "Создать модель анализа текста")