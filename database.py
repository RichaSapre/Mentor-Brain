import sqlite3
import json
from models import MentorModel

DB_PATH = "mentors.db"

def init_db():
    """Initializes the SQLite database and creates the mentors table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # model_json stores the serialized MentorModel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors (
            mentor_id TEXT PRIMARY KEY,
            model_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_mentor_model(mentor_id: str, model: MentorModel):
    """Saves or updates a mentor's thinking pattern in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Convert the Pydantic model to a JSON string for storage
    model_json = model.model_dump_json()
    cursor.execute('''
        INSERT OR REPLACE INTO mentors (mentor_id, model_json)
        VALUES (?, ?)
    ''', (mentor_id, model_json))
    conn.commit()
    conn.close()

def load_mentor_model(mentor_id: str) -> MentorModel:
    """Loads a mentor's thinking pattern from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT model_json FROM mentors WHERE mentor_id = ?', (mentor_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Reconstruct the Pydantic model from the stored JSON string
        data = json.loads(row[0])
        return MentorModel(**data)
    return None

# Initialize the database when this script is imported
init_db()
