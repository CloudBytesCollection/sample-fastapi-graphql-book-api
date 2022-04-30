from unittest.mock import AsyncMock

import pytest


@pytest.fixture()
def mock_update_book(mocker):
    async_mock = AsyncMock()
    mocker.patch("src.services.books.book_service.update_book", side_effect=async_mock)
    return async_mock
