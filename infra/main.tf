terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.50.0"
    }
  }
}

provider "aws" {
  region  = "ap-south-1"
  profile = "notebook-application"
}

resource "aws_dynamodb_table" "token_email_lookup" {
  name         = "token-email-lookup"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "token"

  attribute {
    name = "token"
    type = "S"
  }
}

resource "aws_dynamodb_table" "user_notes" {
  name         = "user-notes"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user"
  range_key    = "create_date"

  attribute {
    name = "user"
    type = "S"
  }
  attribute {
    name = "create_date"
    type = "S"
  }
}
