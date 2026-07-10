from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from app.nexus.exceptions.nexus_exceptions import (
    GraphResponseMissingError,
    NexusError,
    StructuredResponseRetryExceededError,
)


class ExceptionHandlersRegister:
    def register(
        self,
        app: FastAPI,
    ) -> None:
        app.add_exception_handler(
            exc_class_or_status_code=GraphResponseMissingError,
            handler=self._handle_graph_response_missing,
        )
        app.add_exception_handler(
            exc_class_or_status_code=StructuredResponseRetryExceededError,
            handler=self._handle_structured_response_retry_exceeded,
        )
        app.add_exception_handler(
            exc_class_or_status_code=NexusError,
            handler=self._handle_nexus_error,
        )
        app.add_exception_handler(
            exc_class_or_status_code=Exception,
            handler=self._handle_unexpected_error,
        )

    @staticmethod
    async def _handle_graph_response_missing(
        request: Request,
        exc: Exception,
    ) -> Response:
        return JSONResponse(
            status_code=502,
            content={
                "detail": {
                    "error_code": GraphResponseMissingError.code,
                    "message": "O agente não produziu resposta.",
                }
            },
        )

    @staticmethod
    async def _handle_structured_response_retry_exceeded(
        request: Request,
        exc: Exception,
    ) -> Response:
        return JSONResponse(
            status_code=502,
            content={
                "detail": {
                    "error_code": StructuredResponseRetryExceededError.code,
                    "message": "O agente não conseguiu produzir o formato esperado.",
                }
            },
        )

    @staticmethod
    async def _handle_nexus_error(
        request: Request,
        exc: Exception,
    ) -> Response:
        return JSONResponse(
            status_code=500,
            content={
                "detail": {
                    "error_code": NexusError.code,
                    "message": "Erro interno do agente.",
                }
            },
        )

    @staticmethod
    async def _handle_unexpected_error(
        request: Request,
        exc: Exception,
    ) -> Response:
        return JSONResponse(
            status_code=500,
            content={
                "detail": {
                    "error_code": "internal_error",
                    "message": "Erro interno inesperado.",
                }
            },
        )
