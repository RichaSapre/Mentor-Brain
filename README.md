# Mentor Brain

Mentor Brain is an AI-powered system designed to simulate structured mentorship by going beyond simple retrieval-based responses. Instead of just fetching information, it attempts to reason, guide, and respond contextually, much like a human mentor would.

At its core, the system focuses on delivering direction over information. It processes user queries not just as questions, but as intent-driven problems, and generates responses that aim to:

break down thinking
provide actionable guidance
adapt to context

Unlike traditional RAG (Retrieval-Augmented Generation) systems that rely heavily on retrieving documents and stitching responses, Mentor Brain introduces a more reasoning-first approach, where the model is encouraged to interpret, structure, and respond with clarity rather than just retrieval.

The project explores how AI systems can evolve from being information providers to decision-support systems, making them more useful in real-world learning, problem-solving, and career guidance scenarios.
## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key**:
    *   Rename `config_example.py` to `config.py`.
    *   Add your Groq API Key to `GROQ_API_KEY`.

3.  **Import Mentors** (if not already done):
    *   Add transcripts to the `/transcripts` folder.
    *   Run `python3 extract.py` to build the mental models in SQLite.

## Running the API

To start the FastAPI server:

```bash
uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`.

## API Endpoints

### 1. `GET /mentors`
Returns a list of all available mentors in the system.
- **Example Response**: `["Naval", "Paul", "altman"]`

### 2. `POST /mentor`
Generates specialized advice for a given pitch.
- **Body Content**:
    ```json
    {
      "pitch": "I am building a decentralized coffee machine...",
      "mentor_id": "Naval"
    }
    ```
- **Returns**: A JSON object containing `feedback`, `key_questions`, and a `verdict`.

## Testing

Run automated tests with:
```bash
pytest
```
