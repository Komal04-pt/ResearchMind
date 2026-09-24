# 🧠 ResearchMind — Multi-Agent AI Research Team

**ResearchMind** is an automated, multi-agent AI research workspace built with Python and Streamlit. It orchestrates a team of specialized AI agents working together in a sequential pipeline to search, analyze, draft, and critique comprehensive research reports on any topic in real time.

---

## ✨ Features

* **Multi-Agent Orchestration:**
  * 🔍 **Search Agent:** Scours web sources to gather real-time data and relevant research content.
  * 📖 **Reader Agent:** Processes raw search data and extracts core facts and structured summaries.
  * ✍️ **Writer Agent:** Synthesizes facts and drafts a comprehensive, well-structured research report.
  * 🧐 **Critic Agent:** Conducts a thorough review evaluating quality, gaps, and potential improvements.
* **Real-Time Interactive UI:** Custom-styled Streamlit interface featuring dynamic progress cards, live status badges, and step execution timings.
* **Performance Metrics:** Tracks individual agent execution time and word counts for the generated report.
* **Exportable Reports:** Download fully formatted Markdown research reports with a single click.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Frontend / Dashboard:** Streamlit, Custom CSS
* **Agent Framework:** LangChain / LangGraph (Custom Agent Chains)
* **API Dependencies:** Search & LLM APIs (via `agents` module)

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed on your machine:

2. Clone the Repository
Bash
git clone [https://github.com/your-username/ResearchMind.git](https://github.com/your-username/ResearchMind.git)
cd ResearchMind
3. Install Dependencies
Create a virtual environment (optional but recommended) and install the required Python packages:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the root directory and add your required API keys (e.g., OpenAI, Tavily, Google Search APIs depending on your agents.py setup):

Code snippet
MISTRAL_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
5. Run the Application
Bash
streamlit run app.py

📂 Project Structure
├── .gitignore
├── README.md             # Project documentation
├── agents.py             # Agent definitions & logic
├── app.py                # Main Streamlit application UI
├── config.py             # Application & API configurations
├── favicon.png           # Application icon
├── pipeline.py           # Multi-agent execution pipeline
├── requirements.txt      # Python dependencies
└── tools.py              # External tools & search helpers

📸 How It Works
Input Topic: Enter any query or choose from suggested example topics.

Pipeline Execution: Watch the 4 agents complete their designated tasks in sequence.

Review Output: View the final report, critic evaluation, reader summary, and raw search results across structured tabs.

Download: Export the entire report including critic notes as a .md file.
