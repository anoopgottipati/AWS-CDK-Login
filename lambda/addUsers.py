import os
import json
import boto3


table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def handler(event, context):
    body = json.loads(event['body'])
    username = body['username']
    password = body['password']
    
    # Check if the item exists
    response = table.get_item(Key={'username': username})
    if 'Item' in response:
        return {
            'statusCode': 404,
            'body': json.dumps('User already present')
        }
    
    # Store user data in DynamoDB
    table.put_item(
        Item={
            'username': username,
            'password': password
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('User added successfully')
    }

