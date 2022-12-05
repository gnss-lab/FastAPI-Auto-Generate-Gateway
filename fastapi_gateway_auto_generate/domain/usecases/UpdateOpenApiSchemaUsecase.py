from fastapi import FastAPI


class UpdateOpenApiSchemaUsecase:
    def __init__(self) -> None:
        pass

    def execute(self, fast_api_app: FastAPI) -> bool:
        fast_api_app.openapi_schema = None
        fast_api_app.openapi()

        return True
