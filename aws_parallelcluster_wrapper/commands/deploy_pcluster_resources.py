import sys
import click
import random
import string
import os
import json
import logging
from pprint import pprint
import requests
from cookiecutter.main import cookiecutter
from aws_parallelcluster_wrapper.utils import PCLUSTER_RESOURCES_DIR, AMIS_LIST, execute_bash, run_cookiecutter, \
    read_config, write_config, get_terraform_output

"""
Deploy resources needed for PCluster
S3 buckets - admin and user data 
Custom AMI - Install S3 and SSH Fuse, RStudio Server, Python3, vsftp

the files directory has helper directories and scripts
"""

logging.basicConfig(level=logging.DEBUG)


def get_custom_ami_id(config_data):
    r = requests.get(AMIS_LIST)
    amis_list = r.content.decode('UTF-8')
    amis_list = amis_list.split('\n')
    alinux2_list = {}

    # Should probably give a choice between x86_64 and amd
    seen_x86_64 = 0
    seen_alinux2 = 0
    for line in amis_list:
        if '##' in line:
            seen_x86_64 = 0
            if 'x86_64' in line:
                seen_x86_64 = 1
        elif '#' in line:
            seen_alinux2 = 0
            if 'alinux2' in line:
                seen_alinux2 = 1
        else:
            if seen_alinux2 and seen_x86_64:
                t = line.split(': ')
                t[0] = t[0].strip()
                t[1] = t[1].strip()
                alinux2_list[t[0]] = t[1]

    config_data['custom_ami_id'] = alinux2_list[config_data['aws_region']]
    return config_data


@click.command()
@click.option('--config', default=os.path.join(os.getcwd(), 'cookiecutter.json'))
@click.option('--outdir', default=os.path.join(os.getcwd(), 'project', 'terraform-state'))
@click.option('--apply/--no-apply', default=False)
@click.pass_context
def deploy_pcluster_resources(ctx, config, outdir, apply):
    """Apply the terraform state"""
    config = os.path.abspath(config)
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)

    config_data = read_config(config)
    config_data = get_custom_ami_id(config_data)
    write_config(config, config_data)

    new_work_dir = os.path.join(outdir, config_data['terraform_recipes']['pcluster_resources'])
    current_work_dir = os.getcwd()

    run_cookiecutter(
        outdir=outdir,
        current_work_dir=current_work_dir,
        new_work_dir=new_work_dir,
        cookiecutter_dir=PCLUSTER_RESOURCES_DIR,
        config_data=config_data,
        apply=apply,
    )

    logging.info('Deploy pcluster resources: Success')

    terraform_output = get_terraform_output(new_work_dir)

    if 'terraform_output' not in config_data:
        config_data['terraform_output'] = {}
    config_data['terraform_output']['pcluster_resources'] = terraform_output
    write_config(config, config_data)
