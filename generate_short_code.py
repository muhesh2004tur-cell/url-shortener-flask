
import string
import secrets


def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ""

    for i in range(6):
        short_code = short_code + secrets.choice(characters)

    return short_code


code = generate_short_code()
print(code)