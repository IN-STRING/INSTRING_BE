from INewApp.core.error.exception_messages import ErrorSpec


class AppException(Exception):
    def __init__(
        self,
        spec: ErrorSpec,
        # detail: str | None = None,
        errors: list[dict] | None = None,
    ):
        self.code = spec.code
        self.status = spec.status
        # self.detail = detail or spec.default_message
        self.detail = spec.default_message
        self.errors = errors