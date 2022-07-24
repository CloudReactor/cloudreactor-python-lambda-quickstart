provider "aws" {
  # Uncomment this and adjust as necessary, if not setting the AWS_REGION
  # environment variable when running terraform init.
  #region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "example-projects-terraform-remote-state"
    key    = "cloudreactor-python-lambda-quickstart.tfstate"

    # Uncomment this and adjust as necessary, if not setting the AWS_REGION
    # environment variable when running terraform plan / apply.
    # region = "us-east-1"
  }
}

data "aws_caller_identity" "current" {}
