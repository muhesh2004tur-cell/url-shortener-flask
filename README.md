# URL Shortener API

A simple and lightweight **URL Shortener REST API** built with **Python, Flask, and SQLite**.

This project was developed as a backend learning project to understand REST APIs, request validation, database operations, URL redirection, automated testing, environment-based configuration, and Git/GitHub workflow.

---

## Features

- Shorten long URLs into unique 6-character short codes
- Support HTTP and HTTPS URLs
- Validate incoming JSON requests
- Store URL mappings in SQLite
- Redirect short URLs to original URLs
- Handle invalid requests and missing short URLs
- Generate short codes using Python's `secrets` module
- Prevent duplicate short codes
- Automated API testing using pytest
- Environment-variable-based configuration
- Git and GitHub version control

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Flask | Backend REST API |
| SQLite | Database |
| pytest | Automated testing |
| Gunicorn | Production WSGI server |
| Git | Version control |
| GitHub | Source code hosting |

---

## Project Structure

```text
url-shortener-flask/
│
├── main.py
├── test_main.py
├── generate_short_code.py
├── requirements.txt
├── .gitignore
└── README.md
```

> `urls.db`, `practice.db`, `venv/`, cache files, and Python-generated files are excluded from Git using `.gitignore`.

---

# API Endpoints

## 1. Get API Status

### GET `/`

Returns the API status.

### Response

```json
{
  "message": "your url shortner is running"
}
```

---

## 2. Shorten a URL

### POST `/shorten`

Creates a shortened URL.

### Request

```json
{
  "url": "https://www.example.com"
}
```

### Successful Response

```json
{
  "message": "URL shortened successfully",
  "short_code": "Ab12Xy",
  "short_url": "http://127.0.0.1:5000/Ab12Xy"
}
```

### Status Code

```text
201 Created
```

---

## 3. Redirect to Original URL

### GET `/<short_code>`

Redirects the user to the original URL associated with the short code.

### Example

```text
http://127.0.0.1:5000/Ab12Xy
```

If the short code exists, the application redirects the user to the original URL.

### Status Code

```text
302 Found
```

---

# Request Validation

The `/shorten` endpoint validates:

- JSON body is provided
- `url` field exists
- URL is a non-empty string
- URL uses HTTP or HTTPS
- URL contains a valid network location

### Invalid Request

Invalid requests return:

```text
400 Bad Request
```

### Unknown Short Code

If the requested short code does not exist:

```text
404 Not Found
```

### Database Error

If a database error occurs:

```text
500 Internal Server Error
```

---

# Database

The project uses **SQLite** to store URL mappings.

### Database Schema

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

### Column Description

| Column | Description |
|---|---|
| `id` | Unique ID for each URL |
| `short_code` | Generated unique short code |
| `original_url` | Original long URL |
| `created_at` | URL creation timestamp |

The `short_code` column uses `UNIQUE` to prevent duplicate short codes.

---

# Configuration

The application supports environment variables.

```text
BASE_URL
DATABASE_PATH
```

### Local Defaults

```text
BASE_URL=http://127.0.0.1:5000
DATABASE_PATH=urls.db
```

This allows the application configuration to be changed without modifying the source code.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/muhesh2004tur-cell/url-shortener-flask.git
cd url-shortener-flask
```

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

## 3. Activate the Virtual Environment

Windows CMD:

```cmd
venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

Start the Flask application:

```bash
python main.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

You can test the API using:

- Thunder Client
- Postman
- Browser

---

# Testing

The project uses **pytest** for automated testing.

Run:

```bash
pytest
```

### Current Test Coverage

The test suite covers:

- Home endpoint
- Successful URL shortening
- Missing JSON body
- Missing URL field
- Invalid URL
- Existing short-code redirection
- Unknown short code

Expected result:

```text
7 passed
```

---

# How It Works

```text
                 Long URL
                    │
                    ▼
             POST /shorten
                    │
                    ▼
             Validate URL
                    │
                    ▼
          Generate Short Code
                    │
                    ▼
             Store in SQLite
                    │
                    ▼
          Return Short URL
                    │
                    ▼
          GET /<short_code>
                    │
                    ▼
          Find Original URL
                    │
                    ▼
                Redirect
                    │
                    ▼
             Original Website
```

---

# Short Code Generation

The application generates a random 6-character short code using:

```python
string.ascii_letters + string.digits
```

and Python's secure random selection:

```python
secrets.choice()
```

Example:

```text
Ab12Xy
K9mP2q
X7aBc9
```

Before saving the URL, the application checks whether the generated short code already exists.

If it exists, a new short code is generated.

---

# Error Handling

The application handles different types of errors:

| Situation | Status Code |
|---|---:|
| Successful URL shortening | 201 |
| Successful redirect | 302 |
| Missing JSON body | 400 |
| Missing URL | 400 |
| Invalid URL | 400 |
| Short code not found | 404 |
| Database error | 500 |

---

# What I Learned

Through this project, I practiced:

- Flask application development
- REST API design
- HTTP methods
- HTTP status codes
- JSON request handling
- Input validation
- URL parsing
- Random short-code generation
- SQLite database operations
- Parameterized SQL queries
- Primary keys and unique constraints
- Exception handling
- Separation of route and database logic
- Automated testing with pytest
- Environment variables
- Git and GitHub workflow

---

# Future Improvements

Possible future enhancements include:

- User authentication
- Custom short codes
- URL expiration
- Click analytics
- Rate limiting
- PostgreSQL support
- Frontend interface
- QR code generation
- Cloud deployment

---

# Author

**Muhesh G R**

B.Tech Artificial Intelligence & Data Science

GitHub:

https://github.com/muhesh2004tur-cell

---

# License

This project was created for **educational and portfolio purposes**.