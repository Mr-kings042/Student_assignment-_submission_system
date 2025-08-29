# Student Assignment Submission System

## Overview

This project is a backend system for managing student assignment submissions, built with **Python** and the **FastAPI** framework.  

It provides a comprehensive API for:
- **Teachers** to create, comment, and grade assignments.  
- **Students** to submit their work and receive feedback.  

###  Key Features
- **User Roles**: Differentiates between Student and Teacher roles with specific permissions.  
- **Assignment Management**: Teachers can create, update, view, and delete assignments.  
- **Submission Handling**: Students can submit their work for created assignments.  
- **Interactive Feedback**:
  - **Commenting**: Teachers can post comments on assignments to provide feedback.  
  - **Comment Management**: Teachers can update or delete their own comments.  
  - **Likes**: A system for liking comments or assignments is available.  
- **Secure & Validated**: Uses Pydantic for data validation and includes authorization checks to ensure users can only modify their own resources.  

---

##  Technologies Used

- Python **3.10+** (recommended)  
- **FastAPI**, **Uvicorn**  
- **SQLAlchemy**  
- **Pydantic**  
- **PostgreSQL**  
- **python-dotenv**  

### 📂 Project Structure

main.py → FastAPI app factory and router registration
database/database.py → Engine/session setup; Base declarative
middleware/middleware.py → X-Process-Time header middleware

models/
├── students.py
├── teachers.py
├── assignments.py (Assignment, Comment, Like)

schemas/
├── students.py
├── teachers.py
├── assignments.py (Pydantic models)

crud/
├── students.py
├── teachers.py
├── assignment.py
├── comments.py
├── likes.py

routes/v1/
├── students.py
├── teachers.py
├── assignments.py
├── comments.py
├── likes.py

services/
└── assignment.py → File upload and business logic helpers

.gitignore

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Mr-kings042/Student_assignment-_submission_system.git 
cd Student_assignment_submission_system  
```

### 2 Create and activate a virtual environment:

On Windows:
```bash
python -m venv env
.\env\Scripts\activate
 ```
 - On macOS/Linux:
```bash
python3 -m venv env
source env/bin/activate
```
### 3. Install the dependencies: 


```bash
pip install -r requirements.txt 
```


### 4. Configure Environment Variables: Create a .env file in the root directory and add your database connection string and other configuration variables in see(.env.example file).

### 5. Run the server

```bash
uvicorn main:app --reload
```
  The --reload flag makes the server restart after code changes. The API will be available at http://127.0.0.1:8000, and the interactive documentation (Swagger UI) can be accessed at http://127.0.0.1:8000/docs.
  - Docs: http://127.0.0.1:8000/docs
  - Health: GET /
### 6. API Summary



Base URL: http://127.0.0.1:8000

- Routers & Prefixes

   - Students → /api/v1/students
    - Teachers → /api/v1/teachers
    - Assignments → /api/v1/assignments
    - Comments & Likes → /api/v1/comments
  - Routers and prefixes
### 7. API Endpoints
  -- Here are some example endpoints based on the comments CRUD operations
| **Method** | **Endpoint**                 | **Description**                                                |
| ---------- | ---------------------------- | -------------------------------------------------------------- |
| **POST**   | `/assignments/{id}/comments` | Add a new comment to an assignment.                            |
| **GET**    | `/assignments/{id}/comments` | Get all comments for an assignment.                            |
| **GET**    | `/comments/{id}`             | Get a specific comment by its ID.                              |
| **PUT**    | `/comments/{id}`             | Update an existing comment.                                    |
| **DELETE** | `/comments/{id}`             | Delete a comment (only a teacher with teacher\_id can delete). |
  - (The Full API documentation is available at the /docs endpoint when the application is running.)


## License

 MIT License


## Acknowledgments

Built for AltSchool Python Assignments by Okoh Kingsley – Student Assignment Submission System.
