# Queries | Mutations Cheatsheet

Here are the basic queries to check on our progress 
directly in Graphiql (using GraphQL syntax) at http://0.0.0.0:8000/graphql:

List all author names:
```
query {
  authors {
    name
  }
}
```

List authors with names, ids and their related book titles:
```
query {
  authors {
    name
    authId
    books {
      title
    }
  }
}
```
List all book titles:
```
query {
  books {
    title
  }
}
```
Create a new book:
```
mutation {
	addBook(title: "Idiot", authId: 1) {
		title
	}
}
```