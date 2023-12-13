"""Populating Mongo collections with mock data
Fort simplicity, we assume that the relationship between authors and book is one to many
"""

from pymongo import MongoClient, DESCENDING

CONN = MongoClient("localhost", 27017)
DB_NAME = "lib"
BOOKS_COLL_NAME = "books"
AUTHORS_COLL_NAME = "authors"

# DATA FOR EXPERIMENTS

BOOKS = {
    "War and Peace": 1,
    "Anna Karenina": 2,
    "Crime and Punishment": 3,
    "The Captain's Daughter": 4,
}

AUTHORS = {
    "Fyodor Dostoevsky": 1,
    "Leo Tolstoy": 2,
    "Alexander Pushkin": 3,
}

AUTHORS_BOOKS = {
    1: [3],
    2: [1, 2],
    3: [4],
}


def get_new_id(coll):
    """Imitate auto ID behaviour not to deal with _id"""
    max_id = coll.find().sort([("id", DESCENDING)]).limit(1)[0]["id"]
    return max_id + 1


def add_book_to_author(author, book_id):
    """Add a new book to author's record list"""
    authors = CONN[DB_NAME][AUTHORS_COLL_NAME]
    auths_books = set(author["books"])
    auths_books.add(book_id)
    authors.update_one(
        {"_id": author["_id"]},
        {"$set": {"books": list(auths_books)}},
    )


def get_author_id(book_id):
    for author_id in AUTHORS_BOOKS:
        if book_id in AUTHORS_BOOKS[author_id]:
            return author_id


def populate_db():
    """Insert initial mock data"""
    books_coll = CONN[DB_NAME][BOOKS_COLL_NAME]
    for book_title in BOOKS:
        book_id = BOOKS[book_title]
        books_coll.insert_one(
            {
                "id": book_id,  # just not to mess with Mongo's hideous _id
                "title": book_title,
                "author": get_author_id(book_id),
            }
        )
    authors_coll = CONN[DB_NAME][AUTHORS_COLL_NAME]
    for author_name in AUTHORS:
        author_id = AUTHORS[author_name]
        authors_coll.insert_one(
            {
                "id": author_id,  # just not to mess with Mongo's hideous _id
                "name": author_name,
                "books": AUTHORS_BOOKS[author_id],
            }
        )
    print("Inserted initial mock data")


if __name__ == '__main__':
    populate_db()
