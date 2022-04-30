import datetime

from bson import ObjectId

from src.models.authors.author_models import AuthorInput
from src.models.books.book_models import Book
from src.models.common.response_models import (
    GetResponse,
    CreateResponse,
    UpdateResponse,
    DeleteResponse,
)
from src.services.books import book_service


async def resolve_get_book_by_id(book_id: str) -> GetResponse[Book]:
    return await book_service.get_book_by_id(ObjectId(book_id))


async def resolve_get_book_by_isbn(isbn: str) -> GetResponse[Book]:
    return await book_service.get_book_by_isbn(isbn)


async def resolve_create_book(
    title: str,
    author: AuthorInput,
    price: float,
    subtitle: str = None,
    description: str = None,
    isbn: str = None,
    book_format: str = None,
) -> CreateResponse[Book]:
    new_book = Book(
        None,
        title=title,
        author=author,
        price=price,
        subtitle=subtitle,
        description=description,
        isbn=isbn,
        book_format=book_format,
        rating=None,
        async_update_required=False,
        created_on=datetime.datetime.now(),
        last_updated_on=None,
    )

    return await book_service.create_book(new_book)


async def resolve_update_book(
    book_id: str,
    title: str = None,
    author: AuthorInput = None,
    price: float = None,
    subtitle: str = None,
    description: str = None,
    isbn: str = None,
    book_format: str = None,
    rating: float = None,
) -> UpdateResponse[Book]:
    new_values = {}

    if title is not None:
        new_values["title"] = title

    if price is not None:
        new_values["price"] = price

    if author is not None:
        new_values["author"] = AuthorInput.to_dict()

    if subtitle is not None:
        new_values["subtitle"] = subtitle

    if isbn is not None:
        new_values["isbn"] = isbn

    if book_format is not None:
        new_values["bookFormat"] = book_format

    if description is not None:
        new_values["description"] = description

    if rating is not None:
        new_values["rating"] = rating

    new_values["lastUpdatedOn"] = datetime.datetime.now()

    return await book_service.update_book(ObjectId(book_id), new_values)


async def resolve_delete_book(book_id: str) -> DeleteResponse[Book]:
    return await book_service.delete_book(ObjectId(book_id))
