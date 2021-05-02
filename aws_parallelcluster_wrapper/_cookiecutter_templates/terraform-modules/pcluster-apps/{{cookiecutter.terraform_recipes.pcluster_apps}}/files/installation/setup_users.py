import os
import socket
from user_file_utils import get_users

"""
Once we have create the users, we need to give them proper access
They need to have the 
1. correct variables set in order to access the modules
2. SSH Keys setup
3. A directory on scratch

This script MUST be run as root
"""
user = 'user'


def create_system_dirs():
    os.system('mkdir -p {}'.format(os.environ.get('USER_DATA_DIR')))
    os.system('mkdir -p /scratch/ftp')
    os.system('mkdir -p /apps/users')


def lock_down_admin():
    """Lock down the admin dirs"""
    os.system('chown root:root {}'.format(os.environ.get('ADMIN_DIR')))
    os.system('chmod 770 {}'.format(os.environ.get('ADMIN_DIR')))


def setup_conda_in_apps(this_user):
    """Default conda setup is in ~, but we want it in /apps"""
    os.system('mkdir -p /apps/users/{user}/.conda/pkgs'.format(user=this_user))
    os.system('touch /apps/users/{user}/.conda/pkgs/urls.txt'.format(user=this_user))
    os.system('chown {user}:{user} /apps/users/{user}'.format(user=this_user))
    os.system('chown {user}:{user} /apps/users/{user}/.conda'.format(user=this_user))
    os.system('chown {user}:{user} /apps/users/{user}/.conda/pkgs'.format(user=this_user))
    os.system('chown {user}:{user} /apps/users/{user}/.conda/pkgs/urls.txt'.format(user=this_user))
    os.system('runuser {user} -c "ln -s -f /apps/users/{user}/.conda /home/{user}/"'.format(user=this_user))


def make_ssh_keys(this_user):
    """This creates the ssh keys if they don't already exist. It only needs to be run once.
    Then all SSH keys are placed in a central location in the USER_DATA_DIR"""
    SSH_STORAGE_DIR = os.path.join(os.environ.get('USER_DATA_DIR'), this_user, 'ssh')
    USER_HOME = os.path.join('/home', this_user)
    HOME_SSH_DIR = os.path.join('/home', this_user, '.ssh')

    os.system('mkdir -p {}'.format(SSH_STORAGE_DIR))
    os.system('mkdir -p {}'.format(HOME_SSH_DIR))

    # If we don't already have ssh keys create them in them in the centralized /scratch dir
    if os.path.exists('{SSH_STORAGE_DIR}/id_rsa.pub'.format(SSH_STORAGE_DIR=SSH_STORAGE_DIR)) is False:
        os.system('ssh-keygen -f {SSH_STORAGE_DIR}/id_rsa -N ""'.format(
            SSH_STORAGE_DIR=SSH_STORAGE_DIR))
        os.system(
            'cat {SSH_STORAGE_DIR}/id_rsa.pub > {SSH_STORAGE_DIR}/authorized_keys'.format(
                SSH_STORAGE_DIR=SSH_STORAGE_DIR)
        )

    # if the ssh keys aren't in the user dir copy them over
    if os.path.exists('{HOME_SSH_DIR}/id_rsa.pub'.format(HOME_SSH_DIR=HOME_SSH_DIR)) is False:
        os.system('cp -rf  {SSH_STORAGE_DIR}/*  {HOME_SSH_DIR}'.format(SSH_STORAGE_DIR=SSH_STORAGE_DIR,
                                                                       HOME_SSH_DIR=HOME_SSH_DIR))

    os.system('chmod 700 {HOME_SSH_DIR}'.format(HOME_SSH_DIR=HOME_SSH_DIR))
    os.system('chmod 600 {HOME_SSH_DIR}/authorized_keys'.format(HOME_SSH_DIR=HOME_SSH_DIR))


def setup_user_profile(this_user):
    # Setup HOME
    USER_HOME = os.path.join('/home', this_user)
    if os.path.exists(os.path.join(USER_HOME, '.bashrc')) is False:
        os.system('cp -rf bashrc {}/.bashrc'.format(USER_HOME))
        os.system('chown {}:{} /home/{}/.bashrc'.format(this_user, this_user, this_user))

    # Don't overwrite the existing .bashrc
    if os.path.exists(os.path.join(USER_HOME, '.profile')) is False:
        os.system('cp -rf profile {}/.profile'.format(USER_HOME))
        os.system('chown {user}:{user} /home/{user}/.profile'.format(user=this_user))

    # Using chown -R is very slow when there are a large amount of files
    # So we are only chowning what we have to
    os.system('chown {this_user}:{this_user} /home/{this_user}'.format(this_user=this_user))
    os.system('chown -R {this_user}:{this_user} /home/{this_user}/.ssh'.format(this_user=this_user))


def setup_user_ftp(this_user):
    """
    Setup the user ftp dirs
    :param this_user:
    :return:
    """
    os.system('mkdir -p /scratch/ftp/{}'.format(this_user))
    os.system('chown {this_user}:{this_user} /scratch/ftp/{this_user}'.format(this_user=this_user))
    os.system('chmod 770 /scratch/ftp/{}'.format(this_user))


def user_chowns(this_user):
    """Run a final chown to make sure the permissions are correct"""
    os.system('chown {user}:{user} /home/{user}/.conda'.format(user=this_user))
    os.system('chown {user}:{user} /home/{user}/.bashrc'.format(user=this_user))
    os.system('chown {user}:{user} /home/{user}/.profile'.format(user=this_user))
    os.system('chmod go-w /home/{user}'.format(user=this_user))


def bootstrap():
    """
    Make all the user dirs
    :return:
    """
    for this_user in get_users():

        make_ssh_keys(this_user)
        setup_user_profile(this_user)
        setup_user_ftp(this_user)
        setup_conda_in_apps(this_user)
        user_chowns(this_user)


if __name__ == "__main__":
    create_system_dirs()
    bootstrap()
    lock_down_admin()
