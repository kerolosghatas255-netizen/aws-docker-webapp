resource "aws_security_group" "web" {
  name                   = "aws-docker-webapp-sg"
  description            = "Security group for AWS Docker portfolio project"
  vpc_id                 = "vpc-067e7ebd6216d9464"
  revoke_rules_on_delete = false

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ec2_ssm" {
  name                 = "aws-docker-webapp-ssm-role"
  description          = "Allows EC2 instances to call AWS services on your behalf."
  path                 = "/"
  max_session_duration = 3600

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.ec2_ssm.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2_ssm" {
  name = "aws-docker-webapp-ssm-role"
  role = aws_iam_role.ec2_ssm.name
}

resource "aws_instance" "web" {
  ami           = "ami-05bfa4a7765f38076"
  instance_type = "t3.micro"

  subnet_id                   = "subnet-0d8a35d174a189f1e"
  associate_public_ip_address = true

  key_name             = "aws-docker-webapp-key"
  iam_instance_profile = aws_iam_instance_profile.ec2_ssm.name

  vpc_security_group_ids = [
    aws_security_group.web.id
  ]

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
    http_protocol_ipv6          = "disabled"
    instance_metadata_tags      = "disabled"
  }

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 10
    iops                  = 3000
    throughput            = 125
    encrypted             = true
    kms_key_id            = "arn:aws:kms:eu-north-1:563807597162:key/4a57c50c-8754-4a53-b4b8-0cc766f6f722"
    delete_on_termination = true
  }

  credit_specification {
    cpu_credits = "unlimited"
  }

  tags = {
    Name = "aws-docker-webapp"
  }

  lifecycle {
    prevent_destroy = true
  }
}
