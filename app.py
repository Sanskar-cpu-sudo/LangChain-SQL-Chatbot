import streamlit as st
from pathlib import Path
import sqlite3

from sqlalchemy import create_engine

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent

# =====================================================
# STREAMLIT
# =====================================================

st.set_page_config(
    page_title="LangChain SQL Chat",
    page_icon="🦜"
)

st.title("🦜 Chat With SQL Database")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

options = [
    "Use SQLite Student Database",
    "Connect MySQL Database"
]

selected_option = st.sidebar.radio(
    "Choose Database",
    options
)

# =====================================================
# DATABASE SELECTION
# =====================================================

if options.index(selected_option) == 1:

    db_uri = MYSQL

    mysql_host = st.sidebar.text_input(
        "MySQL Host"
    )

    mysql_user = st.sidebar.text_input(
        "MySQL User"
    )

    mysql_password = st.sidebar.text_input(
        "MySQL Password",
        type="password"
    )

    mysql_db = st.sidebar.text_input(
        "MySQL Database"
    )

else:

    db_uri = LOCALDB

# =====================================================
# GROQ API KEY
# =====================================================

api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password"
)

if not api_key:
    st.stop()

# =====================================================
# LLM
# =====================================================

llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile"
)

# =====================================================
# DATABASE CONFIG
# =====================================================

@st.cache_resource
def configure_db():

    if db_uri == LOCALDB:

        db_path = (
            Path(__file__).parent
            / "student.db"
        ).absolute()

        creator = lambda: sqlite3.connect(
            f"file:{db_path}?mode=ro",
            uri=True
        )

        engine = create_engine(
            "sqlite:///",
            creator=creator
        )

        return SQLDatabase(engine)

    else:

        engine = create_engine(
            f"mysql+mysqlconnector://"
            f"{mysql_user}:"
            f"{mysql_password}@"
            f"{mysql_host}/"
            f"{mysql_db}"
        )

        return SQLDatabase(engine)

db = configure_db()

# =====================================================
# SQL TOOLKIT
# =====================================================

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)

tools = toolkit.get_tools()

# =====================================================
# AGENT
# =====================================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
    You are a SQL assistant.

    Use the provided SQL tools
    to answer database questions.

    Always inspect schema first
    before generating queries.
    """
)

# =====================================================
# CHAT MEMORY
# =====================================================

if (
    "messages" not in st.session_state
    or st.sidebar.button(
        "Clear Chat History"
    )
):
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"How can I help you?"
        }
    ]

# =====================================================
# DISPLAY CHAT
# =====================================================

for msg in st.session_state.messages:

    st.chat_message(
        msg["role"]
    ).write(
        msg["content"]
    )

# =====================================================
# USER INPUT
# =====================================================

user_query = st.chat_input(
    "Ask database questions..."
)

if user_query:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_query
        }
    )

    st.chat_message(
        "user"
    ).write(
        user_query
    )

    with st.chat_message(
        "assistant"
    ):

        response = agent.invoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":user_query
                    }
                ]
            }
        )

        answer = response[
            "messages"
        ][-1].content

        st.write(answer)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )
