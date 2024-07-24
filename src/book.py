class Book():
    def __init__(self, title: str, author: str, year_published: int) -> None:
        self.title = title
        self.author = author
        self.year_published = year_published
        self.available = True
    
    def print(self, end: str="\n") -> None:
        """Prints the book's data in the terminal."""
        print(f"""\"{self.title}\", written by {self.author}, published in {self.year_published}. Status: {"available" if self.available else "checked out."}""", end=end)