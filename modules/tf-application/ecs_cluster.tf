# ECS Task:

resource "aws_ecs_task_definition" "ecs_task_definition" {
  family                   = var.ecs_family_name
  network_mode             = "awsvpc"
  memory                   = var.ecs_task_memory
  cpu                      = var.ecs_task_cpu
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_role.arn

  container_definitions    = jsonencode([{
    name                   = var.docker_container_name
    image                  = var.docker_image_uri

    essential              = true

    portMappings           = [{
      containerPort        = var.ecs_app_port
      protocol             = "tcp"
      hostPort             = var.ecs_app_port
      appProtocol          = "http"
    }]

    logConfiguration          = {
      logDriver               = "awslogs",
      options                 = {
        awslogs-group         = aws_cloudwatch_log_group.ecs_task.name,
        awslogs-region        = var.region,
        awslogs-stream-prefix = "ecs"
      }
    }
    environment               = [
      {
        name  = "AWS_DEFAULT_REGION",
        value = var.region
      },
      {
        name  = "AWS_S3_BUCKET_NAME",
        value = var.s3_bucket_name
      },
      {
        name  = "AWS_DYNAMODB_TABLE_NAME",
        value = var.dynamodb_name
      },
      {
        name  = "PYTHONPATH",
        value = "." }
    ]
  }])
  depends_on  = [aws_cloudwatch_log_group.ecs_task]
}

resource "aws_cloudwatch_log_group" "ecs_task" {
  name          = var.ecs_task_name

  tags          = {
    Name        = "ECS Task Log Group"
    Environment = var.env_name
    Application = "ImageRecognitionApp"
  }
}

resource "aws_iam_role" "ecs_role" {
  name               = var.ecs_task_role_name
  description        = "AWS IAM Role for ESC Task"

  assume_role_policy = jsonencode({
    Version          = "2012-10-17"
    Statement        = [
      {
        Action       = "sts:AssumeRole"
        Effect       = "Allow"
        Principal    = {
          Service    = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role" "ecs_execution_role" {
  name        = var.ecs_task_execution_role_name
  description = "IAM Execution Role for the ECS"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  inline_policy {
    name = "ecs_execution_role_policy"

    policy = jsonencode({
      Version   = "2012-10-17"
      Statement = [
        {
          Effect   = "Allow"
          Action   = [
            "ecr:GetAuthorizationToken",
            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage"
          ]
          Resource = "*"
        }
      ]
    })
  }
}

resource "aws_iam_policy_attachment" "ecs_s3_access" {
  name       = data.aws_iam_policy.ecs_s3_access.name
  roles      = [aws_iam_role.ecs_role.name]
  policy_arn = data.aws_iam_policy.ecs_s3_access.arn
  depends_on = [aws_iam_role.ecs_role]
}

resource "aws_iam_policy_attachment" "ecs_dynamodb_access" {
  name       = data.aws_iam_policy.ecs_dynamodb_access.name
  roles      = [aws_iam_role.ecs_role.name]
  policy_arn = data.aws_iam_policy.ecs_dynamodb_access.arn
  depends_on = [aws_iam_role.ecs_role]
}

resource "aws_iam_policy_attachment" "ecs_app_runner" {
  name       = data.aws_iam_policy.ecs_app_runner.name
  roles      = [aws_iam_role.ecs_execution_role.name]
  policy_arn = data.aws_iam_policy.ecs_app_runner.arn
  depends_on = [aws_iam_role.ecs_execution_role]
}

resource "aws_iam_policy_attachment" "ecs_cloud_watch" {
  name       = data.aws_iam_policy.ecs_cloud_watch.name
  roles      = [aws_iam_role.ecs_execution_role.name]
  policy_arn = data.aws_iam_policy.ecs_cloud_watch.arn
  depends_on = [aws_iam_role.ecs_execution_role]
}

# ECS Cluster:

resource "aws_ecs_cluster" "ecs_cluster" {
  name           = var.ecs_cluster_name
  tags           = {
    Application  = "ImageRecognitionApp"
    Environment = var.env_name
    Name         = "ECSRecAppCluster"
  }
}

# Create new sg for ECS targets

resource "aws_security_group" "ecs_security_group" {
  description       = "ESC SG"
  name_prefix       = var.ecs_sg_prefix
  vpc_id            = var.vpc_id

  ingress {
    description     = "All traffic"
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
    security_groups = [aws_security_group.lb_sg.id]
  }
  egress {
    description     = "All traffic"
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
  depends_on        = [aws_ecs_cluster.ecs_cluster]
}

# ECS Listener for HTTP in the ESC task subnet(works in private subnets):

resource "aws_lb_listener" "ecs_listener" {
  load_balancer_arn  = aws_lb.ecs_load_balancer.arn
  port               = var.ecs_app_port
  protocol           = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ecs_target_group.arn
  }
  depends_on         = [aws_lb_target_group.ecs_target_group]
}

# Load Balancer target group for work with RecApp(works in private subnets)

resource "aws_lb_target_group" "ecs_target_group" {
  name                  = var.ecs_lb_target_group_name
  port                  = var.ecs_app_port
  protocol              = "HTTP"
  target_type           = "ip"
  vpc_id                = var.vpc_id

  health_check {
    path                = var.ecs_lb_health_path
    protocol            = "HTTP"
    port                = var.ecs_app_port
    unhealthy_threshold = 2
    healthy_threshold   = 2
    timeout             = 3
    interval            = 30
  }
  depends_on            = [aws_lb.ecs_load_balancer]
}

# ECS Service(works in private subnets)
resource "aws_ecs_service" "ecs_service" {
  name                 = var.ecs_service_name
  cluster              = aws_ecs_cluster.ecs_cluster.id
  task_definition      = aws_ecs_task_definition.ecs_task_definition.arn
  launch_type          = "FARGATE"

  network_configuration {
    subnets            = var.subnet_ids
    assign_public_ip   = false
    security_groups    = [aws_security_group.ecs_security_group.id]
  }

  desired_count = var.ecs_desired_count

  load_balancer {
    target_group_arn  = aws_lb_target_group.ecs_target_group.arn
    container_name    = var.docker_container_name
    container_port    = var.ecs_app_port
  }
  depends_on = [aws_security_group.ecs_security_group]
}
