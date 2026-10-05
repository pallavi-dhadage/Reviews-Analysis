# Review Sentiment Intelligence Platform

A scalable, maintainable, production-ready analytics platform that extracts sentiment, topics, and actionable insights from customer reviews.

## Architecture & Design
Please see [`docs/design_document.md`](docs/design_document.md) for the complete architecture, data flow, and implementation plan.

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the database and services:
   ```bash
   docker-compose up -d
   ```
3. Run the API (if not using docker):
   ```bash
   uvicorn src.api.main:app --reload
   ```
4. Run the Dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```
