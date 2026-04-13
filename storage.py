"""Модуль для сохранения и загрузки данных"""

import json
import os
from contacts import Contact, PhoneBook


class Storage:
    """Класс для работы с файловым хранилищем"""
    
    def __init__(self, filename="data/contacts.json"):
        self.filename = filename
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Создает директорию для данных, если её нет"""
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def save(self, phonebook):
        """Сохраняет телефонную книгу в файл"""
        data = [contact.to_dict() for contact in phonebook.list_contacts()]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    
    def load(self):
        """Загружает телефонную книгу из файла"""
        phonebook = PhoneBook()
        
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    contact = Contact.from_dict(item)
                    phonebook.add_contact(contact)
        
        return phonebook