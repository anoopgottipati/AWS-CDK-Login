This project is serveless login system which uses Lambda, DynamoDB, API gateway and s3.The stack provides functionalities to create, delete, and update user credentials through RESTful APIs and to upload files to s3.

Features

    UserOperations: create, update, delete, display users
    filesOperations: upload files to s3

Components

    DynamoDB Table: Stores user details with username as the partition key.
    AWS Lambda Functions:
        userOperations: user operations
        fileOperations: to upload files and update s3 key in dynamodb
    API Gateway: APIs for interacting with the Lambda functions:
        /users
        POST, PUT, GET, DELETE
        /users/{username}/files
        POST

Directory Structure

    lambda/: Contains Lambda function code.
        userOperations.py: Handler for user operation.
        fileOperations.py: Handler for uploding files.
