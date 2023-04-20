This method is suitable for transferring small files between the service and API-Gateway. 
If you plan to transfer files larger than 500 MB, 
it is recommended to consider using the method through a [broker](/Usage/FileManipulation/http-https/).

## File transfer to the service

## File retrieval from the services

### 1. Service

In this example, a service implemented through FastAPI will be used. 
If you have a service implemented in another programming language, 
the main requirement is to transfer the file in binary format with the header `application/octet-stream`. 

To pass a file through FastAPI, you can use FileResponse 
(more details can be found in the official documentation: https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse)."

Example of sending a file to an API Gateway:

```python
import os
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, Cookie
from pathlib import Path
from collections import defaultdict

processings = defaultdict(dict)

temdir = Path('/tmp/files')

app = FastAPI()


@app.get("/get_result", tags=["default"])
async def get_result(processing_id: str | None = Cookie(default=None)):

    if not processing_id:
        HTTPException(status_code=400, detail="Upload files first")
    if not processing_id in processings:
        raise HTTPException(status_code=404, detail="No such proc_id")
    if not os.path.exists(temdir / processing_id / 'out'):
        raise HTTPException(status_code=425, 
                            detail = "Run processing first")
    
    files = os.listdir(temdir / processing_id / "out")
    files = [f for f in files if f.endswith('zip')]
    out_file = temdir / processing_id / 'out' / files[0]

    return FileResponse(out_file, 
                        filename = files[0],
                        media_type="application/octet-stream")
```

### 2. API-Gateway

!!! bug
    It is not possible to download a file through Swagger, as when sending a request, 
    the API-Gateway starts streaming byte streams, which can cause the page or the entire browser to crash.

To solve the file download issue, you can either directly paste the URL in the browser, 
use some third-party tools, or use a programming language.

An example of downloading and saving a file using Python:

```python
import requests

cookies = {'processing_id': '0000000000000000001'}

url = 'http://127.0.0.1:8080/service/get_result'
r = requests.get(url, allow_redirects=True, cookies=cookies)

if r.status_code == 200:
    open('save.zip', 'wb').write(r.content)
```