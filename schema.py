"""Here are my GraphQL schemas and resolvers"""

import typing
import strawberry

from db import AUTHORS_COLL_NAME, BOOKS_COLL_NAME, CONN, DB_NAME, add_book_to_author, get_new_id


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


@strawberry.type
class Mutation:
    @strawberry.field
    def add_book(self, title: str, auth_id: int) -> Book:
        books = CONN[DB_NAME][BOOKS_COLL_NAME]
        new_id = get_new_id(books)
        authors = CONN[DB_NAME][AUTHORS_COLL_NAME]
        author = authors.find_one({"id": auth_id})
        if author is None:
            raise Exception(f"Can't find author with id {auth_id}")
        existing_book = books.find_one({"title": title})
        if existing_book is not None:
            raise Exception(f"The book called {title} already exists")
        books.insert_one({
            "id": new_id,
            "title": title,
            "author": auth_id,
        })
        add_book_to_author(author, new_id)
        new_book = books.find_one({"id": new_id})
        return Book(title=new_book["title"], book_id=new_book["id"])


schema = strawberry.Schema(query=Query, mutation=Mutation)


