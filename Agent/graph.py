from Nodes import Coach_agent, User, Critic_agent, Industry, Job
from langgraph.store.postgres import PostgresStore
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, START, END
from state import State
from langchain_core.runnables.config import RunnableConfig


checkpointer = PostgresSaver.from_conn_string(
    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)
store = PostgresStore.from_conn_string(
    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)

builder = StateGraph(State)

builder.add_node("Coach", Coach_agent)
builder.add_node("Critic", Critic_agent)
builder.add_node("User", User)
builder.add_node("Industry", Industry)
builder.add_node("Job", Job)

builder.add_edge(START, "Coach")
# builder.add_edge("Coach", END)

graph = builder.compile(checkpointer=checkpointer, store=store)

config = RunnableConfig(configurable={"thread_id": "thread_id", "user_id": "user_id"})


# initial_input = {"user_query": "Find me a job in AI research."}
# result = graph.invoke(initial_input, config=config)

# print(result)
