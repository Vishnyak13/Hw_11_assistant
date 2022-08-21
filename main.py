from collections import UserDict
from typing import List, Tuple


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: Name, phones: List[Phone] = []) -> None:
        self.name = name
        self.phones = phones

    def add_phone(self, phone: Phone) -> Phone | None:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return phone

    def del_phone(self, phone: Phone) -> None:
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return p

    def change_phone(self, phone, new_phone) -> Tuple[Phone, Phone] | None:
        if self.del_phone(phone):
            self.add_phone(new_phone)
            return phone, new_phone

    def __str__(self) -> str:
        return f'Phones {", ".join([p.value for p in self.phones])}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> Record | None:
        self.data[record.name.value] = record
        return record

    def del_record(self, key: str) -> Record | None:
        rec_del = self.data.get(key)
        if rec_del:
            self.data.pop(key)
            return rec_del


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Please enter the contact in the format:\nName: phone number"
        except ValueError:
            return "Incorrectly entered command!"
        except KeyError:
            return "Contact not found"

    return inner


def unknown_command(*args):
    return "Unknown command, try again or write 'help'!"


def greeting(*args):
    return "Hello! How can I help you?"


def to_exit(*args):
    return "Good bye!"


contact_dict = AddressBook()


@input_error
def add_contact(*args):
    rec = Record(Name(args[0]), [Phone(args[1])])
    if contact_dict.add_record(rec):
        return f"Contact {rec.name.value} successfully added!"
    else:
        return f"Contact {rec.name.value} already in contact list"


@input_error
def change_phone(*args):
    rec = contact_dict.get(args[0])
    if rec:
        rec.change_phone(Phone(args[1]), Phone(args[2]))
        return f'Contact {rec.name.value} has changed successfully.'
    return f'Contact, with name {args[0]} not in contacts list.'


@input_error
def remove_contact(*args):
    rec = notebook.get(args[0])
    if rec:
        rec.del_phone(Phone(args[1]))
        return f'Contact {args[1]} has deleted successfully from contact {rec.name.value}.'
    return f'Contact, with name {args[0]} not in contacts list.'


@input_error
def find_phone(*args):
    return contact_dict[args[0]]


def show_all(*args):
    return "\n".join([f"{key.title()}: {value}" for key, value in contact_dict.items()]) if len(
        contact_dict) > 0 else 'Contacts are empty'


def help(*args):
    return """
Enter "hello", "hi" for greeting
Enter "add", "new" for add new contact
Enter "change", "replace" for change phone
Enter "phone", "number", "find" for find phone
Enter "show all", "show" for show all contacts
Enter "good bye", "close", "exit", ".", "bye", "stop" for exit exit the program
Enter "del", "delete", "remove" for delete contact
Enter "help" to open a list of all commands
"""


commands = {
    greeting: ["hello", "hi"],
    add_contact: ["add", "new"],
    change_phone: ["change", "replace"],
    find_phone: ["phone", "number", "find"],
    show_all: ["show all", "show"],
    to_exit: ["good bye", "close", "exit", ".", "bye", "stop"],
    remove_contact: ["del", "delete", "remove"],
    help: ["help"]
}


def input_parser(user_input):
    for key, values in commands.items():
        for i in values:
            if user_input.lower().startswith(i.lower()):
                return key, user_input[len(i):].strip().split()
    else:
        return unknown_command, []


def main():
    while True:
        user_input = input('Waiting your command:>>> ')
        command, parser_data = input_parser(user_input)
        print(command(*parser_data))
        if command is to_exit:
            break


if __name__ == "__main__":
    main()
