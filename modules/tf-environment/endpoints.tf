resource "aws_vpc_endpoint" "s3_endpoint" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.${data.aws_region.current.name}.s3"
  vpc_endpoint_type = "Gateway"

  tags = {
    Application     = "ImageRecognitionApp"
    Environment     = var.env_name
    Name            = "S3-Endpoint"
  }
}

resource "aws_vpc_endpoint" "ecr_dkr_endpoint" {
  vpc_id              = data.aws_vpc.default.id
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ecr.dkr"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = false
  subnet_ids          = [for subnet in aws_subnet.subnets : subnet.id]
  security_group_ids  = [aws_security_group.security_group.id]

  tags                = {
    Application       = "ImageRecognitionApp"
    Environment       = var.env_name
    Name              = "ECR-DKR-Endpoint"
  }
}

resource "aws_vpc_endpoint" "ecr_api_endpoint" {
  vpc_id              = data.aws_vpc.default.id
  service_name        = "com.amazonaws.${data.aws_region.current.name}.ecr.api"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = false
  subnet_ids          = [for subnet in aws_subnet.subnets : subnet.id]
  security_group_ids  = [aws_security_group.security_group.id]

  tags                = {
    Application       = "ImageRecognitionApp"
    Environment       = var.env_name
    Name              = "ECR-API-Endpoint"
  }
}

resource "aws_vpc_endpoint" "dynamodb_endpoint" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.${data.aws_region.current.name}.dynamodb"
  vpc_endpoint_type = "Gateway"

  tags              = {
    Application     = "ImageRecognitionApp"
    Environment     = var.env_name
    Name            = "DynamoDB-Endpoint"
  }
}

resource "aws_vpc_endpoint" "logs_endpoint" {
  vpc_id              = data.aws_vpc.default.id
  service_name        = "com.amazonaws.${data.aws_region.current.name}.logs"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = false
  subnet_ids          = [for subnet in aws_subnet.subnets : subnet.id]
  security_group_ids  = [aws_security_group.security_group.id]

  tags                = {
    Application       = "ImageRecognitionApp"
    Environment       = var.env_name
    Name              = "Logs-Endpoint"
  }
}
