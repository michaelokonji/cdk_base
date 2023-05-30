from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
    Stack
)
from constructs import Construct

class SecurityStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc:ec2.Vpc,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

# Security group for use by Lambda functions
        lambda_sg = ec2.SecurityGroup(self, "lambdasg",
            vpc=vpc,
            security_group_name="lambda-sg",
            description="SG for Lambda Function",
            allow_all_outbound=True
        )

# Security Group for the Bastion Host
        self.bastion_sg = ec2.SecurityGroup(self, "bastionsg",
            vpc=vpc,
            security_group_name="bastion-sg",
            description="SG for Bastion host",
            allow_all_outbound=True
        )
        self.bastion_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="SSH Access for bastion host"
        )

# Create an IAM role for the Lambda functions
        lambda_role = iam.Role(self, "lamdarole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="lambda-role",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name="service-role/AWSLambdaBasicExecutionRole")
            ]
        )
        lambda_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=['s3:*', 'rds:*'],
                resources=['*'],
                effect=iam.Effect.ALLOW
            )
        )

# Creating SSM Paramter for lambda_sg
        ssm.StringParameter(self, "lambda_sg_ssm",
                parameter_name="/"+prj_name+"/"+env_name+"/lambda-sg-id",
                string_value=lambda_sg.security_group_id
            )
        
# Creating SSM Paramter for lambda_role ARN
        ssm.StringParameter(self, "lambda_role_arn_ssm",
                parameter_name="/"+prj_name+"/"+env_name+"/lambda-role-arn",
                string_value=lambda_role.role_arn
            )
        
# Creating SSM Paramter for lambda_role Name
        ssm.StringParameter(self, "lambda_role_name_ssm",
                parameter_name="/"+prj_name+"/"+env_name+"/lambda-role-name",
                string_value=lambda_role.role_name
            )


