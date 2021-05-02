#!/bin/bash -x

sudo yum install -y epel-release
sudo yum-config-manager --enable epel
sudo yum update -y; yum upgrade -y
sudo yum install -y Lmod git python3 pip3 amazon-efs-utils curl \
    fuse s3fs-fuse fuse-sshfs vsftpd

## Install RStudio

cd /tmp
wget https://download2.rstudio.org/server/centos6/x86_64/rstudio-server-rhel-1.2.5001-x86_64.rpm
sudo yum install -y rstudio-server-rhel-1.2.5001-x86_64.rpm
rm -rf rstudio-server-rhel-1.2.5001-x86_64.rpm

## Install Docker

sudo amazon-linux-extras install -y docker
sudo service docker start
sudo groupmod -g 500 docker
sudo systemctl enable --now docker

## Install Docker Compose
## Docker compose version
## 1.28.0

sudo curl -L "https://github.com/docker/compose/releases/download/1.28.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

#sudo /usr/local/sbin/ami_cleanup.sh

