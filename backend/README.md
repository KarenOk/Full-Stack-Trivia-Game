# Trivia Game API

## Introduction

This API allows you manage a pool of questions and categories for a Trivia game.

## Getting Started

This API is currently not deployed to a remote server and has to be run locally to be used. <br/>

**BASE URL**: `http://localhost:5000`

## Error Handling

### Response Object

Errors are returned as JSON in the following format:

```
{
    "error": 404,
    "message": "The requested resource was not found."
}
```

### Response Keys

`error` - Status code of the error that occurred. <br>
`message` - Accompanying error message.

### Status Codes

`400 (Bad request)` - Your request was not properly formatted. <br>
`404 (Not found)` - The requested resource was not found. <br>
`422 (Unprocessable)` - The server understood your request but it could not be processed. <br>
`500 (Internal server error)` - Something went wrong on the server. <br>

## Endpoint Library

### Categories

#### `GET /categories`

This fetches all the question categories as an object with each category's id as the key and type as value.

##### Query Parameters

This endpoint takes in no query parameter.

##### Request Body

This endpoint doesn't require a request body.

##### Sample Request

`curl http://localhost:5000/categories`

##### Sample Response

```
{
    "1": "Science",
    "2", "Art",
    "3": "History"
}
```

#### `GET /categories/{category_id}/questions`

This returns all the questions along with the total number of questions within a particular category.

##### Query Parameters

This endpoint does not take in query parameters.

##### Request Body

This endpoint does not require a request body.

##### Sample Request

`curl http://localhost:5000/categories/`

##### Sample Response

`questions`: array - All questions within the specified category. <br>
`totalQuestions`: int - Total number of questions within specified category. <br>

```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "totalQuestions": 2
}
```

### Questions

#### `GET /questions`

This returns a paginated list of all questions within the database along, all categories and the total number of questions. Each page contains a maximum of 10 questions.

##### Query Parameters

`page`: int <small> (optional) </small> - Page number starting from 1.

##### Request Body

This endpoint does not require a request body

##### Sample Request

`curl http://localhost:5000/questions?page=2`

##### Sample Response

`questions`: array - Fetched questions. <br>
`totalQuestions`: int - Total number of questions in the database. <br>

```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "categories" : {
    "1": "Science",
    "2", "Art",
    "3": "History"
   },
  "totalQuestions": 2
}
```

### `POST /questions`

This adds a question to the collection of questions in the database. It takes in the question, its category id, its difficulty rating and answer.

#### Query Parameters

This endpoint takes in no query parameters

#### Request Body

`question`: string <small> (required) </small> - Question text content. <br>
`answer`: string <small> (required) </small> - Answer to the question. <br>
`category`: int <small> (required) </small> - Category id of the question's category. <br>
`difficulty`:string <small> (required) </small> - Question's difficulty from 1 to 5. <br>

```
{
    "question": "Which country won the first ever soccer World Cup in 1930?",
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4
}
```

#### Sample Request

`curl http://localhost:5000/questions -X POST -H "{Content-Type: 'application/json'" -d '{ "question": "Which country won the first ever soccer World Cup in 1930?", "answer": "Uruguay", "category": 6, "difficulty": 4 }'`

#### Sample Response

`added`: int - Id of the added question. <br>
`success`: boolean - Request success status. <br>

```
{
    "added": 1,
    "success": True
}
```

### `POST /questions` (SEARCH)

This performs a case insensitive search of questions from the database based on a search term. It returns an array of the questions and the total amount of questions that match the search term.

#### Query Parameters

This endpoint takes in no query parameters

#### Request Body

`searchTerm`: string <small> (required) </small> - Term to search for. <br>

`{ "searchTerm": "soccer"}`

#### Sample Request

`curl http://localhost:5000/questions -X POST -H "{Content-Type: 'application/json'" -d '{ "searchTerm": "soccer"}'`

#### Sample Response

`questions`: array - All questions that match the search term. <br>
`totalQuestions`: int - Total number of questions that match the search term. <br>

```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "totalQuestions": 2
}
```

### `DELETE /questions/{question_id}`

This deletes the question with the specified id. It returns the id of the deleted question and a success status.

#### Query Parameters

This endpoint takes in no query parameters.

#### Request Body

This endpoint requires no request body.

#### Sample Request

`curl http://localhost:5000/questions/1 -X DELETE`

#### Sample Response

`deleted`: int - Id of the deleted question. <br>
`success`: boolean - Request success status. <br>

```
{
    "deleted": 1,
    "success": True
}
```

### Quizzes

#### `POST /quizzes`

This returns a random question from the database within a specified category or from a random category if none is specified. It accepts an array of previous questions to ensure that a question that has been chosen before is not chosen again. If there are no other questions to left, it returns null.

#### Query Parameters

This endpoint takes in no query parameters

#### Request Body

`previous_questions`: array <small> (required) </small> - Contains ids of previously chosen questions. <br>
`quiz_category`: int <small> (optional) </small> - Current category. <br>

```
{
    "previous_questions": [10],
    "quiz_category": 6
}
```

#### Sample Request

`curl http://localhost:5000/questions -X POST -H "{Content-Type: 'application/json'" -d '{"previous_questions": [10], "quiz_category": 6 }'`

#### Sample Response

`question`: object|null - randomly chosen question.

```
{
    "question": {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
}
```
