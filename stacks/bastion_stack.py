from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
    Stack
)
from constructs import Construct

class BastionStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc:ec2.Vpc, sg:ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        bastion_host = ec2.Instance(self, "bastionhost",
            instance_type=ec2.InstanceType("t2.micro"),
            vpc=vpc,
            security_group=sg,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                edition=ec2.AmazonLinuxEdition.STANDARD,
                cpu_type=ec2.AmazonLinuxCpuType.X86_64,
                virtualization=ec2.AmazonLinuxVirt.HVM
            )
        )