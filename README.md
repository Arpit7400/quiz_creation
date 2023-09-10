# Quizz API Documentation

This documentation provides an overview of the Quizz API endpoints and their functionality.

## Base URL

The base URL for all API endpoints is `http://localhost:5000/`.

## Endpoints

### 1. Get All Subjects and Quizzes

- **URL:** `/get_all_subject_quizz`
- **Method:** GET
- **Description:** Get a list of all subjects and their associated quizzes.
- **Response:**
  - Status Code: 200 OK
  - Content: JSON array containing subjects and their quizzes.

### 2. Add Subject, Topic, or Subtopic

- **URL:** `/add_Subject_quizz`
- **Method:** POST
- **Description:** Add a new subject, topic, or subtopic. If a subject or topic does not exist, it will be created. If a subtopic does not exist within a topic, it will be added.
- **Request Body:**
  - `subject` (optional): The name of the subject.
  - `topic` (optional): The name of the topic.
  - `subtopic` (optional): The name of the subtopic.
- **Response:**
  - Status Code: 200 OK
  - Content: JSON message indicating success.

### 3. Get All Quizzes

- **URL:** `/get_all_quizz`
- **Method:** GET
- **Description:** Get a list of all quizzes.
- **Response:**
  - Status Code: 200 OK
  - Content: JSON array containing all quizzes.

### 4. Get Single Quiz

- **URL:** `/get_quizz/<quiz_id>`
- **Method:** GET
- **Description:** Get information about a single quiz by its ID.
- **Parameters:**
  - `quiz_id` (string): The ID of the quiz.
- **Response:**
  - Status Code: 200 OK
  - Content: JSON object containing quiz details.

### 5. Create Quiz

- **URL:** `/create_quizz/<creator_id>`
- **Method:** POST
- **Description:** Create a new quiz.
- **Parameters:**
  - `creator_id` (string): The ID of the quiz creator.
- **Request Body:**
  - `language`: The language of the quiz.
  - `class`: The class or grade level.
  - `subject`: The subject of the quiz.
  - `topic`: The topic of the quiz.
  - `subtopic`: The subtopic of the quiz.
  - `level`: The difficulty level of the quiz.
  - `quiz_type`: The type of quiz.
  - `question_container`: An object containing quiz questions, images, options, and answers.
- **Response:**
  - Status Code: 201 Created
  - Content: JSON object containing the created quiz details.

### 6. Update Quiz

- **URL:** `/update_quizz/<quiz_id>/<creator_id>`
- **Method:** PUT
- **Description:** Update an existing quiz.
- **Parameters:**
  - `quiz_id` (string): The ID of the quiz.
  - `creator_id` (string): The ID of the quiz creator.
- **Request Body:**
  - `language` (optional): Update the language of the quiz.
  - `class` (optional): Update the class or grade level.
  - `subject` (optional): Update the subject of the quiz.
  - `topic` (optional): Update the topic of the quiz.
  - `subtopic` (optional): Update the subtopic of the quiz.
  - `level` (optional): Update the difficulty level of the quiz.
  - `quiz_type` (optional): Update the type of quiz.
  - `question_container` (optional): An object containing updated quiz questions, images, options, and answers.
- **Response:**
  - Status Code: 200 OK
  - Content: JSON message indicating success.

### 7. Delete Quiz

- **URL:** `/delete_quizz/<quiz_id>/<creator_id>`
- **Method:** DELETE
- **Description:** Delete a quiz.
- **Parameters:**
  - `quiz_id` (string): The ID of the quiz.
  - `creator_id` (string): The ID of the quiz creator.
- **Response:**
  - Status Code: 200 OK
  - Content: JSON message indicating success.

## Error Handling

- In case of any errors, the API will return an error message with an appropriate status code (e.g., 400 Bad Request, 403 Forbidden, 404 Not Found, 500 Internal Server Error) along with an error description.

Please note that this documentation provides an overview of the available API endpoints and their functionality. Detailed request and response structures may vary, so refer to the API implementation for specific details.