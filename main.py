from fastapi import FastAPI
from database.database import engine, Base
from middleware.middleware import add_process_time_header
from routes.v1.students import student_router 
from routes.v1.assignments import assignment_router
from routes.v1.teachers import teacher_router
from routes.v1.comments import comments_router
# Create the database tables
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Student Assignment Submission System", version="1.0.0")

@app.get("/")
def home():
    return {"message": "Hello, Welcome to Student Assignment Submission System"}


app.middleware("http")(add_process_time_header)
app.include_router(student_router, prefix="/api/v1/students", tags=["Students"])
app.include_router(assignment_router, prefix="/api/v1/assignments", tags=["Assignments"])
app.include_router(teacher_router, prefix="/api/v1/teachers", tags=["Teachers"])
app.include_router(comments_router, prefix="/api/v1/comments", tags=["Comments"])