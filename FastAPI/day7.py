from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///./mytestdb.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

app = FastAPI()

class SQLQuery(BaseModel):
    query: str

# # --- 1️ Create Students Table Manually ---
# @app.post("/create-table/")
# def create_table(sql: SQLQuery):
#     try:
#         with engine.begin() as conn:
#             conn.execute(text(sql.query))
#         return {"status": "success", "message": "Table created or altered successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # --- 2️ Insert Student Manually ---
# @app.post("/insert-student/")
# def insert_student(sql: SQLQuery):
#     try:
#         with engine.begin() as conn:
#             conn.execute(text(sql.query))
#         return {"status": "success", "message": "Student inserted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # --- 3️ Get All Students Manually ---
# @app.post("/get-students/")
# def get_students(sql: SQLQuery):
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text(sql.query))
#             rows = result.mappings().all()
#         return {"status": "success", "rows": rows}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # --- 4️ Get Single Student Manually ---
# @app.post("/get-student/")
# def get_student(sql: SQLQuery):
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text(sql.query))
#             row = result.mappings().first()
#             if not row:
#                 raise HTTPException(status_code=404, detail="Student not found")
#         return {"status": "success", "student": row}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # --- 5️ Update Student Manually ---
# @app.post("/update-student/")
# def update_student(sql: SQLQuery):
#     try:
#         with engine.begin() as conn:
#             result = conn.execute(text(sql.query))
#             if result.rowcount == 0:
#                 raise HTTPException(status_code=404, detail="No student updated")
#         return {"status": "success", "message": "Student updated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # --- 6️ Delete Student Manually ---
# @app.post("/delete-student/")
# def delete_student(sql: SQLQuery):
#     try:
#         with engine.begin() as conn:
#             result = conn.execute(text(sql.query))
#             if result.rowcount == 0:
#                 raise HTTPException(status_code=404, detail="No student deleted")
#         return {"status": "success", "message": "Student deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))








@app.post("/run-sql/")
def run_sql(sql: SQLQuery):
    try:
        # For DML (insert/update/delete) use begin() to auto-commit
        with engine.begin() as conn:
            result = conn.execute(text(sql.query))

            # Try fetching rows (SELECT)
            try:
                rows = result.mappings().all()
                return {"status": "success", "rows": rows}
            except Exception:
                # Not a SELECT → no rows
                return {"status": "success", "message": "Query executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
