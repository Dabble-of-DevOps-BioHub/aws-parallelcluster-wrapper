"""Console script for aws_parallelcluster_wrapper."""
import sys
import click

import os
from aws_parallelcluster_wrapper.commands import apply_terraform_state, deploy_pcluster_resources, \
    configure_pcluster_slurm


@click.group(help="CLI to help manage SLURM Clusters with AWS Parallelcluster")
@click.pass_context
def cli(ctx):
    pass


cli.add_command(apply_terraform_state.apply_terraform_state)
cli.add_command(deploy_pcluster_resources.deploy_pcluster_resources)
cli.add_command(configure_pcluster_slurm.create_pcluster)


def main():
    cli()


if __name__ == '__main__':
    main()
