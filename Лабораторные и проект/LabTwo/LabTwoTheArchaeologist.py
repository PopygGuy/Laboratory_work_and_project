class Artifact:
    def __init__(self, name, age, origin, rarity):
        self.name = name
        self.age = age
        self.origin = origin
        self.rarity = rarity

    def __str__(self):
        return f"Название: {self.name}, Возраст: {self.age}, Происхождение: {self.origin}, Редкость: {self.rarity}"


class ArtifactCollector:

    def __init__(self):
        self.artifacts = []

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)

    def __iter__(self):
        return iter(self.artifacts)

    def sort_by_age(self):
        self.artifacts.sort(key=lambda artifact: artifact.age)

    def filter_by_origin(self, origin):
        return (artifact for artifact in self.artifacts if artifact.origin == origin)

    def filter_by_rarity(self, rarity):
        return (artifact for artifact in self.artifacts if artifact.rarity == rarity)

    def __reversed__(self):
        return reversed(self.artifacts)

    def find_oldest(self):
        if self.artifacts:
            return max(self.artifacts, key=lambda artifact: artifact.age)
        return None

    def find_by_name(self, name):
        for artifact in self.artifacts:
            if artifact.name == name:
                return artifact
        return None

# Создаем артефакты
mask = Artifact("Golden Mask", 3000, "Egypt", "legendary")
vase = Artifact("Ancient Vase", 2000, "Greece", "rare")
statue = Artifact("Stone Statue", 1500, "Aztec", "common")
amulet = Artifact("Amulet of Anubis", 5000, "Egypt", "legendary")

# Создаем коллекционера артефактов и добавляем в коллекцию
collector = ArtifactCollector()
collector.add_artifact(mask)
collector.add_artifact(vase)
collector.add_artifact(statue)
collector.add_artifact(amulet)

# Итерация по коллекции
print("Все артефакты:")
for artifact in collector:
    print(artifact.name)

# Сортировка по возрасту
print("\nАртефакты по возрасту:")
collector.sort_by_age()
for artifact in collector:
    print(f"{artifact.name}: {artifact.age} лет")

# Фильтрация по происхождению
print("\nАртефакты из Египта:")
for artifact in collector.filter_by_origin("Egypt"):
    print(artifact.name)

# Самый древний артефакт
oldest = collector.find_oldest()
print(f"\nСамый древний артефакт: {oldest.name} ({oldest.age} лет)")

# Поиск по имени
artifact = collector.find_by_name("Ancient Vase")
if artifact:
    print(f"\nАртефакт найден: {artifact.name}, {artifact.age} лет, {artifact.origin}")
else:
    print("\nАртефакт не найден")

# Обратный порядок итерации
print("\nАртефакты в обратном порядке:")
for artifact in reversed(collector):
    print(artifact.name)