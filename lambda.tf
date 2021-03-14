resource "null_resource" "prepare-lambda" {
  triggers = {
    main = filebase64sha256("${path.module}/files/get_domains.py")
    lib  = filebase64sha256("${path.module}/files/aws.py")
  }

  provisioner "local-exec" {
    command = "rm -rf ${path.module}/output || true"
  }

  provisioner "local-exec" {
    command = "mkdir ${path.module}/output"
  }

  provisioner "local-exec" {
    command = "cp ${path.module}/files/* ${path.module}/output"
  }

  provisioner "local-exec" {
    command = "cd ${path.module}/output && zip -r lambda.zip ."
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/files"
  output_path = "${path.module}/output/lambda.zip"

  depends_on  = [null_resource.prepare-lambda]
}

resource "aws_lambda_function" "attach_lambda_function" {
  filename         = "${path.module}/output/lambda.zip"
  function_name    = "${var.name}-${var.environment}"
  role             = aws_iam_role.lambda_role.arn
  description      = "An AWS Lambda '${var.name}' function for ${var.environment}"
  handler          = "get_domains.handler"
  timeout          = "60"
  runtime          = "python3.7"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      SKIP_TAG = var.skip_tag
      REGIONS  = jsonencode(var.regions)
      TYPES    = jsonencode(var.types)
      API_URL  = var.api_url
      SOURCE   = var._source
      GATEID   = var.gateid
    }
  }

  depends_on = [null_resource.prepare-lambda]
}

resource "aws_lambda_alias" "attach_lambda_alias" {
  name             = "${var.name}-${var.environment}"
  description      = "An AWS Lambda function for EC2 HA"
  function_name    = aws_lambda_function.attach_lambda_function.arn
  function_version = "$LATEST"
}

#resource "aws_lambda_permission" "attach_lambda_permission" {
#  statement_id  = "AllowExecutionFromCloudWatch"
#  action        = "lambda:InvokeFunction"
#  function_name = aws_lambda_function.attach_lambda_function.function_name
#  principal     = "events.amazonaws.com"
#  source_arn    = aws_cloudwatch_event_rule.asg_scale_event.arn
#}
