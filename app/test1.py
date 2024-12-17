from fastapi import FastAPI, responses, Body

app = FastAPI()

BOOKS = [
    {'title': 'title_1', 'author': 'author_1', 'category': 'math'},
    {'title': 'title_2', 'author': 'author_2', 'category': 'sci'},
    {'title': 'title_3', 'author': 'author_3', 'category': 'math'},
]

# root route


@app.get('/')
async def home():
    return responses.RedirectResponse('/docs')


@app.get('/books')
async def all_books():
    return BOOKS


# get specific category
@app.get('/get_by_category')
async def get_by_category(category: str):
    return [book.get('title') for book in BOOKS if book['category'] == category]
# first endpoint


@app.get('/books/{book_title}')
async def specific_book(book_title: str):
    for book in BOOKS:
        if book.get('title').lower() == book_title.lower():
            return book

# a post request to add more books


@app.post('/add_books')
async def add_book(book=Body()):
    if book not in BOOKS:
        BOOKS.append(book)

# A PUT request to update a book


@app.put('/update_book')
async def update_book(updated_book=Body()):
    for book in range(len(BOOKS)):
        if BOOKS[book].get('title').lower() == updated_book.get('title').lower():
            BOOKS[book] = updated_book
