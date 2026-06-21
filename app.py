import streamlit as st
import re
from collections import Counter
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Text Analyzer Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean & Professional (NO keyboard/AI logos)
st.markdown("""
<style>
    /* Hide ALL Streamlit branding and logos */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a2e;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    .sidebar-stat {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    
    .sidebar-stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    
    .sidebar-stat-label {
        font-size: 0.8rem;
        color: #6c757d;
        margin-top: 0.2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        margin-top: 0.3rem;
    }
    
    /* Result cards */
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #4a90d9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    
    /* Stat boxes */
    .stat-box {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 0.3rem 0;
    }
    
    .stat-box:hover {
        border-color: #4a90d9;
        box-shadow: 0 2px 8px rgba(74, 144, 217, 0.1);
    }
    
    /* Word items */
    .word-item {
        display: inline-block;
        padding: 0.4rem 1rem;
        margin: 0.2rem;
        border-radius: 20px;
        background: #f0f4ff;
        border: 1px solid #d4e0ff;
        font-size: 0.9rem;
        color: #1a1a2e;
        transition: all 0.2s;
    }
    
    .word-item:hover {
        background: #4a90d9;
        color: white;
        border-color: #4a90d9;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(74, 144, 217, 0.3);
    }
    
    .stButton > button[kind="primary"] {
        background: #4a90d9;
        color: white;
    }
    
    /* Info box */
    .info-box {
        background: #f0f4ff;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #4a90d9;
        margin: 0.5rem 0;
    }
    
    /* History items */
    .history-item {
        background: white;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        border-left: 3px solid #4a90d9;
        margin: 0.4rem 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: all 0.2s;
    }
    
    .history-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4a90d9;
        border-radius: 10px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4a90d9;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_analyses' not in st.session_state:
    st.session_state.total_analyses = 0
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# ============================================
# SIDEBAR - Clean Dashboard
# ============================================
with st.sidebar:
    # Title (NO logos)
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">📊</div>
        <div style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">Text Analyzer</div>
        <div style="font-size: 0.8rem; color: #6c757d;">Pro Edition</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistics Dashboard
    st.markdown("""
    <div style="font-size: 0.9rem; font-weight: 600; color: #1a1a2e; margin-bottom: 0.5rem;">
        Dashboard
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="sidebar-stat">
            <div class="sidebar-stat-value">{st.session_state.total_analyses}</div>
            <div class="sidebar-stat-label">Total Analyses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="sidebar-stat">
            <div class="sidebar-stat-value">{len(st.session_state.history)}</div>
            <div class="sidebar-stat-label">Saved History</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats (if history exists)
    if st.session_state.history:
        total_words = sum(h.get('words', 0) for h in st.session_state.history)
        avg_words = total_words // len(st.session_state.history) if st.session_state.history else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 0.8rem; border-radius: 8px; text-align: center; border: 1px solid #e9ecef;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">{total_words}</div>
                <div style="font-size: 0.7rem; color: #6c757d;">Total Words</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 0.8rem; border-radius: 8px; text-align: center; border: 1px solid #e9ecef;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e;">{avg_words}</div>
                <div style="font-size: 0.7rem; color: #6c757d;">Avg Words</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About section
    st.markdown("""
    <div style="font-size: 0.9rem; font-weight: 600; color: #1a1a2e; margin-bottom: 0.5rem;">
        About
    </div>
    <div style="font-size: 0.85rem; color: #495057; line-height: 1.6;">
        Text Analyzer Pro provides instant, detailed statistics about any text using pure Python NLP techniques.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    st.markdown("""
    <div style="font-size: 0.85rem; color: #495057;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.3rem 0;">
            <span>📝</span> Word & Character Count
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.3rem 0;">
            <span>📄</span> Sentence & Paragraph Analysis
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.3rem 0;">
            <span>💭</span> Sentiment Detection
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.3rem 0;">
            <span>⏱️</span> Reading Time Estimation
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.3rem 0;">
            <span>📊</span> Text Complexity Scoring
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.3rem 0;">
            <span>🔥</span> Most Common Words
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tips
    st.markdown("""
    <div style="font-size: 0.9rem; font-weight: 600; color: #1a1a2e; margin-bottom: 0.5rem;">
        Tips
    </div>
    <div style="font-size: 0.8rem; color: #6c757d; line-height: 1.6;">
        • Longer text = more accurate results<br>
        • Use proper punctuation<br>
        • Try the example texts below
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; font-size: 0.7rem; color: #adb5bd; padding: 0.5rem 0;">
        Version 2.0
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================
st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
    <span style="font-size: 2.5rem;">📊</span>
    <div>
        <div style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">Text Analyzer Pro</div>
        <div style="color: #6c757d; font-size: 1rem;">Get instant, detailed statistics about any text</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Info box (NO AI/keyboard markers)
st.markdown("""
<div class="info-box">
    <strong>Tip:</strong> Paste any text to analyze its structure, complexity, and sentiment.
    All analysis is done locally - no data is sent anywhere.
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Analyze", "History", "About"])

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
        st.markdown("""
        <div style="font-weight: 500; color: #1a1a2e; margin-bottom: 0.5rem;">
            Quick Examples
        </div>
        """, unsafe_allow_html=True)
        
        examples = [
            "The quick brown fox jumps over the lazy dog. This is a classic pangram used to test fonts and typing skills.",
            "I love this product! It's amazing and works perfectly. The customer service was outstanding. Highly recommended!",
            "The weather today is terrible. It's raining heavily and I can't go outside. I'm so disappointed.",
            "Data science is fascinating. It combines statistics, programming, and domain knowledge to extract insights from data."
        ]
        
        selected = st.selectbox(
            "Try one:",
            ["Select..."] + examples,
            key="example_selector",
            label_visibility="collapsed"
        )
        
        if selected != "Select...":
            user_text = selected
            st.session_state.input_text = selected
    
    # Analysis buttons
    col_analyze, col_clear = st.columns([3, 1])
    
    with col_analyze:
        analyze_clicked = st.button("Analyze Text", type="primary", use_container_width=True)
    
    with col_clear:
        if st.button("Clear", use_container_width=True):
            st.session_state.input_text = ""
            st.rerun()
    
    # ============================================
    # ANALYSIS LOGIC
    # ============================================
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
        
        # Reading time
        reading_time = round(word_count / 200, 1)
        
        # Text complexity
        long_words = [w for w in words if len(w) > 6]
        complexity = len(long_words) / len(words) if words else 0
        
        # Sentiment score
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'best', 'love', 'happy', 'awesome', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'sad', 'angry', 'poor', 'disappointed']
        
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        sentiment_score = (pos_count - neg_count) / (pos_count + neg_count + 1) if (pos_count + neg_count + 1) > 0 else 0
        
        if sentiment_score > 0.2:
            sentiment_label = "Positive"
            sentiment_emoji = "😊"
        elif sentiment_score < -0.2:
            sentiment_label = "Negative"
            sentiment_emoji = "😞"
        else:
            sentiment_label = "Neutral"
            sentiment_emoji = "😐"
        
        # Display results
        st.markdown("---")
        st.markdown("### Analysis Results")
        
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
                <div class="metric-value">{reading_time}</div>
                <div class="metric-label">Reading Time (min)</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed statistics
        st.markdown("### Detailed Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span>📝</span>
                    <div>
                        <div style="font-size: 0.8rem; color: #6c757d;">Characters (no spaces)</div>
                        <div style="font-size: 1.5rem; font-weight: 600; color: #1a1a2e;">{char_no_space}</div>
                    </div>
                </div>
            </div>
            <div class="stat-box">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span>📑</span>
                    <div>
                        <div style="font-size: 0.8rem; color: #6c757d;">Paragraphs</div>
                        <div style="font-size: 1.5rem; font-weight: 600; color: #1a1a2e;">{paragraph_count}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span>🔤</span>
                    <div>
                        <div style="font-size: 0.8rem; color: #6c757d;">Unique Words</div>
                        <div style="font-size: 1.5rem; font-weight: 600; color: #1a1a2e;">{unique_words}</div>
                    </div>
                </div>
            </div>
            <div class="stat-box">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span>📏</span>
                    <div>
                        <div style="font-size: 0.8rem; color: #6c757d;">Avg Word Length</div>
                        <div style="font-size: 1.5rem; font-weight: 600; color: #1a1a2e;">{avg_word_len:.2f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-box">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span>{sentiment_emoji}</span>
                    <div>
                        <div style="font-size: 0.8rem; color: #6c757d;">Sentiment</div>
                        <div style="font-size: 1.5rem; font-weight: 600;">{sentiment_label}</div>
                    </div>
                </div>
            </div>
            <div class="stat-box">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span>📊</span>
                    <div>
                        <div style="font-size: 0.8rem; color: #6c757d;">Complexity</div>
                        <div style="font-size: 1.5rem; font-weight: 600; color: #1a1a2e;">{complexity:.1%}</div>
                        <div style="font-size: 0.7rem; color: #6c757d;">Long words > 6 characters</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Most common words
        if most_common:
            st.markdown("### Most Common Words")
            
            words_html = ""
            for word, count in most_common:
                size = 16 + (count * 2)
                words_html += f'<span class="word-item" style="font-size: {size}px;">{word} ({count})</span> '
            
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e9ecef;">
                {words_html}
            </div>
            """, unsafe_allow_html=True)
        
        # Text preview
        with st.expander("Text Preview"):
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1.2rem; border-radius: 10px; border-left: 4px solid #4a90d9;">
                <p style="font-style: italic; margin: 0; color: #1a1a2e;">"{text}"</p>
                <hr style="margin: 0.8rem 0; border-color: #e9ecef;">
                <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.85rem; color: #6c757d;">
                    <span>📝 {word_count} words</span>
                    <span>🔤 {char_count} characters</span>
                    <span>📄 {sentence_count} sentences</span>
                    <span>⏱️ {reading_time} min read</span>
                </div>
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
        
        st.success("✅ Analysis saved to history")
        
    elif analyze_clicked:
        st.warning("Please enter some text to analyze")

with tab2:
    st.markdown("### Analysis History")
    
    if st.session_state.history:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{len(st.session_state.history)}** analyses saved")
        with col2:
            if st.button("Export History", use_container_width=True):
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
                    label="Download",
                    data=history_text,
                    file_name="text_analysis_history.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        st.markdown("---")
        
        for entry in reversed(st.session_state.history):
            sentiment_emoji = "😊" if entry['sentiment'] == "Positive" else "😞" if entry['sentiment'] == "Negative" else "😐"
            
            st.markdown(f"""
            <div class="history-item">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span>{sentiment_emoji}</span>
                        <span style="font-weight: 500; color: #1a1a2e;">"{entry['text']}"</span>
                    </div>
                    <span style="font-size: 0.8rem; color: #6c757d;">{entry['timestamp']}</span>
                </div>
                <div style="display: flex; gap: 1.2rem; flex-wrap: wrap; margin-top: 0.4rem; font-size: 0.8rem; color: #6c757d;">
                    <span>📝 {entry['words']}</span>
                    <span>🔤 {entry['characters']}</span>
                    <span>📄 {entry['sentences']}</span>
                    <span>⏱️ {entry['reading_time']}m</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Clear All History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #6c757d;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📭</div>
            <div style="font-size: 1.1rem;">No analysis history yet</div>
            <div style="font-size: 0.9rem;">Analyze some text in the <strong>Analyze</strong> tab</div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e9ecef;">
            <div style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-bottom: 1rem;">
                Technology
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem; color: #495057;">
                <div><strong>Framework:</strong> Streamlit</div>
                <div><strong>Language:</strong> Python</div>
                <div><strong>Dependencies:</strong> None (pure Python)</div>
                <div><strong>Data:</strong> All local, no external calls</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e9ecef;">
            <div style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-bottom: 1rem;">
                What It Analyzes
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem; color: #495057;">
                <div>📝 Word & Character Count</div>
                <div>📄 Sentence & Paragraph Analysis</div>
                <div>⏱️ Reading Time Estimation</div>
                <div>📊 Text Complexity Scoring</div>
                <div>💭 Sentiment Detection</div>
                <div>🔥 Most Common Words</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e9ecef;">
            <div style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-bottom: 1rem;">
                Why This Project
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem; color: #495057;">
                <div>✅ Zero external dependencies</div>
                <div>✅ Instant deployment</div>
                <div>✅ Fast analysis (milliseconds)</div>
                <div>✅ Clean, professional UI</div>
                <div>✅ Perfect for hackathons</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e9ecef;">
            <div style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; margin-bottom: 1rem;">
                Use Cases
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem; color: #495057;">
                <div>📝 Content writing analysis</div>
                <div>📱 Social media post checking</div>
                <div>📚 Academic text review</div>
                <div>📧 Email analysis</div>
                <div>📝 Blog post optimization</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer (NO AI/keyboard markers)
st.markdown("---")
st.caption("Text Analyzer Pro | Pure Python | No external dependencies")