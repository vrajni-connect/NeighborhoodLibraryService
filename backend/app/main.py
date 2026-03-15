from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select
from sqlmodel import Session

from .database import create_db_and_tables, get_session
from .models import Book, Member, Borrow

# API app instance
app = FastAPI(title="Neighborhood Library Service")

# Startup event initializes DB tables from models.
@app.on_event("startup")
def startup_event():
    create_db_and_tables()

# --- Book Endpoints ---

@app.post("/books", response_model=Book)
def create_book(book: Book, session: Session = Depends(get_session)):
    """Create a new book record."""
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book, session: Session = Depends(get_session)):
    """Update book metadata."""
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = book.title
    db_book.author = book.author
    db_book.isbn = book.isbn
    db_book.published_year = book.published_year
    db_book.total_copies = book.total_copies
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books", response_model=list[Book])
def list_books(session: Session = Depends(get_session)):
    """Return all books."""
    return session.exec(select(Book)).all()

# --- Member Endpoints ---

@app.post("/members", response_model=Member)
def create_member(member: Member, session: Session = Depends(get_session)):
    """Create a new member record."""
    session.add(member)
    session.commit()
    session.refresh(member)
    return member

@app.put("/members/{member_id}", response_model=Member)
def update_member(member_id: int, member: Member, session: Session = Depends(get_session)):
    """Update member data."""
    db_member = session.get(Member, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    db_member.name = member.name
    db_member.email = member.email
    db_member.phone = member.phone
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member

@app.get("/members", response_model=list[Member])
def list_members(session: Session = Depends(get_session)):
    """List all members."""
    return session.exec(select(Member)).all()

# --- Borrowing / Returning ---

@app.post("/borrow", response_model=Borrow)
def borrow_book(member_id: int, book_id: int, session: Session = Depends(get_session)):
    """Create a borrow record if copies are available."""
    member = session.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    active_count = session.exec(
        select(Borrow).where(Borrow.book_id == book_id, Borrow.returned_at == None)
    ).all()
    if len(active_count) >= book.total_copies:
        raise HTTPException(status_code=400, detail="All copies are currently borrowed")

    borrow = Borrow(member_id=member_id, book_id=book_id)
    session.add(borrow)
    session.commit()
    session.refresh(borrow)
    return borrow

@app.post("/return/{borrow_id}", response_model=Borrow)
def return_book(borrow_id: int, session: Session = Depends(get_session)):
    """Mark a borrow record as returned."""
    borrow = session.get(Borrow, borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.returned_at is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    from datetime import datetime
    borrow.returned_at = datetime.utcnow()
    session.add(borrow)
    session.commit()
    session.refresh(borrow)
    return borrow

@app.get("/members/{member_id}/borrowed", response_model=list[Borrow])
def borrowed_by_member(member_id: int, session: Session = Depends(get_session)):
    """List all borrow records for one member."""
    member = session.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return session.exec(select(Borrow).where(Borrow.member_id == member_id)).all()

@app.get("/borrows", response_model=list[Borrow])
def list_borrows(active_only: bool = False, session: Session = Depends(get_session)):
    """List all borrows, optionally only active (not returned)."""
    query = select(Borrow)
    if active_only:
        query = query.where(Borrow.returned_at == None)
    return session.exec(query).all()
