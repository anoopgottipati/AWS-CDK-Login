import os
import json
import boto3
import re


table_name = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def handler(event, context):
    
    username = event['pathParameters']['username']
    filename = getFileName(event)
    file_content = getFileContent(event)
    
    s3_key = f'{username}/{filename}'
    
    s3.put_object(
        Bucket=bucket_name,
        Body=file_content,
        Key=s3_key,
    )
    
    response = table.get_item(
        Key={
        'username': username
        }
    )
    
    user = response['Item']
    
    s3_key_list = user.get('s3_bucket_key_list', [])
    
    if s3_key not in s3_key_list:
        s3_key_list.append(s3_key)
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(f"file with name {filename} is already present")
        }
    
    table.update_item(
            Key={
                'username': username
            },
            UpdateExpression='SET s3_bucket_key_list = :s3_key_list',
            ExpressionAttributeValues={
                ':s3_key_list': s3_key_list
            }
        )
    
    return {
            'statusCode': 200,
            'body': json.dumps("file uploded")
        }


def getFileName(event):
    body = event['body']
    pattern = r'Content-Disposition: form-data;.*?filename="([^"]+)"'
    # Search for the pattern in the data
    match = re.search(pattern, body, re.IGNORECASE)
    filename = match.group(1)
    return filename

def getFileContent(event):
    body = event['body']
    content_pattern = rf'Content-Type: [^\r\n]+\r\n\r\n([\s\S]*?)\r\n----------------------------'
    content_match = re.search(content_pattern, body, re.IGNORECASE)
    file_content = content_match.group(1).strip()
    return file_content