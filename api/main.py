from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class SearchTerms(BaseModel):
    terms: str

app = FastAPI()

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

