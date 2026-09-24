from agents import search_agent, reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str):
    print("=" * 80)
    print("Step 1 - Search Agent is working...")
    print("=" * 80)
    search_result = search_agent.invoke({"topic": topic})
    print(search_result)

    print("\n" + "=" * 80)
    print("Step 2 - Reader Agent is processing...")
    print("=" * 80)
    summarized_info = reader_agent.invoke({"research": search_result})
    print(summarized_info)

    print("\n" + "=" * 80)
    print("Step 3 - Writer Agent is drafting the report...")
    print("=" * 80)
    draft_report = writer_chain.invoke({
        "topic": topic,
        "research": summarized_info
    })
    print(draft_report)

    print("\n" + "=" * 80)
    print("Step 4 - Critic Agent is evaluating...")
    print("=" * 80)
    evaluation = critic_chain.invoke({"report": draft_report})
    print(evaluation)

if __name__ == "__main__":
    topic_input = input("\nEnter a research topic: ")
    if topic_input.strip():
        run_research_pipeline(topic_input)
    else:
        print("Topic cannot be empty!")