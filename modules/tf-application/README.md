## Application module

to deploy non-persistent infrastructure

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.8.5 |
| <a name="requirement_archive"></a> [archive](#requirement\_archive) | 2.7.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | 2.7.0 |
| <a name="provider_aws"></a> [aws](#provider\_aws) | ~> 5.0 |

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_log_group.ecs_task](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_default_subnet.default_subnet_a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/default_subnet) | resource |
| [aws_ecs_cluster.ecs_cluster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_cluster) | resource |
| [aws_ecs_service.ecs_service](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_service) | resource |
| [aws_ecs_task_definition.ecs_task_definition](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_task_definition) | resource |
| [aws_eip.nat](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip) | resource |
| [aws_iam_policy.lambda_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_policy_attachment.ecs_app_runner](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment) | resource |
| [aws_iam_policy_attachment.ecs_cloud_watch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment) | resource |
| [aws_iam_policy_attachment.ecs_dynamodb_access](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment) | resource |
| [aws_iam_policy_attachment.ecs_s3_access](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy_attachment) | resource |
| [aws_iam_role.ecs_execution_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role.ecs_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role.lambda_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.lambda_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_event_source_mapping.sqs_trigger](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_event_source_mapping) | resource |
| [aws_lambda_function.lambda_script](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lb.ecs_load_balancer](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb) | resource |
| [aws_lb_listener.ecs_listener](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener) | resource |
| [aws_lb_target_group.ecs_target_group](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_target_group) | resource |
| [aws_nat_gateway.gw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/nat_gateway) | resource |
| [aws_route_table.nat_gw](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table) | resource |
| [aws_route_table_association.primary_private_subnet](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | resource |
| [aws_route_table_association.secondary_private_subnet](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) | resource |
| [aws_security_group.ecs_security_group](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_security_group.lb_sg](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [archive_file.lambda_payload](https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file) | data source |
| [aws_dynamodb_table.table_name](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/dynamodb_table) | data source |
| [aws_iam_policy.ecs_app_runner](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy) | data source |
| [aws_iam_policy.ecs_cloud_watch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy) | data source |
| [aws_iam_policy.ecs_dynamodb_access](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy) | data source |
| [aws_iam_policy.ecs_s3_access](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy) | data source |
| [aws_s3_bucket.bucket_name](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/s3_bucket) | data source |
| [aws_sqs_queue.queue_name](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/sqs_queue) | data source |
| [aws_subnets.default_subnets](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/subnets) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_docker_container_name"></a> [docker\_container\_name](#input\_docker\_container\_name) | Docker image name | `string` | `"RekImage"` | no |
| <a name="input_docker_image_uri"></a> [docker\_image\_uri](#input\_docker\_image\_uri) | URI of the Docker image | `string` | n/a | yes |
| <a name="input_dynamodb_name"></a> [dynamodb\_name](#input\_dynamodb\_name) | Name of the Dynamo DB table | `string` | n/a | yes |
| <a name="input_ecs_app_port"></a> [ecs\_app\_port](#input\_ecs\_app\_port) | ECS Port Number for the App | `number` | `80` | no |
| <a name="input_ecs_cluster_name"></a> [ecs\_cluster\_name](#input\_ecs\_cluster\_name) | ECS Cluster Name | `string` | `"ECSRecAppCluster"` | no |
| <a name="input_ecs_family_name"></a> [ecs\_family\_name](#input\_ecs\_family\_name) | ECS Family Name | `string` | `"ECSRecoginitonApp"` | no |
| <a name="input_ecs_lb_health_path"></a> [ecs\_lb\_health\_path](#input\_ecs\_lb\_health\_path) | ESC Load Balancer Health Check Path | `string` | `"/ui/"` | no |
| <a name="input_ecs_lb_target_group_name"></a> [ecs\_lb\_target\_group\_name](#input\_ecs\_lb\_target\_group\_name) | ESC Load Balancer Target Group Name | `string` | `"esc-rek-target-group"` | no |
| <a name="input_ecs_service_name"></a> [ecs\_service\_name](#input\_ecs\_service\_name) | ECS Service Name | `string` | `"ECSServiceRecApp"` | no |
| <a name="input_ecs_sg_prefix"></a> [ecs\_sg\_prefix](#input\_ecs\_sg\_prefix) | ECS Prefix for SG | `string` | `"ecssg"` | no |
| <a name="input_ecs_task_cpu"></a> [ecs\_task\_cpu](#input\_ecs\_task\_cpu) | ECS Task CPU | `number` | `1024` | no |
| <a name="input_ecs_task_execution_role_name"></a> [ecs\_task\_execution\_role\_name](#input\_ecs\_task\_execution\_role\_name) | ECS Task ExecutionRole Name | `string` | `"ECSTaskExecutionRole"` | no |
| <a name="input_ecs_task_memory"></a> [ecs\_task\_memory](#input\_ecs\_task\_memory) | ECS Task Memory | `number` | `3072` | no |
| <a name="input_ecs_task_name"></a> [ecs\_task\_name](#input\_ecs\_task\_name) | ECS Task Name | `string` | `"ECSRecApp"` | no |
| <a name="input_ecs_task_role_name"></a> [ecs\_task\_role\_name](#input\_ecs\_task\_role\_name) | ECS Task Role Name | `string` | `"ECSTaskRole"` | no |
| <a name="input_env_name"></a> [env\_name](#input\_env\_name) | Environment Name | `string` | `"dev"` | no |
| <a name="input_lambda_function_name"></a> [lambda\_function\_name](#input\_lambda\_function\_name) | Lambda function name | `string` | `"lambda_script"` | no |
| <a name="input_lambda_iam_policy_name"></a> [lambda\_iam\_policy\_name](#input\_lambda\_iam\_policy\_name) | The lambda IAW policy name | `string` | `"lamda_iam_policy"` | no |
| <a name="input_lambda_role_name"></a> [lambda\_role\_name](#input\_lambda\_role\_name) | The lambda role name | `string` | `"lambda_role"` | no |
| <a name="input_lambda_timeout"></a> [lambda\_timeout](#input\_lambda\_timeout) | Lambda timeout secs | `number` | `10` | no |
| <a name="input_lambda_zip_archive"></a> [lambda\_zip\_archive](#input\_lambda\_zip\_archive) | zip with lambda function | `string` | `"lambda_function_payload.zip"` | no |
| <a name="input_lb_public_name"></a> [lb\_public\_name](#input\_lb\_public\_name) | Load Balancer for public name | `string` | `"LBAppRecPublic"` | no |
| <a name="input_lb_public_sg_name"></a> [lb\_public\_sg\_name](#input\_lb\_public\_sg\_name) | Load Balancer SG for public name | `string` | `"lb_sg"` | no |
| <a name="input_python_version"></a> [python\_version](#input\_python\_version) | Python version for lambda function | `string` | `"python3.12"` | no |
| <a name="input_region"></a> [region](#input\_region) | The AWS region for resources | `string` | `"eu-central-1"` | no |
| <a name="input_s3_bucket_name"></a> [s3\_bucket\_name](#input\_s3\_bucket\_name) | S3 Bucket name | `string` | n/a | yes |
| <a name="input_sqs_name"></a> [sqs\_name](#input\_sqs\_name) | SQS Queue name | `string` | n/a | yes |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | The list of subnet IDs | `list(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | VPC id | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_load_balancer_dns_name"></a> [load\_balancer\_dns\_name](#output\_load\_balancer\_dns\_name) | The public DNS name of the load balancer |
