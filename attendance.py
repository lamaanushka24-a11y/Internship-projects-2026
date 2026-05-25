import streamlit as st
import random
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Sample Training Data (Intents)
data = {
    "intents": [
        {"tag": "greeting", "patterns": ["Hi", "Hello", "Is anyone there?", "Hey"], "responses": ["Hello! How can I help you today?", "Hi there! What can I do for you?"]},
        {"tag": "goodbye", "patterns": ["Bye", "See you later", "Goodbye"], "responses": ["Goodbye! Have a great day.", "See you soon!"]},
        {"tag": "placement_query", "patterns": ["How do I prepare for placements?", "placement tips", "job interview help"], "responses": ["Focus on Data Structures, Algorithms, and core CS fundamentals like OS and DBMS!", "Practice coding daily on LeetCode and keep your resume updated."]}
    ]
}

# 2. Preprocessing & Training
X, y = [], []
for intent in data['intents']:
    for pattern in intent['patterns']:
        X.append(pattern.lower())
        y.append(intent['tag'])

vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)
clf = LogisticRegression()
clf.fit(X_vectorized, y)

# 3. Chatbot Logic
def get_bot_response(user_text):
    # Rule-based quick check
    if user_text.lower() in ['hi', 'hello', 'hey']:
        return "Hello! (Rule-based response)"
    
    # ML Classification
    vec = vectorizer.transform([user_text.lower()])
    tag = clf.predict(vec)[0]
    
    for intent in data['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "I'm sorry, I didn't quite understand that."

# 4. Streamlit UI Layout
st.title("🤖 Smart Chatbot Assistant")
user_input = st.text_input("You: ", placeholder="Type your message here...")
if user_input:
    st.markdown(f"**Bot:** {get_bot_response(user_input)}")
