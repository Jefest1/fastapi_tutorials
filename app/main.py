from fastapi import FastAPI, responses, Path, Query, HTTPException
from Dependencies.books import Books
from schemas.books import BookRequest
from core.config import settings
from starlette import status

# create an app instance
app = FastAPI(title=settings.PROJECT_TITLE)

BOOKS = [
    Books(1, 'Animals', 'Jef', 'All animals book', 4),
    Books(2, 'Python', 'Me', 'Python book', 5),
    Books(3, 'Java', 'Jef', 'Java book', 4),
    Books(4, 'C++', 'Me', 'C++ book', 5),
    Books(5, 'JavaScript', 'Jef', 'JavaScript book', 4),
]

# set a routing to docs if user access root


@app.get('/')
async def home():
    return responses.RedirectResponse('/docs')


@app.get('/books', status_code=status.HTTP_200_OK)
async def all_books():
    return BOOKS


@app.post('/add_book', status_code=status.HTTP_201_CREATED)
async def add_book(book_request: BookRequest):
    new_book = Books(**book_request.model_dump())
    BOOKS.append(get_id(new_book))

# Auto add book id


def get_id(book: Books):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

# read books by id


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail={
                        'message': f'Book with id {book_id} not found'})


@app.get('/books/', status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_by_rating = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_by_rating.append(book)
            return books_by_rating
    raise HTTPException(status_code=404, detail=f"No book with rating {
                        book_rating} found")


@app.put('/add_book', status_code=status.HTTP_204_NO_CONTENT)
async def add_book(updated_book: BookRequest):
    book_exist = False
    book = Books(**updated_book.model_dump())
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_exist = True
    if not book_exist:
        raise HTTPException(
            status_code=404, detail=f"No book with id {book.id} found")
