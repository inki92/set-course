resource "aws_subnet" "subnets" {
  vpc_id       = data.aws_vpc.default.id

  for_each     = { for idx, az in var.availability_zones :
    az => var.cidr_blocks[idx]
  }

  availability_zone = each.key
  cidr_block        = each.value

  #map_public_ip_on_launch = true

  tags          = {
    Name        = "subnet-${each.key}"
    Environment = var.env_name
    Application = "ImageRecognitionApp"
  }
}

resource "aws_security_group" "security_group" {
  description   = "SG for ECS in private subnets"
  name          = var.sg_name
  vpc_id        = data.aws_vpc.default.id

  ingress {
    description = "All traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = var.cidr_blocks
  }

  egress {
    description = "All traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "Security Group for App"
    Environment = var.env_name
    Application = "ImageRecognitionApp"
  }
}
