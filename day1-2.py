from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, date, time
import pytz
app = FastAPI()

class leapyear(BaseModel):
    user_name : str
    date_of_birth :date
    email : str
    age : int
@app.post('/leapyear')
def leapyear(leapyear : leapyear):
    utc_dob = leapyear.date_of_birth.replace(tzinfo=pytz.UTC)
    year = str(leapyear.date_of_birth).split('-')[0]
    if len(year)==4:
        if int(year)%4 == 0:
            return {f'leap year'}
        else: return {f'not leap year'}
        