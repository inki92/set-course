""" Conftest for the pytest. """

import hashlib
import hcl2
import boto3
import pytest
from botocore.exceptions import ClientError


@pytest.fixture(scope="session")
def terraform_data_dev():
    """ Collect terraform data from DEV env modules. """
    with open("tests/test_data/tf-dev/main.tf", "r", encoding="utf-8") as f:
        data = hcl2.load(f)

    environment = data['module'][0]['environment']
    application = data['module'][1]['application']

    def get_value(value):
        if isinstance(value, list):
            return str(value[0])  # 1 value from the list
        return str(value)

    return {
        "dynamodb_name": get_value(environment["dynamodb_name"]),
        "bucket_name": get_value(environment["bucket_name"]),
        "sns_name": get_value(environment["sns_name"]),
        "sqs_name": get_value(environment["sqs_name"]),
        "sg_name": get_value(environment["sg_name"]),
        "docker_image_uri": get_value(application["docker_image_uri"]),
        "lambda_function_name": get_value(application["lambda_function_name"]),
        "ecs_family_name": get_value(application["ecs_family_name"]),
        "ecs_cluster_name": get_value(application["ecs_cluster_name"]),
        "ecs_service_name": get_value(application["ecs_service_name"]),
        "lb_public_name": get_value(application["lb_public_name"])
    }


@pytest.fixture(scope="session")
def terraform_data_qa():
    """ Collect terraform data from QA env modules. """
    with open("tests/test_data/tf-qa/main.tf", "r") as f:
        data = hcl2.load(f)

    environment = data['module'][0]['environment']
    application = data['module'][1]['application']

    def get_value(value):
        if isinstance(value, list):
            return str(value[0])  # 1 value from the list
        return str(value)

    return {
        "dynamodb_name": get_value(environment["dynamodb_name"]),
        "bucket_name": get_value(environment["bucket_name"]),
        "sns_name": get_value(environment["sns_name"]),
        "sqs_name": get_value(environment["sqs_name"]),
        "sg_name": get_value(environment["sg_name"]),
        "docker_image_uri": get_value(application["docker_image_uri"]),
        "lambda_function_name": get_value(application["lambda_function_name"]),
        "ecs_family_name": get_value(application["ecs_family_name"]),
        "ecs_cluster_name": get_value(application["ecs_cluster_name"]),
        "ecs_service_name": get_value(application["ecs_service_name"]),
        "lb_public_name": get_value(application["lb_public_name"])
    }


@pytest.fixture
def lb_url_dev(terraform_data_dev):
    """ Collect DEV env LB url. """
    # name of Load Balancer from terraform_data
    lb_public_name = terraform_data_dev['lb_public_name']
    elbv2 = boto3.client("elbv2", region_name="eu-central-1")

    try:
        # description of Load Balancer by the name
        response = elbv2.describe_load_balancers(
            Names=[lb_public_name]
        )
        # check for LB
        lb_dns_name = response['LoadBalancers'][0]['DNSName']
        return lb_dns_name

    except elbv2.exceptions.LoadBalancerNotFoundException:
        assert False, f"Load Balancer {lb_public_name} not found."
    except KeyError:
        assert False, "Could not find DNS name in the response."


@pytest.fixture
def lb_url_qa(terraform_data_qa):
    """ Collect QA env LB url. """
    # name of Load Balancer from terraform_data
    lb_public_name = terraform_data_qa['lb_public_name']
    elbv2 = boto3.client("elbv2", region_name="eu-central-1")

    try:
        # description of Load Balancer by the name
        response = elbv2.describe_load_balancers(
            Names=[lb_public_name]
        )
        # check for LB
        lb_dns_name = response['LoadBalancers'][0]['DNSName']
        return lb_dns_name

    except elbv2.exceptions.LoadBalancerNotFoundException:
        assert False, f"Load Balancer {lb_public_name} not found."
    except KeyError:
        assert False, "Could not find DNS name in the response."


@pytest.fixture
def test_image_path():
    """ Test image path. """
    return "tests/test_data/test.jpg"


@pytest.fixture
def image_hash(test_image_path):
    """ Test image sha256 sum. """
    with open(test_image_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


@pytest.fixture(scope="session", autouse=True)
def cleanup_s3_buckets(terraform_data_dev, terraform_data_qa):
    """ Fixture for cleaning up S3 bucket after all tests. """
    bucket_name_dev = terraform_data_dev["bucket_name"]
    bucket_name_qa = terraform_data_qa["bucket_name"]

    # S3 initialization
    s3_client = boto3.client('s3')

    # cleaning all dev
    def delete_all_objects_in_bucket_dev():
        try:
            # list of the objects
            response = s3_client.list_objects_v2(Bucket=bucket_name_dev)
            if 'Contents' in response:
                for obj in response['Contents']:
                    s3_client.delete_object(
                        Bucket=bucket_name_dev,
                        Key=obj['Key']
                    )
            print(f"All objects from {bucket_name_dev} have been deleted.")
        except ClientError as e:
            print(f"Error deleting objects from bucket {bucket_name_dev}: {e}")

    # cleaning all dev
    def delete_all_objects_in_bucket_qa():
        try:
            # list of the objects
            response = s3_client.list_objects_v2(Bucket=bucket_name_qa)
            if 'Contents' in response:
                for obj in response['Contents']:
                    s3_client.delete_object(
                        Bucket=bucket_name_qa,
                        Key=obj['Key']
                    )
            print(f"All objects from {bucket_name_qa} have been deleted.")
        except ClientError as e:
            print(f"Error deleting objects from bucket {bucket_name_qa}: {e}")

    yield
    delete_all_objects_in_bucket_dev()
    delete_all_objects_in_bucket_qa()
