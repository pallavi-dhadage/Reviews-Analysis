# Review Sentiment Intelligence Platform - System Design

## 1. Problem Statement
Businesses generate massive amounts of customer feedback across various platforms (Amazon, Yelp, Google Play, X). Manually analyzing these reviews is inefficient and prone to bias. There is a critical need for an automated, scalable, and intelligent platform capable of ingesting diverse review streams to extract sentiment, detect topics, identify specific complaints, predict ratings, and track trends over time. This intelligence allows businesses to proactively improve their products, address customer pain points, and monitor brand reputation.

## 2. Recommended Architecture
The platform is designed following a microservices-inspired, modular monolithic approach to facilitate a smooth transition from MVP to a distributed system. 

**Core Layers:**
1. **Ingestion Layer:** Connectors for APIs and batch file processors (CSV/JSON). Uses a unified schema adapter.
2. **Preprocessing Layer:** Text cleaning, tokenization, language detection, and PII masking.
3. **NLP/ML Layer:** 
   - *Baseline:* VADER/TextBlob for sentiment, TF-IDF + NMF for topics.
   - *Advanced (Transformer):* Hugging Face `pipeline` (e.g., DistilBERT for sentiment/rating prediction), BERTopic for topic modeling.
4. **Analytics Layer:** Aggregation of sentiments, time-series metrics, and aspect extraction.
5. **Persistence Layer:** PostgreSQL (for structured review metadata and predictions) + Local Storage/S3 (for raw data/models).
6. **API Layer:** FastAPI exposing RESTful endpoints for ingestion triggers and analytics retrieval.
7. **Dashboard Layer:** Streamlit for an interactive, data-rich user interface.
8. **Orchestration & Deployment:** Dockerized containers orchestrated via Docker Compose.

## 3. Tech Stack
- **Language:** Python 3.10+
- **Data Processing:** `pandas`, `numpy`
- **NLP/ML:** `spacy`, `nltk`, `scikit-learn`, `transformers`, `bertopic`
- **Backend API:** `FastAPI`, `uvicorn`, `pydantic`
- **Database:** `PostgreSQL` (using `SQLAlchemy` ORM)
- **Dashboard:** `Streamlit`
- **Containerization:** `Docker`, `Docker Compose`
- **Testing & Quality:** `pytest`, `black`, `flake8`, `mypy`

## 4. Folder Structure
```text
reviews_analysis/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── csv_loader.py
│   │   └── api_client.py
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── text_cleaner.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sentiment.py
│   │   └── topic_modeling.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── database.py
│   └── api/
│       ├── __init__.py
│       ├── main.py
│       └── routes.py
├── dashboard/
│   └── app.py
├── tests/
│   ├── test_ingestion.py
│   └── test_models.py
├── docs/
│   └── design_document.md
├── .env.example
├── .gitignore
├── requirements.txt
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.dashboard
└── README.md
```

## 5. Data Flow
1. **Ingestion:** Raw reviews (CSV/JSON/API) are fetched and passed to the ingestion module.
2. **Standardization:** Ingested data is mapped to a unified Pydantic schema (e.g., `id`, `text`, `source`, `timestamp`, `rating`).
3. **Preprocessing:** Text is cleaned (lowercased, HTML removed, stop words removed if needed).
4. **Inference:** Preprocessed text is passed to ML models:
   - Sentiment pipeline assigns a polarity score.
   - Topic model assigns a topic ID/label.
   - Aspect extractor highlights key terms.
5. **Storage:** Processed records and model predictions are saved to PostgreSQL.
6. **Retrieval:** The Streamlit dashboard calls the FastAPI endpoints, which query PostgreSQL and return aggregated metrics.

## 6. Model Pipeline
- **Sentiment Analysis:** 
  - *MVP:* Lexicon-based (VADER) for speed and zero-shot capability.
  - *V2:* Hugging Face Transformer (`distilbert-base-uncased-finetuned-sst-2-english`) for nuanced context.
- **Topic Modeling:** 
  - *MVP:* TF-IDF with NMF (Non-negative Matrix Factorization).
  - *V2:* BERTopic for contextual and dense topic clusters.
- **Rating Prediction:** Zero-shot classification or a regressor trained on text embeddings.

## 7. API Endpoints (FastAPI)
- `POST /api/v1/ingest`: Upload CSV/JSON or trigger an API pull.
- `GET /api/v1/reviews`: Fetch reviews with optional filters (source, sentiment, date).
- `GET /api/v1/analytics/sentiment-trend`: Time-series sentiment aggregation.
- `GET /api/v1/analytics/topics`: Top topics and associated keywords.
- `POST /api/v1/analyze`: Real-time analysis of a single review text payload.

## 8. Dashboard Pages (Streamlit)
- **Overview:** High-level KPIs (Total Reviews, Average Sentiment, Average Rating).
- **Sentiment Trends:** Line charts showing sentiment changes over time.
- **Topic Analysis:** Word clouds and bar charts of prominent complaints/topics.
- **Deep Dive:** A data table to filter, search, and read individual reviews and their predictions.

## 9. Training / Evaluation Plan
- **Data Splitting:** 80/10/10 (Train/Val/Test) for custom models.
- **Metrics:**
  - *Sentiment/Rating:* F1-Score, Precision, Recall, MAE (for ratings).
  - *Topics:* Coherence Score (c_v).
- **Tracking:** Use `MLflow` (optional for MVP, added in V2) to log model hyperparameters and metrics.

## 10. Deployment Plan
- **Containerization:** Separate Docker images for the API backend and Streamlit dashboard.
- **Orchestration:** `docker-compose` to spin up PostgreSQL, API, and Dashboard simultaneously.
- **Cloud Path (Future):** Deploy Docker containers to AWS ECS or GCP Cloud Run, with managed PostgreSQL (RDS/Cloud SQL).

## 11. Testing Plan
- **Unit Testing:** `pytest` for preprocessing functions and model prediction wrappers.
- **Integration Testing:** Test API endpoints using FastAPI's `TestClient`.
- **Data Validation:** Pydantic models ensure schema integrity on ingestion.

## 12. Implementation Roadmap
- **Phase 1 (MVP Foundation):** Repository setup, data ingestion layer, PostgreSQL schema, simple preprocessing.
- **Phase 2 (NLP Core):** Implement VADER sentiment, NMF topic modeling, basic FastAPI endpoints.
- **Phase 3 (UI & Integration):** Build Streamlit dashboard, connect to FastAPI, Dockerize the stack.
- **Phase 4 (Advanced Models):** Swap baselines for Transformers (DistilBERT, BERTopic).
- **Phase 5 (Production Polish):** Comprehensive testing, CI/CD pipeline, and README documentation.

---
*Assumptions made:* 
- We are starting with an MVP structure that can run locally via Docker.
- Advanced ML models will run on CPU initially; GPU support will be configurable.
- The dataset scale for the MVP fits within a standard relational database (PostgreSQL).
