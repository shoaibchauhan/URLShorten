from collections import defaultdict
from datetime import datetime, timedelta
import random
import string
from urllib.parse import unquote, urlparse
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from myapp.models import URLMapping
from myapp.schemas import URLShortenRequest, URLShortenResponse, CustomURLShortenRequest,CustomURLShortenResponse



router=APIRouter()

def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_original_url(full_url: str) -> str:
    full_url = unquote(full_url)
    parsed_url = urlparse(full_url)
    short_url = parsed_url.path.split('/')[-1]
    
    try:
        url_mapping = URLMapping.objects.get(short_url=short_url)
        
        # Check if the URL mapping is expired
        if url_mapping.is_expired():
            raise HTTPException(status_code=410, detail="This short URL has expired.")

        url_mapping.access_count += 1
        url_mapping.save()
        return url_mapping.original_url
    except URLMapping.DoesNotExist:
        raise HTTPException(status_code=404, detail="Short URL not found")

    

@router.post("/url/shorten", response_model=URLShortenResponse)
def shorten_url(request: URLShortenRequest):
    original_url = request.url
    short_url = generate_short_url()

    # Store the mapping in the database
    URLMapping.objects.create(original_url=original_url, short_url=short_url)
    
    short_url = f"http://localhost:8000/r/{short_url}"
    return {"short_url": short_url}




@router.post("/r/my-custom-url", response_model=CustomURLShortenResponse)
def shorten_url_custom(request: CustomURLShortenRequest):
    original_url = request.url
    custom_slug = request.custom_slug
    expiration_days = request.expiration_days

    # Check if the custom slug is unique
    if URLMapping.objects.filter(short_url=custom_slug).exists():
        raise HTTPException(status_code=400, detail="Custom short URL slug already exists.")

    # Use the ORM to create the URL mapping with an expiration date
    url_mapping = URLMapping.create(original_url=original_url, short_url=custom_slug, duration=expiration_days)

    short_url = f"http://localhost:8000/r/{custom_slug}"
    return {"short_url": short_url, "custom_slug": custom_slug}



@router.get("/r/<short_url>")
def redirect_url(full_url: str):
    try:
        # Get the original URL using the provided full URL
        original_url = get_original_url(full_url)
        # Redirect to the original URL with a 302 status code
        response = RedirectResponse(url=original_url, status_code=302)
        response.headers["X-Redirect-Message"] = "HTTP 302 redirect to the original URL."
        return response
    
    except HTTPException as e:
         # Return a 404 error with a custom message
         raise HTTPException(status_code=e.status_code, detail="HTTP 404: Short URL not found.")
    









    # @router.post("/url/shorten", response_model=URLShortenResponse)
# def shorten_url(request: URLShortenRequest):
#     short_url = generate_short_url()
#     original_url = request.url

#     # Store the mapping in the database
#     URLMapping.objects.create(original_url=original_url, short_url=short_url)
    
#     short_url = f"http://localhost:8000/r/{short_url}"
#     return {"short_url": short_url}




# @router.get("/r/{full_url:path}")
# def redirect_url(full_url: str):
#     try:
#         # Get the original URL using the provided full URL
#         original_url = get_original_url(full_url)

#         # Redirect to the original URL with a 302 status code
#         response = RedirectResponse(url=original_url, status_code=302)
#         response.headers["X-Redirect-Message"] = "HTTP 302 redirect to the original URL."
#         return response
#     except HTTPException as e:
#         # Return a 404 error with a custom message
#         raise HTTPException(status_code=e.status_code, detail="HTTP 404: Short URL not found.")