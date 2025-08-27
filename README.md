## AWS CDK Infrastructure Project (Python)

This project provisions a simple web infrastructure using **AWS CDK in Python**.
It demonstrates Infrastructure as Code (IaC) and deploys a production-style environment.

## Architecture
The stack includes:
- **VPC** with public & private subnets
- **ECS Cluster** with Fargate service
- **Application Load Balancer (ALB)** for HTTP/HTTPS traffic
- **S3 Bucket** for static assets (private by default)
- **CloudFormation Outputs** → ALB DNS name and S3 bucket name

## Prerequisites
- AWS Account with configured **AWS CLI** credentials
- **Node.js** (for AWS CDK CLI)
- **Python 3.9+** with `venv`

Install CDK globally if not already:
npm install -g aws-cdk


Setup & Deployment

1. Clone the repository :
   git clone https://github.com/hishilathapa/aws-cdk-infra.git   cd aws-cdk-infra

2. Create and activate virtual environment :
     # Mac/Linux : python -m venv .venv   source .venv/bin/activate
   
     # Windows PowerShell : python -m venv .venv   .venv\Scripts\Activate.ps1

3. Install dependencies :
    pip install -r requirements.txt

4. Bootstrap CDK (first time only) :
    cdk bootstrap

5. Deploy the stack :
    cdk deploy

6. Cleanup to avoid AWS charges :
    cdk destroy

##Outputs
After deployment, CDK will print:
ALB DNS Name → use this in a browser to test the service
S3 Bucket Name → private bucket for static asset storage


