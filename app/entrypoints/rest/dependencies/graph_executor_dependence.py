import logging
from typing import Annotated

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException

from app.nexus.executor.graph_executor import GraphExecutor

logger: logging.Logger = logging.getLogger(name=__name__)


def graph_executor_dependence(request: Request) -> GraphExecutor:
    executor: GraphExecutor | None = getattr(
        request.app.state,
        "graph_executor",
        None,
    )

    if executor is None:
        logger.error(msg="GraphExecutor não inicializado no estado da aplicação.")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error_code": "service_unavailable",
                "message": "Serviço indisponível.",
            },
        )

    return executor


GraphExecutorDependence = Annotated[GraphExecutor, Depends(dependency=graph_executor_dependence)]
