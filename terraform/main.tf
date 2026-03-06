provider "aws" {
  access_key = "test"
  secret_key = "test"
  region     = "us-east-1"
  s3_use_path_style = true

  endpoints {
    s3       = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "media_bucket" {
  bucket = "sentinel-raw-media"
}

resource "aws_dynamodb_table" "analysis_results" {
  name         = "AnalysisResults"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "FileId"

  attribute {
    name = "FileId"
    type = "S"
  }
}