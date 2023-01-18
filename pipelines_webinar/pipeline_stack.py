from constructs import Construct
from aws_cdk import ( 
Stack,
SecretValue,
aws_codepipeline as codepipeline,
pipelines
)

from .webservice_stage import WebServiceStage

APP_ACCOUNT = '782160816199'

class PipelineStack(Stack):
  def __init__(self, scope: Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    source_artifact = codepipeline.Artifact()
    
    pipeline = pipelines.CodePipeline(self, 'Pipeline',
      pipeline_name='WebinarPipeline',

      synth=pipelines.ShellStep("Synth",
        input=pipelines.CodePipelineSource.git_hub("abhishekbose86/CDK-aws-code-pipeline", "main",
        authentication=SecretValue.secrets_manager("github-token")),
        commands=[
          'npm install -g aws-cdk && pip install -r requirements.txt',
          'pytest unittests',
          'cdk synth'
        ]
    ))

    pre_prod_app = WebServiceStage(self, 'Pre-Prod', env={
      'account': APP_ACCOUNT,
      'region': 'us-east-2',
    })
    pipeline.add_stage(pre_prod_app)
    pipeline.add_stage(WebServiceStage(self, 'Prod', env={
      'account': APP_ACCOUNT,
      'region': 'us-east-2',
    }))



