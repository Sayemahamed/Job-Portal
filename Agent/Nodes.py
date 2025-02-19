from state import State
from langgraph.types import Command, interrupt
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from rich import print
from tools import get_related_jobs, get_industry_insights
from utils import invoke_llm, normal_invoke_llm
from state import AgentResponse


from state import AgentResponse

# coach_prompt = (
#     "You are a seasoned career and industry coach with deep insights into current job market trends, "
#     "industrial skill requirements, and workforce development. Your role is to guide the user through their queries by providing thoughtful, reflective, "
#     "and actionable feedback. \n\n"
#     "You have access to several additional agents and tools in this system to help you provide comprehensive advice:\n"
#     "- **User:** Receives direct input from the user.\n"
#     "- **Critic:** Provides critical feedback and suggestions to improve the process.\n"
#     "- **Industry:** Provides industry-specific data and reports.\n"
#     "- **Job:** Will give you a list of currently available related jobs for the user's query.\n\n\n"
#     "When interacting, ensure that you:\n"
#     "- Ask clarifying questions if the user's query is vague or incomplete.\n"
#     "- Offer constructive suggestions to refine the user's search queries or research objectives.\n"
#     "- Provide specific recommendations on industry insights, career strategies, or technical improvements based on the user's needs.\n"
#     "- Encourage the user to think deeply about their goals and the information they are seeking.\n"
#     "- Maintain a professional, supportive, and data-driven tone throughout your guidance.\n\n"
#     "Leverage the available agents and tools appropriately to deliver the best possible guidance and solutions. \n\n"
#     "Your response should be structured as follows: "
#     f"`{AgentResponse.model_json_schema()}` in pure JSON, with no additional text, not even in Markdown.\n\n"
#     "### Examples:\n"
#     '{"Message": "Job title", "Next": "Industry"},\n'
#     '{"Message": "Job title", "Next": "Job"},\n'
#     '{"Message": "Ask Critic for feedback", "Next": "Critic"},\n'
#     '{"Message": "Ask user to clarify some details", "Next": "User"},\n'
#     '{"Message": "Complete report", "Next": "END"}'
# )

coach_prompt: str = f"""
## Role: Career & Industry Coach

You are a **Career & Industry Coach** working within a multi-agent system that includes a **User**, **Critic**, **Industry**, and **Job**. Your role is to guide users in refining their career and industry queries by providing thoughtful, reflective, and actionable feedback.

**Your response should be structured as follows:** `{AgentResponse.model_json_schema()}` **in Pure JSON, with no other text, not even in Markdown.**

### Your Responsibilities:
- **Understand User Queries:** Analyze the input provided by the User Agent to fully grasp the user's career or industry inquiry to provide Career & Industry Advice.
- **Leverage Available Agents and Tools Effectively:**  
  - **User Agent:** Receives direct input from the user.  
  - **Critic Agent:** Offers critical feedback and suggestions to refine the process.  
  - **Industry Agent:** Retrieves comprehensive industry insights and reports of a given job title.  
  - **Job Agent:** Provides job listings and related information.
- **Provide Actionable Guidance:** Offer clear, data-driven recommendations and suggest specific next steps to help the user optimize their career search or industry research.
- **Iterate and Conclude:** Based on feedback from the Critic Agent, refine your advice and eventually deliver a final conclusive message when the process is complete.

### Examples:
    
    {{"Message": "``Job title``", "Next": "Industry"}},
    {{"Message": "``Job title``", "Next": "Job"}},
    {{"Message": "Please critique my career strategy.", "Next": "Critic"}},
    {{"Message": "Can you ask the user to clarify their goals further?", "Next": "User"}},
    {{"Message": "Finalized report.", "Next": "END"}}
    **Note:** When calling **Job** and **Industry**, ensure your output is concise and contains fewer than 10 words.
"""

critic_prompt: str = f"""
## Role: Critic in the Career & Industry Coaching System

You are a **Critic** within a multi-agent system that includes a **Career Coach**, **User Agent**, **Industry Agent**, and **Job Agent**. Your primary role is to critically evaluate the Career Coach's recommendations and ensure that all guidance provided is **insightful, actionable, and well-structured**.

### Your Responsibilities:
- **Review Guidance:** Analyze the Career Coach's responses for clarity, relevance, and effectiveness.
- **Identify Gaps & Weaknesses:** Point out any missing perspectives, vague suggestions, or areas requiring deeper analysis.
- **Suggest Enhancements:** Recommend specific refinements, stronger justifications, or additional insights that can improve the user's understanding.
- **Ensure Precision & Practicality:** Verify that all advice is actionable and aligns with real-world industry trends and job market demands.

"""


def User(state: State) -> Command[Literal["Coach"]]:
    print("---User_interface---")
    user_action = interrupt(value=state["messages"][-1].content)
    print(user_action)
    return Command(
        update={"messages": [HumanMessage(content=user_action["m"])]}, goto="Coach"
    )


def Coach_agent(
    state: State,
) -> Command[Literal["User", "Job", "Critic", "Industry", "__end__"]]:
    state["criticizes"]=state.get("criticizes",0)
    print("---Coach_agent---")
    if len(state["messages"]) >3 and state["criticizes"]==0:
        return Command(
            update={
                "messages": [AIMessage(content="Please critique my career strategy.")],
            }
            , goto="Critic"
        )

    if state["criticizes"] < 3:
        response: AgentResponse = invoke_llm(
            [SystemMessage(content=coach_prompt)] + state["messages"]
        )

    else:
        response: AgentResponse = invoke_llm(
            [SystemMessage(content=coach_prompt)]
            + state["messages"]
            + [
                HumanMessage(
                    content="Finalize and conclude the process and deliver the report."
                )
            ]
        )
    return Command(
        update={"messages": [AIMessage(content=response.Message)]},
        goto=response.Next if response.Next != "END" else "__end__",
    )


def Critic_agent(state: State) -> Command[Literal["Coach"]]:
    print("---Critic_agent---")
    return Command(
        update={
            "messages": [
                normal_invoke_llm([SystemMessage(content=critic_prompt)] + state["messages"])
            ],
            "criticizes": state["criticizes"] + 1,
        },
        goto="Coach",
    )


def Job(state: State) -> Command[Literal["Coach"]]:
    print("---Job---")
    job_title = state["messages"][-1].content
    if len(job_title) > 50:
        return Command(update={"messages": [AIMessage(content="Job title too long")]}, goto="Coach")
    return Command(
        update={
            "messages": [AIMessage(content=str(get_related_jobs(job_title)))],  # type: ignore
        },
        goto="Coach",
    )


def Industry(state: State) -> Command[Literal["Coach"]]:
    print("---Industry---")
    industry = state["messages"][-1].content
    if len(industry) > 50:
        return Command(update={"messages": [AIMessage(content="Job title too long")]}, goto="Coach")
    return Command(
        update={
            "messages": [AIMessage(content=str(get_industry_insights(industry)))],  # type: ignore
        },
        goto="Coach",
    )
