import json
import boto3

s3_client=boto3.client('s3')

def lambda_handler(event, context):
    print(f"Lambda function Updated successful!")

    for record in event['Records']:
        bucket_name= record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']
        print(f"New file detected: {file_key} in bucket {bucket_name}")

        new_key = file_key.replace("raw-data/", "processed-data/")
        s3_client.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'key': file_key},
            Key=new_key
        )

        s3_client.delete_object(Bucket=bucket_name, Key=file_key)

        print(f"file moved to {new_key}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('File moved successfully')
    }