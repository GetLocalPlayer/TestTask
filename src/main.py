from typing import Any
from command_listener import CommandListener
from book import Book


db = []
filepath = "db"
cmd = CommandListener()


def save_to_disc() -> None:
    """Converts each book's data into a string where each field
    value is separated by new line and saves it to a text file."""
    with open(filepath, "w") as f:
        for b in db:
            nl = '\n'
            s = f"{nl if f.tell() else ''}{b.id}{nl}{b.title}{nl}{b.author}{nl}{b.year_published}{nl}{int(b.available)}"
            f.write(s)


def load_from_disc() -> None:
    """Loads the database file from the disc, converting its text
    into Book instances following the pattern it was saved with
    in `save_to_disc()` fu
    nciton. """
    try:
        with open(filepath, "r") as f:
            data = f.read().splitlines()
            for i in range(0, len(data), 5):
                id, title, author, year, available = data[i: i + 5]
                b = Book(int(id), title, author, int(year))
                b.available = bool(int(available))
                db.append(b)
    except FileNotFoundError:
        print("No database file found. Another will be created.")
    except ValueError:
        print("Error: cannot read the database file format. Another will be created.")


@cmd.register_command("add", "adds a book to the database with unique ID.")
def add(args: str) -> None:
    print("Enter the book's title > ", end="")
    title = input()
    print("Enter the book's author > ", end="")
    author = input()
    print("Enter the year when the book was published > ", end="")
    try:
        year = int(input())
    except ValueError:
        print("Error: incorrect year.")
    else:
        b = Book(0 if not db else db[-1].id + 1, title, author, year)
        db.append(b)
        print("A book has been added in the library:")
        b.print()
    print()


def find_by_field(field: str, value: Any) -> None:
    """Finds a book dependin on the passed field name and its value."""
    books = [elem for elem in db if elem.__dict__[field] == value]
    if not books:
        print("No book found.")
    else:
        print(f"Found {len(books)} book{'s' if books else ''}:")
        for b in books:
            print(f"    ", end="")
            b.print()
        print()
    return books
    

@cmd.register_command("find_author", "find a book by the given author.")
def find_by_author(args: str) -> None:
    if not args:
        print("Enter the book's author.")
        return
    find_by_field("author", args.strip())


@cmd.register_command("find_title", "find a book by the given title.")
def find_by_title(args: str) -> None:
    if not args:
        print("Enter the book's title.")
        return
    find_by_field("title", args.strip())


@cmd.register_command("find_year", "find a book by the given year the book was published in.")
def find_by_year(args: str) -> None:
    if not args:
        print("Enter the year when the book was published.")
        return
    try:
        y = int(args)
    except ValueError:
        print("Error: incorrect year given.")
    else:
        find_by_field("year_published", y)


@cmd.register_command("find", "finds a book by the given title, author, or year of publication.")
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


@cmd.register_command("delete", "deletes a book with the given Id from the database.")
def delete(args: str) -> None:
    if not args:
        print("Enter a valid Id.")
        return
    try:
        id = int(args)
    except ValueError:
        print("Error: incorrect Id")
        return
    try:
        b: Book = next(elem for elem in db if elem.id == id)
    except StopIteration:
        print(f"No book found with Id {id}")
    else:
        db.remove(b)
        print(f"    Book deleted:\n    ", end="")
        b.print()


@cmd.register_command("change_status", "changes the status of the book from \"available\" to \"checked out\" and vice versa")
def change_status(args: str) -> None:
    try:
        id = int(args)
    except ValueError:
        print("Error: incorrect Id")
        return 
    try:
        b: Book = next(elem for elem in db if elem.id == id)
    except StopIteration:
        print(f"No book found with Id {id}")
    else:
        b.available = not b.available
        print(f"Book status changed: \"{b.title}\"\n    Written by {b.author}\n    Published in {b.year_published}")
        print(f"""    New status: {"available" if b.available else "checked out"}""")


@cmd.register_command("show_all", "shows all books currenly recorded in the library.")
def show_all(args: str) -> None:
    if not db:
        print("No book exists in the library.")
    for b in db:
        print("    ")
        b.print(end="")
    print("\n")


@cmd.register_command("close", "closes the application.")
def close(args: str) -> None:
    cmd.stop()



if __name__ == "__main__":
    load_from_disc()
    print("************* Welcome to the library *************")
    print("Enter your command or type `help` to see the list of available commands.")
    cmd.run()
    save_to_disc()
    print("The session is over.")
    print()