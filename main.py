import sys

from auth.controller import display_login, display_register
from database.models import migrator
from friend.controller import display_view_friend, display_add_friend, display_block_user, display_unblock
from menu.controller import display_menu
from message.controller import display_sent_message


# sync_logger.info("Main", "test logger")

def main(user_id):
    while True:
        option = display_menu(2)
        if option == 1:
            # Message
            option = display_menu(3)
            if option == 1:
                '''
                    View and Send
                '''
                display_sent_message(user_id)
            elif option == 2:
                print('Back to main')
            else:
                print('Invalid option. Please option number message menu')
        elif option == 2:
            # Friend
            option = display_menu(4)
            if option == 1:
                '''
                    View
                '''
                display_view_friend(user_id)
            elif option == 2:
                '''
                    Add friend
                '''
                display_add_friend(user_id)
            elif option == 3:
                '''
                    Block
                '''
                display_block_user(user_id)
            elif option == 4:
                '''
                    Unblock
                '''
                display_unblock(user_id)
            elif option == 5:
                print('Back to main')
            else:
                print('Invalid option. Please option number friend menu')
        elif option == 3:
            # Logout
            break
        else:
            print('Invalid option. Please option: 1, 2 or 3')


def migrate():
    migrator.run()


def auth():
    while True:
        option = display_menu(1)
        if option == 1:
            user_id = display_login()
            print(user_id)
            if user_id >= 0:
                main(user_id)
        elif option == 2:
            display_register()
        elif option == 3:
            break
        else:
            print('Invalid option. Please option: 1, 2 or 3')


if __name__ == '__main__':
    if sys.argv and len(sys.argv) > 1 and sys.argv[1] == "migrate":
        migrate()
    else:
        auth()
