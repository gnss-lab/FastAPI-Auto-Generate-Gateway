# Service management

The library has built-in urls for managing services. Service management is enabled by default. If desired, you can disable the built-in service management system if you do not need it. There is a `service_management` parameter for this.

## URLs



### Add service

| Method | Path         |
| ------ | ------------ |
| POST   | /service     |

#### Description

Adds a service to the database.

#### Body

```json
{
  "domain": "string",
  "name_service": "string",
  "port": 80
}
```

- domain - The domain of your service. **It is mandatory** to specify the protocol. For example, `http://127.0.0.1`
- name_service - The name of the service. It must be unique.
After specifying the name, the URL will look like this: `https://127.0.0.1:80/{name_service}/...`
- port - The port of the service.

!!! failure
    You cannot specify the port in the domain. For example: `http://127.0.0.1:8080`<br>
    You need to specify them separately.

#### Response

True if the addition was successful, otherwise False.

#### Example (*Python requests*)

```python
# Install the Python Requests library:
# `pip install requests`

import requests


def send_request():
    # Request
    # POST http://127.0.0.1:5000/service

    try:
        response = requests.post(
            url="http://127.0.0.1:5000/service",
            params={
                "ip": "127.0.0.1",
                "port": "8080",
                "name_service": "Hello",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
```


### Delete service

### Refresh services

| Method | Path         |
| ------ | ------------ |
| PATCH  |  /services   |


#### Description

Updates the URL and checks the functionality of the services without first restarting the program.


#### Example (*Python requests*)

```python
# Install the Python Requests library:
# `pip install requests`

import requests


def send_request():
    # Request
    # PATCH http://127.0.0.1:5000/services

    try:
        response = requests.patch(
            url="http://127.0.0.1:5000/services",
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
```


### Get info all services