""" Job used to calculate average book ratings """
from src.services.books import book_service


async def update_average_book_ratings():
    update_response = await book_service.bulk_update_book_ratings()

    if update_response.update_responses.__len__() > 0:
        print(
            "A total of "
            + str(update_response.update_responses.__len__())
            + " record(s) were updated"
        )
    else:
        print("No records were updated")
