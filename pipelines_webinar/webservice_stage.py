from aws_cdk import Stage
from constructs import Construct

from .pipelines_webinar_stack import PipelinesWebinarStack

class WebServiceStage(Stage):
  def __init__(self, scope: Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    service = PipelinesWebinarStack(self, 'WebService')

    self.url_output = service.url_output

