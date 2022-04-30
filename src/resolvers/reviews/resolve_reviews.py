import datetime
from bson import ObjectId

from src.models.common.response_models import (
    GetResponse,
    CreateResponse,
    UpdateResponse,
    DeleteResponse,
)
from src.models.reviews.review_models import Review
from src.services.reviews import review_service


async def resolve_get_review_by_id(review_id: str) -> GetResponse[Review]:
    return await review_service.get_review_by_id(ObjectId(review_id))


async def resolve_get_review_by_book_id(book_id: str) -> GetResponse[Review]:
    return await review_service.get_reviews_by_book_id(book_id)


async def resolve_create_review(
    book_id: str, reviewer_id: str, rating: float, review_comments: str = None
) -> CreateResponse[Review]:
    new_review = Review(
        None,
        book_id,
        reviewer_id,
        rating,
        review_comments,
        datetime.datetime.now(),
        None,
    )

    return await review_service.create_review(new_review)


async def resolve_update_review(
    review_id: str, rating: float, review_comments: str = None
) -> UpdateResponse[Review]:
    new_values = {}

    if review_comments is not None:
        new_values["review_comments"] = review_comments

    if rating is not None:
        new_values["rating"] = rating

    new_values["lastUpdatedOn"] = datetime.datetime.now()

    return await review_service.update_review(ObjectId(review_id), new_values)


async def resolve_delete_review(review_id: str) -> DeleteResponse[Review]:
    return await review_service.delete_review(ObjectId(review_id))
