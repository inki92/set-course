# data from variables:

data "aws_dynamodb_table" "table_name" {
  name         = var.dynamodb_name
}

data "aws_sqs_queue" "queue_name" {
  name         = var.sqs_name
}

data "aws_s3_bucket" "bucket_name" {
  bucket       = var.s3_bucket_name
}

# policy names:

data "aws_iam_policy" "ecs_s3_access" {
  name         = "AmazonS3FullAccess"
}

data "aws_iam_policy" "ecs_dynamodb_access" {
  name         = "AmazonDynamoDBFullAccess"
}

data "aws_iam_policy" "ecs_app_runner" {
  name         = "AWSAppRunnerServicePolicyForECRAccess"
}

data "aws_iam_policy" "ecs_cloud_watch" {
  name         = "CloudWatchLogsFullAccess"
}

# lambda archive file:

data "archive_file" "lambda_payload" {
  type        = "zip"
  source_file = "${path.module}/lambda/index.py"
  output_path = "${path.module}/${var.lambda_zip_archive}"
}

# default public subnets
data "aws_subnets" "default_subnets" {
  filter {
    name   = "default-for-az"
    values = ["true"]  # filter for default subnets
  }

  filter {
    name   = "vpc-id"
    values = [var.vpc_id]  # vpc id
  }
}
