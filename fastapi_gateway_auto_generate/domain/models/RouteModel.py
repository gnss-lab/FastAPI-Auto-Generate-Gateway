from dataclasses import dataclass
from fastapi import FastAPI
from typing import List, Optional, Sequence, Dict, Union, Any, Type


@dataclass
class RouteModel:
    """A data class for storing data about a microservice.
    Args:
        request_method (Any): Is a callable (like app.get, app.post and so on.)
        gateway_path (str): Is the path to bind gateway.
        service_url (str): Is url path to microservice (like "https://api.example.com/v1")
        service_path (str): The path to the endpoint on another service.
        query_params (Optional[List[str]]): Used to extract query parameters from endpoint and transmission to microservice
        query_required (Optional[List[bool]]): Defines whether the specified parameters are mandatory for the request to the microservice.
        query_is_cookie (Optional[List[bool]]): Determines whether the specified parameters should be passed as a cookie.
        form_params (Optional[List[str]]): Used to extract form model parameters from endpoint and transmission to microservice
        body_params (Optional[List[str]]): Used to extract body model from endpoint and transmission to microservice
        tags (Optional[List[str]]): Allows grouped objects in the api docs
        dependencies (Optional[str]): See documentation for details - https://fastapi.tiangolo.com/tutorial/dependencies/#declare-the-dependency-in-the-dependant
    """

    request_method: Any
    gateway_path: str
    service_url: str
    service_path: str
    query_params: Optional[List[str]] = None
    query_required: Optional[List[bool]] = None
    query_is_cookie: Optional[List[bool]] = None
    form_params: Optional[List[str]] = None
    body_params: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    dependencies: Optional[str] = None
    # override_headers: bool = True
    # response_model: Optional[Type[Any]] = None
    # status_code: Optional[int] = None
    # summary: Optional[str] = None
    # description: Optional[str] = None
    # response_description: str = "Successful Response"
    # responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
    # deprecated: Optional[bool] = None
    # operation_id: Optional[str] = None
    # response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    # response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    # response_model_by_alias: bool = True
    # response_model_exclude_unset: bool = False
    # response_model_exclude_defaults: bool = False
    # response_model_exclude_none: bool = False
    # include_in_schema: bool = True
    # response_class: Type[Response] = Default(JSONResponse),
    # name: Optional[str] = None,
    # callbacks: Optional[List[BaseRoute]] = None,
    # openapi_extra: Optional[Dict[str, Any]] = None
