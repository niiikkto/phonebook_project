"""Главный модуль программы Телефонная книга"""

from contacts import Contact, PhoneBook
from storage import Storage
from utils import display_menu, validate_phone, validate_email


def main():
    """Основная функция программы"""
    print("Загрузка телефонной книги...")
    
    # Инициализация хранилища и загрузка данных
    storage = Storage()
    phonebook = storage.load()
    
    print(f"Загружено {len(phonebook.list_contacts())} контактов")
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            # Добавление контакта
            print("\n--- Добавление нового контакта ---")
            name = input("Имя: ").strip()
            
            if phonebook.find_contact(name):
                print(f"Ошибка: Контакт с именем '{name}' уже существует!")
                continue
            
            phone = input("Телефон: ").strip()
            if not validate_phone(phone):
                print("Ошибка: Неверный формат телефона!")
                continue
            
            email = input("Email (необязательно): ").strip()
            if email and not validate_email(email):
                print("Ошибка: Неверный формат email!")
                continue
            
            address = input("Адрес (необязательно): ").strip()
            
            contact = Contact(name, phone, email, address)
            phonebook.add_contact(contact)
            storage.save(phonebook)
            print(f"Контакт '{name}' успешно добавлен!")
        
        elif choice == '2':
            # Поиск контакта
            print("\n--- Поиск контакта ---")
            name = input("Введите имя для поиска: ").strip()
            contact = phonebook.find_contact(name)
            
            if contact:
                print(f"\nКонтакт найден:")
                print(f"  Имя: {contact.name}")
                print(f"  Телефон: {contact.phone}")
                print(f"  Email: {contact.email or 'не указан'}")
                print(f"  Адрес: {contact.address or 'не указан'}")
            else:
                print(f"Контакт '{name}' не найден!")
        
        elif choice == '3':
            # Показать все контакты
            print("\n--- Все контакты ---")
            contacts = phonebook.list_contacts()
            
            if not contacts:
                print("Телефонная книга пуста.")
            else:
                print(f"\nВсего контактов: {len(contacts)}")
                print("-" * 50)
                for i, contact in enumerate(contacts, 1):
                    print(f"{i}. {contact}")
                print("-" * 50)
        
        elif choice == '4':
            # Удаление контакта
            print("\n--- Удаление контакта ---")
            name = input("Введите имя контакта для удаления: ").strip()
            
            confirm = input(f"Вы уверены, что хотите удалить '{name}'? (да/нет): ").lower()
            if confirm == 'да':
                if phonebook.remove_contact(name):
                    storage.save(phonebook)
                    print(f"Контакт '{name}' удален!")
                else:
                    print(f"Контакт '{name}' не найден!")
            else:
                print("Операция отменена.")
        
        elif choice == '5':
            # Обновление контакта
            print("\n--- Обновление контакта ---")
            name = input("Введите имя контакта для обновления: ").strip()
            
            if not phonebook.find_contact(name):
                print(f"Контакт '{name}' не найден!")
                continue
            
            print("Оставьте поле пустым, чтобы не менять значение")
            new_phone = input(f"Новый телефон (было: {phonebook.find_contact(name).phone}): ").strip()
            if new_phone and not validate_phone(new_phone):
                print("Ошибка: Неверный формат телефона!")
                continue
            
            new_email = input(f"Новый email (было: {phonebook.find_contact(name).email}): ").strip()
            if new_email and not validate_email(new_email):
                print("Ошибка: Неверный формат email!")
                continue
            
            new_address = input(f"Новый адрес (было: {phonebook.find_contact(name).address}): ").strip()
            
            phonebook.update_contact(
                name,
                new_phone if new_phone else None,
                new_email if new_email else None,
                new_address if new_address else None
            )
            storage.save(phonebook)
            print(f"Контакт '{name}' обновлен!")
        
        elif choice == '6':
            # Выход
            print("Сохранение данных...")
            storage.save(phonebook)
            print("До свидания!")
            break
        
        else:
            print("Неверный выбор. Пожалуйста, выберите 1-6.")


if __name__ == "__main__":
    main()