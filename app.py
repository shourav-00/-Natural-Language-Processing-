import streamlit as st
import re
from collections import Counter
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Text Analyzer",
    page_icon="📊",
    layout="wide"
)

# Hide Streamlit branding
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total' not in st.session_state:
    st.session_state.total = 0

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard")
    st.markdown("---")
    st.metric("Total Analyses", st.session_state.total)
    st.metric("History", len(st.session_state.history))
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("- Word & Character Count")
    st.markdown("- Sentence & Paragraph Analysis")
    st.markdown("- Sentiment Detection")
    st.markdown("- Reading Time")
    st.markdown("- Most Common Words")
    st.markdown("---")
    st.caption("v1.0")

# Main
st.title("📝 Text Analyzer")
st.caption("Analyze any text instantly")

# Input
col1, col2 = st.columns([3, 1])

with col1:
    text = st.text_area(
        "Enter your text:",
        height=150,
        placeholder="Type or paste text here...",
        key="input"
    )

with col2:
    st.write("")
    st.write("")
    examples = [
        "I love this product! It's amazing and works perfectly.",
        "This is terrible. I'm very disappointed with the service.",
        "The weather is nice today. I think I'll go for a walk."
    ]
    selected = st.selectbox("Try example:", ["Select..."] + examples)
    if selected != "Select...":
        text = selected
        st.session_state.input = selected

# Buttons
col1, col2 = st.columns([3, 1])
with col1:
    analyze = st.button("🔍 Analyze", type="primary", use_container_width=True)
with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.input = ""
        st.rerun()

# Analysis
if analyze and text.strip():
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(text.split())
    char_count = len(text)
    sentences = len(re.findall(r'[.!?]+', text))
    paragraphs = len([p for p in text.split('\n') if p.strip()])
    unique = len(set(words))
    avg_word = sum(len(w) for w in words) / len(words) if words else 0
    reading_time = round(word_count / 200, 1)
    
    # Common words
    common = Counter(words).most_common(5)
    
    # Sentiment
    pos_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'happy', 'best']
    neg_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'sad', 'disappointed']
    pos = sum(1 for w in words if w in pos_words)
    neg = sum(1 for w in words if w in neg_words)
    sentiment_score = (pos - neg) / (pos + neg + 1) if (pos + neg + 1) > 0 else 0
    
    if sentiment_score > 0.2:
        sentiment = "😊 Positive"
    elif sentiment_score < -0.2:
        sentiment = "😞 Negative"
    else:
        sentiment = "😐 Neutral"
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Results")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Words", word_count)
    col2.metric("Characters", char_count)
    col3.metric("Sentences", sentences)
    col4.metric("Reading Time", f"{reading_time}m")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Unique Words", unique)
    col2.metric("Avg Word Length", f"{avg_word:.2f}")
    col3.metric("Sentiment", sentiment)
    
    if common:
        st.write("**Most Common Words:**")
        cols = st.columns(len(common))
        for i, (word, count) in enumerate(common):
            cols[i].metric(word, count)
    
    # Save history
    st.session_state.history.append({
        'text': text[:50] + '...' if len(text) > 50 else text,
        'words': word_count,
        'sentiment': sentiment,
        'time': datetime.now().strftime("%H:%M")
    })
    st.session_state.total += 1
    
    st.success("✅ Analysis saved!")

elif analyze:
    st.warning("⚠️ Please enter some text")

# History tab
with st.expander("📜 History"):
    if st.session_state.history:
        for h in reversed(st.session_state.history[-10:]):
            st.write(f"**{h['text']}**")
            st.caption(f"Words: {h['words']} | {h['sentiment']} | {h['time']}")
            st.divider()
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No history yet")

st.divider()
st.caption("Text Analyzer | Pure Python | No external dependencies")