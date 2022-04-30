import strawberry
from strawberry.asgi import GraphQL
from src.resolvers.books.resolve_books import *
from src.resolvers.reviews.resolve_reviews import *
from src.middlewares.authorization import RequestHeaderValidation


@strawberry.type
class Query:
    # Book Queries
    get_book_by_id = strawberry.field(
        resolve_get_book_by_id, permission_classes=[RequestHeaderValidation]
    )
    get_book_by_isbn = strawberry.field(
        resolve_get_book_by_isbn, permission_classes=[RequestHeaderValidation]
    )

    # Review Queries
    get_review_by_id = strawberry.field(
        resolve_get_review_by_id, permission_classes=[RequestHeaderValidation]
    )
    get_review_by_book_id = strawberry.field(
        resolve_get_review_by_book_id, permission_classes=[RequestHeaderValidation]
    )


@strawberry.type
class Mutation:
    # Book Create, Update, and Delete Mutations
    create_book = strawberry.field(
        resolve_create_book, permission_classes=[RequestHeaderValidation]
    )
    update_book = strawberry.field(
        resolve_update_book, permission_classes=[RequestHeaderValidation]
    )
    delete_book = strawberry.field(
        resolve_delete_book, permission_classes=[RequestHeaderValidation]
    )

    # Review Create, Update, and Delete Mutations
    create_review = strawberry.field(
        resolve_create_review, permission_classes=[RequestHeaderValidation]
    )
    update_review = strawberry.field(
        resolve_update_review, permission_classes=[RequestHeaderValidation]
    )
    delete_review = strawberry.field(
        resolve_delete_review, permission_classes=[RequestHeaderValidation]
    )


schema = strawberry.Schema(query=Query(), mutation=Mutation())
graphql_app = GraphQL(schema, debug=True)
