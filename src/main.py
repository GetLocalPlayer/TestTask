from typing import Any
from command_listener import CommandListener
from book import Book
from book_storage import BookStorage


FILEPATH = "db"

# Commands (command, description)
CMD_ADD = "add", "adds a book to the database with unique ID."
CMD_DELETE = "delete", "deletes a book with the given Id from the database."
CMD_FIND = "find", "finds a book by the given title, author, or year of publication."
CMD_FIND_BY_YEAR = "find_year", "find a book by the given year the book was published in."
CMD_FIND_BY_AUTHOR = "find_author", "find a book by the given author."
CMD_FIND_BY_TITLE = "find_title", "find a book by the given title."
CMD_CLOSE = "close", "closes the application."
CMD_SHOW_ALL = "show_all", "shows all books currenly recorded in the library."
CMD_CHANGE_STATUS = "change_status", "changes the status of the book from \"available\" to \"checked out\" and vice versa"

# Errors
ERR_INCORRECT_ID = "Error: incorrect ID,"
ERR_INCORRECT_YEAR = "Error: incorrect year."

# Messages
MSG_NO_BOOK_FOUND = "No book found."
MSG_NO_BOOK_EXISTS = "No book exists in the library."
MSG_STATUS_CHANGED = "Book status changed"


cmd = CommandListener()
storage = BookStorage(FILEPATH)


@cmd.register_command(CMD_ADD[0], CMD_ADD[1])
def add(args: str) -> None:
    print("Enter the book's title > ", end="")
    title = input()
    print("Enter the book's author > ", end="")
    author = input()
    print("Enter the year when the book was published > ", end="")
    try:
        year = int(input())
    except ValueError:
        print(ERR_INCORRECT_YEAR)
    else:
        b = Book(title, author, year)
        id = storage.add(b)
        print("The book has been added in the library with id: %d\n    " % id, end="")
        b.print()
    print()


def find_by_field(field: str, value: Any) -> None:
    """Finds a book dependin on the passed field name and its value."""
    books = storage.find(lambda id, b : b.__dict__[field] == value)
    if not books:
        print(MSG_NO_BOOK_FOUND)
    else:
        print("Found %d book%s:" % (len(books), "s" if len(books) > 0 else ""))
        for id, b in sorted(books.items()):
            print("    [id: %d]" % id, end="")
            b.print()
        print()
    return books
    

@cmd.register_command(CMD_FIND_BY_AUTHOR[0], CMD_FIND_BY_AUTHOR[1])
def find_by_author(args: str) -> None:
    if not args:
        print("Enter the book's author.")
        return
    find_by_field("author", args.strip())


@cmd.register_command(CMD_FIND_BY_TITLE[0], CMD_FIND_BY_TITLE[1])
def find_by_title(args: str) -> None:
    if not args:
        print("Enter the book's title.")
        return
    find_by_field("title", args.strip())


@cmd.register_command(CMD_FIND_BY_YEAR[0], CMD_FIND_BY_YEAR[1])
def find_by_year(args: str) -> None:
    if not args:
        print("Enter the year when the book was published.")
        return
    try:
        y = int(args)
    except ValueError:
        print(ERR_INCORRECT_YEAR)
    else:
        find_by_field("year_published", y)


@cmd.register_command(CMD_FIND[0], CMD_FIND[1])
def find(args: str) -> None:
    if not args:
        print("Enter the title, the author's name, or the year when the book was published.")
        return
    print("Searching by title...")
    find_by_title(args)
    print("Searching by author...")
    find_by_author(args)
    if args.isdigit():
        print("Searching by year...")
        find_by_year(args)


@cmd.register_command(CMD_DELETE[0], CMD_DELETE[1])
def delete(args: str) -> None:
    if not args:
        print("Enter a valid Id.")
        return
    try:
        id = int(args)
    except ValueError:
        print(ERR_INCORRECT_ID)
        return
    b: Book = storage.pop(id)
    if b:
        print(f"Book deleted:\n    ", end="")
        b.print()
    else:
        print(MSG_NO_BOOK_FOUND)


@cmd.register_command(CMD_CHANGE_STATUS[0], CMD_CHANGE_STATUS[1])
def change_status(args: str) -> None:
    try:
        id = int(args)
    except ValueError:
        print(ERR_INCORRECT_ID)
        return 
    b: Book = storage.get(id)
    if b:
        b.available = not b.available
        print("%s\n    " % MSG_STATUS_CHANGED, end="")
        b.print()
    else:
        print(MSG_NO_BOOK_FOUND)


@cmd.register_command(CMD_SHOW_ALL[0], CMD_SHOW_ALL[1])
def show_all(args: str) -> None:
    ids = list(storage)
    if not ids:
        print(MSG_NO_BOOK_EXISTS)
        return
    for id in ids:
        print("    [id: %d]" % (id), end="")
        storage.get(id).print()
    print("\n")


@cmd.register_command(CMD_CLOSE[0], CMD_CLOSE[1])
def close(args: str) -> None:
    cmd.stop()


if __name__ == "__main__":
    print("************* Welcome to the library *************")
    storage.load_from_disc()
    print("Enter your command or type `help` to see the list of available commands.")
    cmd.run()
    storage.save_to_disc()
    print("The session is over.")
    print()