from database.db_utils import get_friends, detail_user, search_user, update_list_friend, get_block_user, update_block, \
    list_friend_by_sent_date


def process_data(user_id):
    '''
    :param user_id:
    :return: list friend is order by time desc
    '''
    list_friends_message = list_friend_by_sent_date(user_id)
    list_ids = list()
    list_items = list()
    total_inbox = 0

    for friend in list_friends_message:
        item = dict()
        if friend.get('sender') == user_id:
            if friend.get('receiver') not in list_ids:
                item['id'] = friend.get('receiver')
                item['seen'] = friend.get('is_read')
                item['sent_date'] = friend.get('sent_date')
                # Update list ID
                list_ids.append(friend.get('receiver'))
                # Append item to list
                list_items.append(item.copy())
        elif friend.get('receiver') == user_id:
            if friend.get('sender') not in list_ids:
                item['unread'] = 0
                if friend.get('is_read') == 0:
                    item['unread'] = 1
                    total_inbox += 1
                item['id'] = friend.get('sender')
                item['sent_date'] = friend.get('sent_date')
                # Update list ID
                list_ids.append(friend.get('sender'))
                # Append item to list
                list_items.append(item.copy())
            else:
                if friend.get('is_read') == 0:
                    for item in list_items:
                        if item.get('id') == friend.get('sender') and 'unread' in item:
                            item['unread'] += 1
                            total_inbox += 1

    list_friends = get_friends(user_id)

    for data in list_items:
        flag = 0
        for friend in list_friends:
            if data['id'] == friend['id']:
                flag = 1
                data.update({'username': friend['username']})
        if flag == 0:
            username = detail_user(data['id'])[0].get('username')
            data.update({'username': username})

    ret_data = list_items

    # Friend not in message
    for friend in list_friends:
        for data in list_items:
            if friend['id'] != data['id']:
                ret_data.append(friend)

    return total_inbox, ret_data


def search_friends(user_id, username):
    if len(username) > 0:
        list_friends = get_friends(user_id)
        ret_friend = list()

        for friend in list_friends:
            if username.lower() in friend['username'].lower():
                ret_friend.append(friend)
        return ret_friend
    else:
        return -1


def sort_username_friend(list_friend):
    if len(list_friend) > 1:
        new_list_friend = sorted(list_friend, key=lambda k: k['username'].lower())
        return new_list_friend
    else:
        return list_friend


def remove_friend(user_id, obj):
    list_friends = get_friends(user_id)

    list_friends.remove(obj)
    # Update friend
    if update_list_friend(user_id, list_friends):
        return True

    return False


def display_view_friend(user_id):
    if get_friends(user_id):
        if len(get_friends(user_id)) > 0:
            list_friend = get_friends(user_id)
            index = 0
            for friend in list_friend:
                index += 1
                print("{}. {}".format(index, friend.get('username')))

            print('''\n DETAIL FRIEND
            0: Exit
            Number(in list): Detail a friend
            *: Search friend in list
            ''')
            try:
                option = input('Option:\t')
                if option == '*':
                    username = input("Search:\t")
                    list_friends_temp = search_user(username)
                    if list_friends_temp and len(list_friends_temp) > 0:
                        index = 0
                        for friend in list_friends_temp:
                            index += 1
                            print("{}. {}".format(index, friend.get('username')))

                        print('''\n DETAIL FRIEND
                        0: Exit
                        Number(in list): Detail a friend
                        ''')
                        number = int(input("Number:\t"))

                        if 0 < number <= len(list_friends_temp):
                            friend = list_friends_temp[number - 1]
                            id = friend.get('id')
                            item = detail_user(id)

                            for key, value in item.items():
                                if value is not None:
                                    print("{}: {}".format(key, value))

                            print('''REMOVE
                            0: Exit
                            1: Remove
                            ''')
                            number = int(input("Number:\t"))

                            if number == 0:
                                print("Exit")
                            elif number == 1:
                                if remove_friend(user_id, friend):
                                    print('Remove successfully')
                                else:
                                    print("Can not remove!!")
                                    return -1
                            else:
                                print('Invalid option')
                                return -1
                        elif number == 0:
                            print('Exit')
                        else:
                            print('Not invalid number. Please try again')
                            return -1
                    else:
                        print('No result')
                        return -1
                elif 0 < int(option) <= len(list_friend):
                    id = list_friend[int(option) - 1].get('id')
                    info = detail_user(id)[0]

                    for key, value in info.items():
                        if value is not None:
                            print("{}: {}".format(key, value))

                    print('''REMOVE
                    0: Exit
                    1: Remove
                    ''')
                    number = int(input("Number:\t"))

                    if number == 0:
                        print("Exit")
                    elif number == 1:
                        if remove_friend(user_id, friend):
                            print('Remove successfully')
                        else:
                            print("Can not remove!!")
                            return -1
                    else:
                        print('Invalid option')
                        return -1

                elif int(option) == 0:
                    print('Exit')
                else:
                    print('Not invalid number. Please try again')
                    return -1
            except Exception as Ex:
                print(Ex)
                return -1
        else:
            print('No Friend')
            return -1
    else:
        print('Not Found !')
        return -1


def display_add_friend(user_id):
    # Search friend by name
    username = input("Search username:\t")
    if len(username) > 0:
        list_users = search_user(username)
        if list_users and len(list_users) > 0:
            index = 0
            list_friends = get_friends(user_id)
            for user in list_users:
                index += 1
                if user in list_friends:
                    print("{}. {} [Friend]".format(index, user['username']))
                else:
                    print("{}. {} ".format(index, user['username']))
            try:
                print('''\n ADD FRIEND
                0: Exit
                Number(in list): Add friend
                ''')
                number = int(input("Number:\t"))
                if 0 < number <= len(list_users):
                    list_friends = get_friends(user_id)
                    if list_friends and len(list_friends) >= 0:
                        # Check friend is existed or not
                        friend_id = list_users[number - 1].get('id')
                        for friend in list_friends:
                            if friend_id == friend.get('id'):
                                print('Friend is existed!!')
                                return -1
                    friend = list_users[number - 1]
                    list_friends.append(friend)
                    new_list_friend = sort_username_friend(list_friends)
                    if update_list_friend(user_id, new_list_friend):
                        print("Add friend successfully")
                    else:
                        list_friends = list()
                        list_friends.append(friend)
                        if update_list_friend(list_friends):
                            print("Add friend successfully")
                elif number == 0:
                    print("Exit")
                else:
                    print('Invalid number. Please try again')
                    return -1
            except Exception as Ex:
                print(Ex)
        else:
            print("No result")
            return -1
    else:
        print('Username is empty!!')
        return -1


def display_block_user(user_id):
    block_user = get_block_user(user_id)
    username = input("Search:\t")
    if len(username) > 0:
        list_users = search_user(username)
        index = 0
        for user in list_users:
            # Except user self
            index += 1
            if user in block_user:
                print("{}. {} has blocked".format(index, user['username']))
            else:
                print("{}. {}".format(index, user['username']))
        try:
            print('''\n BLOCK USER
                0: Exit
                Number(in list): Blocked
                ''')
            number = int(input('Number:\t'))
            if 0 < number <= len(list_users):
                user = list_users[number - 1]
                # Except user block self
                if user not in block_user:
                    if user.get('id') == user_id:
                        print('Can not bock.Just You!!')
                        return -1

                    block_user.append(user)
                    update_block(user_id, block_user)
                    print("Block is successfully")
                else:
                    print("{} has blocked. Can not block!!".format(user['username']))
                    return -1
            elif number == 0:
                print("Exit")
            else:
                print('Invalid. Please try again')
        except Exception as Ex:
            print(Ex)
            return -1


def display_unblock(user_id):
    block_user = get_block_user(user_id)
    if len(block_user) > 0:
        print('''LIST BLOCK USER
        ''')
        index = 0
        for user in block_user:
            index += 1
            print("{}. {}".format(index, user['username']))
        try:
            print('''\n UNBLOCK USER
            0: Exit
            Number(in list): Unblock
            ''')
            number = int(input("Number:\t"))
            if 0 < number <= len(block_user):
                del block_user[number - 1]
                update_block(user_id, block_user)
                print('Unblock successfully')
            elif number == 0:
                print("Exit")
            else:
                print("Invalid. Please Try again!!")
                return -1
        except Exception as Ex:
            print(Ex)
            return -1
    else:
        print('No block user')
        return -1