"""Вспомогательные функции"""

def validate_phone(phone):
    """Проверяет корректность номера телефона"""
    # Удаляем все нецифровые символы для проверки
    digits = ''.join(filter(str.isdigit, phone))
    return len(digits) >= 5  # Минимальная длина номера


def validate_email(email):
    """Простая проверка email"""
    if not email:
        return True  # Email может быть пустым
    return '@' in email and '.' in email


def display_menu():
    """Отображает главное меню"""
    print("\n" + "="*40)
    print("        ТЕЛЕФОННАЯ КНИГА")
    print("="*40)
    print("1. Добавить контакт")
    print("2. Найти контакт")
    print("3. Показать все контакты")
    print("4. Удалить контакт")
    print("5. Обновить контакт")
    print("6. Выйти")
    print("="*40)
    return input("Выберите действие (1-6): ")