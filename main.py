import datetime
import graphdoc  # type: ignore
import graphql
import uvicorn
from graphql import GraphQLSyntaxError
from starlette.responses import Response
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from src.config import settings
from src.graphql_api import graphql_app
from src.jobs.book_ratings_job import update_average_book_ratings

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


# Load static files (site template for docs, etc.)
app.mount(
    "/doc_templates",
    StaticFiles(directory=Path(__file__).parent.absolute() / "./src/doc_templates"),
    name="doc_templates",
)


@app.get("/graphql/docs", include_in_schema=False)
async def get_graphql_docs():
    """
    handler for graphql docs
    """
    # Update the following to match your schema file naming
    path = "./schema.graphql"

    with open(path, "r", encoding="utf-8") as graphql_file:
        schema = graphql_file.read()

    try:
        graphql.parse(schema)
    except GraphQLSyntaxError as e:
        raise Exception(path, str(e)) from e
    return Response(
        content=graphdoc.to_doc(
            schema, templates_path="src/doc_templates", use_cache=False
        ),
        media_type="text/html",
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=True,
        port=settings.PORT,
        debug=settings.DEBUG_MODE,
    )
