#!/usr/bin/env bash

export ADMIN_DIR="/scratch/admin"
export NEW_USER_DATA_DIR="/scratch/admin/user-data"

NEW_USER=$1

sudo mkdir -p ${ADMIN_DIR}
sudo mkdir -p ${NEW_USER_DATA_DIR}
sudo touch /scratch/admin/user-data/new-users.txt
sudo touch /scratch/admin/user-data/chpasswords.txt

cd /home/ec2-user/bootstrap-scripts && \
sudo python ./create_new_user.py ${NEW_USER} && \
sudo ./create_users.sh

