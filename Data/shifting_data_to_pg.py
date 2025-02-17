import sqlite3
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

# Define the PostgreSQL engine using your connection string
engine: Engine = create_engine(
    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)

# Connect to the SQLite database and load the 'Job' table into a DataFrame
sqlite_conn = sqlite3.connect("jobs.db")
df = pd.read_sql_query("SELECT * FROM Job", sqlite_conn)
sqlite_conn.close()

# Write the DataFrame to PostgreSQL in a table named 'Job'
# if_exists='replace' will drop the existing table if it exists.
df.to_sql("Job", engine, if_exists="replace", index=False)

print("Data migration from SQLite to PostgreSQL completed successfully!")
