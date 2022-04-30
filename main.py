import datetime
import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from src.config import settings
from src.graphql_api import graphql_app
from src.jobs.book_ratings_job import update_average_book_ratings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.mount("/graph", graphql_app)


# Add CORS middleware - Specify the permitted headers, methods, and origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to lock down if applicable to your use case
    allow_credentials=False,  # Must be false if all origins (*) is allowed
    allow_methods=["*"],
    allow_headers=["X-Forwarded-For", "Authorization", "Content-Type"],
)


@app.on_event("startup")
async def startup():
    public_paths = ({"/", "/graph/"},)


@app.get("/")
async def root():
    return {
        "message": {
            "app_name": settings.APP_NAME,
            "system_time": datetime.datetime.now(),
        }
    }


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 24 hours
async def mass_update_book_ratings() -> None:
    """Scheduled job used to update book ratings based on the set time duration."""
    await update_average_book_ratings()


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.HOST, reload=True, port=settings.PORT, debug=False
    )
