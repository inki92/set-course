# Load Balancer for the public subnets

resource "aws_security_group" "lb_sg" {
  name           = var.lb_public_sg_name
  description    = "Security Group for the Load Balancer"
  vpc_id         = var.vpc_id

  ingress {
    description  = "All traffic"
    from_port    = var.ecs_app_port
    to_port      = var.ecs_app_port
    protocol     = "tcp"
    cidr_blocks  = ["0.0.0.0/0"]
  }

  egress {
    description  = "All traffic"
    from_port    = 0
    to_port      = 0
    protocol     = "-1"
    cidr_blocks  = ["0.0.0.0/0"]
  }

  tags = {
    Application  = "ImageRecognitionApp"
    Name         = "Public-Load-Balancer-SG"
  }
}

resource "aws_lb" "ecs_load_balancer" {
  name               = var.lb_public_name
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]

  # default public subnets
  subnets            = data.aws_subnets.default_subnets.ids

  enable_deletion_protection = false

  tags = {
    Application  = "ImageRecognitionApp"
    Environment = var.env_name
    Name         = "Public-Load-Balancer"
  }
}
