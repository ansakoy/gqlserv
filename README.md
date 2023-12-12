# A toy GraphQL-server / query tool

## Dependencies:
```commandline
pip install "strawberry-graphql[debug-server]"
pip install "gql[all]"
pip install graphql-query
pip install pymongo
```

## Run local lab
Start MongoDB:
```commandline
# on Mac
mongod --config /usr/local/etc/mongod.conf
```
Populate with mock data:
```commandline
python db.py
```
Run strawberry dev server:
```commandline
strawberry server schema
```

## Helpful links:

* [Strawberry docs](https://strawberry.rocks/docs)
* [graphql_query](https://denisart.github.io/graphql-query/)