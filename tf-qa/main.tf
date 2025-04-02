provider "aws" {
  region                       = "eu-central-1"
}

terraform {
  backend "s3" {
    bucket                     = "iac-ter-state"
    key                        = "terraform/qa-state/terraform.tfstate"
    region                     = "eu-central-1"
    encrypt                    = true
  }
}

module "environment" {
  env_name                     = "qa"
  source                       = "../modules/tf-environment/"
  dynamodb_name                = "Image-qa"
  bucket_name                  = "image-rek-bucket-qa"
  sns_name                     = "image-rek-sns-qa"
  sqs_name                     = "image-rek-sqs-qa"
  sg_name                      = "SecurityGroupImageRekQA"
  cidr_blocks                  = [
    "172.31.112.0/20",
    "172.31.128.0/20"
  ]
}

module "application" {
  env_name                     = "qa"
  depends_on                   = [module.environment]
  source                       = "../modules/tf-application/"
  sqs_name                     = module.environment.sqs_name
  s3_bucket_name               = module.environment.s3_bucket_name
  dynamodb_name                = module.environment.dynamodb_table_name
  subnet_ids                   = module.environment.subnet_ids
  vpc_id                       = module.environment.default_vpc_id
  region                       = module.environment.default_region_name
  docker_image_uri             = "692859924835.dkr.ecr.eu-central-1.amazonaws.com/imagerecrepo:latest"
  lambda_role_name             = "lambda_role_qa"
  lambda_iam_policy_name       = "lamda_iam_policy_qa"
  lambda_function_name         = "lambda_script_qa"
  lambda_zip_archive           = "lambda_function_payload.zip"
  docker_container_name        = "RekImageQA"
  ecs_family_name              = "ECSRecoginitonAppQA"
  ecs_task_name                = "ECSRecAppQA"
  ecs_desired_count            = 1
  ecs_task_memory              = 3072
  ecs_task_cpu                 = 1024
  ecs_task_role_name           = "ECSTaskRoleQA"
  ecs_task_execution_role_name = "ECSTaskExecutionRoleQA"
  ecs_cluster_name             = "ECSRecAppClusterQA"
  ecs_sg_prefix                = "ecssgqa"
  ecs_app_port                 =  80
  ecs_lb_target_group_name     = "esc-rek-target-group-qa"
  ecs_lb_health_path           = "/ui/"
  ecs_service_name             =  "ECSServiceRecAppQA"
  lb_public_sg_name            = "lb_sg_qa"
  lb_public_name               = "LBAppRecPublicQA"
}
