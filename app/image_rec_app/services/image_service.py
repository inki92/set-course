""" Image Service Module. """

import os
from datetime import datetime
from flask import Response, jsonify, request
from image_rec_app.clients.storage_client import ImageStorageClient
from image_rec_app.clients.db_client import ImageDatabaseClient
from image_rec_app.models.image_model import Image
from image_rec_app.models.image_status_model import ImageStatus


class ImageService:
    """ Image Service Class. """
    storage_client = ImageStorageClient()
    db_client = ImageDatabaseClient()

    @staticmethod
    def create(file=None):
        """
        Static method for uploading an image to
        the S3 bucket and creates a corresponding database entry.
        """
        if file is None:
            return Response("No file provided", status=400)

        try:
            file_binary = file.read()
            # upload file to the s3
            result = ImageService.storage_client.create(file_binary)

            file_id = result['file_id']
            file_size = result['file_size']

            bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
            if not bucket_name:
                raise EnvironmentError(
                    "AWS_S3_BUCKET_NAME environment variable not set"
                )

            # create Image record
            image_record = Image(
                ImageName=file_id,
                ObjectPath=f"S3://{bucket_name}/{file_id}",
                ObjectSize=str(file_size),
                LabelValue=[],
                Status=ImageStatus.NEW
            )

            # add record via db_client
            db_response = ImageService.db_client.create(image_record)

            if db_response != 200:
                return Response("Failed to create database record", status=500)

            return Response(f"Image uploaded: ID: {file_id}", status=200)

        except Exception as e:
            return Response(f"Internal server error: {str(e)}", status=500)

    @staticmethod
    def get(id):
        """ Method for retrieving image metadata based on ID."""
        try:
            image = ImageService.db_client.read(id)

            # image checking
            if not image:
                return Response("Image not found", status=404)

            # create json responce
            try:
                metadata = {
                    "ImageName": image.ImageName,
                    "ObjectPath": image.ObjectPath,
                    "ObjectSize": image.ObjectSize,
                    "TimeAdded": image.TimeAdded.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if isinstance(image.TimeAdded, datetime)
                    else image.TimeAdded,
                    "TimeUpdated": image.TimeUpdated.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if isinstance(image.TimeUpdated, datetime)
                    else image.TimeUpdated,
                    "LabelValue": image.LabelValue,
                    "Status": image.Status.value
                    if hasattr(image.Status, 'value')
                    else image.Status
                }
            except Exception as e:
                metadata = {
                    "ImageName": image.ImageName,
                    "Status": image.Status.value
                    if hasattr(image.Status, 'value')
                    else image.Status
                }
                # debug
                print(e)

            return jsonify(metadata), 200

        except Exception as e:
            return Response(f"Internal server error: {str(e)}", status=500)

    @staticmethod
    def delete(id):
        """ Method for deleting an image by ID. """
        try:
            # delete from s3
            result_s3 = ImageService.storage_client.delete(id)
            result_db = ImageService.db_client.delete(id)
            if "Error" in result_s3 or result_db:
                return Response(
                    f"S3 operation result: {result_s3}, "
                    f"DB result: {result_db}",
                    status=404
                )

            return Response(
                "Image deleted successfully.",
                status=200
            )
        except Exception as e:
            return Response(
                f"Internal server error: {str(e)}",
                status=500
            )

    @staticmethod
    def search(label_query=None):
        """
        Method for searching images by label.
        similar curl command:
            curl -X GET "http://url/image?label_query=A
        """
        try:
            if not label_query:
                return Response(
                    "label_query is required for search.",
                    status=400
                )

            matching_ids = ImageService.db_client.search(label_query)

            if not matching_ids:
                return jsonify(
                    {"message": "No images found with the specified label."}
                ), 404

            return jsonify({"matching_ImageNames": matching_ids}), 200
        except Exception as e:
            return Response(f"Internal server error: {str(e)}", status=500)

    @staticmethod
    def download(id):
        """ Method for downloading an image file from S3 bucket by ID."""
        try:
            file_binary, error = ImageService.storage_client.read(id)
            if error:
                return Response("Image not found", status=404)
            response = Response(
                file_binary,
                status=200,
                content_type="application/octet-stream"
            )
            response.headers["Content-Disposition"] = \
                f"attachment; filename={id}"
            return response
        except Exception as e:
            return Response(
                f"Internal server error: {str(e)}",
                status=500,
                content_type="text/plain"
            )

    @staticmethod
    def update_file_image(id, file=None):
        """
        Method for updating an existing image
        in the S3 bucket with a new file.
        """
        if file is None:
            return Response("No file provided", status=400)

        try:
            # read new file
            file_binary = file.read()
            result = ImageService.storage_client.update(file_binary, id)
            # check for error in the response
            if "Error" in result:
                return Response(result, status=404)
            return Response(result, status=200)
        except Exception as e:
            return Response(f"Internal server error: {str(e)}", status=500)

    @staticmethod
    def update_data_image(id):
        """ Method for updating image data in the database by ID."""
        try:
            # get current image from db
            current_image = ImageService.db_client.read(id)
            if not current_image:
                return Response("Image not found", status=404)

            # get data from the request
            data = request.json
            labels = data.get('LabelValue')
            status = data.get('Status')
            object_path = data.get('ObjectPath')

            # create dict with new fields
            fields_to_update = {}
            if labels is not None:
                fields_to_update['LabelValue'] = labels
            if status is not None:
                fields_to_update['Status'] = status
            if object_path is not None:
                fields_to_update['ObjectPath'] = object_path

            # debug
            print(f"Fields to update: {fields_to_update}")

            # check for new fields
            if not fields_to_update:
                return Response("No fields to update", status=400)

            # update data
            ImageService.db_client.update(current_image, **fields_to_update)
            print(f"Updating image ImageName: {id}")
            print(f"Received LabelValue: {labels}")
            print(f"Received Status: {status}")
            print(f"Received ObjectPath: {object_path}")

            return Response(status=204)  # 204 No Content
        except Exception as e:
            return Response(f"Internal server error: {str(e)}", status=500)
