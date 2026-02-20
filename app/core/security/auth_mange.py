import string
import secrets
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import Session, select
from app.core.config import settings
from app.models.postgresDB.maintable.user import User

class AuthManager:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
        self.secret_key = settings.KEY
        self.algorithm = "HS256"

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