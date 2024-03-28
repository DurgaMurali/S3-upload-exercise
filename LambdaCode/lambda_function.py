import json
import boto3, logging

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
bikeTable = dynamodb.Table('e-bike-table')

def lambda_handler(event, context):
    print(event)
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_name = event['Records'][0]['s3']['object']['key']
    
    # eventTime is the time the event is triggered and not the object created time in S3. Therefore using head_object for metadata
    #file_size = event['Records'][0]['s3']['object']['size']
    #date_time = event['Records'][0]['eventTime']
    
    head_response = s3.head_object(Bucket=bucket_name, Key=object_name)
    
    print(head_response)
    print("last-modified : " + head_response['ResponseMetadata']['HTTPHeaders']['last-modified'])
    print("size : " + head_response['ResponseMetadata']['HTTPHeaders']['content-length'])
    
    file_size = head_response['ResponseMetadata']['HTTPHeaders']['content-length']
    date_time = head_response['ResponseMetadata']['HTTPHeaders']['last-modified']
    
    object_name = object_name.split('/')
    date_time = date_time.split()
    date = date_time[1] + " " + date_time[2] + " " + date_time[3]
    time = date_time[4] + " " + date_time[5]
    
    db_response = bikeTable.put_item(
        Item={
            'bike-name': str(object_name[1]),
            'date-created': str(date),
            'time-created': str(time),
            'file-size': str(file_size)
        })
    
    return {
        'statusCode': 200,
        'body': json.dumps(str(object_name[1]) + ' copied to S3 bucket: ' + str(bucket_name))
    }
