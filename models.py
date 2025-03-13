from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    available_copies = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    loaned_books = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<Reader {self.name}>"

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __repr__(self):
        return f"<Loan {self.uid}>"
