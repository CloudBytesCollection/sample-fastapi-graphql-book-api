import datetime
from typing import List

import strawberry
from bson import ObjectId
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult

from src.clients.db import MongoClient
from src.models.books.book_models import Book
from src.models.common.response_models import (
    CreateResponse,
    GetResponse,
    DeleteResponse,
    UpdateResponse,
)
from src.models.db.db_models import (
    DatabaseCollectionTypes,
    BulkRecordUpdateResponse,
    UpdateRecord,
)

db_client = MongoClient()


async def get_book_by_id(book_id: strawberry.ID) -> GetResponse[Book]:
    result = await db_client.get_record(
        DatabaseCollectionTypes.BOOKS.value, {"_id": ObjectId(book_id)}
    )

    return GetResponse[Book](
        result=Book.from_dict(result), error_message=None, success=True
    )


async def get_book_by_isbn(isbn: str) -> GetResponse[Book]:
    result = await db_client.get_record(
        DatabaseCollectionTypes.BOOKS.value, {"isbn": isbn}
    )

    return GetResponse[Book](
        result=Book.from_dict(result), error_message=None, success=True
    )


async def get_books_to_update() -> List[str]:
    """Retrieves books requiring an async update"""
    result = await db_client.get_records(
        DatabaseCollectionTypes.BOOKS.value, {"asyncUpdateRequired": True}
    )

    books = []

    async for doc in result:
        books.append(str(doc["_id"]))

    return books


async def bulk_update_book_ratings() -> BulkRecordUpdateResponse:
    """Updates book ratings for all books with asyncUpdateRequired flag"""
    books = await get_books_to_update()

    rating_responses = await get_bulk_avg_reservation_rating_by_book_ids(books)

    bulk_results = []
    for rating_response in rating_responses:
        update_query = {
            "rating": rating_response["avg_rating"],
            "asyncUpdateRequired": False,
            "lastUpdatedOn": datetime.datetime.now(),
        }

        result: UpdateResponse[Book] = await update_book(
            rating_response["_id"], update_query
        )

        bulk_results.append(result)

    return BulkRecordUpdateResponse(bulk_results)


async def get_bulk_avg_reservation_rating_by_book_ids(
    book_ids: List[str],
) -> List[dict]:
    """
    Retrieves the average rating for all book IDs passed in
    """
    pipeline = db_client.build_bulk_avg_value_pipeline("bookId", book_ids, "rating")

    cursor = await db_client.aggregate(DatabaseCollectionTypes.REVIEWS.value, pipeline)
    results = await cursor.to_list(length=1000)

    return results


async def create_book(book: Book) -> CreateResponse[Book]:
    new_book = book.to_dict()
    result: InsertOneResult = await db_client.create_record(
        DatabaseCollectionTypes.BOOKS.value, new_book
    )
    if result is None or result.inserted_id is None:
        book_response = CreateResponse[Book](
            result=None,
            error_message="An error occurred during book creation.",
            success=False,
        )
    else:
        new_book["_id"] = result.inserted_id
        book_response = CreateResponse[Book](
            result=Book.from_dict(new_book), error_message=None, success=True
        )

    return book_response


async def update_book(
    book_id: strawberry.ID, updated_book: dict
) -> UpdateResponse[Book]:
    result: UpdateResult = await db_client.get_and_update_record(
        DatabaseCollectionTypes.BOOKS.value,
        {"_id": ObjectId(book_id)},
        {"$set": updated_book},
    )

    if result is None:
        book_response = UpdateResponse[Book](
            result=None,
            error_message="An error occurred updating the book.",
            success=False,
        )
    else:
        book_response = UpdateResponse[Book](
            result=Book.from_dict(result),
            error_message=None,
            success=True,
        )

    return book_response


async def delete_book(book_id: strawberry.ID) -> DeleteResponse[Book]:
    delete_result: DeleteResult = await db_client.delete_record(
        DatabaseCollectionTypes.BOOKS.value, {"_id": book_id}
    )

    delete_response = DeleteResponse[Book](
        result=delete_result, record_id=book_id, error_message=None, success=True
    )

    return delete_response
