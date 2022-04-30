from typing import List

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import settings

mongo_client: AsyncIOMotorClient

DB_URL = settings.DB_URL
DB_NAME = settings.DB_NAME


class MongoClient:
    async def get_record(self, collection: str, query: dict) -> dict:
        return await self.get_db()[collection].find_one(query, {"id": False})

    async def get_record_count(self, collection: str, query: dict) -> dict:
        return await self.get_db()[collection].count_documents(query)

    async def aggregate(self, collection: str, pipeline: list[dict]) -> dict:
        return self.get_db()[collection].aggregate(pipeline=pipeline, allowDiskUse=True)

    async def get_records(self, collection: str, query: dict, projection: dict = None):
        return self.get_db()[collection].find(query, projection)

    async def get_records_with_pagination(
        self, collection: str, query: dict, pagination_info: dict, limit: int
    ) -> dict:
        return (
            self.get_db()[collection]
            .find(query)
            .skip(pagination_info["skip"])
            .limit(limit)
        )

    async def create_record(self, collection: str, query: dict) -> dict:
        if "_id" in query:
            del query["_id"]

        return await self.get_db()[collection].insert_one(query)

    async def update_record(
        self, collection: str, object_query: dict, update_query: dict
    ) -> dict:
        if "_id" in update_query:
            del update_query["_id"]

        return await self.get_db()[collection].update_one(object_query, update_query)

    async def get_and_update_record(
        self, collection: str, object_query: dict, update_query: dict
    ) -> dict:
        if "_id" in update_query:
            del update_query["_id"]

        return await self.get_db()[collection].find_one_and_update(
            object_query, update_query
        )

    async def delete_record(self, collection: str, query: dict) -> dict:
        return await self.get_db()[collection].delete_one(query)

    async def delete_all_records(self, collection: str, query: dict) -> dict:
        return await self.get_db()[collection].delete_many(query)

    @staticmethod
    def get_db() -> AsyncIOMotorDatabase:
        return AsyncIOMotorClient(DB_URL)[DB_NAME]

    @staticmethod
    def build_bulk_avg_value_pipeline(
        field_to_match: str,
        field_values_to_match: List[object],
        field_to_calculate_average: str,
    ) -> list[dict]:
        return [
            {"$match": {field_to_match: {"$in": field_values_to_match}}},
            {
                "$group": {
                    "_id": "$" + field_to_match,
                    "avg_rating": {"$avg": "$" + field_to_calculate_average},
                }
            },
        ]

    @staticmethod
    def build_avg_value_pipeline(
        field_to_match: str,
        field_values_to_match: object,
        field_to_calculate_average: str,
    ) -> list[dict]:
        return [
            {"$match": {field_to_match: field_values_to_match}},
            {
                "$group": {
                    "_id": "$" + field_to_match,
                    "avg_rating": {"$avg": "$" + field_to_calculate_average},
                }
            },
        ]

    @staticmethod
    def build_top_ranking_pipeline(match: dict, limit: int = None) -> list[dict]:
        return [match, {"$sort": {"rating": -1}}, {"$limit": limit}]
