variable "bucket_name" {
  type        = string
  description = "Name of the S3 bucket to create"
}

variable "sns_name" {
  type        = string
  description = "Name of the SNS topic to create"
}

variable "sqs_name" {
  type        = string
  description = "Name of the SQS Queue to create"
}

variable "dynamodb_name" {
  type        = string
  description = "Name of the Dynamo DB table to create"
}

variable "table_hash_key" {
  type        = string
  description = "Name of the hash key for Dynamo DB table"
  default     = "ImageName"
}

variable "availability_zones" {
  description = "List of availability zones for subnets"
  type        = list(string)
  default = [
    "eu-central-1a",
    "eu-central-1b"
  ]
}

variable "cidr_blocks" {
  description = "List of CIDR blocks"
  type        = list(string)
  default = [
    "172.31.64.0/20",
    "172.31.192.0/20"
  ]
}

variable "sg_name" {
  type        = string
  description = "Name of the security group"
  default     = "default-security-group"
}

variable "env_name" {
  description = "Environment Name"
  type        = string
  default     = "dev"
}