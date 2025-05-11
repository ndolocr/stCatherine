import re
from datetime import datetime
 
def validate_name(name):
    if re.fullmatch(r'[A-Za-z]+', name):
        return True
    return False

def validate_gender(gender):
    return gender.capitalize() in {"Male", "Female"}

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    return False

def is_alphanumeric(value):
    if re.match(r'^[A-Za-z0-9]+$', value):
        return True
    return False

def validate_phone_num(phone_num):
    if re.fullmatch(r'\d{9}', phone_num) and len(phone_num)==12:
        return True
    return False

def validate_date(date_string):
    date_format='%Y-%m-%d'
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False