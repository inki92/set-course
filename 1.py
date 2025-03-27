import hcl2

def terraform_data_dev():
    """ Collect terraform data from DEV env modules. """
    with open("tests/test_data/tf-dev/main.tf", "r", encoding="utf-8") as f:
        data = hcl2.load(f)

    environment = data['module'][0]['environment']
    application = data['module'][1]['application']

    # if it list - collect 1 element
    def get_value(value):
        if isinstance(value, list):
            return str(value[0])  # 1 value from list
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

a = terraform_data_dev()
print(a)