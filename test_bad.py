# test_bad.py - файл для демонстрации


def bad_function(name, age, city):  # лишние пробелы
    if name == "":  # нет пробелов вокруг оператора
        return 0
    print("Hello - test_bad.py:9")
    return name, age, city  # нет пробела после запятой


x = 10  # нет пробелов
