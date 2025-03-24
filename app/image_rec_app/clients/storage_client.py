""" S3 client for image_rec_app. """

import os
import uuid
import boto3
from botocore.exceptions import ClientError


class ImageStorageClient:
    """ AWS S3 Client."""

    def __init__(self):
        """ AWS S3 Client initialization. """
        s3_bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        s3_client = boto3.resource("s3")
        self.bucket = s3_client.Bucket(s3_bucket_name)

    def create(self, file_binary):
        """
        Method for uploading binary file
        to the root of the S3 bucket with a unique name.
        """
        file_id = str(uuid.uuid4())  # uniq name generation

        try:
            # upload file to the root
            self.bucket.put_object(Body=file_binary, Key=file_id)
            file_size = len(file_binary)  # file size in bytes
            return {
                "file_id": file_id,
                "file_size": file_size
            }
        except ClientError as e:
            return {"error": f"Error uploading file: {e}"}

    def read(self, path):
        """
        Method for downloading file from S3 bucket
        and return as binary.
        """
        try:
            file_obj = self.bucket.Object(path)
            file_binary = file_obj.get()['Body'].read()
            return file_binary, None  # none for exception
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None, f"Error: File at {path} does not exist."
            else:
                return None, f"Error downloading file: {e}"

    def update(self, file_binary, path):
        """
        Method for replacing existing file in
        the S3 bucket at specified path.
        """
        if not file_binary:
            return "Please, provide the file."
        try:
            # del old before uploading new
            self.bucket.Object(path).load()
            self.bucket.Object(path).delete()
            self.bucket.put_object(Body=file_binary, Key=path)
            return f"File updated successfully at {path}."
        except ClientError as e:
            return f"Error updating file: {e}"

    def delete(self, path):
        """
        Method for deleting file from the S3 bucket
        at the specified path.
        """
        try:
            self.bucket.Object(path).load()  # check existing
            self.bucket.Object(path).delete()
            return f"File deleted successfully from {path}."
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return f"Error: File at {path} does not exist."
            else:
                return f"Error deleting file: {e}"
