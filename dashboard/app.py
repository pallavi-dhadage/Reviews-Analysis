import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="Review Intelligence Platform", layout="wide")

API_URL = "http://localhost:8000/api/v1"

st.title("Review Sentiment Intelligence Dashboard")
st.markdown("Analyze customer reviews, extract sentiment, and identify key complaints.")

# Sidebar Navigation
page = st.sidebar.selectbox("Navigate", ["Overview", "Real-time Analysis", "Batch Ingestion"])

if page == "Overview":
    st.header("Platform Metrics")
    try:
        response = requests.get(f"{API_URL}/analytics/sentiment-summary")
        if response.status_code == 200:
            data = response.json()
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Reviews Ingested", data.get("total_reviews", 0))
            col2.metric("Average Sentiment Score", data.get("average_sentiment", 0.0))
            col3.metric("Platform Status", "Online")
        else:
            st.error("Could not fetch metrics.")
    except Exception as e:
        st.error(f"API Connection Error: {e}")

elif page == "Real-time Analysis":
    st.header("Analyze a Single Review")
    review_text = st.text_area("Enter review text here:")
    if st.button("Analyze Sentiment"):
        if review_text:
            try:
                res = requests.post(f"{API_URL}/analyze", json={"text": review_text})
                if res.status_code == 200:
                    result = res.json()
                    st.success(f"Sentiment Label: **{result['sentiment_label'].upper()}**")
                    st.info(f"Sentiment Score (Compound): {result['sentiment_score']}")
                else:
                    st.error("Failed to analyze text.")
            except Exception as e:
                st.error(f"API Connection Error: {e}")
        else:
            st.warning("Please enter some text.")

elif page == "Batch Ingestion":
    st.header("Ingest CSV Dataset")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    source_name = st.text_input("Source Name (e.g., Amazon, Yelp)", value="Amazon")
    text_col = st.text_input("Text Column Name", value="review_text")
    rating_col = st.text_input("Rating Column Name (Optional)", value="")
    
    if st.button("Start Ingestion"):
        if uploaded_file is not None and source_name and text_col:
            st.info("Ingesting...")
            # We can use requests.post with files
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            params = {
                "source_name": source_name,
                "text_col": text_col,
            }
            if rating_col:
                params["rating_col"] = rating_col
                
            try:
                res = requests.post(f"{API_URL}/ingest", params=params, files=files)
                if res.status_code == 200:
                    st.success(f"Successfully ingested {res.json().get('records_inserted')} records!")
                else:
                    st.error(f"Ingestion failed: {res.text}")
            except Exception as e:
                st.error(f"API Connection Error: {e}")
        else:
            st.warning("Please upload a file and provide the required column names.")
