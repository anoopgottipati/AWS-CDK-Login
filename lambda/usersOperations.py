import os
import json
import boto3


table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def handler(event, context):
    
    http_method = event['httpMethod']
    
    if http_method == "POST":
        return addUser(event)
    if http_method == "PUT":
        return updateUser(event)
    if http_method == "DELETE":
        return deleteUser(event)
    if http_method == "GET":
        return displayUser(event)

def addUser(event):
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
    
def updateUser(event):
    body = json.loads(event['body'])
    username = body['username']
    password = body['password']
    newPassword = body['newPassword']
    
    # Check if the item exists
    response = table.get_item(Key={'username': username})
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps('User not found')
        }
    
    if password == response['Item'].get('password'):
        table.update_item(
            Key={
                'username': username
            },
            UpdateExpression='SET password = :newPassword',
            ExpressionAttributeValues={
                ':newPassword': newPassword
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Password changed successfully')
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Wrong password')
        }

def deleteUser(event):
    body = json.loads(event['body'])
    username = body['username']
    password = body['password']
    
    # Check if the item exists
    response = table.get_item(Key={'username': username})
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps('User not found')
        }
    
    if password == response['Item'].get('password'):
        table.delete_item(
            Key={
            'username': username
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('User deleted successfully')
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Wrong password')
        }

def displayUser(event):
    response = table.scan()
    data = response['Items']
    
    return {
            'statusCode': 200,
            'body': json.dumps(data)
        }