from constructs import Construct
from aws_cdk import (
    aws_ec2 as _ec2,
    aws_ecs as _ecs,
    aws_ecs_patterns as _ecs_patterns,
    aws_ecr as _ecr,
    aws_route53 as _route53,
    aws_certificatemanager as _cert_manager,
    aws_route53_targets as _targets,
    aws_elasticloadbalancingv2 as _elasticloadbalancingv2,
)
from aws_cdk.core import Stack, Duration

from src.config import settings

LOCAL_NETWORK = settings.LOCAL_NETWORK_CIDR


class ContainerizedGraphQLAPIStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_name = settings.APP_NAME.lower().replace(" ", "-")
        api_resource_prefix = f"{api_name}-{settings.ENV_TYPE.lower()}"
        image_name = settings.APP_NAME.lower().replace(" ", "")

        # Environment variables required by container
        env_var = {
            "DB_URL": settings.DB_URL,
            "DB_NAME": settings.DB_NAME,
            "HOST": settings.HOST,
            "PORT": str(settings.PORT),  # must be string
        }

        # Use the bookapi image from private book-api ECR repository
        repo = _ecr.Repository.from_repository_name(
            self, image_name, repository_name=api_name
        )

        image = _ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=_ecs.EcrImage.from_ecr_repository(repository=repo),
            container_name=api_resource_prefix,
            container_port=settings.PORT,
            environment=env_var,  # required or else the service will crash,
        )

        # Create the VPC with two availability zones
        vpc = _ec2.Vpc(
            self,
            "BookApiStackVPC",
            max_azs=2,  # Default is all AZs
        )

        # Uncomment the following to retrieve VPC from Name
        # Hint: Look at VPC entries for details
        # vpc = _ec2.Vpc.from_lookup(self, 'BookApiStackVPC', vpc_name="ExistingVPCName")

        # Add the interface for ECR
        vpc.add_interface_endpoint(
            "EcrDockerEndpoint", service=_ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER
        )

        # Create Security Groups and attach to VPC
        sg = _ec2.SecurityGroup(
            self,
            id=f"{api_resource_prefix}sg-1",
            vpc=vpc,
            allow_all_outbound=True,
            description=f"{api_resource_prefix}-security-group",
        )

        # Option to allow any connection on HTTPS
        # Use caution with this, it can open your API vulnerabilities
        # Note: No SSH is permitted with this security group on any port
        # and ingress for this stack is set to HTTPs only
        # sg.add_ingress_rule(
        #     peer=_ec2.Peer.any_ipv4(),
        #     connection=_ec2.Port.tcp(443),
        #     description="https",
        # )

        # Restricting HTTP and HTTPS to Local Network Only
        # Expand this to allow a list of external networks
        sg.add_ingress_rule(
            peer=_ec2.Peer.ipv4(LOCAL_NETWORK),
            connection=_ec2.Port.tcp(443),
            description="https-local",
        )

        # sg.add_ingress_rule(
        #     peer=_ec2.Peer.ipv4(LOCAL_NETWORK),
        #     connection=_ec2.Port.tcp(80),
        #     description="http-local",
        # )

        cluster = _ecs.Cluster(
            self,
            f"{api_resource_prefix}-cluster",
            vpc=vpc,
        )

        # The following needs to be your desired hosted zone and domain
        hosted_zone = _route53.HostedZone.from_lookup(
            self, f"{image_name}-hosted-zone", domain_name=settings.DOMAIN_NAME
        )

        # Create the certificate for the above domain
        certificate = _cert_manager.Certificate(
            self,
            f"{image_name}-certificate",
            domain_name=f"*.{settings.DOMAIN_NAME}",
            validation=_cert_manager.CertificateValidation.from_dns(hosted_zone),
        )

        lb = _elasticloadbalancingv2.ApplicationLoadBalancer(
            self,
            f"{image_name}-load-balancer",
            vpc=vpc,
            internet_facing=True,
            security_group=sg,
        )

        # Setup for BookAPI Fargate Service - A Serverless / Pay-as-you-go Setup
        # The open_listener set to True will set Ingress for 80 and 443 with 0.0.0.0/0
        service = _ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            id=api_resource_prefix,
            service_name=api_resource_prefix,
            cluster=cluster,  # Required
            cpu=256,  # Default
            desired_count=1,  # Default is 1
            task_image_options=image,
            memory_limit_mib=512,  # Default
            certificate=certificate,
            redirect_http=True,
            open_listener=False,  # Set to true for full open access on Ports 443/80
            security_groups=[sg],
            load_balancer=lb,
            protocol=_elasticloadbalancingv2.ApplicationProtocol.HTTPS,
        )

        record_target = _route53.RecordTarget.from_alias(
            _targets.LoadBalancerTarget(service.load_balancer)
        )
        _route53.ARecord(
            self,
            f"{image_name}-dns-record",
            zone=hosted_zone,
            record_name="api",
            ttl=Duration.minutes(1),
            target=record_target,
        )

        # Uncomment the following to wire up your own health check
        # service.target_group.configure_health_check(
        #     port=str(settings.PORT),
        #     path='/',
        # )
