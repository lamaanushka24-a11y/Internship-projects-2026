import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Sentiment Dashboard", page_icon="📊", layout="wide")

st.title("📊 Real-Time Sentiment Analysis Dashboard")
st.write("Type any product review, tweet, or statement below to analyze its emotional sentiment score.")

# Text inputs
user_text = st.text_area("Enter text to analyze:", placeholder="Type something like: 'I love this project, it works great!'")

# Built-in lightweight lexicon analyzer logic
positive_words = ['love', 'great', 'amazing', 'good', 'excellent', 'happy', 'best', 'awesome', 'perfect', 'easy', 'smooth']
negative_words = ['bad', 'hate', 'worst', 'terrible', 'broken', 'error', 'fail', 'slow', 'difficult', 'annoying', 'wrong']

if st.button("Analyze Sentiment"):
    if user_text.strip() == "":
        st.warning("Please enter some text first!")
    else:
        # Convert text to lowercase and split into individual words
        words = user_text.lower().split()
        
        pos_count = sum(1 for word in words if any(pos in word for pos in positive_words))
        neg_count = sum(1 for word in words if any(neg in word for neg in negative_words))
        
        # Calculate final metrics
        if pos_count > neg_count:
            sentiment = "POSITIVE 🟢"
            score = 100 if neg_count == 0 else round((pos_count / (pos_count + neg_count)) * 100, 1)
            color = "green"
        elif neg_count > pos_count:
            sentiment = "NEGATIVE 🔴"
            score = 100 if pos_count == 0 else round((neg_count / (pos_count + neg_count)) * 100, 1)
            color = "red"
        else:
            sentiment = "NEUTRAL 🟡"
            score = 50.0
            color = "blue"
            
        st.write("---")
        st.subheader("Analysis Results")
        
        # Display Metrics in Columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Detected Sentiment", value=sentiment)
        with col2:
            st.metric(label="Confidence Score", value=f"{score}%")
            
        # Display Visual Breakdown Data Table
        st.subheader("📋 Keyword Match Metrics")
        data = {
            "Metric Category": ["Positive Target Words", "Negative Target Words", "Total Words Evaluated"],
            "Count Matches": [pos_count, neg_count, len(words)]
        }
        df = pd.DataFrame(data)
        st.table(df)
