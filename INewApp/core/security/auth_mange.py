import string
import secrets
from pwdlib import PasswordHash
from fastapi_mail import MessageSchema
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from INewApp.domains.users.models.user_table import User
from INewApp.core.redis_set import redis_client
from INewApp.core.config import fm

class AuthManager:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()


    def hash_password(self, password: str):
        return self.password_hash.hash(password)


    def verify_password(self, password: str, hashed_password: str):
        return self.password_hash.verify(password, hashed_password)


    @staticmethod
    def _make_auth_otp():
        char = string.ascii_letters + string.digits
        otp = ''.join(secrets.choice(char) for _ in range(6))
        return otp

    async def check_user(self, session: AsyncSession, email: str, password: str):
        result = await session.exec(select(User).where(User.email == email))
        user = result.first()
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user


    async def send_otp(self, email: str, prefix: str = "verify"):
        otp = self._make_auth_otp()
        redis_client.setex(f"{prefix}:{email}", 300, otp)

        message = MessageSchema(
            subject="[INSTRING] 회원가입 인증번호",
            recipients=[email],
            body=f"인증번호는 {otp} 입니다",
            subtype="html"
        )
        await fm.send_message(message)


auth_manager = AuthManager()