import os
import json
import boto3


table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def handler(event, context):
    
    response = table.scan()
    data = response['Items']
    
    return {
            'statusCode': 200,
            'body': json.dumps(data)
        }