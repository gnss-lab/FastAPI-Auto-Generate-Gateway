import os
from pprint import pprint

from fastapi_gateway_auto_generate import Generator, Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
import json

from tests.builders.FakeServices import FakeServices


def test_generator():
    app = FastAPI()

    config = Config(
        fast_api_app=app,
        db_path="./tmp/"
    )

    autoRG = Generator(
        config=config
    )

    client = TestClient(app)

    fake_service = FakeServices().with_domain().with_name().with_port().build()

    payload = {
        "domain": fake_service["domain"],
        "name_service": fake_service["name"],
        "port": fake_service["port"]
    }

    client.post("/service", content=json.dumps(payload))

    client.get("/services", params={"page": 1})

    responses = client.delete("/service", params={"id_service": 1})

    client.patch("/services")

    #
    # params = {
    #     "id": 0
    # }
    #
    # response = client.delete("/service", params=params)

    pprint(responses.text)
    os.remove(config.get_database_absolute_path())

    # if __name__ == "__main__":
    #     uvicorn.run(app=app, port=5000, log_level="info")
