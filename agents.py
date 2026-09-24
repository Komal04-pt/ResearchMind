import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableLambda
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_mistralai import ChatMistralAI

load_dotenv()

mistral_key = os.getenv("MISTRAL_API_KEY")

# Spaces out Mistral calls to avoid 429 "Rate limit exceeded" errors
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.2,   # 1 call every 5 seconds
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)

# Initialize Mistral AI LLM
llm = ChatMistralAI(
    model="open-mistral-7b",
    api_key=mistral_key,
    max_retries=5,
    rate_limiter=rate_limiter,
)

# 1. Search Agent (real web search, no LLM call)
search_tool = DuckDuckGoSearchResults(max_results=6)


def _run_search(inputs: dict) -> str:
    try:
        return search_tool.invoke(inputs["topic"])
    except Exception as e:
        return f"Search failed: {e}. No web results available."


search_agent = RunnableLambda(_run_search)

# 2. Reader / Scraper Agent Chain
reader_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert reading assistant. Read through gathered information and summarize the core key takeaways clearly. Always keep the source URLs next to the facts they support."),
    ("human", "Extract the most vital points from the research below. Keep the source links:\n\n{research}")
])

reader_agent = reader_prompt | llm | StrOutputParser()

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