import csv
import json
import random
from models import db, Book, Reader

# Function to create the database tables
def create_tables(app):
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        print("Tables created successfully.")

# Function to populate the database with dummy data
def populate_books_from_json(app, file_path='dummy_books.json'):
    with open(file_path, 'r') as file:
        books_data = json.load(file)

    with app.app_context():
        for book in books_data:
            # Check if the book already exists in the database
            existing_book = Book.query.filter_by(id=book.get('id')).first()
            if not existing_book:
                new_book = Book(
                    title=book.get('title'),
                    author=book.get('author'),
                    publication_year=book.get('publication_year'),
                    available_copies=random.randint(1, 5)  # Random number of available copies
                )
                db.session.add(new_book)
        
        db.session.commit()
        print(f"Inserted {len(books_data)} books into the database.")


def populate_readers_from_json(app, file_path='dummy_readers.json'):
    with open(file_path, 'r') as file:
        readers_data = json.load(file)

    with app.app_context():
        for reader in readers_data:
            existing_reader = Reader.query.filter_by(id=reader.get('id')).first()
            if not existing_reader:
                new_reader = Reader(
                    id=reader.get('id'),
                    name=reader.get('name'),
                    address=reader.get('address'),
                    email=reader.get('email'),
                    phone=reader.get('phone'),
                    loaned_books=reader.get('loaned_books', [])  # Default to an empty list if none
                )
                db.session.add(new_reader)
        
        db.session.commit()
        print(f"Inserted {len(readers_data)} readers into the database.")


def check_credentials(username, password):
    with open("credentials.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False
