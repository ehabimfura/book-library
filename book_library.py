import datetime
import json
import os

DB_FILE = "db.json"


class Entity:
    def __init__(self, id):
        self.id = id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def update_timestamp(self):
        self.updated_at = datetime.datetime.now()


class Book:
    def __init__(self, id, title, author, genre, year):
        self.id = id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.is_borrowed = False

    def to_json_dict(self):
        created_str = self.created_at if isinstance(self.created_at, str) else self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_str = self.updated_at if isinstance(self.updated_at, str) else self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "id": self.id,
            "Created_at": created_str,
            "Updated_at": updated_str,
            "Title": self.title,
            "Author": self.author,
            "Genre": self.genre,
            "Year": self.year,
            "is_borrowed": self.is_borrowed
        }

    def load_from_dict(self, data):
        book = Book(data["id"], data["Title"], data["Author"], data["Genre"], data["Year"])
        book.created_at = data["Created_at"]
        book.updated_at = data["Updated_at"]
        book.is_borrowed = data["is_borrowed"]
        return book


class User:
    def __init__(self, id, name):
        self.id = id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.name = name

    def borrow_book(self, book, history, history_id):
        if any(h.id == history_id for h in history):
            print(f"History entry with id {history_id} already exists (PK violation). Borrow aborted.")
            return
        if not book.is_borrowed:
            book.is_borrowed = True
            self.update_timestamp()
            entry = History(history_id, book.id, self.id)
            history.append(entry)
            print(f"{self.name} has borrowed '{book.title}'.")
        else:
            print(f"'{book.title}' is already borrowed.")

    def update_timestamp(self):
        self.updated_at = datetime.datetime.now()

    def to_json_dict(self):
        created_str = self.created_at if isinstance(self.created_at, str) else self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_str = self.updated_at if isinstance(self.updated_at, str) else self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "id": self.id,
            "Created_at": created_str,
            "Updated_at": updated_str,
            "Name": self.name
        }

    def load_from_dict(self, data):
        user = User(data["id"], data["Name"])
        user.created_at = data["Created_at"]
        user.updated_at = data["Updated_at"]
        return user


class History(Entity):
    def __init__(self, id, book_id, user_id):
        super().__init__(id)
        self.book_id = book_id
        self.user_id = user_id
        self.date_borrowed = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_returned = None

    def to_json_dict(self):
        return {
            "id": self.id,
            "Book_ID": self.book_id,
            "User_ID": self.user_id,
            "date_borrowed": self.date_borrowed,
            "date_returned": self.date_returned
        }

    def load_from_dict(self, data):
        entry = History(data["id"], data["Book_ID"], data["User_ID"])
        entry.date_borrowed = data["date_borrowed"]
        entry.date_returned = data["date_returned"]
        return entry


def load_database():
    if not os.path.exists(DB_FILE):
        return {"books": [], "users": [], "history": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_database(db_data):
    with open(DB_FILE, "w") as f:
        json.dump(db_data, f, indent=4)


def initialize_dummy_data():
    b1 = Book(101, "The Great Gatsby", "F. Scott Fitzgerald", "Novel", 1925)
    b2 = Book(102, "To Kill a Mockingbird", "Harper Lee", "Novel", 1960)
    b3 = Book(103, "1984", "George Orwell", "Dystopian", 1949)
    b4 = Book(104, "Pride and Prejudice", "Jane Austen", "Romance", 1813)
    u1 = User(1, "Alice")
    u2 = User(2, "Bob")
    u3 = User(3, "Carol")
    u4 = User(4, "David")

    db = {
        "books": [b1.to_json_dict(), b2.to_json_dict(), b3.to_json_dict(), b4.to_json_dict()],
        "users": [u1.to_json_dict(), u2.to_json_dict(), u3.to_json_dict(), u4.to_json_dict()],
        "history": []
    }
    save_database(db)
    print("Database initialized with dummy data entries.")


if not os.path.exists(DB_FILE):
    initialize_dummy_data()

db = load_database()

active_books = [Book(0, "", "", "", 0).load_from_dict(b) for b in db["books"]]
active_users = [User(0, "").load_from_dict(u) for u in db["users"]]
active_history = [History(0, 0, 0).load_from_dict(h) for h in db.get("history", [])]

print("\n--- Displaying Books Read From Storage ---")
for book in active_books:
    print(f"[{book.id}] {book.title} - Borrowed Status: {book.is_borrowed}")

print("\n--- Modifying Title of Book 101 ---")
active_books[0].title = "The Great Gatsby (Special Edition)"

active_users[1].borrow_book(active_books[0], active_history, history_id=1001)

db["books"] = [book.to_json_dict() for book in active_books]
db["users"] = [user.to_json_dict() for user in active_users]
db["history"] = [entry.to_json_dict() for entry in active_history]
save_database(db)
print("\nChanges saved successfully to db.json.")
