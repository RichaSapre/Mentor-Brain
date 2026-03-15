from pydantic import BaseModel, Field
from typing import List, Literal

# This model represents the structured thinking pattern of a mentor
class MentorModel(BaseModel):
    mentor_id: str
    mental_models: List[str] = Field(default_factory=list)      # Frameworks/lenses they use
    red_flags: List[str] = Field(default_factory=list)          # Things that make them skeptical
    questions_always_asked: List[str] = Field(default_factory=list)  # Recurring questions
    advice_patterns: List[str] = Field(default_factory=list)    # How they structure and deliver feedback

# This model represents the feedback given by a mentor for a specific pitch
class MentorAdvice(BaseModel):
    mentor_id: str
    feedback: str
    key_questions: List[str] = Field(default_factory=list)
    verdict: str = "explore" # Using str instead of Literal to be resilient to AI output
