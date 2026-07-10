from langchain.agents.middleware import ModelCallLimitMiddleware


class ToolLoopGuardMiddleware(ModelCallLimitMiddleware):
    def __init__(
        self,
        run_limit: int = 10,
    ):
        super().__init__(
            run_limit=run_limit,
            exit_behavior="error",
        )
