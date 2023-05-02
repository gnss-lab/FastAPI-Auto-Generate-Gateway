from fastapi import (FastAPI,
                     File,
                     UploadFile,
                     Response,
                     Cookie)

from .domain.entity.ConversionParams import ConversionParams

tags_metadata = [
    {
        "name": "default",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/"
        },
        "x-auto-generate-in-api-gateway": True,
    },
    {
        "name": "default2",
        "x-auto-generate-in-api-gateway": False,
        "x-enable-auth-in-api-gateway": False,
        "x-large-file": True,
        "x-large-file-queues": ["test1", "test2"],
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.post("/rinex_to_csv/upload_rinex")
async def upload_rinex(response: Response,
                       rinex: UploadFile = File(description="Load RINEX file"),
                       rinex_to_csv_processing_id: str | None = Cookie(default=None)):
    pass


@app.post("/rinex_to_csv/upload_nav", tags=["default"])
async def upload_nav(response: Response,
                     url: str,
                     rinex: UploadFile = File(description="Load NAV file"),
                     rinex_to_csv_processing_id: str | None = Cookie(default=None),
                     ):
    pass


@app.post("/rinex_to_csv/run", tags=["default2"])
async def run_processing(params: ConversionParams,
                         rinex_to_csv_processing_id: str | None = Cookie(default=None)):
    pass


@app.get("/rinex_to_csv/get_result", tags=["defaultssss"])
async def get_result():
    pass