#################################################################
# Custom Configuration
#################################################################

import batchspawner

#################################################################
# Networking
#################################################################

c.JupyterHub.bind_url = 'http://0.0.0.0:8000'
#c.Jupyterhub.ip = '0.0.0.0'
#c.Jupyterhub.port = 80
c.Application.log_level = 'DEBUG'
c.Spawner.default_url = '/lab'

# Hub IP
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8081
# Use the private DNS so we aren't exposing the API publically!
# Go to the EC2 instance and get the PRIVATE IP4 address 172.31.48.251
#  ip-172-31-48-251.eu-west-2.compute.internal
c.JupyterHub.hub_connect_ip = 'ip-172-31-96-234.ec2.internal'

c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'
c.JupyterHub.cookie_secret_file = '/apps/software-configs/jupyterhub/jupyterhub_cookie_secret'

#################################################################
# Authentication
#################################################################

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
c.PAMAuthenticator.open_sessions = False
# This is just for debugging until SSL is set
# c.Authenticator.admin_users = set(['jillian',])

#################################################################
# Batchspawner
#################################################################

#c.Spawner.ip = '0.0.0.0'
#c.ProfilesSpawner.ip = '0.0.0.0'
#
c.Spawner.debug = True
##c.JupyterHub.spawner_class = 'batchspawner.SlurmSpawner'
#c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'
c.BatchSpawnerBase.debug = True
## Sometimes we have to wait awhile for a node to spin up
c.Spawner.http_timeout = 60
c.Spawner.start_timeout = 500

#------------------------------------------------------------------------------
# BatchSpawnerBase configuration
#   Providing default values that we may omit in the profiles
#------------------------------------------------------------------------------

c.BatchSpawnerBase.req_nprocs = '2'
c.BatchSpawnerBase.req_partition = 'dev'
c.BatchSpawnerBase.req_runtime = '1:00:00'
c.BatchSpawnerBase.req_memory = '2gb'
c.BatchSpawnerBase.req_options = ''

c.SlurmSpawner.batch_script = """#!/bin/bash
#SBATCH --output={{homedir}}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --chdir={{homedir}}
#SBATCH --export={{keepvars}}
#SBATCH --get-user-env=L
{% if partition  %}#SBATCH --partition={{partition}}
{% endif %}{% if runtime    %}#SBATCH --time={{runtime}}
{% endif %}{% if memory     %}#SBATCH --mem={{memory}}
{% endif %}{% if gres       %}#SBATCH --gres={{gres}}
{% endif %}{% if nprocs     %}#SBATCH --cpus-per-task={{nprocs}}
{% endif %}{% if reservation%}#SBATCH --reservation={{reservation}}
{% endif %}{% if options    %}#SBATCH {{options}}{% endif %}
set -euo pipefail
trap 'echo SIGTERM received' TERM

module load Miniconda3
source activate /apps/easybuild/1.0/software/jupyterhub/0.9.4


env |grep JUP

{{prologue}}
which jupyterhub-singleuser
{% if srun %}{{srun}} {% endif %}{{cmd}}
echo "jupyterhub-singleuser ended gracefully"
{{epilogue}}
"""

import shlex

import batchspawner
from jupyterhub.spawner import LocalProcessSpawner
from .slurm_form_spawner import SlurmFormSpawner

c.JupyterHub.spawner_class = SlurmFormSpawner


