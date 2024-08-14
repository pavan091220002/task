from fastapi import FastAPI, File, UploadFile, HTTPException,status
from fastapi.responses import JSONResponse
import boto3
from werkzeug.utils import secure_filename

app = FastAPI()

AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
S3_BUCKET_NAME = ''

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

MAX_FILE_SIZE = 500 * 1024

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file part")

    if file.filename == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No selected file")

    file_size = len(await file.read())
    await file.seek(0)  

    if file_size > MAX_FILE_SIZE:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "File size exceeds 500 KB"})

    filename = secure_filename(file.filename)
    s3.upload_fileobj(file.file, S3_BUCKET_NAME, filename)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "File uploaded successfully"})


