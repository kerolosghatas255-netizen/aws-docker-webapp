# \# AWS Docker Web Application

# 

# A hands-on DevOps portfolio project demonstrating containerization, automated testing, secure AWS deployment, and Infrastructure as Code.

# 

# \## Architecture

# 

# ```mermaid

# flowchart TD

# &#x20;   Developer\[Developer] -->|git push| GitHub\[GitHub Repository]

# 

# &#x20;   GitHub --> TFV\[Terraform Validation]

# &#x20;   GitHub --> Tests\[Docker Integration Tests]

# 

# &#x20;   TFV --> Deploy\[Deployment Job]

# &#x20;   Tests --> Deploy

# 

# &#x20;   Deploy -->|OIDC| IAM\[AWS IAM Role]

# &#x20;   IAM --> SSM\[AWS Systems Manager]

# &#x20;   SSM --> EC2\[AWS EC2 Ubuntu Server]

# 

# &#x20;   Internet\[Internet] -->|HTTP :80| Nginx\[Nginx Reverse Proxy]

# &#x20;   Nginx --> App\[Flask + Gunicorn]

# &#x20;   App --> DB\[(PostgreSQL)]

# &#x20;   DB --> Volume\[(Persistent Docker Volume)]

# 

# &#x20;   Terraform\[Terraform IaC] --> EC2

# &#x20;   Terraform --> SG\[Security Group]

# &#x20;   Terraform --> IAMResources\[IAM / OIDC / SSM Resources]

# ```

# 

# \## Technology Stack

# 

# \- AWS EC2

# \- AWS IAM

# \- AWS Systems Manager

# \- GitHub OIDC

# \- Terraform

# \- GitHub Actions

# \- Docker

# \- Docker Compose

# \- Nginx

# \- Gunicorn

# \- Flask

# \- PostgreSQL

# \- Ubuntu Linux

# 

# \## Application Architecture

# 

# The application runs as three Docker Compose services:

# 

# \- `nginx` — public reverse proxy on port 80

# \- `app` — Flask application running with Gunicorn

# \- `db` — PostgreSQL database

# 

# Only Nginx is exposed publicly.

# 

# Gunicorn port `5000` and PostgreSQL port `5432` remain inside the Docker network.

# 

# \## Health Checks

# 

# The application provides:

# 

# \- `/health` — application health

# \- `/db-health` — PostgreSQL connectivity

# \- `/visits` — persistent database write/read test

# 

# Both the application and PostgreSQL services include Docker health checks.

# 

# \## Persistent Database Storage

# 

# PostgreSQL uses a Docker named volume.

# 

# Persistence was tested by:

# 

# 1\. Creating records through `/visits`

# 2\. Stopping and recreating the containers

# 3\. Accessing `/visits` again

# 4\. Confirming the counter continued instead of resetting

# 

# This verifies that database data survives container recreation.

# 

# \## CI/CD

# 

# Every push to `main` triggers GitHub Actions.

# 

# The pipeline contains three stages:

# 

# \### 1. Terraform Validation

# 

# GitHub Actions runs:

# 

# ```bash

# terraform fmt -check

# terraform init -backend=false

# terraform validate

# ```

# 

# \### 2. Docker Integration Tests

# 

# The pipeline:

# 

# \- validates Docker Compose

# \- builds the containers

# \- starts Nginx, Flask, and PostgreSQL

# \- checks application health

# \- checks database health

# \- performs database write/read tests

# \- cleans up the test environment

# 

# \### 3. AWS Deployment

# 

# Deployment only starts after both validation jobs succeed.

# 

# The deployment flow is:

# 

# ```text

# GitHub Actions

# &#x20;     ↓

# GitHub OIDC

# &#x20;     ↓

# Temporary AWS IAM credentials

# &#x20;     ↓

# AWS Systems Manager

# &#x20;     ↓

# EC2

# &#x20;     ↓

# git fetch / reset

# &#x20;     ↓

# docker compose up -d --build

# &#x20;     ↓

# health verification

# ```

# 

# No permanent AWS access keys are stored in GitHub.

# 

# The EC2 SSH private key is also not stored in GitHub.

# 

# \## AWS Security

# 

# \### Security Group

# 

# Inbound access:

# 

# \- Port `22` — trusted administrator IP only

# \- Port `80` — public HTTP access

# 

# Not exposed publicly:

# 

# \- Gunicorn `5000`

# \- PostgreSQL `5432`

# 

# \### EC2

# 

# The EC2 instance uses:

# 

# \- Ubuntu Server

# \- `t3.micro`

# \- encrypted `gp3` EBS storage

# \- IMDSv2 required

# \- AWS Systems Manager integration

# 

# \### IAM

# 

# The EC2 instance has an IAM role with:

# 

# ```text

# AmazonSSMManagedInstanceCore

# ```

# 

# GitHub Actions uses a separate IAM role through OIDC.

# 

# The deployment role is restricted to the project repository and the `main` branch.

# 

# \## Terraform

# 

# The AWS infrastructure is managed with Terraform.

# 

# Terraform manages:

# 

# \- EC2 instance

# \- Security Group

# \- EC2 IAM role

# \- EC2 instance profile

# \- SSM policy attachment

# \- GitHub OIDC provider

# \- GitHub deployment IAM role

# \- GitHub deployment policy

# \- IAM policy attachment

# 

# The infrastructure was originally created manually and then imported into Terraform.

# 

# After import and configuration, Terraform reached zero drift:

# 

# ```text

# No changes. Your infrastructure matches the configuration.

# ```

# 

# \## Terraform Structure

# 

# ```text

# infra/

# └── terraform/

# &#x20;   ├── main.tf

# &#x20;   ├── providers.tf

# &#x20;   ├── variables.tf

# &#x20;   ├── outputs.tf

# &#x20;   └── .terraform.lock.hcl

# ```

# 

# Terraform state and `.tfvars` files are excluded from Git.

# 

# \## Terraform Outputs

# 

# Run:

# 

# ```bash

# terraform output

# ```

# 

# Outputs include:

# 

# \- EC2 instance ID

# \- current public IP

# \- public DNS

# \- Security Group ID

# \- EC2 SSM role ARN

# \- GitHub deployment role ARN

# 

# The EC2 public IP may change after stopping and starting the instance.

# 

# The CI/CD deployment does not depend on the public IP. It uses the EC2 instance ID through AWS Systems Manager.

# 

# \## Run Locally

# 

# Create the environment file:

# 

# ```bash

# cp .env.example .env

# ```

# 

# Start the stack:

# 

# ```bash

# docker compose up -d --build

# ```

# 

# Check services:

# 

# ```bash

# docker compose ps

# ```

# 

# Application:

# 

# ```text

# http://localhost

# ```

# 

# Application health:

# 

# ```text

# http://localhost/health

# ```

# 

# Database health:

# 

# ```text

# http://localhost/db-health

# ```

# 

# Persistent database test:

# 

# ```text

# http://localhost/visits

# ```

# 

# \## Useful Commands

# 

# View application logs:

# 

# ```bash

# docker compose logs app

# ```

# 

# View Nginx logs:

# 

# ```bash

# docker compose logs nginx

# ```

# 

# View PostgreSQL logs:

# 

# ```bash

# docker compose logs db

# ```

# 

# Stop the stack:

# 

# ```bash

# docker compose down

# ```

# 

# Do not use `docker compose down -v` unless you intentionally want to delete the PostgreSQL data volume.

# 

# \## Project Status

# 

# \- Dockerized application ✅

# \- Nginx reverse proxy ✅

# \- PostgreSQL persistence ✅

# \- Health checks ✅

# \- AWS EC2 deployment ✅

# \- GitHub Actions integration tests ✅

# \- OIDC authentication ✅

# \- AWS SSM deployment ✅

# \- Terraform Infrastructure as Code ✅

# \- Terraform CI validation ✅

# 

# HTTPS is not configured because this portfolio environment uses a temporary EC2 public address rather than a permanent domain.

