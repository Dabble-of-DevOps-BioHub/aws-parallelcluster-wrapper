#!/usr/bin/env bash

## This must be run as root, or as a user with elevated permissions
export ADMIN_DIR="/scratch/admin"
export USER_DATA_DIR="/scratch/admin/user-data"

echo "Creating linux users"

mkdir -p ${ADMIN_DIR}
mkdir -p ${USER_DATA_DIR}
touch /scratch/admin/user-data/new-users.txt
touch /scratch/admin/user-data/chpasswords.txt

python ./create_users_file.py

newusers /scratch/admin/user-data/new-users.txt
cat /scratch/admin/user-data/chpasswords.txt | chpasswd
python ./setup_users.py

touch /scratch/admin/user-data/add_groups.sh
chmod 777 /scratch/admin/user-data/add_groups.sh
sudo /scratch/admin/user-data/add_groups.sh

exit 0
