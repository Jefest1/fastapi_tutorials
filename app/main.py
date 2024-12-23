from fastapi import FastAPI, responses, Path, Query, HTTPException, Depends
from Dependencies.books import (get_books,
                                create_book, get_book_by_id_db,
                                get_book_by_author_db, update_book,
                                delete_book_db)
from schemas.books import BookRequest
from core.config import settings
from starlette import status
from db.base import Base
from db.session import engine, get_db
from sqlalchemy.orm import Session

# create a database
Base.metadata.create_all(bind=engine)

# # create an app instance
app = FastAPI(title=settings.PROJECT_TITLE)


# # set a routing to docs if user access root


@app.get('/', status_code=status.HTTP_200_OK)
async def home():
    return responses.RedirectResponse('/docs')


@app.get('/books', status_code=status.HTTP_200_OK)
async def all_books(db: Session = Depends(get_db)):
    books = await get_books(db)
    return books


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return await get_book_by_id_db(book_id, db)


@app.get('/books/author/{author}', status_code=status.HTTP_200_OK)
async def get_book_by_author(author: str, db: Session = Depends(get_db)):
    return await get_book_by_author_db(author, db)


@app.post('/add_book', status_code=status.HTTP_201_CREATED)
async def add_book(book_request: BookRequest, db: Session = Depends(get_db)):
    # get create book function
    await create_book(db, book_request)


@app.put('/books/edit/edit_book', status_code=status.HTTP_204_NO_CONTENT)
async def edit_book(book_id: int, book: BookRequest, db: Session = Depends(get_db),):
    await update_book(book_id, db, book)


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    await delete_book_db(book_id, db)
