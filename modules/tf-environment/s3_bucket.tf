resource "aws_s3_bucket" "image_rek_bucket" {
  bucket         = var.bucket_name

  tags           = {
    Name         = "S3-Bucket-Images"
    Environment  = var.env_name
    Application  = "ImageRecognitionApp"
  }
}

resource "aws_s3_bucket_public_access_block" "access" {
  bucket         = aws_s3_bucket.image_rek_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "ownership" {
  bucket             = aws_s3_bucket.image_rek_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "s3_bucket_acl" {
  depends_on  = [
    aws_s3_bucket_ownership_controls.ownership,
    aws_s3_bucket_public_access_block.access
  ]

  bucket      = aws_s3_bucket.image_rek_bucket.id
  acl         = "private"
}

resource "aws_s3_bucket_policy" "s3_policy" {
  bucket      = aws_s3_bucket.image_rek_bucket.id
  policy      = data.aws_iam_policy_document.s3_bucket_policy.json
}
