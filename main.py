from user import User
from book import Book
from catalog import Catalog
from loan import Loan
from utils import print_books

def main():
    catalog = Catalog()
    catalog.add_book(Book("1984", "George Orwell", "1234567890"))
    catalog.add_book(Book("To Kill a Mockingbird", "Harper Lee", "0987654321"))

    user = User("John Doe")
    loan_system = Loan(catalog)

    loan_system.check_out("1984", user)
    print("John's Borrowed Books:")
    print_books(user.list_borrowed_books())

    loan_system.check_in(user.list_borrowed_books()[0], user)
    print("\nCatalog after returning a book:")
    print_books(catalog.list_books())

if __name__ == "__main__":
    main()
