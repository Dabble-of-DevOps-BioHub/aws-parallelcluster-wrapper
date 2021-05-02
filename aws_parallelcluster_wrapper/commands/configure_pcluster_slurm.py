import sys
import click
import random
import string
import os
import json
import logging
from pprint import pprint
from cookiecutter.main import cookiecutter
from datetime import datetime
from jinja2 import Environment, BaseLoader
import boto3

from pcluster.configure.networking import (
    NetworkConfiguration,
    PublicPrivateNetworkConfig,
    automate_subnet_creation,
    automate_vpc_with_subnet_creation,
)
import pcluster.configure.easyconfig as easyconfig

from aws_parallelcluster_wrapper.utils import PCLUSTER_APP_DIR, AMIS_LIST, execute_bash, read_config, write_config, \
    run_cookiecutter

# So much debugging nonsense here
logging.basicConfig(level=logging.INFO)

IA = ['AFTER_7_DAYS', 'AFTER_14_DAYS', 'AFTER_30_DAYS', 'AFTER_60_DAYS', 'AFTER_90_DAYS']


def validate_transition_to_ia(config_data):
    pass


def validate_compute_resource_length(config_data):
    pass


def validate_section_name(name):
    pass


def configure_queue_settings(config_data):
    """Configure the queues and compute resources
    # TODO Need to add a lot of validation
    The format is [compute_resource ]. compute-resource-name must start with a letter, contain no more than 30 characters, and only contain letters, numbers, hyphens (-), and underscores (_).
    The format is [queue ]. queue-name must start with a lowercase letter, contain no more than 30 characters, and only contain lowercase letters, numbers, and hyphens (-).
    At any time, there can be between zero (0) and the max number of dynamic nodes in a [compute_resource].
    compute_resource_settings
    (Required) Identifies the [compute_resource] sections containing the compute resources configurations for this queue. The section names must start with a letter, contain no more than 30 characters, and only contain letters, numbers, hyphens (-), and underscores (_).
    Up to three (3) [compute_resource] sections are supported for each [queue] section
    """
    for compute_resource in config_data['pcluster']['compute_resources']:
        compute_resource['name'] = compute_resource['instance_type'].replace('.', '-')

    queue_settings = []
    for queue in config_data['pcluster']['queues']:
        queue_settings.append(queue['name'])
        instance_types_cleaned = []
        for instance_type in queue['compute_resource_instance_types']:
            instance_types_cleaned.append(instance_type.replace('.', '-'))

        queue['compute_resource_settings'] = ','.join(instance_types_cleaned)

    config_data['pcluster']['queue_settings'] = ','.join(queue_settings)
    return config_data


def get_efs_ids_from_terraform_output(config_data):
    """Grab the EFS Ids from the previous terraform output"""
    for efs in config_data['pcluster']['efs_resources']:
        name = efs['name']
        id = config_data['terraform_output']['pcluster_resources'][name]['value']
        efs['fs_id'] = id
    return config_data


def get_private_subnet(subnet_list):
    for subnet in subnet_list:
        if subnet['name'] == 'ParallelClusterPrivateSubnet':
            return subnet


def get_public_subnet(subnet_list):
    for subnet in subnet_list:
        if subnet['name'] == 'ParallelClusterPublicSubnet':
            return subnet
    # If we can't find or create a subnet something is screwy
    raise Exception("Cannot find or create a suitable subnet")


def pcluster_automate_subnets(config_data):
    vpc_id = config_data['vpc_id']
    min_subnet_size = int(config_data['pcluster']['max_cluster_size'])
    networking_configuration = PublicPrivateNetworkConfig()
    os.environ["AWS_DEFAULT_REGION"] = config_data['aws_region']
    try:
        vpcs_and_subnets = easyconfig._get_vpcs_and_subnets()
        subnet_list = vpcs_and_subnets["vpc_subnets"][vpc_id]
        private_subnet = get_private_subnet(subnet_list)
        public_subnet = get_public_subnet(subnet_list)
        master_subnet_id = public_subnet['id']
        compute_subnet_id = private_subnet['id']
    except Exception:
        subnets = automate_subnet_creation(vpc_id, networking_configuration, min_subnet_size)
        master_subnet_id = subnets['master_subnet_id']
        compute_subnet_id = subnets['compute_subnet_id']

    config_data['pcluster']['master_subnet_id'] = master_subnet_id
    config_data['pcluster']['compute_subnet_id'] = compute_subnet_id
    return config_data


@click.command()
@click.option('--config', default=os.path.join(os.getcwd(), 'cookiecutter.json'))
@click.option('--outdir', default=os.path.join(os.getcwd(), 'project', 'pcluster-apps'))
@click.option('--apply/--no-apply', default=False)
@click.option('--init/--no-init', default=True)
@click.option('--create/--no-create', default=False)
@click.pass_context
def create_pcluster(ctx, config, outdir, apply, init, create):
    """Configure Pcluster"""
    config = os.path.abspath(config)
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)

    config_data = read_config(config)
    logging.info('Finding or Creating Subnets')
    config_data = pcluster_automate_subnets(config_data)
    logging.info('Configuring Queues')
    config_data = configure_queue_settings(config_data)
    logging.info('Configuring EFS')
    config_data = get_efs_ids_from_terraform_output(config_data)
    write_config(config, config_data)
    config_data['_copy_without_render'] = [
        'files/installation/deploy_jupyterhub/jupyterhub_config.py'
    ]
    write_config(config, config_data)

    new_work_dir = os.path.join(outdir, config_data['terraform_recipes']['pcluster_apps'])

    logging.info('Running cookiecutter')

    run_cookiecutter(
        outdir=outdir,
        current_work_dir=os.getcwd(),
        new_work_dir=new_work_dir,
        cookiecutter_dir=PCLUSTER_APP_DIR,
        config_data=config_data,
        apply=apply,
        init=init
    )

    os.chdir(new_work_dir)
    if create:
        execute_bash('pcluster create -c config {project}-{id}-{stage}'.format(
            id=config_data['id'],
            project=config_data['project'],
            stage=config_data['stage']
        ))
    # client = boto3.client('cloudformation')
