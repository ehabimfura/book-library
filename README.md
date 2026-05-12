# Book Library

A simple Python library management system for tracking books and users, with JSON-based persistence.

## Features

- Add books and users to the library
- Borrow and track books by user
- Persist data across runs via a local JSON database

## Getting Started

```bash
python book_library.py
```

No external dependencies required — uses the Python standard library only.

## Project Structure

```
book_library.py   # Core models and entry point
db.json           # Local data store (auto-created on first run)
```

## How It Works

- `Book` and `User` inherit from `BookUser`, which handles ID and timestamps.
- Data is serialized to `db.json` on every run.
- If no database exists, sample data is initialized automatically.
