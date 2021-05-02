// This resource is created earlier in the pcluster-resources

resource "null_resource" "upload_s3_installation" {
    triggers = {
        always_run = timestamp()
    }
    provisioner "local-exec" {
        command = "aws s3 sync --acl private ${path.module}/files/installation/ s3://{{cookiecutter.s3_installation_bucket}}"
    }
}
