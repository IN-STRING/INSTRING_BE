from INewApp.core.error.exception_messages import ErrorSpec


class AppException(Exception):
    def __init__(
        self,
        spec: ErrorSpec,
        errors: list[dict] | None = None,
    ):
        self.code = spec.code
        self.status = spec.status
        self.detail = spec.default_message
        self.errors = errors