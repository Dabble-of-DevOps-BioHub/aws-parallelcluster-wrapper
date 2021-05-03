FROM python:3.9.4

USER root

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ARG TERRAFORM_VERSION="0.14.5"

RUN apt-get update -y; apt-get upgrade -y; \
    apt-get install -y curl wget vim-tiny vim-athena jq git build-essential

## Install Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && mv terraform /usr/local/bin \
 && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip


RUN echo "alias l='ls -lah'" >> ~/.bashrc
RUN mkdir -p /home/aws_parallelcluster_wrapper
RUN rm -rf /home/aws_parallelcluster_wrapper/*
ADD ./* /home/aws_parallelcluster_wrapper/
WORKDIR /home/aws_parallelcluster_wrapper

# All imports needed for autodoc.
RUN bash -c "pip install --no-cache-dir -r ./requirements_dev.txt -r ./requirements.txt"

# RUN bash -c "make install"

WORKDIR /home