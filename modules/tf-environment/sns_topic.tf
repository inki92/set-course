resource "aws_sns_topic" "image_notification" {
  depends_on    = [aws_s3_bucket.image_rek_bucket]
  name          = var.sns_name

  tags          = {
    Name        = "SNS-Topic"
    Environment = var.env_name
    Application = "ImageRecognitionApp"
  }
}

resource "aws_s3_bucket_notification" "s3_notification" {
  depends_on    = [aws_s3_bucket.image_rek_bucket]
  bucket        = aws_s3_bucket.image_rek_bucket.id

  topic {
    topic_arn   = aws_sns_topic.image_notification.arn
    events      = ["s3:ObjectCreated:*"]
  }
}

resource "aws_sns_topic_policy" "sns_topic_policy" {
  arn           = aws_sns_topic.image_notification.arn
  policy        = data.aws_iam_policy_document.sns_topic_policy.json
}
