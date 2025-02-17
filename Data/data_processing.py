import pandas as pd
import sqlite3

# Read the CSV files
df_skills = pd.read_csv("job_skills.csv")  # Expected columns: job_link, job_skills
df_summary = pd.read_csv("job_summary.csv")  # Expected columns: job_link, job_summary
df_linkedin = pd.read_csv(
    "linkedin_job_postings.csv"
)  # Expected columns: job_link, last_processed_time, got_summary, got_ner, is_being_worked, job_title, company, job_location, first_seen, search_city

# Merge the dataframes on the 'job_link' column
df_merged = pd.merge(df_linkedin, df_summary, on="job_link", how="left")
df_merged = pd.merge(df_merged, df_skills, on="job_link", how="left")

# Select the columns for the Job table
df_job = df_merged[
    ["job_link", "job_title", "company", "job_summary", "job_skills", "job_location"]
]

# Remove rows where job_summary is missing or empty (i.e., jobs without a summary)
df_job = df_job.dropna(subset=["job_summary"])
df_job = df_job[df_job["job_summary"].str.strip() != ""]

# Ensure got_summary is boolean

# Connect to SQLite (or create the database if it doesn't exist)
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Create the Job table with the specified schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Job (
        job_link TEXT PRIMARY KEY,
        job_title TEXT,
        company TEXT,
        job_summary TEXT,
        job_skills TEXT,
        job_location TEXT
    )
""")

# Insert the data into the Job table
df_job.to_sql("Job", conn, if_exists="replace", index=False)

# Commit and close the connection
conn.commit()
conn.close()

print("Data successfully loaded into SQLite database 'jobs.db' in table 'Job'.")
