
resource "null_resource" "upload_s3_user_data" {
    depends_on = [
        module.user_data_s3_bucket,
        aws_iam_policy.s3_policy
    ]
    triggers = {
        always_run = timestamp()
    }
    provisioner "local-exec" {
        command = "aws s3 sync  --acl private ${path.module}/files/user-data/ s3://{{cookiecutter.s3_user_data_bucket}}"
    }
}
