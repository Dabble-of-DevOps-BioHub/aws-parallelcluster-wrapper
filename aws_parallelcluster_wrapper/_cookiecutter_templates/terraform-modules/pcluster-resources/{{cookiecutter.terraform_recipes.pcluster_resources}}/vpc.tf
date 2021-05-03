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

resource "aws_default_subnet" "default_az" {
    count = length(data.aws_availability_zones.available.names)
    availability_zone = data.aws_availability_zones.available.names[count.index]
}

