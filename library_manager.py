import json
import os

# -------------------------
# Book Class
# -------------------------
class Book:
    def __init__(self, book_id, title, author, issued=False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued

    def to_dict(self):
        """Convert Book object to dict for JSON serialization"""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }

# -------------------------
# Library Class
# -------------------------
class Library:
    def __init__(self, filename="library_data.json"):
        self.filename = filename
        self.books = {}  # HashMap-like dictionary {book_id: Book}
        self.load_data()

    def load_data(self):
        """Load books from file"""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                for b in data:
                    book = Book(**b)
                    self.books[book.book_id] = book

    def save_data(self):
        """Save all books to JSON file"""
        with open(self.filename, "w") as f:
            json.dump([b.to_dict() for b in self.books.values()], f, indent=4)

    # -------------------------
    # Book Operations
    # -------------------------
    def add_book(self, book_id, title, author):
        if book_id in self.books:
            print("❌ Book ID already exists!")
            return
        book = Book(book_id, title, author)
        self.books[book_id] = book
        self.save_data()
        print("✅ Book added successfully!")

    def search_by_title(self, title):
        results = [b for b in self.books.values() if title.lower() in b.title.lower()]
        self.display_books(results, f"Search Results for Title '{title}'")

    def search_by_author(self, author):
        results = [b for b in self.books.values() if author.lower() in b.author.lower()]
        self.display_books(results, f"Search Results for Author '{author}'")

    def issue_book(self, book_id):
        if book_id not in self.books:
            print("❌ Book not found!")
