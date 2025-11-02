from models import AddressBook, Record

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

NOT_EXIST = "Contact does not exist, try to add it."

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            # Return our custom errors
            return e if str(e) in [
                'Number should contain 10 digits',
                'Invalid date format. Use DD.MM.YYYY',
                'Record does not have such number'
            ] else f"Enter the argument for the command:\n{HELP}"
        except AttributeError:
            return NOT_EXIST

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
    rec.add_phone(phone)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    rec = book.find(name)
    rec.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book):
    name, = args
    rec = book.find(name)
    return "; ".join([r.value for r in rec.phones])

@input_error
def show_all(book):
    return "\n".join([f"{rec}" for rec in book.data.values()])


@input_error
def add_birthday(args, book):
    name, date = args
    rec = book.find(name)
    rec.set_birthday(date)
    return f"Set birthday for {name}."


@input_error
def show_birthday(args, book):
    name, = args
    rec = book.find(name)
    date = rec.get_birthday()
    return date if date else f"Birthday for {name} is not set."


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
