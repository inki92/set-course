""" Infrastructure tests. """

import socket
import pytest
import boto3
from botocore.exceptions import ClientError

# client initialization
dynamodb = boto3.client("dynamodb", region_name="eu-central-1")
s3 = boto3.client("s3", region_name="eu-central-1")
sns = boto3.client("sns", region_name="eu-central-1")
sqs = boto3.client("sqs", region_name="eu-central-1")
ec2 = boto3.client("ec2", region_name="eu-central-1")
lambda_client = boto3.client("lambda", region_name="eu-central-1")
ecs = boto3.client("ecs", region_name="eu-central-1")
elbv2 = boto3.client("elbv2", region_name="eu-central-1")


def test_aws_provider():
    """ Test for aws provider exists. """
    try:
        # list of regions
        response = ec2.describe_regions()
        assert 'Regions' in response, \
            "AWS provider is not configured correctly."
    except Exception as e:
        assert False, f"AWS provider check failed: {str(e)}"


def check_dynamodb_table_exists(table_name):
    """ Test for DynamoDB table exists. """
    try:
        dynamodb.describe_table(TableName=table_name)
        return True
    except dynamodb.exceptions.ResourceNotFoundException:
        return False


def check_s3_bucket_exists(bucket_name):
    """ Test for S3 bucket exists. """
    try:
        print(bucket_name)
        s3.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False


def check_sns_topic_exists(topic_name):
    """ Test for SNS topic exists. """
    try:
        sns.get_topic_attributes(
            TopicArn=f'arn:aws:sns:eu-central-1:692859924835:{topic_name}'
        )
        return True
    except sns.exceptions.NotFoundException:
        return False


def check_sqs_queue_exists(queue_name):
    """ Test for SQS queue exists. """
    try:
        sqs.get_queue_url(QueueName=queue_name)
        return True
    except sqs.exceptions.QueueDoesNotExist:
        return False


def check_security_group_exists(sg_name):
    """ Test for SG exists. """
    response = ec2.describe_security_groups(
        Filters=[{"Name": "group-name", "Values": [sg_name]}]
    )
    return len(response['SecurityGroups']) > 0


def check_lambda_function_exists(function_name):
    """ Test for lambda function exists. """
    try:
        lambda_client.get_function(FunctionName=function_name)
        return True
    except lambda_client.exceptions.ResourceNotFoundException:
        return False


def check_ecs_task_definition_family_exists(ecs_family_name):
    """ Test for ECS task definition family exists. """
    print(ecs.list_task_definitions(status='ACTIVE'))
    try:
        ecs.describe_task_definition(taskDefinition=ecs_family_name)
        return True
    except ecs.exceptions.ClientException:
        return False


def check_ecs_cluster_exists(cluster_name):
    """ Test for ECS cluster exists. """
    response = ecs.describe_clusters(clusters=[cluster_name])
    if cluster_name in str(response):
        return len(response['clusters']) > 0
    else:
        return False


def check_load_balancer_exists(lb_name):
    """ Test for LB exists. """
    response = elbv2.describe_load_balancers(Names=[lb_name])
    return len(response['LoadBalancers']) > 0


# parametrize - start of all
@pytest.mark.parametrize("resource_name,check_function", [
    ("dynamodb_name", check_dynamodb_table_exists),
    ("bucket_name", check_s3_bucket_exists),
    ("sns_name", check_sns_topic_exists),
    ("sqs_name", check_sqs_queue_exists),
    ("sg_name", check_security_group_exists),
    ("lambda_function_name", check_lambda_function_exists),
    ("ecs_family_name", check_ecs_task_definition_family_exists),
    ("ecs_cluster_name", check_ecs_cluster_exists),
    ("lb_public_name", check_load_balancer_exists)
])
def test_resources_existence(terraform_data_qa, resource_name, check_function):
    """ Test for ALL resources exists. """
    resource_value = terraform_data_qa[resource_name]
    assert check_function(resource_value),\
        f"Resource {resource_value} does not exist on AWS"


def test_load_balancer_dns(lb_url_qa):
    """ Test for LB url exists. """
    try:
        # check for dns resolving
        socket.gethostbyname(lb_url_qa)
        print(f"Successfully resolved DNS: {lb_url_qa}")

    except socket.gaierror as e:
        assert False, f"DNS resolution failed for {lb_url_qa}: {str(e)}"
