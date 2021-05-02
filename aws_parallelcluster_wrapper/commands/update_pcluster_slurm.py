
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

from aws_parallelcluster_wrapper.commands.configure_pcluster_slurm import read_config, pcluster_automate_subnets, configure_queue_settings, get_efs_ids_from_terraform_output
# So much debugging nonsense here
logging.basicConfig(level=logging.INFO)

IA = ['AFTER_7_DAYS', 'AFTER_14_DAYS', 'AFTER_30_DAYS', 'AFTER_60_DAYS', 'AFTER_90_DAYS']

@click.command()
@click.option('--config', default=os.path.join(os.getcwd(), 'cookiecutter.json'))
@click.option('--outdir', default=os.path.join(os.getcwd(), 'project', 'pcluster-apps'))
@click.option('--apply/--no-apply', default=False)
@click.option('--init/--no-init', default=True)
@click.option('--create/--no-create', default=False)
@click.pass_context
def update_pcluster(ctx, config, outdir, apply, init, create):
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

    # run_cookiecutter(
    #     outdir=outdir,
    #     current_work_dir=os.getcwd(),
    #     new_work_dir=new_work_dir,
    #     cookiecutter_dir=PCLUSTER_APP_DIR,
    #     config_data=config_data,
    #     apply=apply,
    #     init=init
    # )

    os.chdir(new_work_dir)
    if create:
        execute_bash('pcluster update -c config {project}-{id}-{stage}'.format(
            id=config_data['id'],
            project=config_data['project'],
            stage=config_data['stage']
        ))
    # client = boto3.client('cloudformation')
