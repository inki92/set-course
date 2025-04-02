resource "aws_dynamodb_table" "rek_table" {
  name           = var.dynamodb_name
  billing_mode   = "PAY_PER_REQUEST" # flexible billing
  hash_key       = var.table_hash_key

  attribute {
    name         = var.table_hash_key
    type         = "S"
  }

  tags           = {
    Name         = "DynamoDB-For-Images-Rec"
    Environment = var.env_name
    Application  = "ImageRecognitionApp"
  }
}
