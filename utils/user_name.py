from user_management.models import User

def generate_unique_username(first_name, last_name):
    base_username = f"{last_name.lower()}.{first_name.lower()}"
    username = base_username
    counter = 1

    from user_management.models import User
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username