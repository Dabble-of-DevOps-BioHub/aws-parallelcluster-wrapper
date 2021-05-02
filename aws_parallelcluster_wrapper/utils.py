import os
import signal
from subprocess import PIPE, STDOUT, Popen
from tempfile import TemporaryDirectory, gettempdir
import logging
from cookiecutter.main import cookiecutter
import json

logging.basicConfig(level=logging.INFO)

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))

TERRAFORM_STATE_DIR = os.path.join(MODULE_DIR, '_cookiecutter_templates', 'terraform-modules', 'terraform-state')
PCLUSTER_RESOURCES_DIR = os.path.join(MODULE_DIR, '_cookiecutter_templates', 'terraform-modules', 'pcluster-resources')
PCLUSTER_APP_DIR = os.path.join(MODULE_DIR, '_cookiecutter_templates', 'terraform-modules', 'pcluster-apps')

PCLUSTER_VERSION = '2.10.1'
AMIS_LIST = 'https://raw.githubusercontent.com/aws/aws-parallelcluster/v{version}/amis.txt'.format(
    version=PCLUSTER_VERSION)


def write_config(config, config_data):
    with open(config, 'w') as outfile:
        # Make sure NOT to sort the keys.
        # Cookiecutter requires that the variables be in order
        json.dump(config_data, outfile, indent=4)


def read_config(config):
    with open(config) as f:
        data = json.load(f)
    return data


def execute_bash(command, switch_cwd=False):
    """
    Execute the bash command in a temporary directory
    which will be cleaned afterwards
    """
    output_encoding = 'utf-8'
    logging.info('Tmp dir root location: \n %s', gettempdir())

    # Prepare env for child process.
    env = os.environ.copy()

    with TemporaryDirectory(prefix='airflowtmp') as tmp_dir:

        def pre_exec():
            # Restore default signal disposition and invoke setsid
            for sig in ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ'):
                if hasattr(signal, sig):
                    signal.signal(getattr(signal, sig), signal.SIG_DFL)
            os.setsid()

        logging.info('Running command: %s', command)
        cwd = os.getcwd()
        if switch_cwd:
            cwd = tmp_dir

        sub_process = Popen(  # pylint: disable=subprocess-popen-preexec-fn
            ['bash', "-c", command],
            stdout=PIPE,
            stderr=STDOUT,
            cwd=cwd,
            env=env,
            preexec_fn=pre_exec,
        )

        logging.info('Output:')
        line = ''
        for raw_line in iter(sub_process.stdout.readline, b''):
            line = raw_line.decode(output_encoding).rstrip()
            logging.info("%s", line)

        sub_process.wait()

        logging.info('Command exited with return code %s', sub_process.returncode)

        if sub_process.returncode != 0:
            raise Exception('Bash command failed. The command returned a non-zero exit code.')

    return line


def run_terraform_init():
    execute_bash('terraform init -input=false')
    execute_bash('terraform refresh')
    execute_bash('terraform plan')


def run_terraform_apply():
    execute_bash('terraform apply -auto-approve')
    execute_bash('terraform output -json > terraform-output.json')


def get_terraform_output(outdir):
    json_file = os.path.join(outdir, 'terraform-output.json')
    return read_config(json_file)


def run_cookiecutter(outdir, current_work_dir, new_work_dir, cookiecutter_dir, config_data, apply=False, init=True,
                     ):
    logging.info('Running cookiecutter {}'.format(cookiecutter_dir))
    os.makedirs(new_work_dir, exist_ok=True)

    cookiecutter(
        cookiecutter_dir,  # path/url to cookiecutter template
        overwrite_if_exists=True,
        extra_context=config_data,
        output_dir=outdir,
        no_input=True,
    )

    os.chdir(new_work_dir)
    logging.info('Changing workdir to {}'.format(new_work_dir))
    logging.info('Running Terraform')

    # May change these
    if init:
        run_terraform_init()
    if init and apply:
        run_terraform_apply()

    os.chdir(current_work_dir)
