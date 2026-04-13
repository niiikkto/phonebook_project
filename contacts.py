"""Модуль для работы с контактами телефонной книги"""

class Contact:
    """Класс, представляющий контакт"""
    
    def __init__(self, name, phone, email="", address=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
    
    def to_dict(self):
        """Преобразует контакт в словарь для JSON"""
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }
    
    @staticmethod
    def from_dict(data):
        """Создает контакт из словаря"""
        return Contact(
            name=data["name"],
            phone=data["phone"],
            email=data.get("email", ""),
            address=data.get("address", "")
        )
    
    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email} | {self.address}"


class PhoneBook:
    """Класс для управления телефонной книгой"""
    
    def __init__(self):
        self.contacts = []
    
    def add_contact(self, contact):
        """Добавляет новый контакт"""
        self.contacts.append(contact)
        return True
    
    def remove_contact(self, name):
        """Удаляет контакт по имени"""
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                self.contacts.remove(contact)
                return True
        return False
    
    def find_contact(self, name):
        """Находит контакт по имени"""
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None
    
    def list_contacts(self):
        """Возвращает список всех контактов"""
        return self.contacts
    
    def update_contact(self, name, new_phone=None, new_email=None, new_address=None):
        """Обновляет информацию о контакте"""
        contact = self.find_contact(name)
        if contact:
            if new_phone:
                contact.phone = new_phone
            if new_email:
                contact.email = new_email
            if new_address:
                contact.address = new_address
            return True
        return False