from crewai import Task


def create_assistant_task(agent, query):
    return Task(
        description=(
            f"Answer the following customer question using only your "
            f"existing knowledge:\n\n"
            f"{query}\n\n"
            "If you know the answer, provide a clear and accurate answer.\n"
            "If you do not know the answer or cannot answer confidently, "
            "return exactly: NEED_WEB_SEARCH"
        ),
        expected_output=(
            "Either a clear answer to the customer's question, or exactly "
            "NEED_WEB_SEARCH if you do not know the answer."
        ),
        agent=agent,
    )


def needs_web_search(output):
    text = output.raw if hasattr(output, "raw") else str(output)
    return "NEED_WEB_SEARCH" in text.upper()


def create_web_search_task(agent, query):
    return Task(
        description=(
            f"The Assistant Agent could not confidently answer the "
            f"following customer question:\n\n"
            f"{query}\n\n"
            "Use the web search tool to research the question. "
            "Provide an accurate and useful answer based on the "
            "information you find."
        ),
        expected_output="A clear and accurate answer based on web search.",
        agent=agent,
    )


def create_entry_task(agent, query, assistant_answer, web_search_answer):
    final_answer = (
        assistant_answer
        if assistant_answer and not needs_web_search(assistant_answer)
        else web_search_answer
    )

    return Task(
        description=(
            "Create the final customer support record.\n\n"
            f"Customer Query:\n{query}\n\n"
            "Assistant Agent Response:\n"
            f"{assistant_answer}\n\n"
            "Web Search Assistant Response:\n"
            f"{web_search_answer}\n\n"
            "Use the assistant answer if it is valid; otherwise use "
            "the web search answer.\n\n"
            f"Final customer response to use:\n{final_answer}"
        ),
        expected_output=(
            "A customer support record containing the query and the appropriate answer."
        ),
        agent=agent,
    )
