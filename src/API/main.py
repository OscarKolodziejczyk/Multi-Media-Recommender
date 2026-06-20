from fastapi import FastAPI, HTTPException
import uvicorn

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

app = FastAPI(title="MultiMediaRecommender")

load_dotenv()

# Load our env variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Create Database Engine
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

@app.get("/")
def read_root():
    return {"Status": "FastAPI server live"}

@app.get("/recommend/{title}")
def get_recommendations(title: str):

    # 1. Open connection to PostgreSQL

    try:
        with engine.connect() as conn:

            query = text("""
            WITH TargetMedia AS (
                -- 1. Find the target vector from whichever table holds the requested title
                SELECT embedding FROM Movies WHERE "Title" = :search_title
                UNION ALL
                SELECT embedding FROM Books WHERE "Title" = :search_title
                UNION ALL
                SELECT embedding FROM Games WHERE "Title" = :search_title
                LIMIT 1
            )
            (
                SELECT "Title", "Description", "DataType",
                    embedding <=> (SELECT embedding FROM TargetMedia) AS cosine_distance
                FROM Movies
                WHERE "Title" != :search_title
                ORDER BY cosine_distance ASC
                LIMIT 5
            )
            UNION ALL
            (
                SELECT "Title", "Description", "DataType",
                    embedding <=> (SELECT embedding FROM TargetMedia) AS cosine_distance
                FROM Books
                WHERE "Title" != :search_title
                ORDER BY cosine_distance ASC
                LIMIT 5
            )
            UNION ALL 
            (
                SELECT "Title", "Description", "DataType",
                    embedding <=> (SELECT embedding FROM TargetMedia) AS cosine_distance
                FROM Games
                WHERE "Title" != :search_title
                ORDER BY cosine_distance ASC
                LIMIT 5
            );
            """)

            result = conn.execute(query, {"search_title": title}).fetchall()

            if not result or result[0].cosine_distance is None:
                raise HTTPException(status_code=404, detail=f"Title {title} not found")

            recommendations = []
            for row in result:
                recommendations.append({
                    "Title": row.Title,
                    "Description": row.Description,
                    "DataType": row.DataType,
                    "Match Score": round(float(row.cosine_distance), 3),
                })

            return {"searched_title": title, "recommendations": recommendations}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
