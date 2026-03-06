import boto3
import time

# LocalStack bağlantısı
# Bu servis sürekli DynamoDB'yi tarayacak
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566",
                          aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")
table = dynamodb.Table('AnalysisResults')


def process_files():
    print("Processor başlatıldı, PENDING dosyalar taranıyor...")
    while True:
        # 1. PENDING olan kayıtları bul
        response = table.scan()
        items = response.get('Items', [])

        for item in items:
            if item['Status'] == 'PENDING':
                print(f"Dosya analiz ediliyor: {item['FileName']} (ID: {item['FileId']})")

                # 2. Analiz simülasyonu (2 saniye bekle)
                time.sleep(2)

                # 3. Durumu güncelle
                table.update_item(
                    Key={'FileId': item['FileId']},
                    UpdateExpression="set #s = :status",
                    ExpressionAttributeValues={':status': 'COMPLETED'},
                    ExpressionAttributeNames={'#s': 'Status'}
                )
                print(f"Analiz tamamlandı: {item['FileId']}")

        time.sleep(5)  # 5 saniyede bir kontrol et


if __name__ == "__main__":
    process_files()