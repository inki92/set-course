# Image Recognition Application

Practice task for SET Advanced course

## Tool and Technologies:
1. Python 3
2. Flask - Python micro web framework
3. Swagger - API documentation
4. Pytest - testing framework
5. terraform - infrastructure as code tool 
6. checkov - terrafrom static code analysis tool
7. tflint - terrafrom static code analysis tool
8. tfsec - terrafrom static code analysis tool

## Cloud native application
### How to run in the local environment:

1. cd set-advanced-course
2. pip3 install -U virtualenv
3. virtualenv venv
4. source venv/bin/activate
5. venv/bin/pip3 install -r requirements.txt
6. export PYTHONPATH variable:
```commandline
export PYTHONPATH=.
```
7. export AWS credentials as variables:
```commandline
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```
8. export AWS bucket, db table and region names as variables:
```commandline
export AWS_S3_BUCKET_NAME="..."
export AWS_DEFAULT_REGION=eu-central-1
export AWS_DYNAMODB_TABLE_NAME="..."
```
9. venv/bin/python image_rec_app/app.py
10. open http://127.0.0.1/ui/


### How to run all tests:
venv/bin/pytest tests/

## Infrastructure as code
### How to run environment deployment:

1. Go to environment directory, for example development environment:
```commandline
cd tf-dev/
```
2. Export environment variables with security credentials:
```commandline
export AWS_ACCESS_KEY_ID="***"
export AWS_SECRET_ACCESS_KEY="***"
```
3. Run next commands:
```commandline
terraform init
terraform apply --auto-approve
```
4. For destroy environment run:
```commandline
terraform destroy --auto-approve
```
### How to run infrastructure tests:
```commandline
venv/bin/pytest tests/
```

By default tests are running only for development environment. 
For add another environment change conftest.py

### How to run static code analysis:

### Checkov:

1. Install checkov
```commandline
venv/bin/pip install checkov
```
2. Start analyse:
```commandline
venv/bin/checkov -d .
```

### TFlint:

1. Install tflint:
```commandline
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
```
2. Create file
```commandline
touch .tflint.hcl
```
3. Run analyse:
```commandline
 tflint --chdir .
```

### TFSec:
1. Install tfsec:
```commandline
curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash
```
2. Start analyse:
```commandline
tfsec .
```
3. Collecting output to the xml report:
```commandline
tfsec . --format=junit > tfsec_output.xml
```

## How to run collecting data for README.md via terraform-docs

1. Install terraform-docs:
```commandline
sudo GOBIN=/usr/local/bin /usr/local/go/bin/go install github.com/terraform-docs/terraform-docs@latest
```
2. Collect data for modules, for example for tf-application:
```commandline
terraform-docs markdown table modules/tf-application/ >> modules/tf-application/README.md
```
