from datetime import datetime
from unittest import mock

import pytest
from bson import ObjectId
from src.models.authors.author_models import Author
from src.models.books.book_models import Book
from src.services.books import book_service
from pymongo.results import InsertOneResult, DeleteResult

from tests.test_utils.test_data import get_book_records


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.get_record")
async def test_get_book_by_id(mock_get_record):
    mock_get_record.return_value = get_book_records()[0]

    get_book_response = await book_service.get_book_by_id(
        ObjectId("620fdbb0cf1be3116b86ad77")
    )

    assert get_book_response is not None
    assert get_book_response.result.author.first_name.__contains__("Fake")
    assert get_book_response.result.author.last_name.__contains__("Author")
    assert get_book_response.result.title.__contains__("Book1")
    assert get_book_response.success is True


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.get_record")
async def test_get_book_by_isbn(mock_get_record):
    mock_get_record.return_value = get_book_records()[0]

    get_book_response = await book_service.get_book_by_isbn("9781234567812")

    assert get_book_response is not None
    assert get_book_response.result.author.first_name.__contains__("Fake")
    assert get_book_response.result.author.last_name.__contains__("Author")
    assert get_book_response.result.title.__contains__("Book1")
    assert get_book_response.success is True


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.get_record")
async def test_get_book_by_id(mock_get_record):
    mock_get_record.return_value = get_book_records()[0]

    get_book_response = await book_service.get_book_by_id(
        ObjectId("620fdbb0cf1be3116b86ad77")
    )

    assert get_book_response is not None
    assert get_book_response.result.author.first_name.__contains__("Fake")
    assert get_book_response.result.author.last_name.__contains__("Author")
    assert get_book_response.result.title.__contains__("Book1")
    assert get_book_response.success is True


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.create_record")
async def test_create_book(mock_create_record):
    mock_create_record.return_value = InsertOneResult(
        inserted_id="61c254f4f2931ef2972ef812", acknowledged=True
    )

    author = Author(first_name="Fake", last_name="Author")

    new_book = Book(
        _id="",
        title="Test Book",
        author=author,
        price=9.99,
        subtitle="subtitle",
        description="description",
        isbn=9781234567812,
        book_format="paperback",
        rating="",
        async_update_required=False,
        created_on="",
        last_updated_on="",
    )

    create_response = await book_service.create_book(new_book)

    assert create_response is not None
    assert create_response.result.author.first_name.__contains__("Fake")
    assert create_response.result.author.last_name.__contains__("Author")
    assert create_response.result.author.middle_name is None
    assert create_response.result.isbn == 9781234567812
    assert create_response.success is True
    assert create_response.result.id is not None


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.create_record")
async def test_create_book_failure(mock_create_record):
    mock_create_record.return_value = InsertOneResult(
        inserted_id=None, acknowledged=False
    )

    author = Author(first_name="Fake", last_name="Author")

    new_book = Book(
        _id=None,
        title="Test Book",
        author=author,
        price=9.99,
        subtitle="subtitle",
        description="description",
        isbn=9781234567812,
        book_format="paperback",
        rating="",
        async_update_required=False,
        created_on="",
        last_updated_on="",
    )

    create_response = await book_service.create_book(new_book)

    assert create_response is not None
    assert create_response.success is False
    assert create_response.result is None


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.get_and_update_record")
async def test_update_book(mock_update_record):
    mock_update_record.return_value = get_book_records()[0]

    new_book_values = {
        "title": "Updated Title",
        "subtitle": "Updated Subtitle",
        "format": "ebook",
        "lastUpdatedOn": datetime.now(),
    }

    update_response = await book_service.update_book(
        ObjectId("620fdbb0cf1be3116b86ad77"), new_book_values
    )

    assert update_response is not None
    assert update_response.result.author.first_name.__contains__("Fake")
    assert update_response.result.author.last_name.__contains__("Author")
    assert update_response.result.author.middle_name is None
    assert update_response.success is True


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.delete_record")
async def test_delete_book(mock_delete_record):
    mock_delete_record.return_value = DeleteResult(
        raw_result={"record_deleted": 0}, acknowledged=True
    )

    delete_response = await book_service.delete_book(
        ObjectId("620fdbb0cf1be3116b86ad77")
    )

    assert delete_response is not None
    assert delete_response.success is True
    assert delete_response.record_id is not None
