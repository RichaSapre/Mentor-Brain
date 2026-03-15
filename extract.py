import os
import sys
import json
import glob
import warnings

# Satisfy the linter and ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Silence warnings
warnings.filterwarnings("ignore")

from groq import Groq
from models import MentorModel
from database import save_mentor_model, load_mentor_model

# API Key Discovery
API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY:
    try:
        import config
        API_KEY = config.GROQ_API_KEY
    except ImportError:
        pass

# Initialize Groq Client
if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    client = None

def clean_json_response(text: str) -> dict:
    """Finds and parses the JSON object from the response text."""
    cleaned = text.strip()
    start = cleaned.find('{')
    end = cleaned.rfind('}') + 1
    if start != -1 and end != 0:
        cleaned = cleaned[start:end]
    return json.loads(cleaned)

def extract_mentor_logic():
    if not API_KEY:
        print("\n❌ Error: Groq API Key missing. Add it to config.py as GROQ_API_KEY")
        return

    transcript_files = glob.glob("transcripts/*.txt")
    
    for file_path in transcript_files:
        mentor_id = os.path.basename(file_path).replace(".txt", "")
        
        # Check if already processed
        if load_mentor_model(mentor_id):
            print(f"✅ {mentor_id} logic already in DB. Skipping.")
            continue

        print(f"🧠 Extracting thinking patterns for: {mentor_id} using Groq...")
        with open(file_path, "r") as f:
            content = f.read()

        prompt = f"""
        Read this mentor transcript. Extract and return ONLY a JSON object with:
        - mental_models: list of frameworks/lenses they use
        - red_flags: things that make them skeptical
        - questions_always_asked: questions they repeatedly return to
        - advice_patterns: how they structure and deliver feedback
        
        Return raw JSON only. No explanation. No markdown backticks.
        
        TRANSCRIPT:
        {content}
        """
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.choices[0].message.content
            raw_data = clean_json_response(text)
            
            mentor_model = MentorModel(
                mentor_id=mentor_id,
                mental_models=raw_data.get("mental_models", []),
                red_flags=raw_data.get("red_flags", []),
                questions_always_asked=raw_data.get("questions_always_asked", []),
                advice_patterns=raw_data.get("advice_patterns", [])
            )
            save_mentor_model(mentor_id, mentor_model)
            print(f"✅ Saved {mentor_id} to DB")
            
        except Exception as e:
            print(f"❌ Error for {mentor_id}: {e}")

if __name__ == "__main__":
    extract_mentor_logic()
