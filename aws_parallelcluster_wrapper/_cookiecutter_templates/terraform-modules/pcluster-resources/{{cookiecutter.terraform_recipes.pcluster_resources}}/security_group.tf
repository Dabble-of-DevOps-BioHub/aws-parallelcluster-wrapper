# Security group to allow all traffic
resource "aws_security_group" "sg_allowall" {
    name = "{{cookiecutter.project}}-allowall"
    description = "quickstart - allow all traffic"

    ingress {
        from_port = "0"
        to_port = "0"
        protocol = "-1"
        cidr_blocks = [
            "0.0.0.0/0"]
    }

    egress {
        from_port = "0"
        to_port = "0"
        protocol = "-1"
        cidr_blocks = [
            "0.0.0.0/0"]
    }

    tags = {
        Project = "{{cookiecutter.project}}"
    }
}

output "additional_security_group_id" {
    value = aws_security_group.sg_allowall.id
}
