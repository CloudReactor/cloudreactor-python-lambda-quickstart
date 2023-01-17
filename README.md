<!--
title: 'AWS Python Scheduled Cron example monitored by CloudReactor'
description: 'This is an example of creating a function that runs as a cron job using the serverless ''schedule'' event, and monitored and managed by CloudReactor.'
layout: Doc
framework: v1
platform: AWS
language: Python
priority: 2
authorLink: 'https://github.com/CloudReactor'
authorName: 'Jeff Tsay'
authorAvatar: 'https://avatars.githubusercontent.com/u/1079646?v=4&s=140'
-->

# CloudReactor Python Lambda Quickstart

![Tests](https://github.com/CloudReactor/cloudreactor-python-lambda-quickstart/workflows/Tests/badge.svg?branch=master)

<img src="https://img.shields.io/github/license/CloudReactor/cloudreactor-python-lambda-quickstart.svg?style=flat-square" alt="License">

This project serves as blueprint to get your python code
running in [AWS Lambda](https://aws.amazon.com/lambda/), deployed by the [serverless](https://www.serverless.com/framework) framework, and
monitored and managed by
[CloudReactor](https://www.cloudreactor.io/). See a
[summary of the benefits](https://docs.cloudreactor.io/cloudreactor.html)
of these technologies. This project is designed with best practices and smart
defaults in mind, but also to be customizable.

It has these features built-in:

* Sets up Tasks to be monitored and managed by CloudReactor
* Reads secrets from AWS Secrets Manager
* Uses [pip-tools](https://github.com/jazzband/pip-tools) to manage only
top-level python library dependencies
* Uses [pytest](https://docs.pytest.org/en/latest/) (automated tests),
[pylint](https://www.pylint.org/) (static code analysis),
[mypy](http://mypy-lang.org/) (static type checking), and
[safety](https://github.com/pyupio/safety) (security vulnerability checking)
for quality control

## Pre-requisites

First, setup AWS and CloudReactor by following the
[pre-requisites](https://docs.cloudreactor.io/full_integration.html#pre-requisites).
You'll be granting CloudReactor permission to start Tasks on your behalf,
creating API keys, and optionally creating an IAM user/role that has permission
to deploy your Tasks.

## Get this project's source code

Next, you'll need to get this project's source code onto a filesystem where you
can make changes. First
[fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo)
the project, then clone your project:

    git clone https://github.com/YourOrg/cloudreactor-python-lambda-quickstart.git

## Requirements

These tools are necessary for local development and deployment:

* [pyenv](https://github.com/pyenv/pyenv) and
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) are used for local
python development
* [pip-tools](https://github.com/jazzband/pip-tools) is used to compile
top-level python library dependencies into requirements.txt files for python
* [nvm](https://github.com/nvm-sh/nvm) is used to provide the NodeJS runtime
used by serverless for deployment

## Development setup

After installing the required tools above, create the virtual environment:

    pyenv virtualenv 3.9.13 cloudreactor-python-lambda-quickstart-dev
    pyenv activate cloudreactor-python-lambda-quickstart-dev
    python install -r requirements.txt -r dev-requirements.txt

To run locally, first copy `config.localdev.json.sample` to
`config.localdev.json` and update the API key value to one created in
CloudReactor that has the Developer access level, either unscoped, or scoped
to the Run Environment you want your Task to appear in.

Before running, ensure you are using the correct virtualenv:

    pyenv activate cloudreactor-python-lambda-quickstart-dev

Finally, to run:

    python -m functions.handler

To run type-checking with mypy:

    mypy -m functions

To run source-code static analysis:

    pylint functions

To check for security vulnerabilities in the python libraries:

    safety check

## Deploying locally

If you don't have NodeJS 14.17.5 installed already in NVM:

    nvm install 14.17.5

Then,

    ./deploy.sh <Run Environment name>

## Deploying with GitHub Action

This project is setup to deploy with a GitHub Action when a commit is pushed to
the master branch. It requires these GitHub secrets to be set:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_REGION
* SERVERLESS_CONFIG_YAML - set to YAML text, use a modified version of
`deploy_config/serverless-config-sample.yml`, with `profile` set to `null`

See serverless's [guide to setting up access keys](https://www.serverless.com/framework/docs/providers/aws/guide/credentials#create-an-iam-user-and-access-key)
to be used for deployment.

### Bundling dependencies

This project uses
[serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements)
to include python libraries.

To build the `requirements.txt` file, the project uses
[pip-tools](https://github.com/jazzband/pip-tools) so that we only have to
manage top-level python library dependencies in `requirements.in`. To update the
compiled `requirements.txt` file:

    pip-compile --allow-unsafe --generate-hashes --output-file=requirements.txt requirements.in

The development environment has additional dependencies found in
`dev-requirements.in`. To update the copiled `dev-requirements.txt` file:

    pip-compile --allow-unsafe --generate-hashes --output-file=dev-requirements.txt dev-requirements.in

Then to install the libraries:

    pip install -r requirements.txt -r dev-requirements.txt

## Installing Secrets

This project is setup to read secrets from AWS Secrets Manager,
using proc_wrapper.
It is possible to populate Secrets Manager using Terraform,
with the instructions below:

Requirements:
* Terraform (tested with version 1.2.5)

First, ensure the S3 bucket `example-projects-terraform-remote-state` exists
and can be accessed the account used to run terraform.

In the `terraform` directory:

```
export AWS_PROFILE=<your AWS profile name>
export AWS_REGION=<AWS region in which your function will execute>
terraform init
terraform workspace new <stage>
terraform plan -out plan.out
terraform apply plan.out
```

Alternatively, you can populate the secrets manually in
the AWS Console. The name of the secret should be `staging/cloudreactor-python-lambda-quickstart/secrets.json` where
`staging` should be replaced with the stage name.
