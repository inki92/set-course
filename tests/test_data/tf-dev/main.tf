provider "aws" {
  region                       = "eu-central-1"
}

terraform {
  backend "s3" {
    bucket                     = "iac-ter-state"
    key                        = "terraform/dev-state/terraform.tfstate"
    region                     = "eu-central-1"
    encrypt                    = true
  }
}

module "environment" {
  env_name                     = "dev"
  source                       = "../modules/tf-environment/"
  dynamodb_name                = "Image-dev"
  bucket_name                  = "image-rek-bucket-dev"
  sns_name                     = "image-rek-sns-dev"
  sqs_name                     = "image-rek-sqs-dev"
  sg_name                      = "SecurityGroupImageRekDev"
  cidr_blocks                  = [
    "172.31.64.0/20",
    "172.31.192.0/20"
  ]
}

module "application" {
  env_name                     = "dev"
  depends_on                   = [module.environment]
  source                       = "../modules/tf-application/"
  sqs_name                     = module.environment.sqs_name
  s3_bucket_name               = module.environment.s3_bucket_name
  dynamodb_name                = module.environment.dynamodb_table_name
  subnet_ids                   = module.environment.subnet_ids
  vpc_id                       = module.environment.default_vpc_id
  region                       = module.environment.default_region_name
  docker_image_uri             = "692859924835.dkr.ecr.eu-central-1.amazonaws.com/imagerecrepo:latest"
  lambda_role_name             = "lambda_role_dev"
  lambda_iam_policy_name       = "lamda_iam_policy_dev"
  lambda_function_name         = "lambda_script_dev"
  lambda_zip_archive           = "lambda_function_payload.zip"
  docker_container_name        = "RekImageDev"
  ecs_family_name              = "ECSRecoginitonAppDev"
  ecs_task_name                = "ECSRecAppDev"
  ecs_task_memory              = 3072
  ecs_task_cpu                 = 1024
  ecs_task_role_name           = "ECSTaskRoleDev"
  ecs_task_execution_role_name = "ECSTaskExecutionRoleDev"
  ecs_cluster_name             = "ECSRecAppClusterDev"
  ecs_sg_prefix                = "ecssg"
  ecs_app_port                 =  80
  ecs_lb_target_group_name     = "esc-rek-target-group-dev"
  ecs_lb_health_path           = "/ui/"
  ecs_service_name             =  "ECSServiceRecAppDev"
  lb_public_sg_name            = "lb_sg_dev"
  lb_public_name               = "LBAppRecPublicDev"
}
