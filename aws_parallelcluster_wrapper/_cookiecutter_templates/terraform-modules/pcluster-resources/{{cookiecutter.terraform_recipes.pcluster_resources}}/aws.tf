provider "aws" {
  region  = "{{cookiecutter.aws_region}}"
}

# created by terraform-state
terraform {
  backend "s3" {
    bucket = "{{cookiecutter.terraform_state.s3_bucket}}-{{cookiecutter.stage}}-terraform-state"
    key = "terraform/{{cookiecutter.project}}-pcluster-resources.tfstate"
    region = "{{cookiecutter.aws_region}}"
    encrypt = true
    dynamodb_table = "{{cookiecutter.terraform_state.s3_bucket}}-{{cookiecutter.stage}}-terraform-state-lock"
  }
}
