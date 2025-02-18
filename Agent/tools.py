import psycopg
from rich import print
from sqlmodel import SQLModel, Session, select, Field, create_engine, distinct
from tavily import TavilyClient
import requests
import os
from urllib.parse import urlparse
import tempfile

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
    info_title: str = Field(default=None)
    content: str = Field(default=None, nullable=True)



def get_industry_insights(query: str):
    search_results = tavily.search(
        query=f"{query} (filetype:pdf OR filetype:doc OR filetype:md OR filetype:docx OR filetype:pptx OR filetype:csv) (site:.edu OR site:.org OR site:.net OR site:.biz)",
        search_depth="advanced",
        max_results=4,
        include_links=True,
        include_answer=False,
        include_raw_content=False,
    )
    
    # Extract the URL and title from the search results
    output = [{"url": each["url"], "title": each["title"]} for each in search_results.get("results", [])]
    ans=[]
    # Create a temporary directory for file downloads
    with tempfile.TemporaryDirectory() as temp_dir:
        # Open a database session
        with Session(engine) as session:
            for item in output:
                # Check if the URL already exists in the Information table
                statement = select(Information).where(Information.info_link == item["url"])
                existing = session.exec(statement).first()
                
                if not existing:
                    try:
                        # Download the file from the URL
                        response = requests.get(item["url"])
                        if response.status_code == 200:
                            # Extract a filename from the URL; generate one if not available
                            parsed = urlparse(item["url"])
                            filename = os.path.basename(parsed.path)
                            if not filename:
                                filename = f"downloaded_{hash(item['url'])}.dat"
                            
                            file_path = os.path.join(temp_dir, filename)
                            
                            # Save the downloaded file
                            with open(file_path, "wb") as f:
                                f.write(response.content)
                            print(f"Downloaded file saved as: {file_path}")
                            
                            # Post the file to the conversion service using a curl-like request
                            convert_url = "http://localhost:8003/convert"
                            with open(file_path, "rb") as file_to_upload:
                                files = {"file": file_to_upload}
                                post_response = requests.post(convert_url, files=files)
                            
                            # Capture the conversion response (assumed to be text)
                            conv_text = post_response.text
                            print(f"Conversion response for {filename}: {post_response.status_code} {conv_text}")
                            
                            # Create a new record with the conversion response stored in 'content'
                            new_info = Information(
                                info_link=item["url"],
                                info_title=item["title"],
                                content=conv_text
                            )
                            ans.append({ "info_title": item["title"], "content": conv_text[500:]})
                            session.add(new_info)
                        else:
                            print(f"Failed to download file from {item['url']}. Status code: {response.status_code}")
                    except Exception as e:
                        print(f"Error processing {item['url']}: {e}")
                else:
                    ans.append({ "info_title": item["title"], "content": existing.content[500:]})
            # Commit all changes to the database
            session.commit()
    return ans

# Example usage:

if __name__ == "__main__":
    related_jobs = get_related_jobs("gen")
    print(related_jobs)

    temp=get_industry_insights("Nursing")

    print(temp)
    
