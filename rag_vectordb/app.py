import streamlit as st
import requests
import time

# --------------------------------
# CONFIG
# --------------------------------
API_URL = "http://localhost:8000/ask"

st.set_page_config(
    page_title="Science RAG (KG + Vector)",
    layout="wide"
)

st.title("📘 10th Std Science – Hybrid RAG Chatbot")
st.caption("Knowledge Graph + Vector DB + Corrective RAG")

# --------------------------------
# SESSION STATE
# --------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "query" not in st.session_state:
    st.session_state.query = ""

# --------------------------------
# SIDEBAR CONTROLS
# --------------------------------
st.sidebar.header("⚙️ Controls")

allow_web = st.sidebar.checkbox(
    "Allow Web Search (DuckDuckGo)",
    value=False
)

show_route = st.sidebar.checkbox(
    "Show routing info",
    value=True
)

clear_chat = st.sidebar.button("🧹 Clear Chat")

if clear_chat:
    st.session_state.history = []
    st.rerun()

# --------------------------------
# INPUT AREA
# --------------------------------
st.markdown("### Ask a Science Question")

query = st.text_input(
    "Your question",
    key="query",
    placeholder="e.g. What is the formula of rusting of iron?"
)

ask_btn = st.button("Ask")

# --------------------------------
# HANDLE ASK
# --------------------------------
if ask_btn and query.strip():

    start_time = time.time()

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                API_URL,
                json={
                    "query": query,
                    "allow_web": allow_web
                },
                timeout=120
            ).json()
        except Exception as e:
            st.error(f"API Error: {e}")
            st.stop()

    elapsed = round(time.time() - start_time, 2)

    answer = response.get("answer", "")
    route = response.get("route", "UNKNOWN")

    # Save to history
    st.session_state.history.append({
        "question": query,
        "answer": answer,
        "route": route,
        "time": elapsed
    })

    # Note: Can't clear st.session_state.query directly as it's bound to text_input
    # User will need to clear manually or use st.experimental_rerun()

# --------------------------------
# CHAT HISTORY
# --------------------------------
st.markdown("---")
st.markdown("### 💬 Conversation")

for chat in reversed(st.session_state.history):
    st.markdown(f"**🧑 Question:** {chat['question']}")
    st.markdown(f"**🤖 Answer:** {chat['answer']}")

    if show_route:
        st.caption(
            f"Route: `{chat['route']}` | ⏱ {chat['time']} sec"
        )

    st.markdown("---")

# --------------------------------
# FOOTER
# --------------------------------
st.caption(
    "Routes: KG = Knowledge Graph | VECTOR = Textbook | HYBRID = KG + Vector | WEB = DuckDuckGo"
)
