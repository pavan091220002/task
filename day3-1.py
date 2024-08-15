import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class AddressModel(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

    @validator('zip_code')
    def validate_zip_code(cls, value):
        if not value.isdigit() or len(value) != 5:
            raise ValueError('Zip code must be a 5-digit number')
        return value

class UserModel(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    age: Optional[int] = Field(None, ge=18)
    addresses: List[AddressModel]
    is_active: bool = True

    @validator('email')
    def validate_email(cls, value):
        if not value.endswith('@example.com'):
            raise ValueError('Email must end with @example.com')
        return value

async def create_user(user: UserModel):
    if user.first_name == 'John':
        logger.info('First log: User first name is John')

    if user.last_name == 'Doe':
        logger.info('Second log: User last name is Doe')

    if user.is_active:
        logger.info('Third log: User is active')

    created_user = user 
    return created_user

@app.post('/users', status_code=201)
async def important_view(user: UserModel):
    try:
        created_user = await create_user(user)
        return created_user
    except Exception as e:
        logger.error('Something went wrong', exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
