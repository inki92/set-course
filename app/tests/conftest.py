""" Testing configs and fixtures. """

import os
from unittest.mock import patch, MagicMock
import pytest
import image_rec_app.app
from image_rec_app.clients.db_client import ImageDatabaseClient
from image_rec_app.clients.storage_client import ImageStorageClient
from image_rec_app.config import TestingConfig


@pytest.fixture(scope='session')
def set_testing_env():
    """ Testing environment values. """
    os.environ["AWS_ACCESS_KEY_ID"] = "test_key_id"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test_secret_key"
    os.environ["AWS_S3_BUCKET_NAME"] = "test_bucket"
    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"
    os.environ["AWS_DYNAMODB_TABLE_NAME"] = "test_dynamoDB_table"


@pytest.fixture(scope='session')
def app(set_testing_env):
    """ Create testing Flask app."""
    app = image_rec_app.app.create_app(config_class=TestingConfig)
    yield app


@pytest.fixture(scope='session')
def client(app, set_testing_env):
    """ Create testing client. """
    return app.test_client()


@pytest.fixture
def mock_storage_client():
    """Fixture to mock ImageStorageClient for API tests."""
    with patch(
            "image_rec_app.services.image_service.ImageStorageClient"
    ) as mock:
        yield mock.return_value


@pytest.fixture
def mock_db_client():
    """Fixture to mock ImageDatabaseClient for API tests."""
    with patch(
            "image_rec_app.services.image_service.ImageDatabaseClient"
    ) as mock:
        yield mock.return_value


@pytest.fixture
def db_client():
    """ Create mocked object for db client for UNIT tests. """
    client = ImageDatabaseClient()
    client.table = MagicMock()
    return client


@pytest.fixture(scope='function')
def storage_client():
    """ Create a mock storage client for UNIT tests. """
    storage_client = ImageStorageClient()
    storage_client.bucket = MagicMock()
    return storage_client
