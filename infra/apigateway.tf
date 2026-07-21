resource "aws_apigatewayv2_api" "notebook_application_api" {
  name          = "notebook-application-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "notebook_application_integration" {
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.notebook_application_lambda.invoke_arn
  api_id           = aws_apigatewayv2_api.notebook_application_api.id
}

resource "aws_apigatewayv2_route" "notebook_application_route" {
  route_key = "GET /notes"
  target    = "integrations/${aws_apigatewayv2_integration.notebook_application_integration.id}"
  api_id    = aws_apigatewayv2_api.notebook_application_api.id
}

resource "aws_apigatewayv2_stage" "notebook_application_stage" {
  name        = "$default"
  auto_deploy = true
  api_id      = aws_apigatewayv2_api.notebook_application_api.id
}

resource "aws_lambda_permission" "notebook_api_lambda_permission" {
  action        = "lambda:InvokeFunction"
  principal     = "apigateway.amazonaws.com"
  function_name = aws_lambda_function.notebook_application_lambda.function_name
  source_arn    = "${aws_apigatewayv2_api.notebook_application_api.execution_arn}/*/*"
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.notebook_application_api.api_endpoint
}
