cat <<EOF > README.md
# Sentinel-S3: Cloud-Native Media Analysis Pipeline

A local AWS-simulated media processing pipeline built with **Microservices architecture**. This project demonstrates how to handle asynchronous media processing using **S3** for storage and **DynamoDB** for metadata persistence, all running locally via **LocalStack**.

## 🚀 Architecture
* **FastAPI (API Service):** Handles media uploads and records initial metadata.
* **Python (Processor Service):** A background worker that monitors and processes "PENDING" files.
* **LocalStack:** Simulates AWS services (S3 & DynamoDB) in a local Docker container.
* **Docker Compose:** Orchestrates all services into a single, unified environment.



## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Frameworks:** FastAPI, Boto3
* **Infrastructure:** Docker, Docker Compose, Terraform
* **Cloud Simulation:** LocalStack

## 📦 Setup & Run

1. **Start the System:**
   \`\`\`bash
   docker compose up --build
   \`\`\`

2. **Initialize Infrastructure (One-time):**
   \`\`\`bash
   # Create S3 Bucket
   docker exec -it sentinel-s3-localstack awslocal s3 mb s3://sentinel-raw-media

   # Create DynamoDB Table
   docker exec -it sentinel-s3-localstack awslocal dynamodb create-table \\
       --table-name AnalysisResults \\
       --attribute-definitions AttributeName=FileId,AttributeType=S \\
       --key-schema AttributeName=FileId,KeyType=HASH \\
       --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
   \`\`\`

## 🧪 Testing the Pipeline
Upload a file to trigger the process:
\`\`\`bash
curl -X POST "http://127.0.0.1:8001/upload" -F "file=@requirements.txt"
\`\`\`
Monitor the \`processor-service\` logs to see the status transition from **PENDING** to **COMPLETED**.

---
Developed by **Ali Gaffar Toksoy**
EOF

# Git işlemlerini başlat
git add README.md
git commit -m "docs: add professional English README"
git push -u origin main --force
