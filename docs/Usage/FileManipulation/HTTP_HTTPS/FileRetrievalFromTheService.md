# File retrieval from the services

## Service

In this example, a service implemented through FastAPI will be used. 
If you have a service implemented in another programming language, 
the main requirement is to transfer the file in binary format with the header (application/octet-stream). 
To pass a file through FastAPI, you can use FileResponse 
(more details can be found in the official documentation: https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse)."

## API-Gateway

!!! bug
    It is not possible to download a file through Swagger, as when sending a request, 
    the API-Gateway starts streaming byte streams, which can cause the page or the entire browser to crash.

To solve the file download issue, you can either directly paste the URL in the browser, 
use some third-party tools, or use a programming language.

An example of downloading and saving a file using Python:

```python
import requests

cookies = {'rinex_to_csv_processing_id': '0000000000000000001'}

url = 'http://127.0.0.1:8080/rinex/rinex_to_csv/get_result'
r = requests.get(url, allow_redirects=True, cookies=cookies)

if r.status_code == 200:
    open('save.zip', 'wb').write(r.content)
```