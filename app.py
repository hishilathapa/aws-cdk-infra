#!/usr/bin/env python3
import aws_cdk as cdk
import os
from stack import WebInfraStack

app = cdk.App()
WebInfraStack(app, "WebInfraStack",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)
app.synth()
