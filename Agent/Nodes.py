from state import State
from langgraph.types import Command, interrupt
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from rich import print
from utils import invoke_llm,normal_invoke_llm,execute_sql
from state import AgentResponse

execute_sql("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'job'")
def User(state: State) -> Command[Literal["Coach"]]:
    print("---User_interface---")
    user_action = interrupt(value=state["messages"][-1].content)
    return Command(
        update={"messages": [HumanMessage(content=user_action)]}, goto="Coach"
    )


def Coach_agent(
    state: State,
) -> Command[Literal["User", "Job", "Critic", "Industry", "END"]]:
    print("---Coach_agent---")
    if state["criticizes"] < 2:
        response: AgentResponse = invoke_llm(
            [SystemMessage(content="")] + state["messages"]
        )

    else:
        response: AgentResponse = invoke_llm(
            [SystemMessage(content="")]
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
            "messages": [normal_invoke_llm([SystemMessage(content="")] + state["messages"])],
            "criticizes": state["criticizes"] + 1,
        },
        goto="Coach",
    )

def Job(state: State) -> Command[Literal["Coach"]]:
    print("---Job---")
    pass


def Industry(state: State) -> Command[Literal["Coach"]]:
    print("---Industry---")
    pass