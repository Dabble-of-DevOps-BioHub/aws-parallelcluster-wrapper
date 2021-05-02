provider "aws" {
    region = "{{cookiecutter.aws_region}}"
}

# This only works with terraform >= 0.14

module "terraform_state_backend" {
    source = "cloudposse/tfstate-backend/aws"
    version = "0.30.0"
    namespace = "{{cookiecutter.terraform_state.s3_bucket}}"
    stage = "{{cookiecutter.stage}}"
    name = "terraform"
    attributes = [
        "state"]

    terraform_backend_config_file_path = "."
    terraform_backend_config_file_name = "backend.tf"
    force_destroy = false
}
