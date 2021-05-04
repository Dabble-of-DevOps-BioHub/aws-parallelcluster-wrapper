FROM python:3.8

USER root

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ARG TERRAFORM_VERSION="0.14.5"

RUN apt-get update -y; apt-get upgrade -y; \
    apt-get install -y curl wget vim-tiny vim-athena jq git build-essential s3fs

## Install Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && mv terraform /usr/local/bin \
 && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip


# All imports needed for autodoc.
WORKDIR /usr/src/app
COPY . .
RUN bash -c "pip install wheel; pip install --no-cache-dir  -r ./requirements.txt; python setup.py build; python setup.py install -v"

# RUN bash -c "make install"

# WORKDIR /home