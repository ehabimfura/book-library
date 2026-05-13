# Book Library

A Python library management system for tracking books, users, and borrow history, with JSON-based persistence.

## Features

- Track books with title, author, genre, year, and borrow status
- Manage library users
- Borrow books with full history logging
- Primary key violation guard — prevents duplicate history entries
- Persist all data across runs via a local JSON database

## Getting Started

```bash
python3 book_library.py
```

No external dependencies required — uses the Python standard library only.

## Project Structure

```
book_library.py   # Models, database layer, and entry point
db.json           # Local data store (auto-created on first run)
```

## Data Models

### Entity (base class)
Inherited only by `History`. Provides `id`, `created_at`, `updated_at`, and `update_timestamp()`.

### Book (independent)
Stores book metadata. Not derived from `Entity`.

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Primary key |
| `Created_at` | str | Creation timestamp |
| `Updated_at` | str | Last update timestamp |
| `Title` | str | Book title |
| `Author` | str | Author name |
| `Genre` | str | Genre |
| `Year` | int | Publication year |
| `is_borrowed` | bool | Current borrow status |

### User (independent)
Stores user data. Not derived from `Entity`.

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Primary key |
| `Created_at` | str | Creation timestamp |
| `Updated_at` | str | Last update timestamp |
| `Name` | str | User's name |

### History (extends Entity)
One record per borrow event.

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Primary key |
| `Book_ID` | int | Foreign key → Book |
| `User_ID` | int | Foreign key → User |
| `date_borrowed` | str | When the book was borrowed |
| `date_returned` | str \| null | When the book was returned |

## How It Works

1. On startup, `db.json` is loaded and all three collections — books, users, and history — are reconstructed into live objects.
2. `User.borrow_book(book, history, history_id)` marks a book as borrowed and appends a new `History` entry. It first checks that `history_id` is not already present in the history list to prevent primary key violations.
3. After any borrow operation, all three arrays are serialized and written back to `db.json` atomically.
4. If `db.json` does not exist on first run, the database is seeded with four sample books and four sample users.
