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

from aws_parallelcluster_wrapper.utils import TERRAFORM_STATE_DIR, read_config, write_config, execute_bash

logging.basicConfig(level=logging.DEBUG)


@click.command()
@click.option('--config', default=os.path.join(os.getcwd(), 'cookiecutter.json'))
@click.option('--outdir', default=os.path.join(os.getcwd(), 'terraform-recipes', 'terraform-state'))
@click.pass_context
def apply_terraform_state(ctx, config, outdir):
    """Apply the terraform state"""

    config = os.path.abspath(config)
    outdir = os.path.abspath(outdir)

    # random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    random_string = datetime.today().strftime('%Y%m%d')
    # click.echo(click.style('Hello World!', fg='green', bold=True))

    config_data = read_config(config)
    if not config_data['id']:
        config_data['id'] = random_string

    # outdir = os.path.join(outdir, config_data['terraform_recipes']['terraform_state'])
    os.makedirs(outdir, exist_ok=True)
    current_work_dir = os.getcwd()
    new_work_dir = os.path.join(outdir, config_data['terraform_recipes']['terraform_state'])

    # TODO Add a force flag
    # TODO Test switch over to run_cookiecutter function
    if not os.path.exists(new_work_dir):
        cookiecutter(
            TERRAFORM_STATE_DIR,  # path/url to cookiecutter template
            overwrite_if_exists=True,
            extra_context=config_data,
            output_dir=outdir,
            no_input=True
        )

        logging.info('Changing workdir to {}'.format(new_work_dir))
        os.chdir(new_work_dir)

        execute_bash('terraform init')
        execute_bash('terraform refresh')
        execute_bash('terraform plan')
        execute_bash('terraform apply -auto-approve')

        os.chdir(current_work_dir)
        write_config(config, config_data)

    else:
        logging.info('Terraform state dir already exists! Doing nothing.')
