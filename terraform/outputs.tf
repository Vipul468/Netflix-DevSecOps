output "aws_account_id" {
  description = "AWS Account ID used by Terraform"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_caller_arn" {
  description = "AWS ARN used by Terraform"
  value       = data.aws_caller_identity.current.arn
}

output "vpc_id" {
  description = "Netflix DevSecOps VPC ID"
  value       = aws_vpc.main.id
}