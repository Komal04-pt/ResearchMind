import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableLambda
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent

from tools import web_search, scrape_url

load_dotenv()

try:
    mistral_key = st.secrets.get("MISTRAL_API_KEY")
except Exception:
    mistral_key = None
mistral_key = mistral_key or os.getenv("MISTRAL_API_KEY")

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.2,
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)

llm = ChatMistralAI(
    model="open-mistral-7b",
    api_key=mistral_key,
    max_retries=5,
    rate_limiter=rate_limiter,
)

# 1. Search Agent
search_executor = create_agent(
    model=llm,
    tools=[web_search],
    system_prompt="You are a research assistant. Use the web_search tool to find recent, reliable information on the given topic. Call the tool as many times as needed with focused queries, then return the raw titles, URLs and snippets you gathered. Do not summarize yet, just collect the sources.",
)


def _run_search(inputs: dict) -> str:
    try:
        result = search_executor.invoke(
            {"messages": [("user", f"Research this topic: {inputs['topic']}")]}
        )
        return result["messages"][-1].content
    except Exception as e:
        return f"Search failed: {e}. No web results available."


search_agent = RunnableLambda(_run_search)

# 2. Reader Agent
reader_executor = create_agent(
    model=llm,
    tools=[scrape_url],
    system_prompt="You are an expert reading assistant. You are given raw search results (titles, URLs, snippets). Use the scrape_url tool to open the most relevant URLs and read their full content, then summarize the core key takeaways clearly. Always keep the source URLs next to the facts they support.",
)


def _run_reader(inputs: dict) -> str:
    try:
        result = reader_executor.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Read the URLs below in more depth and extract the most vital points. Keep the source links:\n\n{inputs['research']}",
                    )
                ]
            }
        )
        return result["messages"][-1].content
    except Exception as e:
        return f"Reading failed: {e}. Using raw search results only."


reader_agent = RunnableLambda(_run_reader)

# 3. Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured, and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 2 well-explained points)
- Conclusion
- Sources (list relevant sources)

Be detailed, factual and professional.
Only cite URLs that appear in the research provided. Do not invent sources."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# 4. Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in the exact format:

Score: X/10

Strengths:
- ...
- ...

Area to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()