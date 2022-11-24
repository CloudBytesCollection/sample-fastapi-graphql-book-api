import aws_cdk as cdk

from book_api_stack import ContainerizedGraphQLAPIStack

from src.config import settings

app = cdk.App()

ContainerizedGraphQLAPIStack(
    app,
    "ContainerizedGraphQLAPIStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    env=cdk.Environment(account=settings.AWS_ACCOUNT, region=settings.AWS_REGION),
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

app.synth()
