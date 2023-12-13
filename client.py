"""Here are my client queries"""
from pprint import pprint

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql_query import Argument, Field, Operation, Query

transport = AIOHTTPTransport(url="http://0.0.0.0:8000/graphql")

client = Client(transport=transport, fetch_schema_from_transport=True)


def get_books():
    books = Query(
        name="books",
        fields=["title"],
    )
    operation = Operation(type="query", queries=[books])
    print(operation.render())
    query = gql(operation.render())
    result = client.execute(query)
    print(result)


def get_authors():
    authors = Query(name="authors", fields=["name"])
    operation = Operation(type="query", queries=[authors])
    query = gql(operation.render())
    result = client.execute(query)
    print(result)


def get_books_query():
    return Query(
        name="books",
        fields=[
            "title",
            Field(name="author", fields=["name"]),
        ],
    )


def get_authors_query():
    return Query(
        name="authors",
        fields=[
            "name",
            Field(name="books", fields=["title"]),
        ]
    )


def perform_op(queries):
    operation = Operation(type="query", queries=queries)
    query = gql(operation.render())
    result = client.execute(query)
    pprint(result)


def add_book(title, auth_id):
    mutation = Query(
        name="addBook",
        arguments=[
            Argument(name="title", value=f'"{title}"'),
            Argument(name="authId", value=auth_id),
        ],
        fields=[
            "title",
            Field(name="author", fields=["name"]),
        ]
    )
    operation = Operation(
        type="mutation",
        # name="addBook",
        queries=[mutation],
    )
    print(operation.render())
    query = gql(operation.render())
    result = client.execute(query)
    pprint(result)


if __name__ == '__main__':
    # get_books()
    # get_authors()
    # perform_op([get_books_query(), get_authors_query()])
    add_book("The Bronze Horseman", 3)



