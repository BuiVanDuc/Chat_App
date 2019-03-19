from playhouse.shortcuts import model_to_dict

from database.models import ChatAppUser, ChatAppMessage

'''
AUTHENTICATION
'''


def login(password, email):
    try:
        user = ChatAppUser.get(ChatAppUser.email == email, ChatAppUser.password == password)
        return user
    except ChatAppUser.DoesNotExist:
        return None


def register(username, password, birthday, fullname, email, address, sex=None):
    try:
        ChatAppUser.create(username=username, password=password, birthday=birthday, fullname=fullname, email=email,
                           address=address,
                           sex=sex)
        return True
    except Exception as Ex:
        print(Ex)
        return False


'''
FRIEND
'''


def get_friends(user_id):
    try:
        query = ChatAppUser.select(ChatAppUser.friend).where(ChatAppUser.id == user_id)
        return model_to_dict(query.get()).get('friend')
    except ChatAppUser.DoesNotExist:
        return None


def detail_user(user_id):
    try:
        user = ChatAppUser.select(ChatAppUser.fullname, ChatAppUser.email, ChatAppUser.sex, ChatAppUser.birthday,
                                  ChatAppUser.address).where(ChatAppUser.id == user_id)
        return list(user.dicts())
    except ChatAppUser.DoesNotExist:
        return None


def search_user(username):
    try:
        users = ChatAppUser.select(ChatAppUser.id, ChatAppUser.username).order_by(ChatAppUser.username.asc()).where(
            ChatAppUser.username.contains(username))
        return list(users.dicts())
    except Exception as Ex:
        print(Ex)
        return None


def update_list_friend(user_id, list_friend):
    try:
        query = (ChatAppUser
                 .update({ChatAppUser.friend: list_friend})
                 .where(ChatAppUser.id == user_id))
        if query.execute() >= 1:
            return True
    except ChatAppUser.DoesNotExist:
        return False

    return False


def get_block_user(user_id):
    try:
        query = ChatAppUser.select(ChatAppUser.block_user).where(ChatAppUser.id == user_id)
        return model_to_dict(query.get()).get('block_user')
    except ChatAppUser.DoesNotExist:
        return None


def update_block(user_id, list_block_user):
    try:
        query = (ChatAppUser
                 .update({ChatAppUser.block_user: list_block_user})
                 .where(ChatAppUser.id == user_id))
        if query.execute() >= 1:
            return True
    except ChatAppUser.DoesNotExist:
        return False

    return False


'''
MESSAGE
'''


def get_message(sender_id, receiver_id):
    try:
        messages = (
            (ChatAppMessage.select().where(ChatAppMessage.sender == sender_id, ChatAppMessage.receiver == receiver_id) |
             (ChatAppMessage.select().where(ChatAppMessage.sender == receiver_id,
                                            ChatAppMessage.receiver == sender_id))).order_by(
                ChatAppMessage.sent_date.asc()))
        return list(messages.dicts())
    except ChatAppMessage.DoesNotExist:
        return None


def sent_message(sender_id, receiver_id, message):
    try:
        ChatAppMessage.create(sender_id=sender_id, receiver_id=receiver_id, message=message)
        return True
    except Exception as Ex:
        print(Ex)
        return False


def update_is_read_message(user_id, sender, date):
    try:
        query = (ChatAppMessage
                 .update({ChatAppMessage.is_read: 1, ChatAppMessage.read_date: date})
                 .where(ChatAppMessage.receiver == user_id, ChatAppMessage.sender == sender)
                 )
        if query.execute() >= 1:
            return True
    except ChatAppMessage.DoesNotExist:
        return False
    return False


def list_friend_by_sent_date(user_id):
    try:
        query = (ChatAppMessage
                 .select(ChatAppMessage.sender, ChatAppMessage.receiver, ChatAppMessage.is_read, ChatAppMessage.message,
                         ChatAppMessage.sent_date)
                 .where((ChatAppMessage.sender == user_id) |
                        (ChatAppMessage.receiver == user_id))
                 .order_by(ChatAppMessage.sent_date.desc())
                 )
        return list(query.dicts())
    except Exception as Ex:
        print(Ex)


if __name__ == '__main__':
    # user= login('Mvs@12345', 'testnv@gmail.com')
    # print(user)
    # print(model_to_dict(user))
    # print(login('Mvs@12345', '0163800ff'))
    list_friend_by_sent_date(1)
    # print(detail_user([]))
    # print(update_friend(1, [{'id': 1, 'username': 'testnv'}, {'id': 2, 'username': 'ducbv'}]))
    # print(sent_message(3, 1, 'xin chao'))
    # time_now = get_date_now()
    # print(update_is_read_message(2, 1, time_now))
