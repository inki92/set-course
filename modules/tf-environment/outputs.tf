output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.image_rek_bucket.bucket
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table"
  value       = aws_dynamodb_table.rek_table.name
}

output "subnet_ids" {
  description = "The IDs of all Subnets"
  value = [
    for subnet in aws_subnet.subnets : subnet.id
  ]
}

output "default_vpc_id" {
  description = "The ID of the default VPC"
  value       = data.aws_vpc.default.id
}

output "default_region_name" {
  description = "The name of the default region"
  value       = data.aws_region.current.name
}

output "sns_name" {
  description = "The name of the SNS topic"
  value       = var.sns_name
}

output "sqs_name" {
  description = "The name of the SQS Queue"
  value       = var.sqs_name
}

output "sg_name" {
  description = "The name of the security group"
  value       = var.sg_name
}
