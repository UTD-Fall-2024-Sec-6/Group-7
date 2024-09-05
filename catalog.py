class Catalog:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def list_books(self):
        return self.books