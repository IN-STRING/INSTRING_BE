import string
import secrets
from pwdlib import PasswordHash
from sqlmodel import Session, select
from INewApp.domains.users.models.user_table import User

class AuthManager:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def hash_password(self, password: str):
        return self.password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        return self.password_hash.verify(password, hashed_password)

    @staticmethod
    def make_auth_otp():
        char = string.ascii_letters + string.digits
        otp = ''.join(secrets.choice(char) for _ in range(6))
        return otp

    def check_user(self, session: Session, email: str, password: str):
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

auth_manager = AuthManager()