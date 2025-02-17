from langchain_openai import ChatOpenAI
from state import AgentResponse
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage, FunctionMessage
import json
from rich import print
from firecrawl import FirecrawlApp
from sqlmodel import SQLModel, Session, select, Field, create_engine, distinct
import psycopg

conn = psycopg.connect(
    host="localhost", port=5432, dbname="postgres", user="postgres", password="postgres"
)

# conn.close()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def normal_invoke_llm(prompt: list[AnyMessage]) -> AIMessage:
    return AIMessage(content=llm.invoke(prompt).content)


def invoke_llm(prompt: list[AnyMessage], count: int = 0) -> AgentResponse:
    if count > 2:
        raise Exception("Too many attempts to parse response")
    response: AIMessage = llm.invoke(prompt)  # type: ignore
    print("""-^""" * 80)
    print(prompt)
    print("""-^""" * 80)
    print(response.content)
    print("""-^""" * 80)
    try:
        response_json = json.loads(str(response.content))
        return AgentResponse.model_validate(response_json)
    except Exception as e:
        validation_schema: str = json.dumps(AgentResponse.model_json_schema(), indent=2)
        return invoke_llm(
            [
                AIMessage(content=response.content),
                HumanMessage(
                    content=f"Give the previous response as valid JSON response that strictly matches this schema:\n{validation_schema} Give Only JSON , no other text, not even in Markdown"
                ),
            ],
            count=count + 1,
        )


def execute_sql(sql) -> AIMessage:
    response = []
    with conn.cursor() as cur:
        for row in cur.execute(sql):
            response.append(row)
        return AIMessage(content=str(response))


class Job(SQLModel, table=True):
    job_link: str = Field(default=None, primary_key=True)
    job_title: str = Field(default=None)
    company: str = Field(default=None)
    job_summary: str = Field(default=None)
    job_skills: str = Field(default=None)
    job_location: str = Field(default=None)


engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/postgres")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    statement = select(distinct(Job.job_title)).order_by(Job.job_title)
    results = session.exec(statement)
    count = 0
    for job_title in results:
        # print(job_title)
        count = count + 1
    print(count)

# app = FirecrawlApp()

# response = app.scrape_url(url='https://docs.mendable.ai', params={
# 	'formats': [ 'markdown' ],
# })

if __name__ == "__main__":
    print(execute_sql("SELECT * FROM job LIMIT 10"))
    print(
        execute_sql(
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'job'"
        )
    )
