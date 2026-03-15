import os
import sys
import sqlite3
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure local imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from advisor import get_advice
from database import DB_PATH
from models import MentorAdvice

# Define the request body for the /mentor endpoint
class PitchRequest(BaseModel):
    pitch: str
    mentor_id: str

# Initialize FastAPI app
app = FastAPI(title="Mentor Brain API")

# Add CORS middleware to allow calls from front-end apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mentor Brain API"}

@app.get("/mentors", response_model=List[str])
def list_mentors():
    """Returns a list of all mentor IDs currently stored in the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT mentor_id FROM mentors")
        rows = cursor.fetchall()
        conn.close()
        
        # Extract the IDs from the list of tuples
        return [row[0] for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mentor", response_model=MentorAdvice)
def mentor_advice(request: PitchRequest):
    """
    Accepts a pitch and mentor ID, and returns specialized advice 
    from that mentor's perspective.
    """
    try:
        advice = get_advice(request.pitch, request.mentor_id)
        return advice
    except ValueError as e:
        # This occurs if the mentor_id is not found in the DB
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # For any other errors (like Groq API issues)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# If you want to run it directly from this script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
