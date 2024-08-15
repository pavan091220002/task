from fastapi import FastAPI, HTTPException,status,Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, JSON, MetaData, Table
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from typing import List
import psycopg2

app = FastAPI(tags = ["Employee_details"])

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit = False, autoflush = False,bind = engine)

Base = declarative_base()
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

class employee(BaseModel):
    id : int
    name:str
    email:str
    password :str
class ResponseModel(BaseModel):
    id :int
    name :str
    email :str
    class config:
        orm_mode =True

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

@app.post('/employee',status_code = status.HTTP_201_CREATED)
def add(request:employee,db:Session = Depends(get_db)):
    new_employee = Employee(id =request.id,name = request.name ,email=request.email,password = request.password)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.put('/employee/{id}')
def update(id,request:employee,db:Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id)
    if not employee.first():
        pass
    employee.update(request.dict())
    db.commit()
    return {'Employee details updated successfully'}
        
@app.get('/employee',response_model =List[ResponseModel])
def employee(request:employee,db:Session = Depends(get_db)):
    return db.query(Employee).all()


@app.get('/employee/{id}',response_model =ResponseModel)
def employee(id, db:Session = Depends(get_db)):
    return db.query(Employee).filter(Employee.id == id).first()

@app.delete('/employee/{id}')
def employee(id, db:Session = Depends(get_db)):
    db.query(Employee).filter(Employee.id == id).delete(synchronize_session = False)
    db.commit()
    return {'Employee details deleted'} 
