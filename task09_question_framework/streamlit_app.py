import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="Task 09 Question Generator",
    page_icon=" ",
    layout="wide"
)

# Dark Style
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
.stApp {
    background-color: #0e1117;
}
.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 15px;
    border: 1px solid #2e3440;
}
.big {
    font-size: 28px;
    font-weight: bold;
}
.small {
    color: #9aa0a6;
}
</style>
""", unsafe_allow_html=True)

# Session State
if "previous_context" not in st.session_state:
    st.session_state.previous_context = []

# Header
st.markdown("<div class='big'> Intelligent Question Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='small'>Generate domain-based technical interview questions</div>", unsafe_allow_html=True)
st.write("")

# Sidebar
st.sidebar.title("⚙️ Controls")

domain = st.sidebar.selectbox(
    "Select Domain",
    ["AI/ML", "Python", "DSA", "Web Development", "Database"]
)

difficulty = st.sidebar.selectbox(
    "Select Difficulty",
    ["easy", "medium", "hard"]
)

generate = st.sidebar.button(" Generate Question")

# Stats
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Questions Asked", len(st.session_state.previous_context))

with col2:
    st.metric("Current Domain", domain)

with col3:
    st.metric("Difficulty", difficulty)

st.write("")

# Generate Question
if generate:

    payload = {
        "domain": domain,
        "difficulty": difficulty,
        "previous_context": st.session_state.previous_context
    }

    with st.spinner("Generating smart question..."):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/generate-question",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                data = result["data"]

                st.success("Question Generated Successfully")

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader(" Question ID")
                st.write(data["question_id"])

                st.subheader(" Topic")
                st.write(data["topic"])

                st.subheader(" Type")
                st.write(data["type"])

                st.subheader(" Question")
                st.write(data["question_text"])

                st.markdown("</div>", unsafe_allow_html=True)

                st.session_state.previous_context.append(
                    data["question_text"]
                )

            else:
                st.error("No more matching questions found.")

        except:
            st.error("API server not running. Start FastAPI first.")

# Previous Questions
if st.session_state.previous_context:
    st.write("")
    st.subheader(" Previously Asked Questions")

    for i, q in enumerate(
        st.session_state.previous_context,
        start=1
    ):
        st.markdown(f"{i}. {q}")