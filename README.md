# SHL AI Conversational Recommendation API

An AI-powered REST API that recommends the most relevant SHL assessments based on a job description or hiring requirement.

The system uses Google's Gemini model to analyze recruiter queries and intelligently recommend suitable SHL assessments from a curated assessment catalog.

---

## Live Demo

**API URL**

https://shl-ai-conversational-recommender.onrender.com

**Swagger Documentation**

https://shl-ai-conversational-recommender.onrender.com/docs

---

## Features

- Recommend SHL assessments from natural language job descriptions.
- AI-powered recommendation generation using Google Gemini.
- Returns structured JSON responses.
- FastAPI-based REST API.
- Interactive Swagger UI.
- Ready for deployment on Render.

---

## Project Structure

```
SHL-AI-Conversational-Recommender
│
├── app
│   ├── main.py
│   ├── recommend.py
│   ├── llm.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── parser.py
│   ├── scraper.py
│   ├── catalog_builder.py
│   └── ...
│
├── data
│   ├── catalog.json
│   └── assessment_urls.json
│
├── requirements.txt
├── README.md
└── runtime.txt
```

---

## Technology Stack

- Python 3.11
- FastAPI
- Google Gemini API
- Pydantic
- BeautifulSoup
- Requests
- Uvicorn

---

## How It Works

1. User submits a job description.
2. The application loads the SHL assessment catalog.
3. Google Gemini analyzes the recruiter requirement.
4. Gemini selects the most suitable assessments from the available catalog.
5. The API returns:
   - Recommendation explanation
   - Matching assessments
   - Category
   - Official SHL URLs

---

## API Endpoints

### GET /

Health check

Response

```json
{
  "status": "running",
  "message": "SHL AI Recommendation API"
}
```

---

### POST /recommend

Request

```json
{
  "query": "Java Backend Developer"
}
```

Example Response

```json
{
  "query": "Java Backend Developer",
  "recommendation": "Recommended assessments include coding simulations, technical skill evaluation, and personality assessment.",
  "assessments": [
    {
      "name": "SHL Coding Skills Assessment and Simulations",
      "category": "Skills & Simulations",
      "score": 0.98,
      "url": "https://www.shl.com/..."
    },
    {
      "name": "Fast, Simple Technical Skill Assessment",
      "category": "Skills & Simulations",
      "score": 0.95,
      "url": "https://www.shl.com/..."
    },
    {
      "name": "SHL Occupational Personality Questionnaire (OPQ)",
      "category": "Personality Assessment",
      "score": 0.85,
      "url": "https://www.shl.com/..."
    }
  ]
}
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/vinod694/SHL-AI-Conversational-Recommender.git

cd SHL-AI-Conversational-Recommender
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run Locally

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

## Deployment

This project is deployed on Render.

Start Command

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Sample Queries

- Java Backend Developer
- Python Developer
- Customer Support Executive
- Data Analyst
- DevOps Engineer
- AI Engineer
- Sales Executive
- Software Tester

---

## Repository

https://github.com/vinod694/SHL-AI-Conversational-Recommender

---

## Author

Vinod Kumar Nevuluri