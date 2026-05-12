import datetime
import json
import os

DB_FILE = "db.json"

class BookUser:
    def __init__(self, id):
        self.id = id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def update_timestamp(self):
        self.updated_at = datetime.datetime.now()

class Book(BookUser):
    def __init__(self, id, title, author, year, genre):
        super().__init__(id)
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.is_borrowed = False

    def to_json_dict(self):
        created_str = self.created_at if isinstance(self.created_at, str) else self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "created_at": created_str,
            "is_borrowed": self.is_borrowed
        }

    def load_from_dict(self, data):
        book = Book(data["id"], data["title"], data["author"], data["year"], data["genre"])
        book.created_at = data["created_at"]
        book.is_borrowed = data["is_borrowed"]
        return book

class User(BookUser):
    def __init__(self, name, id):
        super().__init__(id)
        self.name = name

    def borrow_book(self, book):
        if not book.is_borrowed:
            book.is_borrowed = True
            self.update_timestamp()
            print(f"{self.name} has borrowed '{book.title}'.")
        else:
            print(f"'{book.title}' is already borrowed.")

    def to_json_dict(self):
        created_str = self.created_at if isinstance(self.created_at, str) else self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_str = self.updated_at if isinstance(self.updated_at, str) else self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "name": self.name,
            "id": self.id,
            "created_at": created_str,
            "updated_at": updated_str
        }

    def load_from_dict(self, data):
        user = User(data["name"], data["id"])
        user.created_at = data["created_at"]
        user.updated_at = data["updated_at"]
        return user


def load_database():
    if not os.path.exists(DB_FILE):
        return {"books": [], "users": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_database(db_data):
    with open(DB_FILE, "w") as f:
        json.dump(db_data, f, indent=4)


def initialize_dummy_data():
    b1 = Book(101, "The Great Gatsby", "F. Scott Fitzgerald", 1925, "Novel")
    b2 = Book(102, "To Kill a Mockingbird", "Harper Lee", 1960, "Novel")
    b3 = Book(103, "1984", "George Orwell", 1949, "Dystopian")
    b4 = Book(104, "Pride and Prejudice", "Jane Austen", 1813, "Romance")
    u1 = User("Alice", 1)
    u2 = User("Bob", 2)
    u3 = User("Carol", 3)
    u4 = User("David", 4)

    db = {
        "books": [b1.to_json_dict(), b2.to_json_dict(), b3.to_json_dict(), b4.to_json_dict()],
        "users": [u1.to_json_dict(), u2.to_json_dict(), u3.to_json_dict(), u4.to_json_dict()]
    }
    save_database(db)
    print("Database initialized with dummy data entries.")
