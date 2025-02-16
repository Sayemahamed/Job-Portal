from pydantic import BaseModel
from typing import Literal
from langgraph.graph.message import MessagesState


class AgentResponse(BaseModel):
    Message: str
    Next: Literal["User", "Job", "Critic", "Industry", "END", "Coach"]


class State(MessagesState):
    criticizes: int
