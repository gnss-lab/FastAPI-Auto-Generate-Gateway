# How to use

## 1. Additional metadata for tags

In order for the url from the microservice to be transferred to the API Gateway, 
you need to add additional metadata for your tags. In our case, this is `x-auto-generate-in-api-gateway`. 

For example, we have such a microservice. 

!!! example
    The example was taken on the website [FastAPI (Create metadata for tags)](https://fastapi.tiangolo.com/tutorial/metadata/#create-metadata-for-tags)

<details>
<summary>app.py</summary>
<pre>
<code>
```python
from fastapi import FastAPI

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
```
</code>
</pre>
</details>

Adds an additional tag `x-auto-generate-in-api-gateway` in order for it to be transferred to the API Gateway.

<details>
<summary>app.py</summary>
<pre>
<code>
```python
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
        "x-auto-generate-in-api-gateway": True, # Tag for transferred to the API Gateway
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/"
        },
        "x-auto-generate-in-api-gateway": True, # Tag for transferred to the API Gateway
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```
</code>
</pre>
</details>

Now who has the tag `users` and `items` will be automatically transferred to the API Gateway.

!!! question
    If you suddenly change the tag for some reason, then you can do this when creating an object in the API Gateway

## 2. Initializing an object in the API Gateway

> Documentation in development