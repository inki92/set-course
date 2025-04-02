variable "dynamodb_name" {
  type        = string
  description = "Name of the Dynamo DB table"
}

variable "subnet_ids" {
  description = "The list of subnet IDs"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC id"
  type        = string
}

variable "docker_image_uri" {
  description = "URI of the Docker image"
  type        = string
}

variable "region" {
  description = "The AWS region for resources"
  type        = string
  default     = "eu-central-1"
}

variable "lambda_role_name" {
  description = "The lambda role name"
  type        = string
  default     = "lambda_role"
}

variable "lambda_iam_policy_name" {
  description = "The lambda IAW policy name"
  type        = string
  default     = "lamda_iam_policy"
}

variable "python_version" {
  description = "Python version for lambda function"
  type        = string
  default     = "python3.12"
}

variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
  default     = "lambda_script"
}

variable "lambda_timeout" {
  description = "Lambda timeout secs"
  type        = number
  default     = 10
}

variable "lambda_zip_archive" {
  description = "zip with lambda function"
  type        = string
  default     = "lambda_function_payload.zip"
}

variable "docker_container_name" {
  description = "Docker image name"
  type        = string
  default     = "RekImage"
}

variable "sqs_name" {
  description = "SQS Queue name"
  type        = string
}

variable "s3_bucket_name" {
  description = "S3 Bucket name"
  type        = string
}

variable "ecs_family_name" {
  description = "ECS Family Name"
  type        = string
  default     = "ECSRecoginitonApp"
}

variable "ecs_task_name" {
  description = "ECS Task Name"
  type        = string
  default     = "ECSRecApp"
}

variable "ecs_task_memory" {
  description = "ECS Task Memory"
  type        = number
  default     = 3072
}

variable "ecs_task_cpu" {
  description = "ECS Task CPU"
  type        = number
  default     = 1024
}

variable "ecs_task_role_name" {
  description = "ECS Task Role Name"
  type        = string
  default     = "ECSTaskRole"
}

variable "ecs_task_execution_role_name" {
  description = "ECS Task ExecutionRole Name"
  type        = string
  default     = "ECSTaskExecutionRole"
}

variable "ecs_cluster_name" {
  description = "ECS Cluster Name"
  type        = string
  default     = "ECSRecAppCluster"
}

variable "ecs_sg_prefix" {
  description = "ECS Prefix for SG"
  type        = string
  default     = "ecssg"
}

variable "ecs_app_port" {
  description = "ECS Port Number for the App"
  type        = number
  default     = 80
}

variable "ecs_lb_target_group_name" {
  description = "ESC Load Balancer Target Group Name"
  type        = string
  default     = "esc-rek-target-group"
}

variable "ecs_lb_health_path" {
  description = "ESC Load Balancer Health Check Path"
  type        = string
  default     = "/ui/"
}

variable "ecs_service_name" {
  description = "ECS Service Name"
  type        = string
  default     = "ECSServiceRecApp"
}

variable "lb_public_sg_name" {
  description = "Load Balancer SG for public name"
  type        = string
  default     = "lb_sg"
}

variable "lb_public_name" {
  description = "Load Balancer for public name"
  type        = string
  default     = "LBAppRecPublic"
}

variable "env_name" {
  description = "Environment Name"
  type        = string
  default     = "dev"
}

variable "ecs_desired_count" {
  description = "Number of instances"
  type        = number
  default     = 2
}
