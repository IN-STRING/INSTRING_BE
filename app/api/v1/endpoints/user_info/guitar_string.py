from datetime import timezone, datetime
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.core.config import settings
from app.api.depends import SessionDep
from app.core.security.jwt_token import jwt_manager
from app.models.postgresDB.user import User


guitar_string_date_router = APIRouter()

@guitar_string_date_router.get("/api/guitars/string-status")
def get_string_status(
        session: SessionDep,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)]
):
    user = session.get(User, userdata["sub"])

    changed_at = user.updated_at
    now = datetime.now(timezone.utc)
    elapsed = (now - changed_at).days

    progress = min(elapsed / settings.STRING_MAX_DAY, 1.0)

    if progress < 0.25:
        message = "줄 상태가 좋습니다"
        level = "good"
    elif progress < 0.5:
        message = "아직 괜찮습니다"
        level = "normal"
    elif progress < 0.75:
        message = "슬슬 교체를 고려해보세요"
        level = "warning"
    else:
        message = "악기줄이 너무 오래 되었습니다!!"
        level = "danger"

    return {"message": message, "level": level}