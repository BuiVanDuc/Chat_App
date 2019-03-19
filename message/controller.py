from database.db_utils import sent_message, search_user, get_message, \
    update_is_read_message, get_friends, update_list_friend, get_block_user
from friend.controller import process_data
from utils.date_util import get_date_now, convert_datetime_to_string


def display_sent_message(user_id):
    print('''MESSAGE
    #: List friend message
    *: Search username
    ''')

    total_inbox, list_friends = process_data(user_id)
    print('Inbox ({})'.format(total_inbox))
    option = input("Option:\t")

    if option == "#":
        index = 0

        if len(list_friends) > 0:
            for friend in list_friends:
                index += 1
                if 'unread' in friend:
                    print("{}. {} Unread:({}) [{}]".format(index, friend.get('username'), friend.get('unread'),
                                                           convert_datetime_to_string(friend.get('sent_date'))))
                elif 'seen' in friend:
                    if friend.get('seen') == 0:
                        print("{}. {} (A message delivered) [{}]".format(index, friend.get('username'),
                                                                         convert_datetime_to_string(
                                                                             friend.get('sent_date'))))
                    elif friend.get('seen') == 1:
                        print("{}. {} (Seen) [{}]".format(index, friend.get('username'), convert_datetime_to_string(
                            friend.get('sent_date'))))
                else:
                    print("{}. {} No message".format(index, friend.get('username')))
        else:
            print('No friend message!!')
            return -1
        # Sent message
        print('''
        0: Exit
        Number(in list): View detail and Sent message
        ''')
        try:
            number = int(input("Number:\t"))
            if 0 < number <= len(list_friends):
                receiver_id = list_friends[number - 1].get('id')
                username = list_friends[number - 1].get('username')

                # Show detail message
                list_messages = get_message(user_id, receiver_id)
                print("<<< {}".format(username))
                if len(list_messages) > 0:
                    for message in list_messages:
                        if message['sender'] == user_id:
                            print("me: ({}) [{}]".format(message['message'], message['sent_date']))
                        else:
                            print("{}: ({}) [{}]".format(username, message['message'], message['sent_date']))
                            # Update is read message:
                            time_now = get_date_now()
                            update_is_read_message(user_id, receiver_id, time_now)
                else:
                    print("Say hi to {}".format(username))

                # Check blocked or not
                blocker_user = get_block_user(user_id)
                if len(blocker_user) > 0:
                    for user in blocker_user:
                        if receiver_id == user['id']:
                            print('Can not sen message. Please unblock to send message[{}]'.format(username))
                            return -1
                # Check your friend block user
                blocker_user = get_block_user(receiver_id)
                if len(blocker_user) > 0:
                    for user in blocker_user:
                        if user_id == user['id']:
                            print('Can not sen message. You are blocked [{}]'.format(username))
                            return -1

                message = input("Type a message:\t")

                if len(message) > 0:
                    if sent_message(user_id, receiver_id, message):
                        print("Sent message successfully")
                else:
                    print('message is empty')
                    return -1
            elif number == 0:
                print("Exit")
            else:
                print("invalid option")
        except Exception as Ex:
            print(Ex)
            return -1
    # Search username
    elif option == "*":
        list_friends = get_friends(user_id)
        username = input("Search:\t")
        if len(username) > 0:
            list_username = search_user(username)
            if len(list_username) > 0:
                index = 0
                for username in list_username:
                    index += 1
                    if username in list_friends:
                        print("{}. {} [Friend]".format(index, username.get('username')))
                    else:
                        print("{}. {}".format(index, username.get('username')))
                print('''
                0: Exit
                Number(in list): View detail and sent message
                ''')
                try:
                    number = int(input('Number:\t'))
                    if 0 < number <= len(list_username):
                        user = list_username[number - 1]
                        receiver_id = user.get('id')
                        username = user.get('username')
                        list_messages = get_message(user_id, receiver_id)

                        # Show messages
                        if len(list_messages) > 0:
                            for message in list_messages:
                                if message['sender'] == user_id:
                                    print("me: ({}) [{}]".format(message['message'], message['sent_date']))
                                else:
                                    print("{}: ({}) [{}]".format(username, message['message'], message['sent_date']))

                                # Update is read message:
                                time_now = get_date_now()
                                update_is_read_message(user_id, receiver_id, time_now)
                        else:
                            print("No Message.>>>Say hi to {}".format(username))

                            # Check blocked or not
                            blocker_user = get_block_user(user_id)
                            if blocker_user > 0:
                                for user in blocker_user:
                                    if receiver_id == user['id']:
                                        print(
                                            'Can not sen message. Please unblock to send message[{}]'.format(username))
                                        return -1
                            # Check your friend block user
                            blocker_user = get_block_user(receiver_id)
                            if blocker_user > 0:
                                for user in blocker_user:
                                    if user_id == user['id']:
                                        print('Can not sen message. You are blocked [{}]'.format(username))
                                        return -1

                        message = input("Type a message:\t")
                        if len(message) > 0:
                            if sent_message(user_id, receiver_id, message):
                                print('Successfully')
                                # Update list friend
                                if user not in list_friends:
                                    list_friends.append(user)
                                    update_list_friend(user_id, list_friends)
                            else:
                                print("Could not sent. Sorry!! The system is having trouble")
                                return -1
                        else:
                            print('Message is empty.Please try again!!')
                            return -1
                except Exception as Ex:
                    print(Ex)
                    return -1
            else:
                print('No result!!')
                return -1
        else:
            print('Username empty. Not Found')
            return -1
    else:
        print('Invalid option!!')
        return -1