from fastapi import FastAPI, HTTPException,status,Depends,Query
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, JSON, MetaData, Table
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from typing import List

app = FastAPI(tags = ["EMployee-details"],
    prefix = "/employee")

SQLALCHEMY_DATABASE_URL = 'postgresql:///./product1.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args= {
    'check_same_thread': False
})

sessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush = False)

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
    passwoed :str
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

@app.post('/',status_code = status.HTTP_201_CREATED)
def add(request:Employee,db:Session = Depends(get_db)):
    new_employee = Employee(name=request.name ,id =request.id ,email=request.email,password = request.password)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.put('/{id}')
def update(id,request:Employee,db:Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id)
    if not employee.first():
        pass
    employee.update(request.dict())
    db.commit()
    return {'Employee details updated successfully'}
        
@app.get("/employees/", response_model=List[Employee])
def read_employees(page: int = Query(1, ge=1), page_size: int = Query(2, ge=1), db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    employees = db.query(Employee).offset(offset).limit(page_size).all()
    return employees

@app.get('/{id}',response_model =ResponseModel)
def product(id, db:Session = Depends(get_db)):
    return db.query(Employee).filter(Employee.id == id).first()


@app.delete('/{id}')
def product(id, db:Session = Depends(get_db)):
    db.query(Employee).filter(Employee.id == id).delete(synchronize_session = False)
    db.commit()
    return {'Employee details deleted'} 