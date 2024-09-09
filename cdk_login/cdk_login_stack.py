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
        
        create_api = apigateway.LambdaRestApi(
            self, "createUsersApi",
            handler=addUsers_lambda,
        )
        create_api.root.add_method("POST")
        
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
        
        delete_api = apigateway.LambdaRestApi(
            self, "deleteUsersApi",
            handler=deleteUsers_lambda,
        )
        delete_api.root.add_method("DELETE")
        
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
        update_api = apigateway.LambdaRestApi(
            self, "updateUsersApi",
            handler=updateUsers_lambda,
        )
        update_api.root.add_method("PUT")
        
