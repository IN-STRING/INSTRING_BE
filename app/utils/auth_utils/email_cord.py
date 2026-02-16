import string
import secrets

def make_auth_otp():
    char = string.ascii_letters + string.digits
    otp = ''.join(secrets.choice(char) for _ in range(6))
    return otp