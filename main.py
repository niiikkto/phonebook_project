"""
Главный модуль приложения "Телефонная книга"
"""
import sys
from typing import List
from models import Contact
from storage import ContactStorage
from utils import format_contact_list, format_contact_details, show_help


class PhoneBookApp:
    """Основной класс приложения телефонной книги"""
    
    def __init__(self):
        """Инициализация приложения"""
        self.storage = ContactStorage()
        self.contacts: List[Contact] = []
        
    def run(self) -> None:
        """Запуск основного цикла приложения"""
        print("\n📞 ДОБРО ПОЖАЛОВАТЬ В ТЕЛЕФОННУЮ КНИГУ! 📞")
        print("Ваш надежный помощник для хранения контактов\n")
        
        # Загружаем сохраненные контакты
        self.contacts = self.storage.load_contacts()
        print(f"📂 Загружено контактов: {len(self.contacts)}")
        
        # Показываем справку
        print(show_help())
        
        # Основной цикл
        while True:
            try:
                command = input("\n🔍 Введите команду: ").strip().lower()
                
                if command == "/exit":
                    self._exit_app()
                    break
                elif command == "/help":
                    print(show_help())
                elif command == "/list":
                    print(format_contact_list(self.contacts))
                elif command == "/favorites":
                    print(format_contact_list(self.contacts, show_favorites_only=True))
                elif command == "/add":
                    self._add_contact()
                elif command.startswith("/view"):
                    self._view_contact(command)
                elif command.startswith("/edit"):
                    self._edit_contact(command)
                elif command.startswith("/delete"):
                    self._delete_contact(command)
                elif command.startswith("/fav"):
                    self._toggle_favorite(command)
                elif command.startswith("/search"):
                    self._search_contacts(command)
                else:
                    print("❌ Неизвестная команда. Введите /help для списка команд.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Программа прервана пользователем")
                self._exit_app()
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                
    def _add_contact(self) -> None:
        """Добавить новый контакт"""
        print("\n📝 ДОБАВЛЕНИЕ НОВОГО КОНТАКТА")
        print("-" * 30)
        
        name = input("Имя контакта: ").strip()
        if not name:
            print("❌ Имя не может быть пустым!")
            return
            
        phone = input("Номер телефона: ").strip()
        if not phone:
            print("❌ Номер телефона не может быть пустым!")
            return
            
        email = input("Email (необязательно): ").strip()
        address = input("Адрес (необязательно): ").strip()
        
        new_contact = Contact(name, phone, email, address)
        
        if self.storage.add_contact(new_contact, self.contacts):
            self.contacts = self.storage.load_contacts()
            print(f"✅ Контакт '{name}' успешно добавлен!")
        else:
            print("❌ Не удалось добавить контакт")
            
    def _view_contact(self, command: str) -> None:
        """Просмотреть детали контакта"""
        parts = command.split()
        if len(parts) != 2:
            print("❌ Использование: /view [ID]")
            return
            
        try:
            contact_id = int(parts[1])
            if 0 <= contact_id < len(self.contacts):
                print(format_contact_details(self.contacts[contact_id]))
            else:
                print(f"❌ Контакт с ID {contact_id} не найден")
        except ValueError:
            print("❌ ID должен быть числом")
            
    def _edit_contact(self, command: str) -> None:
        """Редактировать контакт"""
        parts = command.split()
        if len(parts) != 2:
            print("❌ Использование: /edit [ID]")
            return
            
        try:
            contact_id = int(parts[1])
            if 0 <= contact_id < len(self.contacts):
                contact = self.contacts[contact_id]
                print(f"\n✏️ РЕДАКТИРОВАНИЕ КОНТАКТА: {contact.name}")
                print("(оставьте поле пустым, чтобы не менять)")
                
                new_name = input(f"Новое имя [{contact.name}]: ").strip()
                new_phone = input(f"Новый телефон [{contact.phone}]: ").strip()
                new_email = input(f"Новый email [{contact.email}]: ").strip()
                new_address = input(f"Новый адрес [{contact.address}]: ").strip()
                
                contact.update(
                    name=new_name if new_name else None,
                    phone=new_phone if new_phone else None,
                    email=new_email if new_email else None,
                    address=new_address if new_address else None
                )
                
                if self.storage.save_contacts(self.contacts):
                    print("✅ Контакт успешно обновлен!")
                    self.contacts = self.storage.load_contacts()
                else:
                    print("❌ Не удалось сохранить изменения")
            else:
                print(f"❌ Контакт с ID {contact_id} не найден")
        except ValueError:
            print("❌ ID должен быть числом")
            
    def _delete_contact(self, command: str) -> None:
        """Удалить контакт"""
        parts = command.split()
        if len(parts) != 2:
            print("❌ Использование: /delete [ID]")
            return
            
        try:
            contact_id = int(parts[1])
            if 0 <= contact_id < len(self.contacts):
                contact_name = self.contacts[contact_id].name
                confirm = input(f"⚠️ Удалить контакт '{contact_name}'? (y/n): ")
                
                if confirm.lower() == 'y':
                    del self.contacts[contact_id]
                    if self.storage.save_contacts(self.contacts):
                        print(f"✅ Контакт '{contact_name}' удален")
                        self.contacts = self.storage.load_contacts()
                    else:
                        print("❌ Не удалось удалить контакт")
            else:
                print(f"❌ Контакт с ID {contact_id} не найден")
        except ValueError:
            print("❌ ID должен быть числом")
            
    def _toggle_favorite(self, command: str) -> None:
        """Переключить статус избранного"""
        parts = command.split()
        if len(parts) != 2:
            print("❌ Использование: /fav [ID]")
            return
            
        try:
            contact_id = int(parts[1])
            if 0 <= contact_id < len(self.contacts):
                self.contacts[contact_id].toggle_favorite()
                if self.storage.save_contacts(self.contacts):
                    status = "добавлен в избранное" if self.contacts[contact_id].favorite else "удален из избранного"
                    print(f"✅ Контакт {status}")
                    self.contacts = self.storage.load_contacts()
                else:
                    print("❌ Не удалось обновить статус")
            else:
                print(f"❌ Контакт с ID {contact_id} не найден")
        except ValueError:
            print("❌ ID должен быть числом")
            
    def _search_contacts(self, command: str) -> None:
        """Поиск контактов"""
        parts = command.split(maxsplit=1)
        if len(parts) != 2:
            print("❌ Использование: /search [текст для поиска]")
            return
            
        query = parts[1]
        results = self.storage.search_contacts(self.contacts, query)
        
        if results:
            print(f"\n🔍 Найдено контактов: {len(results)}")
            print(format_contact_list(results))
        else:
            print(f"\n❌ Ничего не найдено по запросу '{query}'")
            
    def _exit_app(self) -> None:
        """Выход из приложения"""
        print("\n👋 До свидания! Ваши контакты сохранены.")
        print("📞 Возвращайтесь к нам снова!")
        sys.exit(0)


def main():
    """Точка входа"""
    app = PhoneBookApp()
    app.run()


if __name__ == "__main__":
    main()