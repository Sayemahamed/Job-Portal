from state import State
from langgraph.types import Command, interrupt
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from rich import print
from utils import invoke_llm
from state import AgentResponse

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
        response: AgentResponse =
            invoke_llm( 
                               [SystemMessage(content="")] + state["messages"]
            )
        
    else:
        response: AgentOutput = 
            invoke_llm(
                [SystemMessage(content="")]
                + state["messages"]
                + [
                    HumanMessage(
                        content="Finalize and conclude the process and deliver the report."
                    )
                ]
            )
    return Command(
        update={"messages": [AIMessage(content=response.message)], "pre": "Coach"},
        goto=response.next if response.next != "END" else "__end__",
    )

def Critic_agent(state: State) -> Command[Literal["Coach"]]:
    print("---Critic_agent---")
    response: AgentOutput =invoke_llm(
        [SystemMessage(content=critic_agent_prompt.format())] + state["messages"]
    )
    return Command(
        update={
            "messages": [AIMessage(content=response.message)],
            "criticizes": state["criticizes"] + 1,
            "pre": "Critic",
        },
        goto=response.next,
    )