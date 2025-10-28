from models import AddressBook, Record, BotError

HELP = f"""
add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує.
change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
phone [ім'я]: Показати телефонні номери для вказаного контакту.
all: Показати всі контакти в адресній книзі.
add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
show-birthday [ім'я]: Показати дату народження для вказаного контакту.
birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
hello: Отримати вітання від бота.
close або exit: Закрити програму.
"""

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError):
            return f"Enter the argument for the command:\n{HELP}"
        except BotError as e:
            return e

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone = args
    rec = book.find(name)
    # If no contact, create it
    if rec is None:
        rec = Record(name)
        book.add_record(rec)
    rec.set_phone(phone)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, phone = args
    rec = book.find(name)
    if rec:
        rec.set_phone(phone)
        return "Contact updated."
    raise BotError("Contact does not exist, try to add it.")


@input_error
def show_phone(args, book):
    name, = args
    rec = book.find(name)
    if rec:
        return rec.get_phone()
    raise BotError("Contact does not exist, try to add it.")


def show_all(book):
    return "\n".join([f"{name}: {rec.get_phone()}" for name, rec in book.data.items()])


@input_error
def add_birthday(args, book):
    name, date = args
    rec = book.find(name)
    if rec:
        rec.set_birthday(date)
        return f"Set birthday for {name}."
    raise BotError("Contact does not exist, try to add it.")


@input_error
def show_birthday(args, book):
    name, = args
    rec = book.find(name)
    if rec:
        date = rec.get_birthday()
        if date:
            return date
        raise BotError(f"Birthday for {name} is not set.")
    raise BotError("Contact does not exist, try to add it.")


def birthdays(book):
    return "\n".join([f"{rec['name']}: {rec['congratulation_date']}" for rec in book.get_upcoming_birthdays()])


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)
        except KeyboardInterrupt:
            print("") # Add new line
            command = "exit"

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print(f"Invalid command.\n{HELP}")


if __name__ == "__main__":
    main()
