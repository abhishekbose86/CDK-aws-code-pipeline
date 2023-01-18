from constructs import Construct
from aws_cdk import ( 
Stack,
SecretValue,
aws_codepipeline as codepipeline,
aws_codepipeline_actions as cpactions,
pipelines
)

from .webservice_stage import WebServiceStage

APP_ACCOUNT = '782160816199'

class PipelineStack(Stack):
  def __init__(self, scope: Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    source_artifact = codepipeline.Artifact()
    cloud_assembly_artifact = codepipeline.Artifact()

    pipeline = pipelines.CodePipeline(self, 'Pipeline',
      cloud_assembly_artifact=cloud_assembly_artifact,
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
    pre_prod_stage = pipeline.add_application_stage(pre_prod_app)
    pre_prod_stage.add_actions(pipelines.ShellScriptAction(
      action_name='Integ',
      run_order=pre_prod_stage.next_sequential_run_order(),
      additional_artifacts=[source_artifact],
      commands=[
        'pip install -r requirements.txt',
        'pytest integtests',
      ],
      use_outputs={
        'SERVICE_URL': pipeline.stack_output(pre_prod_app.url_output)
      }))

    pipeline.add_application_stage(WebServiceStage(self, 'Prod', env={
      'account': APP_ACCOUNT,
      'region': 'us-east-2',
    }))



