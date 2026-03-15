import os
import sys
import json
import warnings

# Path and Warning Fixes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
warnings.filterwarnings("ignore")

from groq import Groq
from models import MentorModel, MentorAdvice
from database import load_mentor_model

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
    cleaned = text.strip()
    start = cleaned.find('{')
    end = cleaned.rfind('}') + 1
    if start != -1 and end != 0:
        cleaned = cleaned[start:end]
    return json.loads(cleaned)

def get_advice(pitch: str, mentor_id: str) -> MentorAdvice:
    mentor_logic = load_mentor_model(mentor_id)
    if not mentor_logic:
        raise ValueError(f"Mentor '{mentor_id}' logic missing in DB.")

    if not API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please add it to config.py.")

    prompt = f"""
    You are {mentor_id}. Here is how you think:
    - Mental Models: {mentor_logic.mental_models}
    - Red Flags: {mentor_logic.red_flags}
    - Questions You Always Ask: {mentor_logic.questions_always_asked}
    - Advice Patterns: {mentor_logic.advice_patterns}

    A founder just gave you this pitch: 
    "{pitch}"

    Respond exactly as this mentor would — use their style, their questions, their judgment.
    Return ONLY JSON with no markdown and no backticks:
    {{ 
      "feedback": "your detailed response here", 
      "key_questions": ["question 1", "question 2"], 
      "verdict": "pass|explore|hard pass" 
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content
        raw_advice = clean_json_response(text)
        
        return MentorAdvice(
            mentor_id=mentor_id,
            feedback=raw_advice.get("feedback", ""),
            key_questions=raw_advice.get("key_questions", []),
            verdict=raw_advice.get("verdict", "explore")
        )
    except Exception as e:
        print(f"❌ Groq API Error for {mentor_id}: {e}")
        return MentorAdvice(
            mentor_id=mentor_id, 
            feedback="Error generating advice.", 
            key_questions=[], 
            verdict="explore"
        )
