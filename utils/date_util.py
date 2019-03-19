from datetime import datetime


def validate_date(date_str, date_format="%d-%m-%Y"):
    try:
        date_obj = datetime.strptime(date_str, date_format)
        return date_obj
    except ValueError:
        print("Format birth of date dd-mm-YYYY")


def convert_datetime_to_string(date_time, format='%H:%M,%d-%m-%Y'):
    if isinstance(date_time, datetime):
        date_time_str = date_time.strftime(format)
        return date_time_str
    print("Input datetime not validate!")
    return None

def get_date_now():
    return datetime.now()
