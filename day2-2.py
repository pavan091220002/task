from fastapi import FastAPI,Query            
#from .schemas import Employee_Details
from .models import Employee
from fastapi_sqlalchemy import DBSessionMiddleware,db

app = FastAPI()

from pydantic import BaseModel

class Employee_Details(BaseModel):
    id: int
    name : str
    email : str
    password : str
app.add_middleware(DBSessionMiddleware, db_url="postgresql+psycopg://postgres:admin@localhost:5432/postgres")

@app.get("/employee")
def get_users(page: int = Query(1, ge=1), page_size: int = Query(2, ge=1)):
    offset = (page - 1) * page_size
    employee = db.session.query(Employee).offset(offset).limit(page_size).all()
    

@app.post("/add_user")
def add_user(employee_data: Employee_Details):
    new_employee = Employee(**employee_data.dict())
    db.session.add(new_employee)
    db.session.commit()
    return {"message":"employee details "}

@app.post("/update_user")
def update_user(employee_data: Employee_Details):
    update_employee = db.session.query(Employee).filter_by(id=employee_data.id).first()
    if employee_data.name:
        update_employee.name = employee_data.name
    if employee_data.email:
        update_employee.email = employee_data.email
    db.session.add(update_employee)
    db.session.commit()
    return {"message": "User updated successfully"}
