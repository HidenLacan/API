# API Library System

This project is a RESTful API for managing books and authors. The system allows users to create, update, retrieve, and delete book and author records. Additionally, it features a recommendation system that suggests books to users based on their favorite books.

## Usage

- Access the endpoints using tools like Postman or cURL.
- Use JWT tokens for accessing protected endpoints (POST, PUT, DELETE).
- Get a JWT token by logging in via `/login`.

## Models

### User

- **email**: User's email (used for login).
- **username**: User's unique username.
- **password**: Hashed password.
- **is_active**: Determines if the user is active.
- **is_admin**: Grants admin permissions.
- **is_staff**: Grants staff access to the admin dashboard.

### Book

- **title**: Title of the book.
- **author**: Foreign key linking to the `Author` model.
- **description**: Description of the book.
- **pub_date**: Publication date of the book.

### Author

- **name**: Name of the author.


## Features

- **User Registration & Authentication**
  - JWT-based authentication.
  - Users can register, login, and access protected endpoints.
  
- **Book Management**
  - Create, retrieve, update, and delete books.
  - Search books by title and author.

- **Author Management**
  - Create, retrieve, update, and delete authors.
  - Search authors by name.

- **Favorite Books**
  - Users can add/remove books from their favorite list.
  - Recommendation system that suggests similar books based on the user’s favorite list.

## API Endpoints

### Books
- **GET** `/books` - Retrieve a list of all books.
- **GET** `/books/:id` - Retrieve a specific book by ID.
- **POST** `/books` - Create a new book (protected).
- **PUT** `/books/:id` - Update an existing book (protected).
- **DELETE** `/books/:id` - Delete a book (protected).

### Authors
- **GET** `/authors` - Retrieve a list of all authors.
- **GET** `/authors/:id` - Retrieve a specific author by ID.
- **POST** `/authors` - Create a new author (protected).
- **PUT** `/authors/:id` - Update an existing author (protected).
- **DELETE** `/authors/:id` - Delete an author (protected).

### Favorites and Recommendations
- **POST** `/favorites/:book_id` - Add a book to the user's favorites (protected).
- **DELETE** `/favorites/:book_id` - Remove a book from the user's favorites (protected).
- **GET** `/favorites` - Retrieve a list of favorite books (protected).
- **GET** `/recommendations` - Get recommended books based on the user's favorite list (protected).

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone 
   cd api_library

2. Installation
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt

3. Set up the database
    python manage.py makemigrations
    python manage.py migrate

4. CreateAdmin
    python manage.py createsuperuser

5. Run 
    python manage.py runserver

