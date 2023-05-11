from fastapi import (FastAPI,
                     File,
                     UploadFile,
                     Response,
                     Cookie)

from .domain.entity.ConversionParams import ConversionParams

app = FastAPI()


@app.post("/rinex_to_csv/upload_rinex")
async def upload_rinex(response: Response,
                       rinex: UploadFile = File(description="Load RINEX file"),
                       rinex_to_csv_processing_id: str | None = Cookie(default=None)):
    pass


@app.post("/rinex_to_csv/upload_nav")
async def upload_nav(response: Response,
                     rinex: UploadFile = File(description="Load NAV file"),
                     rinex_to_csv_processing_id: str | None = Cookie(default=None)
                     ):
    pass


@app.post("/rinex_to_csv/run")
async def run_processing(params: ConversionParams,
                         rinex_to_csv_processing_id: str | None = Cookie(default=None)):
    pass


@app.get("/rinex_to_csv/get_result")
async def get_result(rinex_to_csv_processing_id: str | None = Cookie(default=None)):
    pass
