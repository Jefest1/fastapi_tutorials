from sqlalchemy.orm import Session
from models.books import BookTable
from schemas.books import BookRequest
from fastapi import HTTPException


async def get_books(db: Session):
    return db.query(BookTable).all()


async def create_book(db: Session, book: BookRequest):
    new_book = BookTable(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)


async def get_book_by_id_db(book_id: int, db: Session):
    book = db.query(BookTable).filter(BookTable.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def get_book_by_author_db(author: str, db: Session):
    books = db.query(BookTable).filter(BookTable.author == author).all()
    if books is None:
        raise HTTPException(
            status_code=404, detail=f"No Book found for {author}")
    return books


async def update_book(book_id: int, db: Session, book_request: BookRequest):
    book = await get_book_by_id_db(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_request.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)


async def delete_book_db(book_id: int, db: Session):
    book = await get_book_by_id_db(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
