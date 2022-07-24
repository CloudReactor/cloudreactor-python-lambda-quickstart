locals {
  configurations = {
    defaults = {
        #region = "us-west-2"
    }

    dev = {
    }

    staging = {
    }

    production = {
    }
  }

  namespace = "cloudreactor-python-lambda-quickstart"
  environment = terraform.workspace
  deployment = merge(local.configurations.defaults, local.configurations[terraform.workspace])

  tags = {
    Namespace = local.namespace
    Environment = local.environment
    ManagedBy = "Terraform"
  }

  secrets_json = file("${terraform.workspace}-secrets.json")
}
