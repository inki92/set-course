""" DB client for image_rec_app. """

import os
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from image_rec_app.models.image_model import Image


class ImageDatabaseClient:
    """ AWS DynamoDB Database Client. """

    def __init__(self):
        """ Boto3 client initialization. """
        self.dynamodb = boto3.resource('dynamodb')
        table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME")
        self.table = self.dynamodb.Table(table_name)

    def create(self, image: Image) -> int:
        """ Method for creating Image. """
        item = {
            'ImageName': image.ImageName,
            'ObjectPath': image.ObjectPath,
            'ObjectSize': image.ObjectSize,
            'TimeAdded': image.TimeAdded.strftime("%Y-%m-%d %H:%M:%S"),
            'TimeUpdated': image.TimeUpdated.strftime("%Y-%m-%d %H:%M:%S"),
            'LabelValue': image.LabelValue,
            'Status': image.Status.value  # convert to sting for store
        }

        # debug string
        print("Item to be inserted into DynamoDB:", json.dumps(item, indent=4))

        # insert operation
        try:
            response = self.table.put_item(Item=item)
            resp_value = response['ResponseMetadata']['HTTPStatusCode']
        except ClientError as e:
            print(f"Can't insert: {e.response['Error']['Message']}")
            resp_value = None
        return resp_value

    def read(self, ImageName) -> Image:
        """ Method for reading image object by ID."""
        try:
            response = self.table.get_item(Key={'ImageName': ImageName})
            if 'Item' in response:
                item = response['Item']
                try:
                    image_data = Image(
                        ImageName=item['ImageName'],
                        ObjectPath=item['ObjectPath'],
                        ObjectSize=item['ObjectSize'],
                        TimeAdded=item['TimeAdded'],  # convert to datetime
                        TimeUpdated=item['TimeUpdated'],
                        LabelValue=item['LabelValue'],
                        Status=item['Status']  # convert to status
                    )
                except Exception as e:
                    image_data = Image(
                        ImageName=item['ImageName'],
                        Status=item['Status']
                    )
                    # debug
                    print(f"Something gone wrong: {e}")
            else:
                print("Can't find image.")
                image_data = None
            return image_data
        except ClientError as e:
            print(f"Can't read: {e.response['Error']['Message']}")
            return None

    def update(self, image: Image, **fields_to_update) -> None:
        """
        Method for updating fields in the image and
        updating 'time_updated' field to the current time.
        """
        update_expressions = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        # debug
        print(f"Fields to update: {fields_to_update}")

        for field, value in fields_to_update.items():
            if field not in [
                'ImageName',
                'TimeAdded',
                'TimeUpdated'
            ] and value is not None:
                # prefix for words
                field_name = f"#{field}"
                update_expressions.append(f"{field_name} = :{field}")
                expression_attribute_values[f":{field}"] = value

                # attribute name to expression_attribute_names
                expression_attribute_names[field_name] = field

        # add time_updated
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_expressions.append("TimeUpdated = :TimeUpdated")
        expression_attribute_values[":TimeUpdated"] = current_time

        update_expression = "SET " + ", ".join(update_expressions)

        # debug
        print(f"Update expression: {update_expression}")
        print(f"Expression attribute values: {expression_attribute_values}")
        print(f"Expression attribute names: {expression_attribute_names}")

        # update fields
        try:
            self.table.update_item(
                Key={'ImageName': image.ImageName},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names
            )
            print("Update operation completed successfully.")
        except ClientError as e:
            print(f"Failed to update item: {e.response['Error']['Message']}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def delete(self, ImageName) -> None:
        """ Method for deleting image by ID. """
        try:
            self.table.delete_item(Key={'ImageName': ImageName})
        except ClientError as e:
            print(f"Can't find: {e.response['Error']['Message']}")

    def search(self, label_query: str) -> list:
        """
        Method for finding all records with
        'label_query' in the 'labels' field.
        """
        try:
            response = self.table.scan()
            items = response.get('Items', [])

            matching_ids = [
                item['ImageName'] for
                item in
                items if
                label_query in
                item.get('LabelValue', [])
            ]
            return matching_ids
        except ClientError as e:
            print(f"Can't find: {e.response['Error']['Message']}")
            return []
