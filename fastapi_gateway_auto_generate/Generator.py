import re
# import fs
# import requests
# import validators
# from typing import List, Any
from pathlib import Path
from loguru import logger
# from pprint import pprint
# from fastapi import FastAPI
# from requests import Response
# from types import FunctionType
# from fastapi_gateway import route
# from .RouteModel import RouteModel
# from .utils.OpenApiParser import OpenApiParser
from datamodel_code_generator import InputFileType, generate
# from pydantic import BaseModel, Field
# from fastapi.openapi.utils import get_openapi

from .management import Management
from .Config import Config
import os.path
# from alembic.config import Config as alembic_config
# from alembic import command
from fastapi_gateway_auto_generate.domain.usecases import *
# import uuid
# from fastapi_gateway_auto_generate.domain.models import RouteModel
import os
import glob
import sys


class Generator:

    def __init__(self, config: Config) -> None:
        self.__config = config

        if not os.path.isfile(self.__config.db_path):
            InitDatabaseUsecase().execute(db_url=config.db_url)

        if self.__config.service_management:
            self.__init_management_urls()

        # self.__routes_model: List[RouteModel] = []

        # self.__open_api_parser = OpenApiParser()

        # self.models_routes_vars = {}
        # self.models_routes: None = {}

        self.build()

    def __init_management_urls(self):
        m: Management = Management(config=self.__config)

    def build(self) -> None:
        services_result = BuildRouteModelsUsecase().execute(
            config=self.__config
        )

        BuildRoutesUsecase().execute(
            services_result=services_result,
            fast_api_app=self.__config.fast_api_app
        )

        self.__delete_tmp_files()

    def __delete_tmp_files(self):
        project_root = os.path.dirname(
            sys.modules['fastapi_gateway_auto_generate'].__file__)

        filelist = glob.glob(os.path.join(
            f"{project_root}/tmp/models", "model_*"))
        for f in filelist:
            logger.debug(f)
            os.remove(f)
