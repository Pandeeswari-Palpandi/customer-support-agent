from pathlib import Path

from crewai import Crew, Process

from crew.agents import (
    create_assistant_agent,
    create_entry_agent,
    create_web_search_agent,
)
from crew.tasks import (
    create_assistant_task,
    create_entry_task,
    create_web_search_task,
    needs_web_search,
)


def _get_task_output(result, index):
    tasks_output = getattr(result, "tasks_output", [])
    if index < len(tasks_output):
        task_output = tasks_output[index]
        return getattr(task_output, "raw", str(task_output))
    return str(result)


def run_customer_support(query):
    assistant_agent = create_assistant_agent()
    web_search_agent = create_web_search_agent()
    entry_agent = create_entry_agent()

    assistant_task = create_assistant_task(assistant_agent, query)
    assistant_crew = Crew(
        agents=[assistant_agent],
        tasks=[assistant_task],
        process=Process.sequential,
        verbose=True,
    )
    assistant_result = assistant_crew.kickoff()
    assistant_answer = _get_task_output(assistant_result, 0)

    web_search_answer = ""
    if needs_web_search(assistant_answer):
        web_search_task = create_web_search_task(web_search_agent, query)
        web_search_crew = Crew(
            agents=[web_search_agent],
            tasks=[web_search_task],
            process=Process.sequential,
            verbose=True,
        )
        web_search_result = web_search_crew.kickoff()
        web_search_answer = _get_task_output(web_search_result, 0)

    final_answer = (
        assistant_answer if not needs_web_search(assistant_answer) else web_search_answer
    )

    entry_task = create_entry_task(
        entry_agent,
        query,
        assistant_answer,
        web_search_answer,
    )
    entry_crew = Crew(
        agents=[entry_agent],
        tasks=[entry_task],
        process=Process.sequential,
        verbose=True,
    )
    entry_result = entry_crew.kickoff()
    entry_answer = _get_task_output(entry_result, 0)

    output_file = Path("answers.txt")
    with output_file.open("a", encoding="utf-8") as file:
        file.write("\n" + "=" * 80 + "\n")
        file.write("CUSTOMER SUPPORT RECORD\n")
        file.write("=" * 80 + "\n\n")
        file.write(f"Customer Query:\n{query}\n\n")
        file.write(f"Assistant Answer:\n{assistant_answer}\n\n")
        file.write(f"Web Search Answer:\n{web_search_answer}\n\n")
        file.write(f"Entry Agent Record:\n{entry_answer}\n")

    return {
        "assistant_answer": assistant_answer,
        "web_search_answer": web_search_answer,
        "entry_answer": entry_answer,
        "final_answer": final_answer,
    }
