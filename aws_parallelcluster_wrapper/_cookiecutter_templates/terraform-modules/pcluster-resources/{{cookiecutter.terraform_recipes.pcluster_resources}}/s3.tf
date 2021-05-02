module "installation_s3_bucket" {
    source = "terraform-aws-modules/s3-bucket/aws"

    bucket = "{{cookiecutter.s3_installation_bucket}}"
    acl = "private"

    versioning = {
        enabled = true
    }
}

module "user_data_s3_bucket" {
    source = "terraform-aws-modules/s3-bucket/aws"

    bucket = "{{cookiecutter.s3_user_data_bucket}}"
    acl = "private"

    versioning = {
        enabled = true
    }
}

module "admin_s3_bucket" {
    source = "terraform-aws-modules/s3-bucket/aws"

    bucket = "{{cookiecutter.s3_admin_bucket}}"
    acl = "private"

    versioning = {
        enabled = true
    }
}

data "aws_iam_policy_document" "s3_policy" {
    statement {
        sid = "1"

        actions = [
            "s3:ListAllMyBuckets",
            "s3:GetBucketLocation",
        ]

        resources = [
            "arn:aws:s3:::*",
        ]
    }

    statement {
        actions = [
            "s3:*",
        ]

        resources = [
            "arn:aws:s3:::${module.admin_s3_bucket.this_s3_bucket_id}",
        ]
    }
    statement {
        actions = [
            "s3:*",
        ]

        resources = [
            "arn:aws:s3:::${module.user_data_s3_bucket.this_s3_bucket_id}",
        ]
    }
    statement {
        actions = [
            "s3:*",
        ]

        resources = [
            "arn:aws:s3:::${module.installation_s3_bucket.this_s3_bucket_id}",
        ]
    }
}

resource "aws_iam_policy" "s3_policy" {
    name = "{{cookiecutter.project}}-{{cookiecutter.stage}}-{{cookiecutter.id}}-s3_policy"
    path = "/"
    policy = data.aws_iam_policy_document.s3_policy.json
}

output "user_data_s3_bucket" {
    value = module.user_data_s3_bucket.this_s3_bucket_id
}

output "admin_s3_bucket" {
    value = module.admin_s3_bucket.this_s3_bucket_id
}

output "installation_s3_bucket" {
    value = module.installation_s3_bucket.this_s3_bucket_id
}

output "s3_policy" {
    value = aws_iam_policy.s3_policy.arn
}
