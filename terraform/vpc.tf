resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name    = "netflix-devsecops-vpc"
    Project = "Netflix-DevSecOps"
  }
}

resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name    = "netflix-devsecops-nat-eip"
    Project = "Netflix-DevSecOps"
  }
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_1.id

  tags = {
    Name    = "netflix-devsecops-nat"
    Project = "Netflix-DevSecOps"
  }

  depends_on = [
    aws_internet_gateway.main
  ]
}

resource "aws_route" "private_nat" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main.id
}