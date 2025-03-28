import os
import json
import time
import boto3
from datetime import datetime

rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")
table_name = os.environ['DYNAMODB_TABLE_NAME']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    try:
        for event_record in event["Records"]:
            body = json.loads(event_record["body"])
            message = json.loads(body["Message"])

            for record in message["Records"]:
                bucket = record["s3"]["bucket"]["name"]
                key = record["s3"]["object"]["key"]

            try:
                response = rekognition.detect_labels(
                    Image={"S3Object": {"Bucket": bucket, "Name": key}}
                )
            except Exception as e:
                print(f"Rekognition error: {str(e)}")
                raise

            labels = [label["Name"] for label in response["Labels"]]
            new_labels_list = []
            if labels:
                for label in labels:
                    new_labels_list.append(label)
                status = "RECOGNITION_COMPLETED"
            else:
                status = "RECOGNITION_FAILED"

            max_wait_time = 10
            elapsed_time = 0

            while elapsed_time < max_wait_time:
                try:
                    response = table.get_item(Key={"ImageName": key})
                    if 'Item' in response:
                        break
                    else:
                        print(
                            f"Waiting for record with ImageName {key} "
                            f"to appear in the table..."
                        )
                        time.sleep(1)
                        elapsed_time += 1
                except Exception as e:
                    print(
                        f"Error checking for existence "
                        f"of object {key} in table."
                    )
                    raise
            else:
                print(
                    f"Record with ImageName {key} not found "
                    f"after {max_wait_time} seconds."
                )
                return
            item = response['Item']
            image_metadata = {
                "ImageName": key,
                "ObjectPath": item['ObjectPath'],
                "ObjectSize": item['ObjectSize'],
                "TimeAdded": item['TimeAdded'],
                "TimeUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "LabelValue": new_labels_list,
                "Status": status,
            }
            table.put_item(Item=image_metadata)
    except Exception as e:
        print(
            f"Error processing object {key} "
            f"from bucket {bucket} by "
            f"rekognition service:{e}"
        )
        raise
