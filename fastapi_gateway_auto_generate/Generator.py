import os.path
from .Config import Config
from .management import Management
from fastapi_gateway_auto_generate.domain.usecases import *


class Generator:
    """The class responsible for adding automatic service connections to the FastAPI object.
    Args:
        config (Config): The Config object with its configuration.
    """

    def __init__(self, config: Config) -> None:
        self.__config = config

        if not os.path.isfile(self.__config.db_path):
            InitDatabaseUsecase().execute(db_url=config.db_url)

        if self.__config.service_management:
            self.__init_management_urls()

        self.build()

    def __init_management_urls(self):
        """Service management initialization.
        """
        Management(config=self.__config)

    def build(self) -> None:
        """Adding services to the FastAPI object.
        """

        services_result = BuildRouteModelsUsecase().execute(
            config=self.__config
        )

        BuildRoutesUsecase().execute(
            services_result=services_result,
            fast_api_app=self.__config.fast_api_app
        )
