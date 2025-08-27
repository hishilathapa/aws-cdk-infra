from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_s3 as s3,
    CfnOutput,
    Stack,
)
from aws_cdk import RemovalPolicy
from constructs import Construct

class WebInfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC: Public + Private subnets, NAT
        vpc = ec2.Vpc(self, "WebAppVpc",
            max_azs=2, 
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public", subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                )
            ]
        )

        # ECS Cluster
        cluster = ecs.Cluster(self, "WebAppCluster", vpc=vpc)
        
        # IAM Role for ECS tasks (access S3, CloudWatch)
        task_role = iam.Role(self, "WebAppTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"),
            ]
        )
        
        # ECS Task Definition
        task_definition = ecs.FargateTaskDefinition(
            self, "WebAppTaskDef", task_role=task_role
        )
        # Example container (replace image URI with your own)
        task_definition.add_container("WebAppContainer",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            memory_limit_mib=512,
            cpu=256,
            port_mappings=[ecs.PortMapping(container_port=80)],
        )

        # ECS Service + ALB + Auto Scaling
        service = ecs.FargateService(
            self, "WebAppService",
            cluster=cluster,
            task_definition=task_definition,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            desired_count=2,
            min_healthy_percent=50,
            max_healthy_percent=200,
            assign_public_ip=False,
        )
        scalable_target = service.auto_scale_task_count(
            min_capacity=2, max_capacity=4
        )

        # Application Load Balancer (ALB)
        lb = elbv2.ApplicationLoadBalancer(self, "ALB",
            vpc=vpc,
            internet_facing=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )
        listener = lb.add_listener("Listener", port=80, open=True)
        listener.add_targets("ECS",
            port=80,
            targets=[service],
            health_check=elbv2.HealthCheck(path="/"),
        )
        # Security Groups, HTTPS and enhanced features can be added as needed
        
        # S3 Bucket for static assets
        bucket = s3.Bucket(self, "WebAppAssetsBucket",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL, # Private by default
            removal_policy=RemovalPolicy.DESTROY,  # Change to RETAIN for prod
            auto_delete_objects=True,                 # Only for demo/testing
        )

        # CloudFormation Outputs
        CfnOutput(self, "ALBDNS", value=lb.load_balancer_dns_name)
        CfnOutput(self, "S3BucketName", value=bucket.bucket_name)

        # Optionally add: RDS, VPC interface endpoints, advanced security

