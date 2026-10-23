import streamlit as st

from crew.crew import run_customer_support


st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        .stApp {
            background: #f7f9fc;
        }

        .main-header {
            background: linear-gradient(135deg, #1f2937, #374151);
            padding: 28px 35px;
            border-radius: 18px;
            margin-bottom: 25px;
            color: white;
        }

        .main-header h1 {
            margin: 0;
            font-size: 34px;
            font-weight: 700;
        }

        .main-header p {
            margin-top: 8px;
            font-size: 16px;
            color: #d1d5db;
        }

        .agent-card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #e5e7eb;
            min-height: 120px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.04);
            text-align: center;
        }

        .agent-icon {
            font-size: 38px;
            margin-bottom: 10px;
        }

        .agent-card p {
            color: #6b7280;
            font-size: 14px;
            margin: 0;
        }

        div[data-testid="stAlert"] {
            border-radius: 10px;
        }

        section[data-testid="stSidebar"] {
            background: #111827;
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        .response-icon {
            font-size: 36px;
            margin-top: 18px;
            margin-bottom: 4px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("<h2>🤖 AI Support</h2><p>Multi-Agent Customer Support System</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### ⚙️ Workflow")
    st.markdown(
        """
        * 💬 Assistant tries first.
        * 🌐 Web search is used only when required.
        * 📝 Entry agent records the interaction.
        """
    )
    st.divider()
    st.markdown("### 🧠 Technology")
    st.markdown(
        """
        - CrewAI
        - Streamlit
        - Web Search
        - Python
        - LLM
        """
    )


st.markdown(
    """
    <div class="main-header">
        <h1>🤖 AI Customer Support</h1>
        <p>Intelligent customer support using a conditional multi-agent CrewAI workflow.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">💬</div>
            <p>Knowledge-based response</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">🌐</div>
            <p>Web-based research</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-icon">📝</div>
            <p>Support record</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)
st.subheader("💬 Ask Customer Support")

query = st.text_area(
    "Customer Query",
    placeholder="Example: How can I reset my password?",
    height=130,
)


if st.button("🚀 Get Support", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a customer question.")
    else:
        with st.spinner("AI support agents are processing your question..."):
            result = run_customer_support(query)

        st.success("Customer support processing completed.")
        st.divider()

        st.markdown("<div class='response-icon'>💬</div>", unsafe_allow_html=True)
        assistant_answer = str(result.get("assistant_answer", ""))
        if "NEED_WEB_SEARCH" in assistant_answer.upper():
            st.write("The Assistant could not confidently answer. Web search was triggered.")
        else:
            st.write(assistant_answer)

        st.markdown("<div class='response-icon'>🌐</div>", unsafe_allow_html=True)
        web_search_answer = str(result.get("web_search_answer", ""))
        if web_search_answer.strip():
            st.write(web_search_answer)
        else:
            st.write("Web search was not required.")

        st.markdown("<div class='response-icon'>📝</div>", unsafe_allow_html=True)
        st.write("Support interaction saved to answers.txt.")

