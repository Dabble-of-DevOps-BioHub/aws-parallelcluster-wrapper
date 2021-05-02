#!/usr/bin/env python3

import os
from user_file_utils import get_users, random_string, get_chpass_data, new_users_file, chpass_file, users_list_file
import argparse


def add_user_to_chpass_file(args):
    users_data = get_chpass_data()
    users = []
    for user_data in users_data:
        user_data = user_data.split(':')
        users.append(user_data[0])

    if args.username in users:
        print('User {} already exists in chpassword file'.format(args.username))
    else:
        fh = open(chpass_file(), 'a')
        fh.write("{}:{}\n".format(args.username, random_string()))
        fh.close()


def add_user_to_new_users_file(args):
    """
    Parse the file that we then read in to the linux command newusers
    File format is:
    ania:password:2011:2011:ania:/home/ania:/bin/bash
    user:password:user_id:group_id:group:home:shell
    :param args:
    :param users:
    :return:
    """
    fh = open(new_users_file())
    users = fh.readlines()
    users_data = [l.strip() for l in users]
    users = []
    for user_data in users_data:
        user_data = user_data.split(':')
        users.append(user_data[0])
    fh.close()

    if args.username in users:
        print('User: {} is already here'.format(args.username))
    else:
        # Get the last userid so we can increment by 1
        len_user_data = len(users_data)
        last_user_id = int(users_data[len_user_data - 1].split(':')[2])

        new_users_line = [
            args.username,
            'password',
            str(last_user_id + 1),
            str(last_user_id + 1),
            args.username,
            os.path.join('/home', args.username),
            '/bin/bash'
        ]
        new_users_line = ':'.join(new_users_line)
        fh = open(new_users_file(), 'a')
        fh.write("{}\n".format(new_users_line))
        fh.close()


def add_user_to_users_file(args):
    users_file = users_list_file()
    users = get_users()
    if args.username in users:
        print('User {} already exists.'.format(args.username))
    else:
        fh = open(users_file, "a")
        fh.write("{}\n".format(args.username))
        fh.close()


def get_args():
    parser = argparse.ArgumentParser(description='Add a user to the cluster')
    parser.add_argument('username',
                        help='username to add',
                        )

    return parser.parse_args()


if __name__ == "__main__":
    t_args = get_args()
    add_user_to_users_file(t_args)
    add_user_to_new_users_file(t_args)
    add_user_to_chpass_file(t_args)
