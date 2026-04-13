"""
Модуль для работы с файловым хранилищем контактов
"""
import json
import os
from typing import List, Optional
from models import Contact


class ContactStorage:
    """Класс для управления хранением контактов"""
    
    def __init__(self, filepath: str = "data/contacts.json"):
        """
        Инициализация хранилища
        
        Args:
            filepath: Путь к файлу с данными
        """
        self.filepath = filepath
        self._ensure_data_directory()
        
    def _ensure_data_directory(self) -> None:
        """Создать директорию для данных, если её нет"""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
    def load_contacts(self) -> List[Contact]:
        """
        Загрузить контакты из файла
        
        Returns:
            Список контактов
        """
        if not os.path.exists(self.filepath):
            return []
            
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                contacts = [Contact.from_dict(contact_data) for contact_data in data]
                return contacts
        except (json.JSONDecodeError, FileNotFoundError):
            return []
            
    def save_contacts(self, contacts: List[Contact]) -> bool:
        """
        Сохранить контакты в файл
        
        Args:
            contacts: Список контактов
            
        Returns:
            True если успешно, False если ошибка
        """
        try:
            # Устанавливаем ID для новых контактов
            for i, contact in enumerate(contacts):
                if contact.id is None:
                    contact.id = i
                    
            data = [contact.to_dict() for contact in contacts]
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
            
    def add_contact(self, contact: Contact, contacts: List[Contact]) -> bool:
        """
        Добавить новый контакт
        
        Args:
            contact: Новый контакт
            contacts: Существующий список
            
        Returns:
            True если успешно
        """
        contact.id = len(contacts)
        contacts.append(contact)
        return self.save_contacts(contacts)
        
    def search_contacts(self, contacts: List[Contact], query: str) -> List[Contact]:
        """
        Поиск контактов по имени или телефону
        
        Args:
            contacts: Список контактов для поиска
            query: Поисковый запрос
            
        Returns:
            Список найденных контактов
        """
        query_lower = query.lower()
        return [
            contact for contact in contacts
            if query_lower in contact.name.lower() 
            or query_lower in contact.phone
            or query_lower in contact.email.lower()
        ]