from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorSpec:
    code: str
    status: int
    default_message: str


class ErrorCodes:
    # === User ===
    USER_NOT_FOUND       = ErrorSpec("USER_NOT_FOUND",       404, "유저를 찾을 수 없습니다")
    USER_EMAIL_NOT_FOUND = ErrorSpec("USER_EMAIL_NOT_FOUND", 404, "가입되지 않은 이메일 입니다")
    USER_ALREADY_EXISTS  = ErrorSpec("USER_ALREADY_EXISTS",  409, "이미 가입된 이메일입니다")

    # === Record ===
    RECORD_NOT_FOUND      = ErrorSpec("RECORD_NOT_FOUND",      404, "녹음 파일을 찾지 못했습니다")

    # == Category ==
    CATEGORY_NOT_FOUND   = ErrorSpec("CATEGORY_NOT_FOUND", 404, "해당 카테고리를 찾지 못했습니다")

    # == Song ==
    SONG_NOT_FOUND       = ErrorSpec("SONG_NOT_FOUND", 404, "해당 곡을 찾지 못했습니다")

    # == Level ==
    LEVEL_NOT_FOUND      = ErrorSpec("LEVEL_NOT_FOUND", 404, "해당 레벨을 찾을 수 없습니다")

    # == String ==
    STRING_NOT_FOUND     = ErrorSpec("STRING_NOT_FOUND", 404, "해당 줄을 찾을 수 없습니다")

    # === MODAL ===
    WRONG_INFO           = ErrorSpec("WRONG_INFO", 400, "입력 정보가 일치하지 않습니다")
    MODAL_ALREADY_DONE   = ErrorSpec("ALREADY_DONE", 409, "이미 설문을 완료 했습니다")

    # == DEVICE ==
    REG_ALREADY_DONE     = ErrorSpec("ALREADY_DONE", 409, "이미 등록되어 있습니다")
    DEVICE_NOT_FOUND     = ErrorSpec("DEVICE_NOT_FOUND", 404, "연결된 해당 id의 기기를 찾을 수 없습니다")
    DEVICE_ALREADY_TAKEN = ErrorSpec("DEVICE_ALREADY_TAKEN", 409, "이미 다른 사용자가 등록한 id 입니다")

    # === Auth ===
    CODE_WRONG = ErrorSpec("CODE_WRONG", 400, "인증 코드가 옳지 않습니다")
    UNAUTHENTICATED      = ErrorSpec("UNAUTHENTICATED",      401, "로그인이 필요합니다")
    TOKEN_EXPIRED = ErrorSpec("TOKEN_EXPIRED", 401, "토큰이 만료되었습니다")
    INVALID_TOKEN = ErrorSpec("INVALID_TOKEN", 401, "유효하지 않은 토큰입니다")
    WRONG_TOKEN          = ErrorSpec("WRONG_TOKEN", 401, "옳지 않은 토큰 입니다")
    FORBIDDEN            = ErrorSpec("FORBIDDEN",            403, "권한이 없습니다")
    EMAIL_FORBIDDEN      = ErrorSpec("EMAIL_FORBIDDEN", 403, "이메일 인증이 필요합니다")
    FAILED               = ErrorSpec("FAILED", 400, "인증에 실패하였습니다")

    # === Common ===
    VALIDATION_ERROR     = ErrorSpec("VALIDATION_ERROR",     422, "입력 정보가 정확하지 않습니다")
    INTERNAL_ERROR       = ErrorSpec("INTERNAL_ERROR",       500, "서버 내부 오류가 발생했습니다")