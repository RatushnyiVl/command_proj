from collections import UserDict
from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from re import match

class Field(ABC):
    @abstractmethod
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return str(self.value)


@dataclass
class Email(Field):
    value: str

    def __post_init__(self):
        self.validate(self.value)

    def validate(self, email:str):
        # текст + @ + текст + . + текст
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if not match(pattern, email):
            raise Exception("Uncorrect email format") # -------to change


@dataclass
class Name(Field):
    value:str

    def __repr__(self):
        return str(self.value)


class Phone(Field): 
    def __init__(self, value: str):
        super().__init__(value)
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, num):
        if not Phone.validate(num):
            raise Exception
        self.__value = num
    
    @staticmethod
    def validate(value:str):
        # phone number format validation
        return value.isdigit() and len(value) == 10
    
    def __repr__(self):
        return str(self.value)


@dataclass
class Birthday(Field):
    value:str

    def __post_init__(self):
        try:
            self.value = datetime.strptime(self.value, '%d.%m.%Y').date()
        except Exception:
            raise Exception("Invalid date format. Use DD.MM.YYYY")        
        

class Record:
    def __init__(self, name:str, num:str=None):
        self.name = Name(name)
        self.phones: list[Phone] = [] # Composition
        if num: #----to check
            self.add_phone(num) 
        self.birthday: Birthday = None
        self.email: Email = None

    def add_email(self, email): # -------to check
        self.email = Email(email)
        return "Email address successfully added"

    def add_birthday(self, date:str):
        self.birthday = Birthday(date)
        return "Birthday date successfully added"

    def add_phone(self, num:str):
        try:
            self.phones.append(Phone(num))
        except Exception:
           raise Exception("Phone number must contain 10 digits")
        return f"New phone number has been added. Current {self.name} record: {'; '.join(p.value for p in self.phones)}"

    def remove_phone(self, phone_number:str):
        for p in self.phones:
            if p.value == phone_number:
                self.phones.remove(p)
                return f"Phone number: {phone_number} has been removed."
        return f"Phone number: {phone_number} was not found."
    
    def edit_phone(self, old:str, new:str):
        for idx, p in enumerate(self.phones):
            if p.value == old:
                self.phones[idx] = Phone(new)
                return f"New phone number: {new} has been saved"         
        return f"Phone number: {old} does not exist."

    def find_phone(self, num:str):
        for p in self.phones:
            if p.value == num:
                return p   
        return f"Phone number: {num} was not found"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, email: {self.email}"


class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record
        return f"Record {record.name.value} has been added to the Address Book"
    
    def find(self, user:str):
        return self.data.get(user, "No such a name in the Address Book")
    
    def delete(self, user:str):
        if user in self.data:
            del self.data[user]
            return f"{user} record was deleted"      
        return "No such a name in the Address Book"
    
    def get_upcoming_birthdays(self) -> str:
        if not self.data:
            return "Address book is empty"
        
        current_date = date.today()
        result = []
        for name, record in self.data.items():
            # check wether Record has a birthday info
            if not record.birthday:
                result.append(f"{name} has no birthday information")
                continue        
            
            upcoming_bday_date = record.birthday.value.replace(year=current_date.year)

            # if BD has already passed we take next year
            if upcoming_bday_date < current_date:
                upcoming_bday_date = upcoming_bday_date.replace(year=current_date.year + 1)

            # weekends handling
            if upcoming_bday_date.weekday() == 6: #sunday
                upcoming_bday_date += timedelta(days=1)
            elif upcoming_bday_date.weekday() == 5: # saturday
                upcoming_bday_date += timedelta(days=2)

            # define next 7 days
            congrat_range = (upcoming_bday_date - current_date).days

            # define a person with BD in range of next 7 days
            if 0 <= congrat_range <= 7:
                result.append(f"{name} has a birthday soon!!! Don't forget to congratulate him on {upcoming_bday_date}")

        return '\n'.join(result)

# email1 = Email('ratushnyi@gmail.com')
# print(email1)

# email1 = Email('d@gmail.com')
# print(email1)

# bday = Birthday('12.02.2000')
# print(bday)
# print(type(bday))

# name1 = Name('Vlad')
# print(name1, type(name1))