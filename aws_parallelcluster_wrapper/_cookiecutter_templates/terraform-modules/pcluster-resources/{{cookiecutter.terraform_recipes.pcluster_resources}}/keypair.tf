resource "tls_private_key" "global_key" {
    algorithm = "RSA"
    rsa_bits = 2048
}

resource "local_file" "ssh_private_key_pem" {
    filename = "${path.module}/files/user-data/key-pair/id_rsa"
    sensitive_content = tls_private_key.global_key.private_key_pem
    file_permission = "0600"
}

resource "local_file" "ssh_public_key_openssh" {
    filename = "${path.module}/files/user-data/key-pair/id_rsa.pub"
    content = tls_private_key.global_key.public_key_openssh
}

# Temporary key pair used for SSH accesss
resource "aws_key_pair" "quickstart_key_pair" {
    key_name_prefix = "{{cookiecutter.project}}-{{cookiecutter.id}}-keypair"
    public_key = tls_private_key.global_key.public_key_openssh
}

output "aws_keypair" {
//    value = "{{cookiecutter.project}}-{{cookiecutter.id}}-keypair"
    value = aws_key_pair.quickstart_key_pair.key_name
}

output "ssh_private_key_pem" {
    value = "${path.module}/files/user-data/key-pair/id_rsa"
}

output "ssh_public_key_openssh" {
    value = "${path.module}/files/user-data/key-pair/id_rsa.pub"
}
