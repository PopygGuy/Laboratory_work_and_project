# Были исправление в исходном коде "pymorphy2" на момент написания не поддерживает Python 3.12
# Заменил  использование `inspect.getargspec` на `inspect.getfullargspec` в файле `pymorphy2/units/base.py`, использовался дебагер
# Строка: args, varargs, kw, default = inspect.getargspec(cls.__init__)
# И заменил на: args, varargs, kw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(cls.__init__)

import pymorphy2

class Token:
    __slots__ = ('text', '_lemma', 'pos', 'tag', 'dep', 'head', 'ent_type')
    morph_analyzer = pymorphy2.MorphAnalyzer()

    def __init__(self, text):
        self.text = text
        self._lemma = None
        self.pos = None
        self.tag = None
        self.dep = None
        self.head = None
        self.ent_type = None

    # Метод для установки части речи
    def set_pos(self, pos):
        self.pos = pos

    # Метод для установки грамматического тега
    def set_tag(self, tag):
        self.tag = tag

    # Метод для установки синтаксической зависимости
    def set_dep(self, dep):
        self.dep = dep

    # Метод для установки головного элемента
    def set_head(self, head):
        self.head = head

    # Метод для установки типа сущности
    def set_ent_type(self, ent_type):
        self.ent_type = ent_type

    # Метод для установки леммы вручную
    def set_lemma(self, lemma):
        self._lemma = lemma

    # Свойство для получения значения леммы с автоматическим вычислением, если оно None
    @property
    def lemma(self):
        if self._lemma is None:  # Если лемма отсутствует
            parsed = self.morph_analyzer.parse(self.text)[0]  # Анализируем слово
            self._lemma = parsed.normal_form  # Устанавливаем нормальную форму как лемму
        return self._lemma

    # Свойство для запрета установки леммы через прямой доступ
    @lemma.setter
    def lemma(self, value):
        raise AttributeError("Установить атрибут 'lemma' можно только через метод 'set_lemma'.")


if __name__ == "__main__":
    token = Token("кошками")

    # Выводим текст токена
    print(f"Текст токена: {token.text}")

    # Получаем лемму (с автоматическим вычислением)
    print(f"Лемма токена: {token.lemma}")

    # Устанавливаем часть речи
    token.set_pos("NOUN")
    print(f"Часть речи токена: {token.pos}")

    # Пробуем вручную установить лемму через метод
    token.set_lemma("кот")
    print(f"Обновленная лемма токена: {token.lemma}")

    try:
        token.lemma = "новая_лемма"
    except AttributeError as e:
        print(e)  # Установить атрибут 'lemma' можно только через метод 'set_lemma'.