from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List


app = FastAPI()
class finding_duplicates(BaseModel):
    elements : list[int] = None



class ErrorResponsive(BaseModel): 
    error_message :str
    
def validate_request(request:finding_duplicates):
    try:
        if hasattr(request,"elements"):
            if request.elements == None:
                return "Value of field elements is null.",True
            if type(request.elements) is not list:
                return "Value of field elements is not a list.",True
            if request.elements == []:
                return "value of field elements is empty",True
            for element in request.elements:
                if isinstance(element,int) == False:
                    return "element in the list is not of type of integers, must need to enter integers",True
            return "correct request",False
        else:
            return "field elements is missing. elements are required",True
    except Exception as e:
        return e,True
@app.post('/finding_duplicates')
def finding_duplicates(request:finding_duplicates):
    try:
        validation_text, error_flag = validate_request(request)
        if error_flag is True: 
            return ErrorResponsive(error_message= validation_text)
        list= []
        duplicate_elements = []
        for element in request.array:
            if element is int:
                if element not in list:
                    list.append(element)
                else:
                    duplicate_elements.append(element)
                
        duplicate_elements = set(duplicate_elements)
        return {'duplicate_elements':duplicate_elements}
    except Exception as e:
        return ErrorResponsive(error_message=e)
        

