from pydantic import BaseModel
from typing import Literal
from langgraph.graph.message import MessagesState


class AgentResponse(BaseModel):
    Message: str
    Next: Literal["User", "Job", "Critic", "Industry", "END"]


class State(MessagesState):
    criticizes: int
