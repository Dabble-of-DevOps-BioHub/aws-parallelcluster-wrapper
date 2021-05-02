#!/usr/bin/env bash

# pcluster config should have the following
# #post_install_args = https://github.com/aws-samples/aws-parallelcluster-monitoring/tarball/main,aws-parallelcluster-monitoring,install-monitoring.sh
# additional_iam_policies = arn:aws:iam::aws:policy/CloudWatchFullAccess,arn:aws:iam::aws:policy/AWSPriceListServiceFullAccess,arn:aws:iam::aws:policy/AmazonSSMFullAccess,arn:aws:iam::aws:policy/AWSCloudFormationReadOnlyAccess
# tags = {“Grafana” : “true”}


export AWS_ACCESS_KEY_ID="{{cookiecutter.os.env.AWS_ACCESS_KEY_ID}}"
export AWS_SECRET_ACCESS_KEY="{{cookiecutter.os.env.AWS_SECRET_ACCESS_KEY}}"

export AWS_S3_BUCKET="{{cookiecutter.s3_installation_bucket}}"
export ADMIN_DIR="/scratch/admin"
export USER_DATA_DIR="/scratch/admin/user-data"

BOOTSTRAP_DIR="/home/ec2-user/bootstrap-scripts"
mkdir -p ${BOOTSTRAP_DIR}
cd ${BOOTSTRAP_DIR}

aws s3 sync s3://${AWS_S3_BUCKET}/ ./
chmod 777 *.py
chmod 777 *.sh


#######################################################################################################################
# Mount storage necessary for /scratch and /apps
#######################################################################################################################

{% for efs_resource in cookiecutter.pcluster.efs_resources %}

sudo mkdir -p "/{{ efs_resource.name }}"
sudo mountpoint /{{efs_resource.name}} || sudo mount -t efs {{ efs_resource.fs_id }}:/ /{{ efs_resource.name }}

{% endfor %}

#######################################################################################################################
# Create Admin Dirs
#######################################################################################################################

sudo mkdir -p /scratch/admin/service-configs/
unalias cp

#touch /scratch/admin/service-configs/vsftpd.conf
#touch /scratch/admin/service-configs/sshd_config
#cp -rf /scratch/admin/service-configs/vsftpd.conf /etc/vsftpd/vsftpd.conf
#cp -rf /scratch/admin/service-configs/sshd_config /etc/ssh/sshd_config

sudo service vsftpd start
#/usr/sbin/rstudio-server stop || echo "unable to stop rstudio service"

#######################################################################################################################
# Create Admin Dirs
#######################################################################################################################

sudo mkdir -p /scratch/admin/service-configs/

sudo touch /scratch/admin/service-configs/custom-cron-jobs
sudo cp -rf  /scratch/admin/service-configs/custom-cron-jobs /etc/cron.d/

#######################################################################################################################
#  Configure Docker
#######################################################################################################################
sudo groupmod -g 500 docker
sudo service docker start

#######################################################################################################################
#  Configure Users
#######################################################################################################################
env | grep ^PATH
sudo env | grep ^PATH
sudo bash -c "${BOOTSTRAP_DIR}/create_users.sh"
sudo --preserve-env=AWS_ACCESS_KEY_ID --preserve-env=AWS_SECRET_ACCESS_KEY aws s3 sync --acl private ${ADMIN_DIR}/user-data s3://{{cookiecutter.s3_user_data_bucket}}/user-data

#######################################################################################################################
# Install Grafana
#######################################################################################################################
. /etc/parallelcluster/cfnconfig
case ${cfn_node_type} in
    MasterServer)
        cd /tmp
        wget https://raw.githubusercontent.com/aws-samples/aws-parallelcluster-monitoring/main/post-install.sh
        chmod 777 *sh
        ./post-install.sh
        cd ${BOOTSTRAP_DIR}
    ;;
    ComputeFleet)

    ;;
esac

# Ensure the script exits as 0
exit 0
