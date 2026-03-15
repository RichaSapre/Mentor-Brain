# Mentor Brain

A system that extracts reasoning patterns from mentor transcripts and uses them to give pitch feedback in each mentor's unique style (powered by Groq & Llama 3).

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
