# BitHealth Triage API

A simple medical triage API that recommends the most relevant hospital department based on patient information (gender, age, and symptoms). The API uses Google Gemini (via LangChain) to generate recommendations.

## Dependencies

Use Python 3.9+.

Install dependencies with:

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**

```txt
fastapi
uvicorn
python-dotenv
langchain
langchain-google-genai
langchain-core
pydantic
```

## Environment Setup

1. Create a `.env` file in the root directory:

```bash
touch .env
```

2. Add your Google API Key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

3. Get Unique Google API Key from: (https://aistudio.google.com/app/apikey)

## How to Run

Run the FastAPI server:

```bash
python main.py
```

Or manually:

```bash
uvicorn main:app --reload
```

## API Endpoints

### `GET /`

**Description:** Check API status.

**Response:**

```json
{
  "status": "BitHealth Triage API is running."
}
```

### `POST /recommend`

**Description:** Predict the most relevant department based on patient data.

**Request Body:**

| Field | Type | Description |
|-------|------|-------------|
| `gender` | `string` | Patient gender |
| `age` | `integer` | Patient age |
| `symptoms` | `array[string]` | List of patient symptoms |

**Example Request:**

```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
-H "Content-Type: application/json" \
-d '{
  "gender": "male",
  "age": 30,
  "symptoms": ["fever", "headache", "fatigue"]
}'
```

**Example Response:**

```json
{
  "recommended_department": "Internal Medicine"
}
```

## Project Structure

```
├── main.py
├── .env
├── requirements.txt
└── README.md
```
