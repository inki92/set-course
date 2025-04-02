resource "aws_lambda_function" "lambda_script" {
  description       = "Lambda Script for RekApp"
  function_name     = var.lambda_function_name
  role              = aws_iam_role.lambda_role.arn
  filename          = data.archive_file.lambda_payload.output_path
  runtime           = var.python_version
  handler           = "index.lambda_handler"
  timeout           = var.lambda_timeout
  source_code_hash  = data.archive_file.lambda_payload.output_base64sha256
  depends_on        = [aws_iam_role_policy_attachment.lambda_policy_attachment]

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = "Image-${var.env_name}"
    }
  }

  tags              = {
    Name            = "Lambda-Function"
    Environment     = var.env_name
    Application     = "ImageRecognitionApp"
  }
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = data.aws_sqs_queue.queue_name.arn
  function_name    = aws_lambda_function.lambda_script.arn
  enabled          = true
}

# IAM role and policy for the lambda function:

resource "aws_iam_role" "lambda_role" {
  description        = "IAM Role for Lambda"
  name               = var.lambda_role_name

  assume_role_policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
EOF
}

resource "aws_iam_policy" "lambda_policy" {
  name        = var.lambda_iam_policy_name
  description = "Policy for Lambda to access AWS services"

  policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:ReceiveMessage"
        ],
        "Resource": "${data.aws_sqs_queue.queue_name.arn}"
      },
      {
        "Effect": "Allow",
        "Action": [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ],
        "Resource": "${data.aws_dynamodb_table.table_name.arn}"
      },
      {
        "Effect": "Allow",
        "Action": [
          "rekognition:DetectLabels"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject"
        ],
        "Resource": "${data.aws_s3_bucket.bucket_name.arn}/*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
      }
    ]
  }
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
