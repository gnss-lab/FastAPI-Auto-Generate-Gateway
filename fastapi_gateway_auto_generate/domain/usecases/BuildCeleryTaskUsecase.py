import os
import shutil
import tempfile
from datetime import timedelta
from math import ceil
from types import FunctionType
from typing import Any
import pickle

import fastapi
import starlette.datastructures
from celery import shared_task
from fastapi import FastAPI
from kombu import Exchange, Queue, Connection, Producer
from makefun import create_function

from fastapi_gateway_auto_generate import Config
from fastapi_gateway_auto_generate.domain.models import RouteModel


def build_celery_task(file_path, file_name, task_id):
    chunk_size = 10 * 1024 * 1024  # Размер частей, на которые нужно разбить файл
    exchange = Exchange('fastapi_magic_large_files', type='direct')
    queue = Queue('file_chunks_queue', exchange, routing_key='file_chunks')

    i = 0

    with open(file_path, 'rb') as f:
        while True:

            chunk = f.read(chunk_size)
            if not chunk:
                break

            i = i + 1

            print(f"{file_path} -> {i}")


            message = {'chunk': pickle.dumps(chunk), 'filename': os.path.basename(file_path)}
            with Connection('amqp://guest:guest@localhost:5672//') as conn:
                with conn.channel() as channel:
                    exchange.declare(channel=channel)
                    queue.declare(channel=channel)
                    producer = Producer(channel)

                    headers = {
                        "file_name": file_name,
                        "number_file": i,
                        "total_file": ceil(os.path.getsize(file_path) / chunk_size)
                    }

                    producer.publish(message,
                                     serializer='pickle',
                                     exchange=exchange,
                                     routing_key='file_chunks',
                                     headers=headers)
                    #
                    # queue.enqueue(message, serializer='json', exchange=exchange, routing_key='file_chunks')
                    # queue.bind(exchange, channel)
                    # queue.declare()
                    # message = {'message': 'Hello, world!'}
                    # queueбю


class BuildCeleryTaskUsecase:

    def __init__(self, config: Config):
        self.__config = config
        self.build_celery_task_2 = self.__config.celery_app.task()(build_celery_task)

    def execute(self, func_sign: str, fast_api_app: FastAPI, routeModel: RouteModel):
        def func_impl(*args, **kwargs):



            upload_files = [value for value in kwargs.values() if isinstance(value, starlette.datastructures.UploadFile)]

            result = []

            from uuid import uuid4

            task_id = uuid4()

            result.append({"task_id": task_id})

            for file in upload_files:

                # Создаем временный файл и сохраняем в него загруженный файл
                with tempfile.TemporaryFile() as temp_file:
                    shutil.copyfileobj(file.file, temp_file)
                    temp_file.seek(0)

                    # Сохраняем временный файл в системной папке tempfile
                    with tempfile.NamedTemporaryFile(delete=False, dir=tempfile.gettempdir()) as file_to_save:
                        shutil.copyfileobj(temp_file, file_to_save)
                        file_path = file_to_save.name


                result_celery = self.build_celery_task_2.apply_async(args=(file_path, file.filename, task_id,))

                result.append(
                    {"filename": file.filename, "saved_file_path": file_path, "task_id_celery": result_celery.id}
                )

                #
                # print(result_celery.get())

            return result

            # print("args:", args)
            # print("kwargs:", kwargs)
            # print("upload_files:", upload_files)
            # return {"ok": "ok"}

        func: FunctionType = create_function(func_sign, func_impl)

        fast_api_app.post(
            path=routeModel.gateway_path,
            dependencies=routeModel.dependencies
        )(func)


    def test(self):
        return {"ok": "ok"}