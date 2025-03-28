""" API tests for image_rec_app """

import json
import pytest
from flask import url_for


def test_update_image_not_found(client, mock_db_client):
    """ Updating Metadata of a Non-Existent Image """
    mock_db_client.read.return_value = None
    response = client.patch(
        '/image/123',
        data=json.dumps({'LabelValue': ['new_label'], 'Status': 'UPDATED'}),
        content_type='application/json'
    )
    assert response.status_code == 404
    assert b"Image not found" in response.data


def test_create_image_no_file(client):
    """ Attempt to download without file """
    response = client.post(
        '/image',
        data={},
        content_type='multipart/form-data'
    )
    assert response.status_code == 400


def test_get_image_not_found(client, mock_db_client):
    """ Request for an image that does not exist """
    mock_db_client.read.return_value = None
    response = client.get('/image/123')
    assert response.status_code == 404
    assert b"Image not found" in response.data


def test_delete_image_not_found(client, mock_storage_client):
    """ Attempt to delete a non-existent image """
    mock_storage_client.delete.return_value = {"Error": "Not found"}
    response = client.delete('/image/123')
    assert response.status_code == 404


def test_search_image_no_label(client):
    """ Search for images without providing a label """
    response = client.get('/image')
    assert response.status_code == 400
    assert b"label_query is required for search" in response.data


def test_search_image_by_label(client, mock_db_client):
    """ Search for images by label """
    mock_db_client.search.return_value = ['test_id']
    response = client.get('/image?label_query=test_label')
    assert response.json == {
        'message': 'No images found with the specified label.'
    }
