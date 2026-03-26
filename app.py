"""Streamlit UI for ET AI Concierge - Multi-Agent System."""

import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.orchestrator import ConciergeOrchestrator

# Page configuration
st.set_page_config(
    page_title="ET AI Concierge",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .confidence-high {
        color: #28a745;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .response-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        border: 1px solid #dee2e6;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "concierge" not in st.session_state:
    st.session_state.concierge = ConciergeOrchestrator()

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">🎯 ET AI Concierge</h1>
    <p style="color: white; margin: 0; opacity: 0.9;">Your personal guide to everything ET</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - User Profile
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    st.markdown("Tell us about yourself for personalized recommendations")
    
    age = st.number_input("Age", min_value=18, max_value=100, value=28)
    income = st.number_input("Monthly Income (₹)", min_value=0, value=80000, step=10000)
    
    risk_profile = st.select_slider(
        "Risk Profile",
        options=["conservative", "moderate", "aggressive"],
        value="moderate"
    )
    
    interests = st.multiselect(
        "Interests",
        ["Investing", "Technology", "Career Growth", "Entrepreneurship", "Personal Finance"],
        default=["Investing", "Career Growth"]
    )
    
    career_goal = st.selectbox(
        "Career Goal",
        ["career_growth", "investment_learning", "entrepreneurship"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🤖 AI Agents")
    st.markdown("""
    <div class="agent-card">
        📈 <strong>Markets Agent</strong><br>
        Investment & Financial Planning
    </div>
    <div class="agent-card">
        📚 <strong>Masterclass Agent</strong><br>
        Courses & Learning
    </div>
    <div class="agent-card">
        📰 <strong>ET Prime Agent</strong><br>
        Premium Content
    </div>
    <div class="agent-card">
        🎯 <strong>Events Agent</strong><br>
        Events & Networking
    </div>
    <div class="agent-card">
        💳 <strong>Services Agent</strong><br>
        Financial Products
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Quick Examples")
    if st.button("💰 Investment Advice"):
        st.session_state.example_query = "I want to start investing ₹50,000 monthly"
    if st.button("📚 Career Growth"):
        st.session_state.example_query = "I want to grow my career and learn new skills"
    if st.button("🎯 Events"):
        st.session_state.example_query = "What events are happening?"
    if st.button("📰 Content"):
        st.session_state.example_query = "Show me interesting articles to read"

# Main chat area
st.markdown("### 💬 Chat with your AI Concierge")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# User input
user_context = {
    "age": age,
    "income": income,
    "risk_profile": risk_profile,
    "interests": [i.lower() for i in interests],
    "career_goal": career_goal
}

# Handle example query from sidebar
if "example_query" in st.session_state:
    query = st.session_state.example_query
    del st.session_state.example_query
else:
    query = st.chat_input("Ask me anything about investments, courses, events, or financial products...")

# Process query
if query:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").write(query)
    
    # Show thinking indicator
    with st.chat_message("assistant"):
        with st.spinner("🤔 Agents are discussing your request..."):
            # Get response from orchestrator
            response = st.session_state.concierge.process(query, user_context)
        
        st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("""
<p style="text-align: center; color: #6c757d; font-size: 0.8rem;">
    Powered by 5 specialized AI agents working together | ET AI Concierge
</p>
""", unsafe_allow_html=True)
