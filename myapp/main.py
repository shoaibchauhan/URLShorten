from django.core.management import execute_from_command_line
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'URLShorten.settings')
import django
django.setup()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from myapp.controller import router

app = FastAPI()
# Define CORS settings
origins = [
    "http://localhost:8000",  # FastAPI server
    "http://127.0.0.1:8000",  # FastAPI server
    "http://localhost:3000",   # Swagger UI or any other frontend
    "http://127.0.0.1:3000",   # Swagger UI or any other frontend
]  # Allow requests from any origin

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")
def root():
    return {"msg":"hello"}