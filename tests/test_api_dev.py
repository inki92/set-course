""" API tests for deployed via IAC app"""

import hashlib
import os
import time
import requests
import pytest


@pytest.fixture
def image_id(lb_url_dev, test_image_path):
    """ Upload image to the app. """

    # connection test
    response_code = 0
    connection_try: int = 0
    connection_limit = 60
    while response_code != 200:
        try:
            response_code = requests.get(
                f"http://{lb_url_dev}/ui/"
            ).status_code
        except requests.exceptions.RequestException as e:
            if connection_try >= connection_limit:
                # Raise an exception if the connection limit is reached
                raise e
            connection_try += 1
            time.sleep(10)

    with open(test_image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"http://{lb_url_dev}/image", files=files)
    time.sleep(5)

    assert response.status_code == 200
    assert response.text.startswith("Image uploaded: ID: ")

    image_id = response.text.split("ID: ")[1].strip()

    assert image_id

    yield image_id


def test_1_get_image_data(lb_url_dev, image_id):
    """ Test for get image data after uploading and recognition. """
    response = requests.get(f"http://{lb_url_dev}/image/{image_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["ImageName"] == image_id
    assert "LabelValue" in data and len(data["LabelValue"]) > 0
    assert data["Status"] == "RECOGNITION_COMPLETED"

    return data


def test_2_download_image(lb_url_dev, image_id, image_hash):
    """ Test for downloading image from the app. """
    response = requests.get(f"http://{lb_url_dev}/image/file/{image_id}")

    assert response.status_code == 200
    output_path = "output.jpg"

    with open(output_path, "wb") as f:
        f.write(response.content)

    with open(output_path, "rb") as f:
        downloaded_hash = hashlib.sha256(f.read()).hexdigest()

    os.remove(output_path)
    assert downloaded_hash == image_hash


def test_3_update_image_data(lb_url_dev, image_id):
    """ Test for updating data for the image. """
    time.sleep(3)
    payload = {"LabelValue": ["test"], "Status": "NEW"}
    response = requests.patch(
        f"http://{lb_url_dev}/image/{image_id}", json=payload
    )

    assert response.status_code == 204


def test_5_delete_image(lb_url_dev, image_id):
    """ Test for deleting image. """
    response = requests.delete(f"http://{lb_url_dev}/image/{image_id}")
    time.sleep(5)
    assert response.status_code == 200
    assert response.text == "Image deleted successfully."
