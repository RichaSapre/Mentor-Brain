from advisor import get_advice
from extract import extract_mentor_logic
from database import load_mentor_model
import os

def run_test():
    """Runs a sample pitch through the mentor brains and prints their advice."""
    
    # 1. Try to get key from Environment Variable or config.py
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        try:
            import config
            api_key = config.GOOGLE_API_KEY
        except ImportError:
            pass

    if not api_key:
        print("\n❌ ERROR: GOOGLE_API_KEY is missing.")
        print("Please add it to a config.py file or run: export GOOGLE_API_KEY='your_key'\n")
        return

    # 2. Process transcripts (this will fill the database)
    print("--- 1. Initializing Mentor Brains ---")
    extract_mentor_logic()
    
    # 2. Automatically discover mentors from the transcripts folder
    transcript_files = [f for f in os.listdir("transcripts") if f.endswith(".txt")]
    mentors = [f.replace(".txt", "") for f in transcript_files]
    
    if not mentors:
        print("No mentors found in /transcripts folder.")
        return

    # 3. Define the test pitch
    pitch = (
        "We are building an AI-powered personal trainer that uses your phone camera "
        "to track your form in real-time. It's for busy professionals who want to work out "
        "at home but are afraid of getting injured. We plan to charge a $20/month subscription."
    )
    
    print(f"\n--- 2. Pitching: {pitch} ---\n")
    
    # 4. Get and display advice for all discovered mentors
    for mentor_id in mentors:
        # ...
        try:
            advice = get_advice(pitch, mentor_id)
            print("=" * 60)
            print(f"MENTOR: {mentor_id}")
            print(f"VERDICT: {advice.verdict.upper()}")
            print("-" * 60)
            print(f"FEEDBACK: {advice.feedback}")
            print("-" * 60)
            print(f"KEY QUESTIONS: {', '.join(advice.key_questions)}")
            print("=" * 60 + "\n")
        except Exception as e:
            print(f"Could not get advice from {mentor_id}: {e}")

if __name__ == "__main__":
    run_test()
