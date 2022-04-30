from unittest.mock import AsyncMock

import pytest


@pytest.fixture()
def mock_get_record(mocker):
    async_mock = AsyncMock()
    mocker.patch("src.clients.db.MongoClient.get_record", side_effect=async_mock)
    return async_mock


@pytest.fixture()
def mock_get_records(mocker):
    async_mock = AsyncMock()
    mocker.patch("src.clients.db.MongoClient.get_records", side_effect=async_mock)
    return async_mock


@pytest.fixture()
def mock_update_record(mocker):
    async_mock = AsyncMock()
    mocker.patch(
        "src.clients.db.MongoClient.get_and_update_record", side_effect=async_mock
    )
    return async_mock


@pytest.fixture()
def mock_create_record(mocker):
    async_mock = AsyncMock()
    mocker.patch(
        "src.clients.db.MongoClient.get_and_create_record", side_effect=async_mock
    )
    return async_mock


@pytest.fixture()
def mock_delete_record(mocker):
    async_mock = AsyncMock()
    mocker.patch(
        "src.clients.db.MongoClient.get_and_create_record", side_effect=async_mock
    )
    return async_mock
