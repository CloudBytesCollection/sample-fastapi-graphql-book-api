from typing import List

from bson import ObjectId
from datetime import datetime


def get_book_records() -> dict:
    return [
        {
            "_id": ObjectId("620fdbb0cf1be3116b86ad77"),
            "id": None,
            "title": "Book1",
            "author": {
                "first_name": "Fake",
                "last_name": "Author",
                "middle_name": None,
            },
            "price": 16.99,
            "subtitle": "fake",
            "description": "Fake Book Entry",
            "isbn": "9781234567812",
            "bookFormat": "ebook",
            "rating": 4.166666666666667,
            "asyncUpdateRequired": False,
            "createdOn": datetime(2022, 2, 18, 10, 47, 28, 138000),
            "lastUpdatedOn": datetime(2022, 3, 22, 16, 35, 37, 936000),
        },
        {
            "_id": ObjectId("620fdbb0cf1be3116b86ad78"),
            "id": None,
            "title": "Book2",
            "author": {
                "first_name": "False",
                "last_name": "Author",
                "middle_name": None,
            },
            "price": 16.99,
            "subtitle": "fake",
            "description": "Fake Book Entry",
            "isbn": "9781234567812",
            "bookFormat": "ebook",
            "rating": 4.166666666666667,
            "asyncUpdateRequired": False,
            "createdOn": datetime(2022, 2, 18, 10, 47, 28, 138000),
            "lastUpdatedOn": datetime(2022, 3, 22, 16, 35, 37, 936000),
        },
    ]


def get_review_records() -> List[dict]:
    return [
        {
            "_id": ObjectId("620fdbb0cf1be3116b86ad87"),
            "rating": 4.5,
            "review_comments": "this was awesome",
            "createdOn": datetime(2022, 2, 18, 10, 47, 28, 138000),
            "reviewer_id": "Viratec",
            "lastUpdatedOn": datetime(2022, 3, 22, 16, 35, 37, 936000),
            "book_id": "620fdbb0cf1be3116b86ad77",
        },
        {
            "_id": ObjectId("620fdbb0cf1be3116b86ad88"),
            "rating": 1.5,
            "review_comments": "this was awful",
            "createdOn": datetime(2022, 2, 18, 10, 47, 28, 138000),
            "reviewer_id": "Viratec",
            "lastUpdatedOn": datetime(2022, 3, 22, 16, 35, 37, 936000),
            "book_id": "620fdbb0cf1be3116b86ad78",
        },
    ]
