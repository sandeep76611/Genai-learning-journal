from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    book_number: int
    author: str
    description: str


books_db = {}

# -------------------- CREATE --------------------
@app.post("/books/")
def create_book(book: Book):
    if book.book_number in books_db:
        raise HTTPException(status_code=400, detail="Book already exists")
    books_db[book.book_number] = book.dict()
    return {"message": "Book created successfully", "book": books_db[book.book_number]}

# -------------------- READ BY BOOK NUMBER--------------------
@app.get("/books/{book_number}")
def read_book(book_number: int):
    if book_number not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": books_db[book_number]}

# -------------------- READ ALL BOOKS --------------------
@app.get("/books/")
def read_all_books():
    return {"all_books": books_db}

# -------------------- UPDATE --------------------
@app.put("/books/{book_number}")
def update_book(book_number: int, book: Book):
    if book_number not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_number] = book.dict()
    return {"message": "Book updated successfully", "book": books_db[book_number]}

# -------------------- DELETE --------------------
@app.delete("/books/{book_number}")
def delete_book(book_number: int):
    if book_number not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    deleted_book = books_db.pop(book_number)
    return {"message": "Book deleted successfully", "book": deleted_book}




    # 1: {"book_number": 1, "author": "Eric Matthes", "description": "A hands-on introduction to Python programming."},
    # 2: {"book_number": 2, "author": "Mark Lutz", "description": "Comprehensive guide to Python language and libraries."},
    # 3: {"book_number": 3, "author": "Luciano Ramalho", "description": "Advanced concepts and best practices in Python."},
    # 4: {"book_number": 4, "author": "Joshua Bloch", "description": "Guide to writing effective Java code."},
    # 5: {"book_number": 5, "author": "Robert C. Martin", "description": "Principles of writing clean, maintainable code."},
    # 6: {"book_number": 6, "author": "Andrew Hunt & David Thomas", "description": "Tips for becoming a pragmatic software developer."},
    # 7: {"book_number": 7, "author": "Thomas H. Cormen", "description": "In-depth coverage of algorithms and data structures."},
    # 8: {"book_number": 8, "author": "Erich Gamma", "description": "Classic reference on design patterns in software engineering."},
    # 9: {"book_number": 9, "author": "Ian Goodfellow", "description": "Comprehensive guide to deep learning concepts."},
    # 10: {"book_number": 10, "author": "Stuart Russell", "description": "Foundational book on artificial intelligence."}

# {
#     "book_number": 11,
#     "author": "George Orwell",
#     "description": "A dystopian novel set in a totalitarian society under constant surveillance."
#   },
#   {
#     "book_number": 12,
#     "author": "J.K. Rowling",
#     "description": "A fantasy novel about a young wizard, Harry Potter, and his adventures."
#   },
#   {
#     "book_number": 13,
#     "author": "F. Scott Fitzgerald",
#     "description": "A novel set in the Jazz Age that critiques the American Dream."
#   },
#   {
#     "book_number": 14,
#     "author": "Harper Lee",
#     "description": "A classic novel about racial injustice in the Deep South."
#   },
#   {
#     "book_number": 15,
#     "author": "Dan Brown",
#     "description": "A thriller that blends history, art, and religion with a modern-day mystery."
#   }