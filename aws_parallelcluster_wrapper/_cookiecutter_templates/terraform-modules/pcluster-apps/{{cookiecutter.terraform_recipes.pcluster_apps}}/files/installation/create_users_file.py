#!/usr/bin/env python3

from user_file_utils import random_string, get_users
import os

"""Add System Users
<Username>:<Password>:<UID>:<GID>:<User Info>:<Home Dir>:<Default Shell>

user1:user1@123:601:601:User 1:/home/user1:/bin/bash
user2:user2@123:602:602:User 2:/home/user2:/bin/bash
user3:user3@123:603:603:User 3:/home/user3:/bin/bash
user4:user4@123:604:604:User 4:/home/user4:/bin/bash
user5:user5@123:605:605:User 5:/home/user5:/bin/bash

"""


if __name__ == "__main__":
    ADMIN_DIR = os.environ.get('ADMIN_DIR')
    USER_DATA_DIR = os.environ.get('USER_DATA_DIR')
    users_file = os.path.join(USER_DATA_DIR, 'users_list.txt')
    user = 'user'
    user_id_range = range(2000, 3000)

    if os.path.exists('{}/user-data/new-users.txt'.format(ADMIN_DIR)) is False:
        f = open("{}/user-data/new-users.txt".format(ADMIN_DIR), "w+")
        for index, this_user in enumerate(get_users()):
            i = user_id_range[index]
            user_line = '{this_user}:password:{i}:{i}:{this_user}:/home/{this_user}:/bin/bash'.format(
                this_user=this_user,
                i=i)
            f.write(user_line)
            f.write("\n")
        f.close()

    if os.path.exists('{}/user-data/chpasswords.txt'.format(ADMIN_DIR)) is False:
        f = open("{}/user-data/chpasswords.txt".format(ADMIN_DIR), "w+")
        for this_user in get_users():
            line = '{}:{}'.format(this_user, random_string(10))
            f.write(line)
            f.write("\n")
        f.close()
