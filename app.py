import streamlit as st
import re
from collections import Counter
import random
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Text Analyzer Pro",
    page_icon="📝",
    layout="wide"
)

# Custom CSS - Clean & Professional
st.markdown("""
<style>
    .main { padding: 1rem; }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.3rem;
    }
    .result-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 0.3rem 0;
    }
    .highlight {
        background: #fff3cd;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_analyses' not in st.session_state:
    st.session_state.total_analyses = 0

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Total")
        st.markdown(f"<h2 style='text-align: center;'>{st.session_state.total_analyses}</h2>", 
                   unsafe_allow_html=True)
    with col2:
        st.markdown("#### History")
        st.markdown(f"<h2 style='text-align: center;'>{len(st.session_state.history)}</h2>", 
                   unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📖 About")
    st.markdown("""
    **Text Analyzer Pro** provides instant statistics about any text.
    
    **Features:**
    - Word & character count
    - Sentence & paragraph count
    - Most common words
    - Reading time
    - Text complexity
    - History tracking
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Longer text = more accurate analysis
    - Use proper punctuation for sentence counting
    - Try the example texts below!
    """)
    
    st.markdown("---")
    st.caption("Version 2.0 | No external dependencies")

# Main content
st.title("📝 Text Analyzer Pro")
st.markdown("Get instant, detailed statistics about any text")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📊 Analyze", "📜 History", "ℹ️ About"])

with tab1:
    # Input section
    col_input, col_examples = st.columns([3, 1])
    
    with col_input:
        user_text = st.text_area(
            "Enter your text:",
            height=150,
            placeholder="Paste or type your text here...",
            key="input_text"
        )
    
    with col_examples:
        st.markdown("### Quick Examples")
        examples = [
            "The quick brown fox jumps over the lazy dog. This is a classic pangram used to test fonts and typing skills.",
            "I love this product! It's amazing and works perfectly. The customer service was outstanding. Highly recommended!",
            "The weather today is terrible. It's raining heavily and I can't go outside. I'm so disappointed.",
            "Data science is fascinating. It combines statistics, programming, and domain knowledge to extract insights from data.",
            "Hello world! This is a short text for testing purposes. It has some words and punctuation."
        ]
        
        selected = st.selectbox(
            "Try one:",
            ["Select..."] + examples,
            key="example_selector"
        )
        
        if selected != "Select...":
            user_text = selected
            st.session_state.input_text = selected
    
    # Analysis buttons
    col_analyze, col_clear = st.columns([3, 1])
    
    with col_analyze:
        analyze_clicked = st.button("🔍 Analyze Text", type="primary")
    
    with col_clear:
        if st.button("🗑️ Clear"):
            st.session_state.input_text = ""
            st.rerun()
    
    # Analysis logic
    if analyze_clicked and user_text.strip():
        text = user_text
        
        # Basic statistics
        word_count = len(text.split())
        char_count = len(text)
        char_no_space = len(text.replace(" ", ""))
        sentence_count = len(re.findall(r'[.!?]+', text))
        paragraph_count = len([p for p in text.split('\n') if p.strip()])
        
        # Word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        most_common = word_freq.most_common(5)
        
        # Unique words
        unique_words = len(set(words))
        
        # Average word length
        avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
        
        # Reading time (average 200 words per minute)
        reading_time = round(word_count / 200, 1)
        
        # Text complexity (based on word length)
        long_words = [w for w in words if len(w) > 6]
        complexity = len(long_words) / len(words) if words else 0
        
        # Sentiment score (simple heuristic)
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'best', 'love', 'happy', 'awesome', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'sad', 'angry', 'poor', 'disappointed']
        
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        sentiment_score = (pos_count - neg_count) / (pos_count + neg_count + 1)
        
        # Display results
        st.markdown("### 📊 Analysis Results")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{word_count}</div>
                <div class="metric-label">Words</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{char_count}</div>
                <div class="metric-label">Characters</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{sentence_count}</div>
                <div class="metric-label">Sentences</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{reading_time} min</div>
                <div class="metric-label">Reading Time</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed statistics
        st.markdown("### 📈 Detailed Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <strong>📝 Characters (no spaces)</strong>
                <h3>{char_no_space}</h3>
            </div>
            <div class="stat-box">
                <strong>📄 Paragraphs</strong>
                <h3>{paragraph_count}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <strong>🔤 Unique Words</strong>
                <h3>{unique_words}</h3>
            </div>
            <div class="stat-box">
                <strong>📏 Avg Word Length</strong>
                <h3>{avg_word_len:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Sentiment
            if sentiment_score > 0.3:
                sentiment_label = "😊 Positive"
                sentiment_color = "#28a745"
            elif sentiment_score < -0.3:
                sentiment_label = "😞 Negative"
                sentiment_color = "#dc3545"
            else:
                sentiment_label = "😐 Neutral"
                sentiment_color = "#ffc107"
            
            st.markdown(f"""
            <div class="stat-box">
                <strong>💭 Sentiment</strong>
                <h3 style="color: {sentiment_color}">{sentiment_label}</h3>
            </div>
            <div class="stat-box">
                <strong>📊 Complexity</strong>
                <h3>{complexity:.1%}</h3>
                <small>Long words > 6 characters</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Most common words
        if most_common:
            st.markdown("### 🔥 Most Common Words")
            
            cols = st.columns(min(len(most_common), 5))
            for i, (word, count) in enumerate(most_common):
                with cols[i % len(cols)]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                        <h3 style="margin: 0;">{word}</h3>
                        <small style="color: #6c757d;">{count} time{'s' if count > 1 else ''}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Text preview with stats
        with st.expander("📝 Text Preview"):
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 3px solid #1f77b4;">
                <p style="font-style: italic; margin: 0;">"{text}"</p>
                <hr style="margin: 0.5rem 0;">
                <small>Total words: {word_count} | Characters: {char_count} | Sentences: {sentence_count}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Save to history
        analysis_entry = {
            'text': text[:100] + ('...' if len(text) > 100 else ''),
            'words': word_count,
            'characters': char_count,
            'sentences': sentence_count,
            'reading_time': reading_time,
            'sentiment': sentiment_label,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.history.append(analysis_entry)
        st.session_state.total_analyses += 1
        
        st.success("✅ Analysis saved to history!")
        
    elif analyze_clicked:
        st.warning("⚠️ Please enter some text to analyze!")

with tab2:
    st.markdown("### 📜 Analysis History")
    
    if st.session_state.history:
        if st.button("💾 Export History"):
            history_text = "Text Analysis History\n"
            history_text += "=" * 50 + "\n\n"
            for entry in st.session_state.history:
                history_text += f"Text: {entry['text']}\n"
                history_text += f"Words: {entry['words']}\n"
                history_text += f"Characters: {entry['characters']}\n"
                history_text += f"Sentences: {entry['sentences']}\n"
                history_text += f"Reading Time: {entry['reading_time']} min\n"
                history_text += f"Sentiment: {entry['sentiment']}\n"
                history_text += f"Time: {entry['timestamp']}\n"
                history_text += "-" * 30 + "\n"
            
            st.download_button(
                label="📥 Download History",
                data=history_text,
                file_name="text_analysis_history.txt",
                mime="text/plain"
            )
        
        # Display history
        for idx, entry in enumerate(reversed(st.session_state.history)):
            with st.container():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 6px; border-left: 3px solid #1f77b4; margin: 0.3rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span><strong>"{entry['text']}"</strong></span>
                        <span style="color: #6c757d; font-size: 0.8rem;">{entry['timestamp']}</span>
                    </div>
                    <div style="display: flex; gap: 1.5rem; margin-top: 0.3rem; font-size: 0.85rem; color: #6c757d;">
                        <span>📝 {entry['words']} words</span>
                        <span>🔤 {entry['characters']} chars</span>
                        <span>📄 {entry['sentences']} sentences</span>
                        <span>⏱️ {entry['reading_time']} min</span>
                        <span>{entry['sentiment']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No analysis history yet. Analyze some text in the 'Analyze' tab!")

with tab3:
    st.markdown("### ℹ️ About This Tool")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🛠️ Technology
        
        - **Framework:** Streamlit
        - **Language:** Python
        - **Dependencies:** None (pure Python)
        - **Data:** All local, no external calls
        
        #### 📊 What It Analyzes
        
        - Word & character count
        - Sentence & paragraph count
        - Reading time estimation
        - Text complexity
        - Basic sentiment (positive/negative/neutral)
        - Most common words
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 Why This Project
        
        - **Zero external dependencies** (No pillow, no torch, no transformers!)
        - **Instant deployment** on Streamlit Cloud
        - **Fast analysis** (results in milliseconds)
        - **Clean, professional UI**
        - **Perfect for hackathons**
        - **No AI/Keyboard markers**
        
        #### 📈 Use Cases
        
        - Content writing analysis
        - Social media post checking
        - Academic text review
        - Email analysis
        - Blog post optimization
        """)
    
    st.markdown("---")
    st.markdown("""
    **How It Works**
    
    The tool uses pure Python to analyze text:
    1. Text is tokenized using simple string operations
    2. Word frequency is calculated with Counter
    3. Sentiment uses a heuristic word list
    4. All results are generated instantly without external calls
    """)

# Footer
st.markdown("---")
st.caption("Text Analyzer Pro | Pure Python | No External Dependencies")