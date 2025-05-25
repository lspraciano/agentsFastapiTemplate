from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError

from app.core.shared.exceptions_handlers.pydantic.request_validation_error import request_validation_exception_handler


def register_exceptions_handlers(
        app: FastAPI
):
    app.add_exception_handler(
        exc_class_or_status_code=FastAPIRequestValidationError,
        handler=request_validation_exception_handler
    )
