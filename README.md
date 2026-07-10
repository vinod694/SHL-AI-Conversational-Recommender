# SHL AI Assessment Recommendation System

An AI-powered recommendation system that helps recruiters identify the most relevant SHL assessments for a given job description using semantic search and Google's Gemini Large Language Model (LLM).

---

# Project Overview

Recruiters often spend significant time searching through the SHL assessment catalog to identify assessments suitable for different job roles.

This project automates that process by combining semantic search with AI-generated recommendations. Given a job description or role title, the system retrieves the most relevant SHL assessments and generates recruiter-friendly recommendations.

---

# Features

- Scrapes SHL Individual Assessment catalog
- Builds a structured assessment catalog
- Generates semantic embeddings using Sentence Transformers
- Stores embeddings in a FAISS vector index
- Retrieves relevant assessments using semantic similarity
- Generates AI-powered recommendations using Gemini
- FastAPI REST API
- Interactive Swagger API documentation
- Structured JSON API responses

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| FastAPI | REST API |
| Playwright | Web Scraping |
| Sentence Transformers | Text Embeddings |
| FAISS | Semantic Vector Search |
| Google Gemini API | Recommendation Generation |
| NumPy | Vector Operations |
| Pydantic | Data Validation |
| Uvicorn | ASGI Server |

---

# Project Structure

```text
shl-ai-agent/
│
├── app/
│   ├── __init__.py
│   ├── scraper.py
│   ├── parser.py
│   ├── catalog_builder.py
│   ├── prepare_catalog.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── llm.py
│   ├── recommend.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── main.py
│   └── .env
│
├── data/
│   ├── assessment_urls.json
│   ├── catalog.json
│   ├── embeddings.npy
│   └── faiss.index
│
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

## 1. Download the project

Download or copy the project into your local machine.

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside the `app` folder.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

# Preparing the Data

If the catalog has not been generated yet, run the scripts in the following order.

## Collect SHL Assessment URLs

```bash
python app/url_collector.py
```

## Scrape Assessment Information

```bash
python app/scraper.py
```

## Build the Catalog

```bash
python app/catalog_builder.py
```

## Generate Embeddings

```bash
python app/embeddings.py
```

## Build the FAISS Index

```bash
python app/vector_store.py
```

---

# Running the API

Start the FastAPI application.

```bash
uvicorn app.main:app --reload
```

The API will start at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## GET /

Returns the API status.

### Response

```json
{
  "status": "running",
  "message": "SHL AI Recommendation API"
}
```

---

## POST /recommend

### Request

```json
{
  "query": "Java Backend Developer"
}
```

### Example Response

```json
{
  "query": "Java Backend Developer",
  "recommendation": "...",
  "assessments": [
    {
      "name": "SHL Coding Skills Assessment and Simulations",
      "category": "Skills & Simulations",
      "score": 0.2528,
      "url": "https://www.shl.com/products/assessments/skills-and-simulations/coding-simulations/"
    },
    {
      "name": "Situational Judgement Tests",
      "category": "Behavioral Assessment",
      "score": 0.2416,
      "url": "https://www.shl.com/products/assessments/behavioral-assessments/situation-judgement-tests-sjt/"
    },
    {
      "name": "Fast, Simple Technical Skill Assessment",
      "category": "Skills & Simulations",
      "score": 0.1795,
      "url": "https://www.shl.com/products/assessments/skills-and-simulations/technical-skills/"
    }
  ]
}
```

---

# System Workflow

1. Collect SHL assessment URLs.
2. Scrape assessment details.
3. Parse and clean assessment information.
4. Build a structured assessment catalog.
5. Generate semantic embeddings.
6. Create a FAISS vector index.
7. Receive a recruiter query.
8. Perform semantic similarity search.
9. Retrieve the most relevant SHL assessments.
10. Use Gemini to generate recruiter-friendly recommendations.
11. Return structured recommendations through the REST API.

---

# Example Query

```
Java Backend Developer
```

Example retrieved assessments:

- SHL Coding Skills Assessment and Simulations
- Situational Judgement Tests
- Fast, Simple Technical Skill Assessment

---

# Future Improvements

- Conversational multi-turn recommendations
- Hybrid keyword + semantic retrieval
- Assessment comparison support
- Context-aware refinement of recommendations
- Deployment using Docker
- CI/CD pipeline
- Authentication and rate limiting
- Automated testing

---

# License

This project was developed as part of the SHL AI Intern Take-home Assignment.

It is intended for educational and demonstration purposes only.