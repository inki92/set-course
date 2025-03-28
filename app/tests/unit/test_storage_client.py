""" Tests for AWS S3 storage client. """

from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from image_rec_app.clients.storage_client import ImageStorageClient


def test_create_image_success(client, storage_client):
    """ Create storage object."""
    # Arrange
    file_binary = b"test binary data"
    # Act
    result = storage_client.create(file_binary)
    # Assert
    storage_client.bucket.put_object.assert_called_once()
    assert 'file_id' in result
    assert len(result['file_id']) > 0
    assert result['file_size'] == len(file_binary)


def test_create_image_failure(storage_client):
    """ Create storage object with client error. """
    # Arrange
    storage_client.bucket.put_object.side_effect = ClientError(
        {"Error": {"Code": "500", "Message": "Internal Server Error"}},
        "PutObject"
    )
    file_binary = b"test binary data"

    # Act
    result = storage_client.create(file_binary)

    # Assert
    assert "Error uploading file" in result["error"]


def test_read_image_success(storage_client):
    """ Read storage object."""
    # Arrange
    mock_file_binary = b"mock binary data"
    storage_client.bucket.Object.return_value.get.return_value = {
        'Body': MagicMock(read=MagicMock(return_value=mock_file_binary))
    }
    path = "mock/path/to/image.jpg"

    # Act
    result, error = storage_client.read(path)

    # Assert
    assert result == mock_file_binary
    assert error is None


def test_read_image_not_found(storage_client):
    """ Read empty file in the storage. """
    # Arrange
    storage_client.bucket.Object.return_value.get.side_effect = ClientError(
        {"Error": {"Code": "404", "Message": "Not Found"}},
        "GetObject"
    )
    path = "mock/path/to/missing_image.jpg"

    # Act
    result, error = storage_client.read(path)

    # Assert
    assert result is None
    assert "does not exist" in error


def test_update_image_success(storage_client):
    """ Update storage object. """
    # Arrange
    file_binary = b"updated binary data"
    path = "mock/path/to/image.jpg"

    # Act
    result = storage_client.update(file_binary, path)

    # Assert
    storage_client.bucket.Object(path).delete.assert_called_once()
    storage_client.bucket.put_object.assert_called_once()
    assert result == f"File updated successfully at {path}."


def test_update_image_failure(storage_client):
    """ Update storage object with the client error. """
    # Arrange
    file_binary = b"updated binary data"
    path = "mock/path/to/image.jpg"
    storage_client.bucket.Object(path).delete.side_effect = ClientError(
        {"Error": {"Code": "500", "Message": "Delete Failed"}},
        "DeleteObject"
    )

    # Act
    result = storage_client.update(file_binary, path)

    # Assert
    assert "Error updating file" in result


def test_delete_image_success(storage_client):
    """ Delete storage object. """
    # Arrange
    path = "mock/path/to/image.jpg"

    # Act
    result = storage_client.delete(path)

    # Assert
    storage_client.bucket.Object(path).load.assert_called_once()
    storage_client.bucket.Object(path).delete.assert_called_once()
    assert result == f"File deleted successfully from {path}."
