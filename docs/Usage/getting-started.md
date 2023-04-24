# Getting started

## 1. Additional metadata for tags

In order for the url from the microservice to be transferred to the API Gateway, 
you need to add additional metadata for your tags. In our case, this is `x-auto-generate-in-api-gateway`. 

For example, we have such a microservice. 

!!! example
    The example was taken on the website [FastAPI (Create metadata for tags)](https://fastapi.tiangolo.com/tutorial/metadata/#create-metadata-for-tags)

=== "app.py"

    ```python
    from fastapi import FastAPI
    import uvicorn

    tags_metadata = [
        {
            "name": "users",
            "description": "Operations with users. The **login** logic is also here.",
        },
        {
            "name": "items",
            "description": "Manage items. So _fancy_ they have their own docs.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
    ]

    app = FastAPI(openapi_tags=tags_metadata)


    @app.get("/users/", tags=["users"])
    async def get_users():
        return [{"name": "Harry"}, {"name": "Ron"}]


    @app.get("/items/", tags=["items"])
    async def get_items():
        return [{"name": "wand"}, {"name": "flying broom"}]

    if __name__ == '__main__':
        uvicorn.run(app, port=5000, log_level="info")
    ```

Adds an additional tag `x-auto-generate-in-api-gateway` in order for it to be transferred to the API Gateway.


=== "app.py"

    ```python
    from fastapi import FastAPI
    import uvicorn

    tags_metadata = [
        {
            "name": "users",
            "description": "Operations with users. The **login** logic is also here.",
            "x-auto-generate-in-api-gateway": True, # (1)!
        },
        {
            "name": "items",
            "description": "Manage items. So _fancy_ they have their own docs.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/"
            },
            "x-auto-generate-in-api-gateway": True, # (2)!
        },
    ]

    app = FastAPI(openapi_tags=tags_metadata)


    @app.get("/users/", tags=["users"])
    async def get_users():
        return [{"name": "Harry"}, {"name": "Ron"}]


    @app.get("/items/", tags=["items"])
    async def get_items():
        return [{"name": "wand"}, {"name": "flying broom"}]

    if __name__ == '__main__':
        uvicorn.run(app, port=5000, log_level="info")
    ```

    1. Tag for transferred to the API Gateway. 
    2. Tag for transferred to the API Gateway. 




Now who has the tag `users` and `items` will be automatically transferred to the API Gateway.

[//]: # (!!! question)

[//]: # (    If you suddenly change the tag for some reason, then you can do this when creating an object in the API Gateway)

## 2. Initializing an object in the API Gateway

### Create Config object

When creating an object, first we need to configure our generator. There is a "Config" class for this.

```python
from fastapi_gateway_auto_generate import Config
from fastapi import FastAPI

app = FastAPI()

config = Config(
    fast_api_app=app,
)
```

!!! info
    You can find more information about the 
    Config class in the [Code Reference.](/CodeReference/#fastapi_gateway_auto_generate.Config)

#### Example creating a simple generator

=== "app.py"

    ```python
    from fastapi_gateway_auto_generate import Generator, Config
    from fastapi import FastAPI
    import uvicorn
    
    app = FastAPI()
    
    config = Config(
        fast_api_app=app,
    )
    
    Generator(
        config=config
    )
    
    if __name__ == "__main__":
        uvicorn.run(app=app, port=5000, log_level="info")
    ```

After all the manipulations, you will have urls in Swagger for managing services. 
You can read more details about Service management [here](/Usage/service-management/).