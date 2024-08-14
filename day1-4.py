from fastapi import FastAPI, File, UploadFile, HTTPException,status
from fastapi.responses import JSONResponse
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = FastAPI()

AWS_ACCESS_KEY = ''
AWS_SECRET_KEY =''
AWS_REGION = ''

textract = boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)
'''textract = boto3.client('textract)'''

@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file part")

    if file.filename == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No selected file")

    file_content = await file.read()

    try:
        response = textract.detect_document_text(Document={'Bytes': file_content})
        blocks = response['Blocks']
        text = ''
        for block in blocks:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + '\n'
            elif block['BlockType'] == 'WORD':
                text += block['Text']

        return JSONResponse(status_code=status.HTTP_200_OK, content={"extracted_text": text})

    except NoCredentialsError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AWS credentials not available")
    except PartialCredentialsError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Incomplete AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


