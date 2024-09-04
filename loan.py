class Loan:
    def __init__(self, catalog):
        self.catalog = catalog

    def check_out(self, book_title, user):
        book = self.catalog.find_book(book_title)
        if book:
            user.borrow_book(book)
            self.catalog.remove_book(book)
            return True
        return False

    def check_in(self, book, user):
        user.return_book(book)
        self.catalog.add_book(book)