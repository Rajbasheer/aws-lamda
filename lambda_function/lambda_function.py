import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print("🚀 Lambda function Updated successful!")

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']
        print(f"📂 New file detected: {file_key} in bucket {bucket_name}")

        # Ensure the file is inside raw-data/ before processing
        if file_key.startswith("raw-data/"):
            new_key = file_key.replace("raw-data/", "processed-data/")

            try:
                # ✅ Fix: Use copy_object() instead of copy.object()
                s3_client.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': file_key},
                    Key=new_key
                )

                # Delete the original file in raw-data/
                s3_client.delete_object(Bucket=bucket_name, Key=file_key)

                print(f"✅ File successfully moved to {new_key}")

            except Exception as e:
                print(f"❌ Error moving file: {str(e)}")

        else:
            print("⚠️ File is not in raw-data/, skipping.")

    return {
        'statusCode': 200,
        'body': json.dumps('File moved successfully!')
    }
