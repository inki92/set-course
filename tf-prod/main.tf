provider "aws" {
  region                       = "eu-central-1"
}

terraform {
  backend "s3" {
    bucket                     = "iac-ter-state"
    key                        = "terraform/prod-state/terraform.tfstate"
    region                     = "eu-central-1"
    encrypt                    = true
  }
}

module "environment" {
  env_name                     = "prod"
  source                       = "../modules/tf-environment/"
  dynamodb_name                = "Image-prod"
  bucket_name                  = "image-rek-bucket-prod"
  sns_name                     = "image-rek-sns-prod"
  sqs_name                     = "image-rek-sqs-prod"
  sg_name                      = "SecurityGroupImageRekProd"
  cidr_blocks                  = [
    "172.31.80.0/20",
    "172.31.96.0/20"
  ]
}

module "application" {
  env_name                     = "prod"
  depends_on                   = [module.environment]
  source                       = "../modules/tf-application/"
  sqs_name                     = module.environment.sqs_name
  s3_bucket_name               = module.environment.s3_bucket_name
  dynamodb_name                = module.environment.dynamodb_table_name
  subnet_ids                   = module.environment.subnet_ids
  vpc_id                       = module.environment.default_vpc_id
  region                       = module.environment.default_region_name
  docker_image_uri             = "692859924835.dkr.ecr.eu-central-1.amazonaws.com/imagerecrepo:latest"
  lambda_role_name             = "lambda_role_prod"
  lambda_iam_policy_name       = "lamda_iam_policy_prod"
  lambda_function_name         = "lambda_script_prod"
  lambda_zip_archive           = "lambda_function_payload.zip"
  docker_container_name        = "RekImageProd"
  ecs_family_name              = "ECSRecoginitonAppProd"
  ecs_task_name                = "ECSRecAppProd"
  ecs_desired_count            = 2
  ecs_task_memory              = 3072
  ecs_task_cpu                 = 1024
  ecs_task_role_name           = "ECSTaskRoleProd"
  ecs_task_execution_role_name = "ECSTaskExecutionRoleProd"
  ecs_cluster_name             = "ECSRecAppClusterProd"
  ecs_sg_prefix                = "ecssgprod"
  ecs_app_port                 =  80
  ecs_lb_target_group_name     = "esc-rek-target-group-prod"
  ecs_lb_health_path           = "/ui/"
  ecs_service_name             =  "ECSServiceRecAppProd"
  lb_public_sg_name            = "lb_sg_prod"
  lb_public_name               = "LBAppRecPublicProd"
}
