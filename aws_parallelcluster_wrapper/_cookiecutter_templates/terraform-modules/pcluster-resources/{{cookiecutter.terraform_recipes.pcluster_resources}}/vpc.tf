data "aws_vpc" "selected" {
    id = "{{cookiecutter.vpc_id}}"
}

data "aws_internet_gateway" "default" {
    filter {
        name = "attachment.vpc-id"
        values = [
            data.aws_vpc.selected.id]
    }
}

data "aws_availability_zones" "available" {
    state = "available"
}

//resource "aws_subnet" "primary" {
//    availability_zone = data.aws_availability_zones.available.names[0]
//
//    # ...
//}

resource "aws_default_subnet" "default_az" {
    count = length(data.aws_availability_zones.available.names)
    availability_zone = data.aws_availability_zones.available.names[count.index]
}


{% for efs in cookiecutter.pcluster.efs_resources %}
resource "aws_efs_file_system" "{{efs.name}}" {
//  tags                            = module.this.tags
  performance_mode                = "{{efs.performance_mode}}"
  tags = {
        "Name" = "{{efs.name}}-{{cookiecutter.project}}-{{cookiecutter.id}}"
        "Environment" = "{{cookiecutter.stage}}"
        "Project" = "{{cookiecutter.project}}-{{cookiecutter.id}}"
        "Stage" = "{{cookiecutter.stage}}"
  }


  #dynamic "lifecycle_policy" {
  #  for_each = var.transition_to_ia == "" ? [] : [1]
  #  content {
  #    transition_to_ia = var.transition_to_ia
  #  }
  #}
}

resource "aws_efs_mount_target" "{{efs.name}}" {
    count = length(aws_default_subnet.default_az)
    file_system_id = aws_efs_file_system.{{efs.name}}.id
    subnet_id      = aws_default_subnet.default_az[count.index].id
    security_groups = [  aws_security_group.sg_allowall.id ]
}

output "{{efs.name}}" {
    value = aws_efs_file_system.{{efs.name}}.id
}

//output "aws_efs_mount_target_{{efs.name}}"{
//    value = aws_efs_mount_target.{{efs.name}}
//}

{% endfor %}

//output "aws_availability_zones" {
//    value = data.aws_availability_zones.available.names
//}
//
//output "aws_default_subnets" {
//    value = aws_default_subnet.default_az
//}
