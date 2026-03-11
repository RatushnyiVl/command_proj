from custom_classes import *
from variables import info

import pickle

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone"
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the name as an argument."
        except Exception as e:
            return f"An error occurred: {e}"

    return inner


@input_error
def parse_input(user_input:str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args:list, contacts:AddressBook): # ----------
    name, phone, *_ = args
    if name in contacts.data:
        return contacts.data[name].add_phone(phone)
    
    new_record = Record(name, phone)
    return contacts.add_record(new_record)

@input_error
def new_email(args:list, contacts:AddressBook):
    name, email, *_ = args
    return contacts.data[name].add_email(email)

@input_error
def change_contact(args:list, contacts:AddressBook):
    name, old_phone, new_phone, *_ = args
    record_to_change = contacts.find(name)
    if type(record_to_change) == Record:
        return record_to_change.edit_phone(old_phone, new_phone)
    else:
        return record_to_change

@input_error
def finder(args:list, contacts:AddressBook):
    if contacts:
        for name, rec in contacts.data.items():
            if name == args[0]:
                return rec
            if rec.find_phone(args[0]) == args[0]:
                return rec
            if rec.show_email() == args[0]:
                return rec
        return "No match"
    return "The Address Book is empty."  

@input_error
def show_all(_, contacts:AddressBook):
    if not contacts:
        return "The Address Book is empty."
    return "\n".join(str(p) for p in list(contacts.data.values()))

@input_error
def add_bday(args:list, contacts:AddressBook):
    name, date, *_ = args
    if name in contacts.data:
        return contacts.data[name].add_birthday(date)
    else:
        return "No such a name in the Address Book"
    
def upcomming_bdays(_, contacts: AddressBook):
    return contacts.get_upcoming_birthdays()

@input_error
def del_record(name:list, contacts:AddressBook):
    return contacts.delete(name[0])

def save_data(contacts:AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(contacts, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def show_info(*args):
    return info
   
def main():
    contacts = AddressBook()    
    contacts = load_data()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        # close bot
        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(contacts)
            break
        
        # available commands
        available_commands = {
            'add': add_contact,
            'add-email': new_email,
            'all': show_all,
            'change': change_contact,
            'find': finder,
            'add-bday': add_bday,
            'birthdays': upcomming_bdays,
            'del': del_record,
            'info': show_info
        }

        # command execution
        try:
            print(available_commands[command](args, contacts))
        except:
            print('Invalid command')
        
