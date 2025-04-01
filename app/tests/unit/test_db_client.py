""" Tests for DB Client. """

from datetime import datetime
from unittest.mock import patch, MagicMock
from image_rec_app.models.image_model import Image


def test_create_image_success(client, db_client):
    """ Create DB record. """
    # Arrange
    image = Image(
        ImageName="test_id",
        ObjectPath="path/to/image.jpg",
        ObjectSize=12345,
        TimeAdded=datetime(2025, 3, 1, 10, 0, 0),
        TimeUpdated=datetime(2025, 3, 1, 10, 0, 0),
        LabelValue=["test"],
        Status=MagicMock(value="active")  # MagiMock for status
    )

    db_client.table.get_item.return_value = {}  # return 'not exists'
    db_client.table.put_item.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200}
    }

    # Act
    status_code = db_client.create(image)

    # Assert
    assert status_code == 200
    db_client.table.put_item.assert_called_once()


def test_read_image_success(db_client):
    """ Read DB record. """
    # Arrange
    expected_image = {
        'ImageName': '111',
        'ObjectPath': 'path/to/image.jpg',
        'ObjectSize': 12345,
        'TimeAdded': '2024-01-01 10:00:00',
        'TimeUpdated': '2024-01-01 10:00:00',
        'LabelValue': ['test'],
        'Status': 'active'
    }
    db_client.table.get_item.return_value = {'Item': expected_image}

    # Act
    image = db_client.read('111')

    # Assert
    assert image.ImageName == '111'
    assert image.ObjectPath == 'path/to/image.jpg'
    db_client.table.get_item.assert_called_once_with(Key={'ImageName': '111'})


def test_read_image_not_found(db_client):
    """ Read empty DB record. """
    # Arrange
    db_client.table.get_item.return_value = {}  # return not exists

    # Act
    image = db_client.read('non_existing_id')

    # Assert
    assert image is None
    db_client.table.get_item.assert_called_once_with(
        Key={'ImageName': 'non_existing_id'}
    )


def test_update_image_success(db_client):
    """ Update DB record. """
    # Arrange
    image = Image(
        ImageName='111',
        ObjectPath='path/to/image.jpg',
        ObjectSize=12345,
        TimeAdded=datetime.now(),
        TimeUpdated=datetime.now(),
        LabelValue=['test'],
        Status=MagicMock(value="active")  # MagicMock for the status
    )
    db_client.table.update_item = MagicMock()

    # Act
    db_client.update(image, LabelValue=['updated_test'])

    # Assert
    db_client.table.update_item.assert_called_once()
    args, kwargs = db_client.table.update_item.call_args
    assert kwargs['Key'] == {'ImageName': '111'}
    assert 'SET' in kwargs['UpdateExpression']


def test_delete_image_success(db_client):
    """ Delete DB record."""
    # Arrange
    db_client.table.delete_item = MagicMock()

    # Act
    db_client.delete('111')

    # Assert
    db_client.table.delete_item.assert_called_once_with(
        Key={'ImageName': '111'}
    )


def test_search_images_success(db_client):
    """ Search DB record by label. """
    # Arrange
    db_client.table.scan.return_value = {
        'Items': [
            {'ImageName': '111', 'LabelValue': ['test']},
            {'ImageName': '222', 'LabelValue': ['not_test']}
        ]
    }

    # Act
    matching_ids = db_client.search('test')

    # Assert
    assert matching_ids == ['111']


def test_search_images_not_found(db_client):
    """ Search DB record by incorrect label. """
    # Arrange
    db_client.table.scan.return_value = {
        'Items': [
            {'ImageName': '111', 'LabelValue': ['not_test']}
        ]
    }

    # Act
    matching_ids = db_client.search('111')

    # Assert
    assert matching_ids == []
