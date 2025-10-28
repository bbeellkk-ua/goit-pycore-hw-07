from collections import UserDict
import re
from datetime import datetime, timedelta

date_format = '%d.%m.%Y'

class BotError(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.search(r'^\d{10}$', value):
            raise BotError('Number should contain 10 digits')
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, date_format))
        except ValueError:
            raise BotError('Invalid date format. Use DD.MM.YYYY')

    def __str__(self):
        return self.value.strftime(date_format) if self.value else ''

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = None
        self.birthday = None

    def set_phone(self, phone: str) -> None:
        self.phone = Phone(phone)

    def get_phone(self) -> str | None:
        return self.phone.value

    def set_birthday(self, date: str) -> None:
        self.birthday = Birthday(date)

    def get_birthday(self) -> Birthday | None:
        return self.birthday

    def __str__(self):
        return f'Contact name: {self.name.value}, \
            phones: {'; '.join(p.value for p in self.phones)}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name, None)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        # Get today and closest Sunday
        today = datetime.today().date()
        week_later = today + timedelta(days=7)
        # Create empty list
        result = list()
        # Process users
        for name, u in self.data.items():
            # Get birthday
            bd = u.get_birthday()
            # Skip if birthday is not set yet
            if not bd:
                continue
            # Parse original date
            birthday = bd.value.date()
            # Use same month and day but this year
            birthday_this_year = datetime.strptime(f"{birthday.day}.{birthday.month}.{today.year}", date_format).date()
            # If it happened this year, then try next year
            if birthday_this_year < today:
                birthday_this_year += timedelta(days=365)
            # Skip birthdays outside of 7 days ahead interval
            if birthday_this_year > week_later:
                continue
            # If it is Sat or Sun, then try Mon
            if birthday_this_year.weekday() > 4:
                birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))
            # Add user notification info to the list
            result.append({'name': name, 'congratulation_date': birthday_this_year.strftime(date_format)})
        return result
