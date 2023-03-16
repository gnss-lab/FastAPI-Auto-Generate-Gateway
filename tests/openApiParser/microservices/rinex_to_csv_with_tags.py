from fastapi import (FastAPI,
                     File,
                     UploadFile,
                     Response,
                     Cookie)

from pydantic import BaseModel

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
    },
]


app = FastAPI(openapi_tags=tags_metadata)

class ConversionParams(BaseModel):
    g_signals: list[str] = ['L1C', 'C1C']
    e_signals: list[str] = ['L1C', 'C1C']
    c_signals: list[str] = ['L2I', 'C2I']
    r_signals: list[str] = ['L1C', 'C1C']
    s_signals: list[str] = []
    timestep: int = 30

    def get_signal_by_system(self):
        signal = {'G': self.g_signals,
                  'R': self.r_signals,
                  'E': self.e_signals,
                  'C': self.c_signals,
                  'S': self.s_signals}
        return signal


@app.post("/rinex_to_csv/upload_rinex")
async def upload_rinex(response: Response,
                       rinex: UploadFile = File(description="Load RINEX file"),
                       rinex_to_csv_processing_id: str | None = Cookie(default=None)):
    pass


@app.post("/rinex_to_csv/upload_nav", tags=["default"])
async def upload_nav(response: Response,
                     rinex: UploadFile = File(description="Load NAV file"),
                     rinex_to_csv_processing_id: str | None = Cookie(default=None)
                     ):
    pass

@app.post("/rinex_to_csv/run", tags=["default2"])
async def run_processing(params: ConversionParams,
                         rinex_to_csv_processing_id: str | None = Cookie(default=None)):
    pass


@app.get("/rinex_to_csv/get_result", tags=["default"])
async def get_result(rinex_to_csv_processing_id: str | None = Cookie(default=None)):
    pass
