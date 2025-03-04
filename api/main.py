import html
import psutil
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.parse import quote
from datetime import datetime

class SearchTerms(BaseModel):
    terms: str

app = FastAPI()

# add CORS support for hosting purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

books_api_base_url = "https://www.googleapis.com/books/v1/"

@app.post("/books", status_code=200)
async def search_books(search_terms: SearchTerms):
    # Sanitize input
    terms = html.escape(searchTerms.terms)

    # Ensure search terms are URI encoded
    # Clients are expected to send encoded version of search terms: e.g., encodeURIComponent('search+terms')
    if (" " in terms):
        terms = terms.replace(" ", "+")

    if ("+" in terms):
        terms = quote(terms)

    # search by volumes
    endpoint = books_api_base_url + 'volumes?q=' + terms
    response = requests.get(endpoint)

    if response.status_code == 200:
        try:
            # The items array contains a list objects with pertinent search results
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

@app.get("/health-details", status_code=200)
async def health_details():
    try:
        # 1, 5, 15 minute intervals
        cpu_load_avg_1_min, cpu_load_avg_5_min, cpu_load_avg_15_min = psutil.getloadavg()
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        virtual_memory = psutil.virtual_memory()

        return {
            "cpu": {
                "count": psutil.cpu_count(),
                "percent": psutil.cpu_percent(),
                "loadavg": {
                    "1min": cpu_load_avg_1_min,
                    "5min": cpu_load_avg_5_min,
                    "15min": cpu_load_avg_15_min
                }
            },
            "memory": {
                "percent": virtual_memory.percent,
                "total": virtual_memory.total / (1024.0 ** 3),
                "available": virtual_memory.available / (1024.0 ** 3),
                "used": virtual_memory.used / (1024.0 ** 3),
                "free": virtual_memory.free / (1024.0 ** 3)
            },
            "uptime": uptime
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

