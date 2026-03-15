import pytest
from models import MentorModel, MentorAdvice
from database import init_db, save_mentor_model, load_mentor_model
import os

def test_models_vaildation():
    """Verify that Pydantic models validate correctly."""
    model = MentorModel(
        mentor_id="test_mentor",
        mental_models=["First Principles"],
        red_flags=["Slow iteration"],
        questions_always_asked=["Why now?"],
        advice_patterns=["Be blunt"]
    )
    assert model.mentor_id == "test_mentor"
    assert len(model.mental_models) == 1

def test_database_persistence():
    """Verify that we can save and load from SQLite."""
    # Ensure a fresh test DB
    test_db = "test_mentors.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    import database
    database.DB_PATH = test_db
    init_db()
    
    model = MentorModel(
        mentor_id="dummy",
        mental_models=[],
        red_flags=[],
        questions_always_asked=[],
        advice_patterns=[]
    )
    
    save_mentor_model("dummy", model)
    loaded = load_mentor_model("dummy")
    
    assert loaded is not None
    assert loaded.mentor_id == "dummy"
    
    # Clean up
    if os.path.exists(test_db):
        os.remove(test_db)
