import os
import string
import random

user_data_dir = os.environ.get('USER_DATA_DIR') or '/scratch/admin/user-data'


def chpass_file():
    """Users formatted in a file to read in by the linxu command chpass"""
    global user_data_dir
    return os.path.join(user_data_dir, 'chpasswords.txt')


def new_users_file():
    """Users formatted in a file to read in by the linxu command newusers"""
    global user_data_dir
    return os.path.join(user_data_dir, 'new-users.txt')


def users_list_file():
    """This is just a plain text list of usernames"""
    global user_data_dir
    return os.path.join(user_data_dir, 'users_list.txt')


def get_chpass_data():
    fh = open(chpass_file())
    users = fh.readlines()
    users_data = [l.strip() for l in users]
    fh.close()
    return users_data


def get_users():
    """Users are listed one user per line
    user1
    user2
    etc
    returns [users]"""
    fh = open(users_list_file())
    users = fh.readlines()
    return [u.strip() for u in users]


def random_string(string_len=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_len))
