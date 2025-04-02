resource "aws_sqs_queue" "sqs_queue" {
  depends_on    = [aws_s3_bucket.image_rek_bucket]
  name          = var.sqs_name
  fifo_queue    = false

  tags          = {
    Application = "ImageRecognitionApp"
    Environment = var.env_name
    Name        = "SQS-Queue"
  }
}

resource "aws_sqs_queue_policy" "sqs_policy" {
  queue_url  = aws_sqs_queue.sqs_queue.id
  policy     = data.aws_iam_policy_document.sqs_policy.json
}

resource "aws_sns_topic_subscription" "subscription" {
  topic_arn  = aws_sns_topic.image_notification.arn
  protocol   = "sqs"
  endpoint   = aws_sqs_queue.sqs_queue.arn
  depends_on = [aws_sqs_queue.sqs_queue, aws_sns_topic.image_notification]
}
