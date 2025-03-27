import hcl2

def terraform_data_dev():
    """ Collect terraform data from DEV env modules. """
    with open("tests/test_data/tf-dev/main.tf", "r") as f:
        data = hcl2.load(f)

    environment = data['module'][0]['environment']
    application = data['module'][1]['application']

    return {
        "dynamodb_name": str(environment["dynamodb_name"][0]),
        "bucket_name": str(environment["bucket_name"][0]),
        "sns_name": str(environment["sns_name"][0]),
        "sqs_name": str(environment["sqs_name"][0]),
        "sg_name": str(environment["sg_name"][0]),
        "docker_image_uri": str(application["docker_image_uri"][0]),
        "lambda_function_name": str(application["lambda_function_name"][0]),
        "ecs_family_name": str(application["ecs_family_name"][0]),
        "ecs_cluster_name": str(application["ecs_cluster_name"][0]),
        "ecs_service_name": str(application["ecs_service_name"][0]),
        "lb_public_name": str(application["lb_public_name"][0])
    }

a = terraform_data_dev()
print(a.values())
