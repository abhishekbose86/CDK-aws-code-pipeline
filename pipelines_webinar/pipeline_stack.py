from constructs import Construct
from aws_cdk import ( 
Stack,
Environment,
SecretValue,
aws_codepipeline as codepipeline,
pipelines
)

from .webservice_stage import WebServiceStage

APP_ACCOUNT = '782160816199'

class PipelineStack(Stack):
  def __init__(self, scope: Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    source = pipelines.CodePipelineSource.git_hub("abhishekbose86/CDK-aws-code-pipeline", "main",
        authentication=SecretValue.secrets_manager("github-token"))
    pipeline = pipelines.CodePipeline(self, 'Pipeline',
      pipeline_name='WebinarPipeline',

      synth=pipelines.ShellStep("Synth",
        input = source,
        commands=[
          'npm install -g aws-cdk && pip install -r requirements.txt',
          'pytest unittests',
          'cdk synth'
        ]
    ))

    pre_prod_app = WebServiceStage ( self, 'Pre-Prod',
     env = Environment (account = APP_ACCOUNT, region = "us-east-2" ))
    pre_prod_stage = pipeline.add_stage(pre_prod_app)
    pre_prod_stage.add_post( pipelines.ShellStep ('IntegTest',
      input=source,
      commands=[
        'pip install -r requirements.txt',
        'pytest integtests',
      ],
      use_outputs={
        'SERVICE_URL': pipeline.stack_output(pre_prod_app.url_output)
      }))   



