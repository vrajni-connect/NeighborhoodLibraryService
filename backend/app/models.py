from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# Book table stores each title entry and copy count.
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    borrows: List["Borrow"] = Relationship(back_populates="book")

# Member table stores library members.
class Member(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    borrows: List["Borrow"] = Relationship(back_populates="member")

# Borrow table tracks each borrow operation and optional return time.
class Borrow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    member_id: int = Field(foreign_key="member.id")
    book_id: int = Field(foreign_key="book.id")
    borrowed_at: datetime = Field(default_factory=datetime.utcnow)
    returned_at: Optional[datetime] = None

    # Relationship fields for ORM access.
    member: Optional[Member] = Relationship(back_populates="borrows")
    book: Optional[Book] = Relationship(back_populates="borrows")
