import shutil
import tempfile
from types import FunctionType
from typing import Any

import fastapi
import starlette.datastructures
from fastapi import FastAPI
from makefun import create_function

from fastapi_gateway_auto_generate import Config
from fastapi_gateway_auto_generate.domain.models import RouteModel


class BuildCeleryTaskUsecase:

    def __init__(self, config: Config):
        self.__config = config

    def execute(self, func_sign: str, fast_api_app: FastAPI, routeModel: RouteModel):
        def func_impl(*args, **kwargs):
            upload_files = [value for value in kwargs.values() if isinstance(value, starlette.datastructures.UploadFile)]

            result = []

            for file in upload_files:

                # Создаем временный файл и сохраняем в него загруженный файл
                with tempfile.TemporaryFile() as temp_file:
                    shutil.copyfileobj(file.file, temp_file)
                    temp_file.seek(0)

                    # Сохраняем временный файл в системной папке tempfile
                    with tempfile.NamedTemporaryFile(delete=False, dir=tempfile.gettempdir()) as file_to_save:
                        shutil.copyfileobj(temp_file, file_to_save)
                        saved_file_path = file_to_save.name

                result.append({"filename": file.filename, "saved_file_path": saved_file_path})

            return result

            print("args:", args)
            print("kwargs:", kwargs)
            print("upload_files:", upload_files)
            return {"ok": "ok"}

        func: FunctionType = create_function(func_sign, func_impl)

        fast_api_app.post(
            path=routeModel.gateway_path,
            dependencies=routeModel.dependencies
        )(func)



