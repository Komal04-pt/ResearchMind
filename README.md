# 🧠 ResearchMind — Multi-Agent AI Research Team

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-ResearchMind-indigo?style=for-the-badge)](https://researchmind-fqmakjd4qczxteit3fyzzx.streamlit.app/)

👉 **Live Application:** [https://researchmind-fqmakjd4qczxteit3fyzzx.streamlit.app/](https://researchmind-fqmakjd4qczxteit3fyzzx.streamlit.app/)

**ResearchMind** is an automated, multi-agent AI research workspace built with Python and Streamlit. It orchestrates a team of specialized AI agents working together in a sequential pipeline to search, analyze, draft, and critique comprehensive research reports on any topic in real time.

---

## ✨ Features

- **Multi-Agent Orchestration:**
  - 🔍 **Search Agent:** Scours web sources to gather real-time data and relevant research content.
  - 📖 **Reader Agent:** Processes raw search data and extracts core facts and structured summaries.
  - ✍️ **Writer Agent:** Synthesizes facts and drafts a comprehensive, well-structured research report.
  - 🧐 **Critic Agent:** Conducts a thorough review evaluating quality, gaps, and potential improvements.
- **Real-Time Interactive UI:** Custom-styled Streamlit interface featuring dynamic progress cards, live status badges, and step execution timings.
- **Performance Metrics:** Tracks individual agent execution time and word counts for the generated report.
- **Exportable Reports:** Download fully formatted Markdown research reports with a single click.

---

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Frontend / Dashboard:** Streamlit, Custom CSS
- **Agent Framework:** LangChain / LangGraph (Custom Agent Pipeline)
- **Search & Tools:** Web Search Integration (`tools.py`)

---

## 📁 Project Structure

```text
.
├── .gitignore
├── README.md             # Project documentation
├── agents.py             # Agent definitions & logic
├── app.py                # Main Streamlit application UI
├── config.py             # Application & API configurations
├── favicon.png           # Application icon
├── pipeline.py           # Multi-agent execution pipeline
├── requirements.txt      # Python dependencies
└── tools.py              # External tools & search helpers

```
🚀 Getting Started
1. Clone the Repository
git clone https://github.com/Komal04-pt/ResearchMind.git
cd ResearchMind

3. Set Up Virtual Environment

python -m venv .venv
Activate Environment:

Windows:
DOS
.venv\Scripts\activate
macOS / Linux:

source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Up Environment Variables
Create a .env file in the root directory and add your required API keys:

Code snippet
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key

5. Run the Application
streamlit run app.py

📸 How It Works
Input Topic: Enter any research query or choose from suggested example topics.
Pipeline Execution: Watch the 4 agents complete their designated tasks in sequence (pipeline.py).
Review Output: View the final report, critic evaluation, reader summary, and raw search results across structured tabs.
Download: Export the complete report including critic notes as a .md file.
