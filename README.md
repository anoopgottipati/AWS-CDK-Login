This project is serveless login system which uses Lambda, DynamoDB and API gateway.The stack provides functionalities to create, delete, and update user credentials through RESTful APIs.

Features

    Create Users: Add new users with their usernames and passwords.
    Delete Users: Remove existing users from the database.
    Update Passwords: Update the passwords for existing users.

Components

    DynamoDB Table: Stores user details with username as the partition key.
    AWS Lambda Functions:
        createUsersLambdaFunction: Handles the creation of new users.
        deleteUsersLambdaFunction: Manages the deletion of users.
        updateUsersLambdaFunction: Updates user passwords.
    API Gateway: Diiferent RESTful APIs for interacting with the Lambda functions:
        POST / for creating users
        DELETE / for deleting users
        PUT / for updating passwords

Directory Structure

    lambda/: Contains Lambda function code.
        addUsers.py: Handler for creating users.
        deleteUsers.py: Handler for deleting users.
        updateUsers.py: Handler for updating passwords.
