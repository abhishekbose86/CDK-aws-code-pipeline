#!/usr/bin/env python3

from aws_cdk import App,Environment

from pipelines_webinar.pipeline_stack import PipelineStack

PIPELINE_ACCOUNT = '782160816199'

app = App()
PipelineStack(app, 'PipelineStack', env = Environment (account = PIPELINE_ACCOUNT, region = "us-east-2" ))

app.synth()
