from pydantic import BaseModel, HttpUrl, constr


class URLShortenRequest(BaseModel):
    url: HttpUrl

class URLShortenResponse(BaseModel):
    short_url: str    

class CustomURLShortenRequest(BaseModel):
    """Request model for shortening a URL with a custom slug and expiration."""
    url: HttpUrl
    custom_slug: constr(min_length=1, max_length=10)  # type: ignore # Custom slug must be between 1 and 10 characters
    expiration_days: int  # Number of days before the URL expires

class CustomURLShortenResponse(BaseModel):
    """Response model for a shortened URL with a custom slug."""
    short_url: str
    custom_slug: constr(min_length=1, max_length=10)  # type: ignore # Reflects the custom slug used
