import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


logger = logging.getLogger(__name__) # 에러 로그 좀 더 좋게 찍어주는거


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        body: dict = {
            "code": exc.code,
            "detail": exc.detail,
        }
        if exc.errors:
            body["errors"] = exc.errors
        return JSONResponse(status_code=exc.status, content=body)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        spec = ErrorCodes.VALIDATION_ERROR
        errors = [
            {
                "field": " → ".join(str(loc) for loc in e["loc"]),
                "detail": e["msg"],
            }
            for e in exc.errors()
        ]
        return JSONResponse(
            status_code=spec.status,
            content={
                "code": spec.code,
                "detail": spec.default_message,
                "errors": errors,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception")
        spec = ErrorCodes.INTERNAL_ERROR
        return JSONResponse(
            status_code=spec.status,
            content={
                "code": spec.code,
                "detail": spec.default_message,
            },
        )