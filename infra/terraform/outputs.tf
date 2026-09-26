output "instance_id" {
  description = "AWS EC2 instance ID"
  value       = aws_instance.web.id
}

output "public_ip" {
  description = "Public IPv4 address of the EC2 instance"
  value       = aws_instance.web.public_ip
}

output "public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.web.public_dns
}

output "security_group_id" {
  description = "Security group attached to the web server"
  value       = aws_security_group.web.id
}

output "ssm_role_arn" {
  description = "IAM role used by the EC2 instance for Systems Manager"
  value       = aws_iam_role.ec2_ssm.arn
}

output "github_deploy_role_arn" {
  description = "OIDC IAM role used by GitHub Actions"
  value       = aws_iam_role.github_deploy.arn
}
