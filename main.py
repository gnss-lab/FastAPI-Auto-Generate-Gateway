from core import FastapiGatewayAutoGenerate
from fastapi import FastAPI
import uvicorn


from loguru import logger


app = FastAPI()


# def reload():
services_url = ["http://127.0.0.1:7200"]

services_url_dict = {
    "mosgim": "http://127.0.0.1:8082",
    "healrinex": "http://10.0.5.93:5577"
}

config = FastapiGatewayAutoGenerate.Config(
    fast_api_app=app,
    db_path="./testdb.db"
)

autoRG = FastapiGatewayAutoGenerate.AutoGenerate(
    config=config
)

# print("OK")
# autoRG.build_routes()


# @app.get("/management/update-services")
# def update_services() -> None:
#     reload()

# # Using FastAPI instance


# @app.get("/url-list")
# def get_all_urls():
#     url_list = [{"path": route.path, "name": route.name}
#                 for route in app.routes]
#     return url_list

if __name__ == "__main__":
    # reload()
    uvicorn.run(app=app, port=5000, log_level="info")
