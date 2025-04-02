# NAT Gateway Setup:

resource "aws_default_subnet" "default_subnet_a" {
  availability_zone = format("%sa", var.region)
}

resource "aws_eip" "nat" {
  domain            = "vpc"
  public_ipv4_pool  = "amazon"
  tags              = {
    Name            = "Nat-GW-IP-Address"
    Environment     = var.env_name
    Application     = "ImageRecognitionApp"
  }
}

resource "aws_nat_gateway" "gw" {
  allocation_id     = aws_eip.nat.id
  subnet_id         = aws_default_subnet.default_subnet_a.id
  tags = {
    Application     = "ImageRecognitionApp"
    Environment     = var.env_name
    Name            = "Nat-GateWay"
  }
  depends_on        = [aws_eip.nat]
}

resource "aws_route_table" "nat_gw" {
  vpc_id            = var.vpc_id

  route {
    cidr_block      = "0.0.0.0/0"
    nat_gateway_id  = aws_nat_gateway.gw.id
  }

  tags              = {
    Application     = "ImageRecognitionApp"
    Environment     = var.env_name
    Name            = "NatGW-Route-Table"
  }
}

resource "aws_route_table_association" "primary_private_subnet" {
  subnet_id         = var.subnet_ids[0]
  route_table_id    = aws_route_table.nat_gw.id
}

resource "aws_route_table_association" "secondary_private_subnet" {
  subnet_id         = var.subnet_ids[1]
  route_table_id    = aws_route_table.nat_gw.id
}
