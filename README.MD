# URL Shortening Service

This is a URL shortening service built with Python, FastAPI, and Django ORM. It allows users to shorten URLs and provides features like custom short URLs, expiration dates, and rate limiting.

## Features

- **Shorten URLs**: Create short links from long URLs.
- **Custom Slugs**: Allow users to specify a custom short URL slug.
- **Expiration Dates**: Set expiration dates for short URLs.
- **Rate Limiting**: Limit the number of requests from a single IP address.
- **Access Tracking**: Keep track of how many times a short URL has been accessed.

## Technologies Used

- **Python**: Programming language used for backend development.
- **FastAPI**: Web framework for building APIs quickly.
- **Django ORM**: Object-Relational Mapping for database interactions.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: ASGI server for serving FastAPI applications.
- **PostgreSQL**: SQL database for storing URL mappings.
- **Pytest**: For unit test case.
- **PyJWT**: For implementing JWT-based authentication (if applicable).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shoaibchauhan/URLShorten.git
   cd URLShorten

2. Create a virtual environment or activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:

    ```bash
    pip install -r requirements.txt

4. Set up your database (if using Django ORM):

    Make sure to configure your database settings in settings.py.


5. Run migrations to create the necessary tables:
    ```bash
    python manage.py migrate

## Usage:

1. Start the Uvicorn server:

    ```bash
    uvicorn main:app --reload
    ```

# API Testing Instructions

You can test the API endpoints using `curl` or Postman or Swagger Docs. Below are the examples for testing the URL shortening API using `curl`.

## To test a shorten_URL to its original / redirect use Postman or You can run the unit test case using pytest myapp.test_url_shortener.py (according to directory) or Use built in Swagger Docs

To Redirect a shorten_URL use the following command in Postman or Curl in import tab:

```bash
curl -X POST http://localhost:8000/url/shorten \
-H "Content-Type: application/json" \
-d '{"url": "http://example.com"}'
```



## Shorten a URL

1. **Shorten a URL**:
   - **Endpoint**: `POST /url/shorten`
   - **Request Body**:
     ```json
     {
       "url": "http://example.com"
     }
     ```

2. **Shorten a Custom URL**:
   - **Endpoint**: `POST /url/shorten/custom`
   - **Request Body**:
     ```json
     {
       "url": "http://example.com",
       "custom_slug": "customslug",
       "expiration_days": 7
     }
     ```

3. **Redirect to Original URL**:
   - **Endpoint**: `GET /r/{short_url}`
   - **Description**: Redirects the user to the original URL corresponding to the provided short slug.

### Rate Limiting

The API implements rate limiting, allowing a maximum of 5 requests per minute per IP address. If the limit is exceeded, a `429 Too Many Requests` error will be returned.
