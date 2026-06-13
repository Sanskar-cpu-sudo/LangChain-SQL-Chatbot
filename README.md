# 🦜 LangChain SQL Chatbot

A Streamlit-based AI chatbot that allows users to interact with SQL databases using natural language. The application uses LangChain, Groq LLMs, and SQL toolkits to convert user questions into SQL queries and retrieve results from SQLite or MySQL databases.

## Features

* Chat with databases using plain English.
* Supports SQLite databases.
* Supports MySQL databases.
* Uses Groq LLM for fast inference.
* Automatically inspects database schema before querying.
* Streamlit-based interactive UI.
* Chat history support.
* Secure API key input.

## Tech Stack

* Python
* Streamlit
* LangChain
* Groq
* SQLAlchemy
* SQLite
* MySQL

## Project Structure

```
LangChain-SQL-Chatbot/
│
├── app.py
├── student.db
├── requirements.txt
├── .gitignore
├── README.md
└── screenshots/
    └── demo.png
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/LangChain-SQL-Chatbot.git
cd LangChain-SQL-Chatbot
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

## Configuration

### Groq API Key

Enter your Groq API key in the sidebar.

Get one from:

https://console.groq.com

### SQLite

Place your SQLite database file (`student.db`) in the project directory.

### MySQL

Provide:

* Host
* Username
* Password
* Database Name

through the sidebar interface.

## Example Questions

* How many students are in the database?
* Show all student names.
* List students with marks above 80.
* What are the available tables?
* Show schema of the student table.

## Future Improvements

* PostgreSQL Support
* Export Query Results to CSV
* Authentication System
* Query History
* Data Visualization
* Multi-Database Connections

## License

MIT License

## Author

Developed using LangChain, Groq, Streamlit, and SQLAlchemy.
