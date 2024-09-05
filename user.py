class User:
    def __init__(self, name):
        self.name = name
        self.books_borrowed = []

    def borrow_book(self, book):
        self.books_borrowed.append(book)

    def return_book(self, book):
        self.books_borrowed.remove(book)

    def list_borrowed_books(self):
        return self.books_borrowed