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
