# Library Management System
class Book:
    def __init__(self, title, author, number_of_copies_available):
        self.title = title
        self.author = author
        self.number_of_copies_available = number_of_copies_available

    def __str__(self):
        return f"Book(title='{self.title}', author='{self.author}', copies_available={self.number_of_copies_available})"


class Reader:
    def __init__(self, name, address, email, phone):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.loaned_books = []
        self.activity_log = []

    def __str__(self):
        return f"Reader(name='{self.name}', email='{self.email}')"


class Loan:
    def __init__(self, uid, date, reader, book):
        self.uid = uid
        self.date = date
        self.reader = reader
        self.book = book

    def __str__(self):
        return f"Loan(uid={self.uid}, date='{self.date}', reader='{self.reader.name}', book='{self.book.title}')"


class Library:
    def __init__(self, name):
        self.name = name
        self.book_catalog = []
        self.loan_catalog = []
        self.reader_catalog = []


class Manager:
    def __init__(self, name):
        self.name = name

    def add(self, collection, item):
        collection.append(item)
        print(f"Added {item} to collection.")

    def get(self, collection, identifier, key="name"):
        for item in collection:
            if getattr(item, key) == identifier:
                print(f"Retrieved {item} from collection.")
                return item
        print(f"No item found with {key} = {identifier}.")
        return None

    def get_all(self, collection):
        print("Retrieved all items from collection.")
        return collection

    def update(self, collection, identifier, updates, key="name"):
        item = self.get(collection, identifier, key)
        if item:
            for attr, value in updates.items():
                setattr(item, attr, value)
            print(f"Updated {item} with {updates}.")
            return True
        print(f"Failed to update: no item with {key} = {identifier}.")
        return False

    def remove(self, collection, identifier, key="name"):
        item = self.get(collection, identifier, key)
        if item:
            collection.remove(item)
            print(f"Removed {item} from collection.")
            return True
        print(f"Failed to remove: no item with {key} = {identifier}.")
        return False


class BookManager(Manager):
    def __init__(self, name):
        super().__init__(name)


class ReaderManager(Manager):
    def __init__(self, name):
        super().__init__(name)


class LoanManager(Manager):
    def __init__(self, name):
        super().__init__(name)

    def create_loan(self, uid, date, reader, book):
        if book.number_of_copies_available > 0:
            book.number_of_copies_available -= 1
            loan = Loan(uid, date, reader, book)
            reader.loaned_books.append(book)
            print(f"Created loan {loan}.")
            return loan
        else:
            print(f"Failed to create loan: No copies available for the book '{book.title}'.")
            raise ValueError(f"No copies available for the book '{book.title}'.")

    def return_book(self, loan, loan_catalog):
        loan.book.number_of_copies_available += 1
        loan.reader.loaned_books.remove(loan.book)
        loan_catalog.remove(loan)
        print(f"Returned book '{loan.book.title}' for loan {loan}.")
        return True

'''# Example Usage
library = Library("Városi Könyvtár")
book_manager = BookManager("Könyv Menedzser")
reader_manager = ReaderManager("Olvasó Menedzser")
loan_manager = LoanManager("Kölcsönzési Menedzser")

# Adding books
book1 = Book("Egri csillagok", "Gárdonyi Géza", 3)
book_manager.add(library.book_catalog, book1)
book2 = Book("Pál utcai fiúk", "Molnár Ferenc", 5)
book_manager.add(library.book_catalog, book2)
book3 = Book("A kőszívű ember fiai", "Jókai Mór", 4)
book_manager.add(library.book_catalog, book3)

# Adding readers
reader1 = Reader("Kovács János", "Budapest, Fő utca 12.", "kovacs.janos@example.com", 123456789)
reader_manager.add(library.reader_catalog, reader1)  # Fixed to use reader_catalog
reader2 = Reader("Nagy Anna", "Debrecen, Kossuth tér 5.", "nagy.anna@example.com", 987654321)
reader_manager.add(library.reader_catalog, reader2)  # Fixed to use reader_catalog
reader3 = Reader("Szabó István", "Szeged, Petőfi utca 8.", "szabo.istvan@example.com", 112233445)
reader_manager.add(library.reader_catalog, reader3)  # Fixed to use reader_catalog

# Creating a loan
try:
    loan1 = loan_manager.create_loan(1, "2024-12-03", reader1, book1)
    loan_manager.add(library.loan_catalog, loan1)
except ValueError as e:
    print(e)

# Returning a book
loan_manager.return_book(loan1, library.loan_catalog)
'''