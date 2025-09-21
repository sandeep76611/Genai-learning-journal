from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text

# Database
DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


app = FastAPI(title="Books Management API")


class SQLQuery(BaseModel):
    query: str

@app.post("/run-sql/")
def run_sql(sql: SQLQuery):
    try:
        with engine.begin() as conn:
            result = conn.execute(text(sql.query))
            
            try:
                rows = result.mappings().all()
                return {"status": "success", "rows": rows}
            except Exception:
                pass

        # Give a friendly message depending on the query
        q = sql.query.strip().lower()
        if q.startswith("insert"):
            message = "Inserted successfully"
        elif q.startswith("create"):
            message = "Table created successfully"
        elif q.startswith("update"):
            message = "Updated successfully"
        elif q.startswith("delete"):
            message = "Deleted successfully"
        elif q.startswith("drop"):
            message = "Table dropped successfully"
        else:
            message = "Query executed successfully"

        return {"status": "success", "message": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
