from crewai import Agent
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()


def create_assistant_agent():
    return Agent(
        role="Customer Support Assistant",
        goal=(
            "Answer the customer's question clearly and accurately "
            "using your own knowledge."
        ),
        backstory=(
            "You are an experienced customer support assistant. "
            "You provide helpful, professional and easy-to-understand "
            "answers to customer questions."
        ),
        verbose=True
    )


def create_web_search_agent():
    return Agent(
        role="Web Search Customer Support Assistant",
        goal=(
            "Research the customer's question using web search and "
            "provide an accurate, up-to-date answer."
        ),
        backstory=(
            "You are a research-oriented customer support specialist. "
            "When a question requires current or external information, "
            "you find relevant information from the web and summarize it "
            "clearly for the customer."
        ),
        tools=[search_tool],
        verbose=True
    )


def create_entry_agent():
    return Agent(
        role="Customer Support Entry Agent",
        goal=(
            "Collect the customer query and the responses produced by "
            "the other support agents and prepare them for recording."
        ),
        backstory=(
            "You are responsible for maintaining customer support records. "
            "You organize the customer query and agent responses into a "
            "clear format suitable for saving."
        ),
        verbose=True
    )
