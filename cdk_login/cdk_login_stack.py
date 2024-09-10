from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    RemovalPolicy,
)
from constructs import Construct

class CdkLoginStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #dynamo db for user details
        users_table = dynamodb.Table(
            self, 'usersTable',
            partition_key=dynamodb.Attribute(
                name='username',
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )
        
        userOperations_lambda = _lambda.Function(
            self, 'userOperationsLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='usersOperations.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'TABLE_NAME': users_table.table_name
            }
        )
        
        users_table.grant_read_write_data(userOperations_lambda)
        
        api = apigateway.RestApi(
            self, "usersApi",
        )
        users_resourse = api.root.add_resource('users')
        
        users_resourse.add_method("POST", apigateway.LambdaIntegration(userOperations_lambda))
        users_resourse.add_method("PUT", apigateway.LambdaIntegration(userOperations_lambda))
        users_resourse.add_method("DELETE", apigateway.LambdaIntegration(userOperations_lambda))
        users_resourse.add_method("GET", apigateway.LambdaIntegration(userOperations_lambda))