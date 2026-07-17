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