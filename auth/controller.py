from playhouse.shortcuts import model_to_dict

from database.db_utils import login, register
from utils.date_util import validate_date
from utils.email_util import is_email_validated
from utils.password_util import encrypt_string, is_validate_password


def display_login():
    email = input("Email:\t")
    if email and len(email) > 0:
        if is_email_validated(email):
            password = input("password:\t")
            if password and len(password) > 0:
                password = encrypt_string(password)
                user = login(password, email)
                if user:
                    user_id = model_to_dict(user).get('id')
                    print("Log in successfully!")
                    return user_id
                else:
                    print("email or password is incorrect")
                    return -1
            else:
                print("Password is empty!!")
                return -1
        else:
            print("Email is invalid")
            return -1
    else:
        print("email is emtpy!!")
        return -1


def display_register():
    username, password, address, email, fullname, birthday = "", "", "", "", "", ""
    sex = -1
    while True:
        if len(username) > 0:
            if is_email_validated(email):
                if is_validate_password(password):
                    if len(fullname) > 0:
                        if validate_date(birthday):
                            if 0 <= sex <= 4:
                                if len(address) > 0:
                                    confirm_password = input("confirm password:\t")
                                    if password == confirm_password:
                                        password = encrypt_string(password)
                                        if register(username, password, birthday, fullname, email, address, sex):
                                            print("Register successfully")
                                            break
                                        else:
                                            print("Can not register")
                                            break
                                    else:
                                        print("Password confirmation doesn't match password")
                                else:
                                    address = input('Address:\t')
                                    if len(address) <= 0:
                                        print("Address is empty. Please enter address")
                            else:
                                try:
                                    print('''\nOPTION GENDER
                                        male: 0,
                                        female: 1,
                                        gay: 2,
                                        lesbian: 3,
                                        other: 4
                                        ''')
                                    sex = input('Sex:\t')
                                    sex = int(sex)
                                except Exception as Ex:
                                    print(Ex)
                                    sex = -1
                        else:
                            birthday = input("Birthday:\t")
                    else:
                        fullname = input("Full name:\t")
                        if len(fullname) <= 0:
                            print("Full name is empty. Please enter full name!!")
                else:
                    password = input("Password:\t")
            else:
                email = input('email address:\t')
                if not is_email_validated(email):
                    print("Email is invalid. Please enter email again!!")
        else:
            username = input("Username:\t")
            if len(username) <= 0:
                print(" username is empty. Please enter your username")

