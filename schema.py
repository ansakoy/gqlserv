"""Here are my GraphQL schemas and resolvers"""

import typing
import strawberry

from db import AUTHORS_COLL_NAME, BOOKS_COLL_NAME, CONN, DB_NAME


def get_author_for_book(root) -> "Author":
    authors = CONN[DB_NAME][AUTHORS_COLL_NAME]
    author = authors.find_one({"books": root.book_id})
    if author is not None:
        return Author(name=author["name"], auth_id=author["id"])


@strawberry.type
class Book:
    title: str
    book_id: int
    author: "Author" = strawberry.field(resolver=get_author_for_book)


def get_books_for_author(root):
    # root is the type object, which allows to grab its values
    auth_id = root.auth_id
    books = CONN[DB_NAME][BOOKS_COLL_NAME]
    return [Book(title=entry["title"], book_id=entry["id" ]) for entry in books.find({"author": auth_id})]


@strawberry.type
class Author:
    name: str
    auth_id: int
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)


def get_authors(root) -> typing.List[Author]:
    authors = CONN[DB_NAME][AUTHORS_COLL_NAME]
    return [Author(name=entry["name"], auth_id=entry["id"]) for entry in authors.find()]


def get_books(root) -> typing.List[Book]:
    books = CONN[DB_NAME][BOOKS_COLL_NAME]
    return [Book(title=entry["title"], book_id=entry["id"]) for entry in books.find()]


@strawberry.type
class Query:
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    books: typing.List[Book] = strawberry.field(resolver=get_books)


schema = strawberry.Schema(query=Query)


