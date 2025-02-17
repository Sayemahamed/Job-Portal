import psycopg
from regex import T
from rich import print
from sqlmodel import SQLModel, Session, select, Field, create_engine, distinct
from tavily import TavilyClient

tavily = TavilyClient()
engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/postgres")

SQLModel.metadata.create_all(engine)


def get_related_jobs(query: str):
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="postgres",
    )
    with conn.cursor() as cur:
        # Use parameterized query to prevent SQL injection
        cur.execute(
            """
            SELECT job_link, job_title, company, job_summary, job_skills, job_location
            FROM job_name 
            ORDER BY embedding <=> ai.ollama_embed('all-minilm', %s)
            LIMIT 10;
        """,
            (query,),
        )

        results = []
        for row in cur.fetchall():
            results.append(
                {
                    # "job_link": row[0],
                    "job_title": row[1],
                    # "company": row[2],
                    "job_summary": row[3],
                    # "job_skills": row[4],
                    # "job_location": row[5]
                }
            )

        return results


class Information(SQLModel, table=True):
    info_link: str = Field(default=None, primary_key=True)
    content: str = Field(default=None)


def get_industry_insights(query: str):
    urls: list[str] = []
    tavily.search(
        query=query,
        search_depth="advanced",
        max_results=4,
        include_links=True,
        include_answer=True,
        include_raw_content=True,
    )


if __name__ == "__main__":
    related_jobs = get_related_jobs("gen")
    print(related_jobs)
