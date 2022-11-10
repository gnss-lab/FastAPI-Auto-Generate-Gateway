from core import AutoRequestGeneration
from fastapi import FastAPI
import uvicorn
if __name__ == "__main__":

    app = FastAPI()

    services_url = ["http://127.0.0.1:8082", "http://10.0.5.93:5577"]

    autoRG = AutoRequestGeneration(fast_api_app=app, services_url=services_url)

    autoRG.build_routes()

    uvicorn.run(app, port=5000, log_level="info")
