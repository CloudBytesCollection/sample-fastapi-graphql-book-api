from datetime import datetime
from unittest import mock

import pytest
from bson import ObjectId

from src.services.reviews import review_service
from pymongo.results import DeleteResult
from tests.test_utils.test_data import get_review_records


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.get_record")
async def test_get_review_by_id(mock_get_record):
    mock_get_record.return_value = get_review_records()[0]

    get_review_response = await review_service.get_review_by_id(
        ObjectId("620fdbb0cf1be3116b86ad87")
    )

    assert get_review_response is not None
    assert get_review_response.result.review_comments.__contains__("this was awesome")
    assert get_review_response.result.rating == 4.5
    assert get_review_response.success is True


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.get_record")
async def test_get_reviews_by_book_id(mock_get_record):
    mock_get_record.return_value = get_review_records()[1]

    get_review_response = await review_service.get_reviews_by_book_id(
        "620fdbb0cf1be3116b86ad77"
    )

    assert get_review_response is not None
    assert get_review_response.result.review_comments.__contains__("this was awful")
    assert get_review_response.result.rating == 1.5
    assert get_review_response.success is True


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.get_and_update_record")
async def test_update_review(mock_update_record):
    mock_update_record.return_value = get_review_records()[0]

    new_review_values = {
        "rating": "5.5",
        "review_comments": "New comments",
        "lastUpdatedOn": datetime.now(),
    }

    update_response = await review_service.update_review(
        ObjectId("620fdbb0cf1be3116b86ad87"), new_review_values
    )

    assert update_response is not None
    assert update_response.success is True
    assert update_response.result.id is not None


@pytest.mark.asyncio
@mock.patch("src.clients.db.MongoClient.delete_record")
async def test_delete_review(mock_delete_record):
    mock_delete_record.return_value = DeleteResult(
        raw_result={"record_deleted": 0}, acknowledged=True
    )

    delete_response = await review_service.delete_review(
        ObjectId("620fdbb0cf1be3116b86ad87")
    )

    assert delete_response is not None
    assert delete_response.success is True
    assert delete_response.record_id is not None
