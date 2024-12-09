import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from urllib.parse import quote

class SearchTerms(BaseModel):
    terms: str

app = FastAPI()

base_url = "https://www.googleapis.com/books/v1/"

@app.post("/books", status_code=200)
async def search_books(search_terms: SearchTerms):
    # Ensure search terms are URI encoded
    # Clients are expected to send encoded version of search terms: e.g., encodeURIComponent('search+terms')
    if "+" in search_terms.terms:
        search_terms.terms = quote(search_terms.terms)

    # search by volumes
    endpoint = base_url + 'volumes?q=' + search_terms.terms
    response = requests.get(endpoint)

    if response.status_code == 200:
        try:
            # The items array contains a list objects with pertanent search results
            return response.json()["items"]
        except requests.exceptions.JSONDecodeError:
            return {
                "status": "Error",
                "code": 500,
                "message": "Failed to decode JSON response"
            }
    else:
        return {
            "status": "Error",
            "code": response.status_code,
            "message": "Failed to fetch data from Google Books API"
        }

@app.get("/health", status_code=200)
async def health_check():
    try:
        return {
            "status": "OK"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{path:path}", status_code=200)
async def catch_all(path: str):
    try:
        return {
            "status": "OK"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

