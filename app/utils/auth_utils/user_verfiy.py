from sqlmodel import select, Session
from app.models.postgresDB.user import User
from app.utils.auth_utils.hash import verify_password

def check_user(session: Session, email: str, password: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user