from os import path
from constructs import Construct
from aws_cdk import ( 
Stack,
CfnOutput,
aws_lambda as lmb,
aws_apigateway as apigw,
)

class PipelinesWebinarStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)

        handler = lmb.Function(self, 'Handler',
            runtime=lmb.Runtime.PYTHON_3_7,
            handler='handler.handler',
            code=lmb.Code.from_asset(path.join(this_dir, 'lambda')))

        gw = apigw.LambdaRestApi(self, 'Gateway',
            description='Endpoint for a simple Lambda-powered web service',
            handler=handler.current_version)

        self.url_output = CfnOutput(self, 'Url',
            value=gw.url)

