from fastapi import FastAPI, UploadFile, File
import boto3
import uuid

app = FastAPI()

# LocalStack S3 ve DynamoDB Bağlantıları
# Docker ağı içinde değil, yerel terminalden çalıştıracağımız için localhost:4566 kullanıyoruz
s3 = boto3.client('s3', endpoint_url="http://localstack:4566",
                  aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localstack:4566",
                          aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")

BUCKET_NAME = "sentinel-raw-media"


@app.get("/")
def home():
    return {"message": "Sentinel API is Online"}


@app.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_name = file.filename

    # 1. Dosyayı S3'e yükle
    s3.upload_fileobj(file.file, BUCKET_NAME, file_id)

    # 2. İşlem kaydını DynamoDB'ye "Pending" olarak yaz
    table = dynamodb.Table('AnalysisResults')
    table.put_item(Item={
        'FileId': file_id,
        'FileName': file_name,
        'Status': 'PENDING'
    })

    return {"status": "Uploaded", "file_id": file_id}