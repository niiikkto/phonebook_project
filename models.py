"""
Модель данных для контакта в телефонной книге
"""
import json
from datetime import datetime
from typing import Dict, Any, List


class Contact:
    """Класс, представляющий контакт в телефонной книге"""
    
    def __init__(self, name: str, phone: str, email: str = "", address: str = ""):
        """
        Инициализация контакта
        
        Args:
            name: Имя контакта
            phone: Номер телефона
            email: Email адрес (опционально)
            address: Адрес (опционально)
        """
        self.id = None
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.favorite = False
        
    def update(self, name: str = None, phone: str = None, 
               email: str = None, address: str = None) -> None:
        """
        Обновить информацию о контакте
        
        Args:
            name: Новое имя
            phone: Новый телефон
            email: Новый email
            address: Новый адрес
        """
        if name:
            self.name = name
        if phone:
            self.phone = phone
        if email:
            self.email = email
        if address:
            self.address = address
        self.updated_at = datetime.now()
        
    def toggle_favorite(self) -> None:
        """Переключить статус избранного"""
        self.favorite = not self.favorite
        
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать контакт в словарь для сохранения"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'favorite': self.favorite
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contact':
        """Создать контакт из словаря"""
        contact = cls(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email', ''),
            address=data.get('address', '')
        )
        contact.id = data.get('id')
        contact.created_at = datetime.fromisoformat(data['created_at'])
        contact.updated_at = datetime.fromisoformat(data['updated_at'])
        contact.favorite = data.get('favorite', False)
        return contact
        
    def __str__(self) -> str:
        favorite_star = "⭐ " if self.favorite else ""
        return f"{favorite_star}{self.name} - {self.phone}"