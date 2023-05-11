from fastapi import FastAPI


class UpdateOpenApiSchemaUsecase:
    """The usecase for updating the OpenAPI schema.
    """

    def __init__(self) -> None:
        pass

    def execute(self, fast_api_app: FastAPI) -> bool:
        """Launch execution of usecase
        Args:
            fast_api_app (FastAPI): Pointer to your FastAPI application.
        """

        fast_api_app.openapi_schema = None
        fast_api_app.openapi()

        return True
