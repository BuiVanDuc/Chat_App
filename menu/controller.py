MENU_CHAT_APP = '''\n MANAGE CHAT APP
1. Login
2. Register
3. Exit
'''

MENU_MAIN = '''\n MANAGE MAIN
1. Message
2. Friend
3. Logout
'''
MENU_MESSAGE = '''\n MANAGE MESSAGE
1. View and Send
2. Back to main
'''

MENU_FRIEND = '''\n MANAGE FRIEND
1. View
2. Add friend
3. Block
4. Unblock
5. Back to main
'''


def display_menu(menu):
    if menu == 1:
        print(MENU_CHAT_APP)
    elif menu == 2:
        print(MENU_MAIN)
    elif menu == 3:
        print(MENU_MESSAGE)
    elif menu == 4:
        print(MENU_FRIEND)
    try:
        option = input('option:\t')
        return int(option)
    except Exception as Ex:
        print(Ex)
        return -1
