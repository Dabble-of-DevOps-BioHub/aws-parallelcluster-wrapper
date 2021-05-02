# Local variables used to reduce repetition
locals {
    node_username = "ec2-user"
}

variable "docker_version" {
    type = string
    description = "Docker version to install on nodes"
    default = "19.03"
}

# AWS EC2 instance for creating a single node RKE cluster and installing the Rancher server
resource "aws_instance" "pcluster_instance" {
    ami = "{{cookiecutter.custom_ami_id}}"
    // Not all AMI types are supported
    instance_type = "t3a.xlarge"

    key_name = aws_key_pair.quickstart_key_pair.key_name
    security_groups = [
        aws_security_group.sg_allowall.name]

// Changed this to just use a file
// So I cantrack the output on the screen
//    user_data = templatefile(
//    join("/", [
//        path.module,
//        "files/install_packages_custom_pcluster_ami.sh"]),
//    {
//        docker_version = var.docker_version
//        username = local.node_username
//    }
//    )

    root_block_device {
        volume_size = 32
    }

    provisioner "file" {
        source = join("/", [
            path.module,
            "files/install_packages_custom_pcluster_ami.sh"])
        destination = "/tmp/script.sh"
        connection {
            type = "ssh"
            host = self.public_ip
            user = local.node_username
            private_key = tls_private_key.global_key.private_key_pem
        }
    }

    provisioner "remote-exec" {
        inline = [
            "chmod +x /tmp/script.sh",
            "/tmp/script.sh args",
            "echo 'Waiting for cloud-init to complete...'",
            "cloud-init status --wait > /dev/null",
            "echo 'Completed cloud-init!'",
        ]

        connection {
            type = "ssh"
            host = self.public_ip
            user = local.node_username
            private_key = tls_private_key.global_key.private_key_pem
        }
    }

    tags = {
        Name = "custom-ami-{{cookiecutter.project}}-{{cookiecutter.stage}}"
        Project = "{{cookiecutter.project}}"
    }
}

resource "aws_ami_from_instance" "pcluster_custom_ami" {
    name = "pcluster_{{cookiecutter.pcluster.pcluster_version}}-{{cookiecutter.aws_region}}-custom_ami"
    source_instance_id = aws_instance.pcluster_instance.id
}

//Once we've created the custom ami we can stop the instance
//aws ec2 stop-instances --instance-ids ${aws_instance.pcluster_instance.id}

output "server_public_ip" {
    value = aws_instance.pcluster_instance.public_ip
}

output "ssh_to_public_server" {
    description = "cd to the dir with the terraform recipe"
    value = "ssh -i id_rsa ${local.node_username}@${aws_instance.pcluster_instance.public_ip}"
}

output "pcluster_custom_ami_id" {
    value = aws_ami_from_instance.pcluster_custom_ami.id
}
