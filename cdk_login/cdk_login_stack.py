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
        
        # 1. creating users
        #Lambda to add user name and password
        addUsers_lambda = _lambda.Function(
            self, 'createUsersLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='addUsers.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'TABLE_NAME': users_table.table_name
            }
        )
        
        #Granting addUsers lambda funtion write permision to dynamo db
        users_table.grant_read_write_data(addUsers_lambda)
        
        api = apigateway.RestApi(
            self, "usersApi",
        )
        users_resourse = api.root.add_resource('users')
        
        users_resourse.add_method("POST", apigateway.LambdaIntegration(addUsers_lambda))
        
        # 2. deleating users
        #Lambda function to delete user
        deleteUsers_lambda = _lambda.Function(
            self, 'deleteUsersLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='deleteUsers.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'TABLE_NAME': users_table.table_name
            }
        )
        
        users_table.grant_read_write_data(deleteUsers_lambda)
        
        users_resourse.add_method("DELETE", apigateway.LambdaIntegration(deleteUsers_lambda))
        
        # 3. update password
        #Lambda function to update password 
        updateUsers_lambda = _lambda.Function(
            self, 'updateUsersLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='updateUsers.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'TABLE_NAME': users_table.table_name
            }
        )
        users_table.grant_read_write_data(updateUsers_lambda)
        
        users_resourse.add_method("PUT", apigateway.LambdaIntegration(updateUsers_lambda))
        
        # 4. Display DynamoDB items
        #Lambda function to get all table items
        displayUsers_lambda = _lambda.Function(
            self, 'displayUsersLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='displayUsers.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'TABLE_NAME': users_table.table_name
            }
        )
        users_table.grant_read_write_data(displayUsers_lambda)
        
        users_resourse.add_method("GET", apigateway.LambdaIntegration(displayUsers_lambda))
