from dataclasses import dataclass
from typing import TypeVar, Optional, Generic, List

import strawberry
from dataclasses_json import LetterCase, dataclass_json

T = TypeVar("T")


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class BaseResponse:
    error_message: Optional[str]
    success: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class GetResponse(Generic[T], BaseResponse):
    result: Optional[T]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class GetListResponse(Generic[T], BaseResponse):
    result: Optional[List[T]]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class CreateResponse(Generic[T], BaseResponse):
    result: Optional[T]
    record_id: strawberry.ID


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class UpdateResponse(Generic[T], BaseResponse):
    result: Optional[T]
    record_id: strawberry.ID


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class DeleteResponse(Generic[T], BaseResponse):
    result: Optional[T]
    record_id: strawberry.ID


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class GetPaginatedResponse(BaseResponse, Generic[T]):
    results: Optional[List[T]] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    total_records: Optional[int] = None
    total_pages: Optional[int] = None
