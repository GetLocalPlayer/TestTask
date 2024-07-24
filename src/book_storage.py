from typing import Callable
from book import Book


class BookStorage():
    def __init__(self, file_path: str) -> None:
        """Creates a new book storage using the given path as
        a path to save the storage's data on the disc."""
        self._books = {}
        self._file_path = file_path
        # Counter for unuque ids.
        self._last_id = 0

    def __iter__(self):
        """ALlows to iterate the storage by sorted ids. """
        return (id for id in sorted(self._books.keys()))

    def add(self, b: Book) -> int:
        """Adds the given book into the storage.
        Return the added book's id."""
        self._last_id += 1
        self._books.update( {self._last_id: b} )
        return self._last_id

    def pop(self, id: int) -> Book | None:
        """Removes a book by the given id from the storage
        returning it if is found or `None` otherwise. """
        try:
            return self._books.pop(id)
        except KeyError:
            return None
        
    def get(self, id: int) -> Book | None:
        """Returns the first book in the database with given ID."""
        try:
            return self._books[id]
        except KeyError:
            return None
        
    def find(self, filter: Callable[[int, Book], bool]) -> dict[int, Book]:
        """Returns a dictionarry of Books in format [id: Book]
        for which the passed filter returns `True`. The filter
        recieves the id and the book instance."""
        return {id: b for id, b in self._books.items() if filter(id, b)}

        
    def save_to_disc(self) -> None:
        """Converts each book's data into a string where each field
        value is separated by new line and saves it to a text file."""
        with open(self._file_path, "w") as f:
            f.write(str(self._last_id))
            for id, b in self._books.items():
                s = "\n%d\n%s\n%s\n%d\n%d" % (id, b.title, b.author, b.year_published, int(b.available))
                f.write(s)


    def load_from_disc(self) -> None:
        """Loads the database file from the disc, converting its text
        into Book instances following the pattern it was saved with
        in `save_to_disc()` method. """
        try:
            with open(self._file_path, "r") as f:
                data = f.read().splitlines()
                self._last_id = int(data.pop(0))
                for i in range(0, len(data), 5):
                    id, title, author, year, available = data[i: i + 5]
                    b = Book(title, author, int(year))
                    b.available = bool(int(available))
                    self._books.update( {int(id): b} )
                print("%d book%s have been load." % (len(self._books), "" if len(self._books) == 1 else "s"))
        except FileNotFoundError:
            print("No database file found. Another will be created.")
        except ValueError:
            print("Error: cannot read the database file format. Another will be created.")
            self._books = {}
            self._last_id = 0
        