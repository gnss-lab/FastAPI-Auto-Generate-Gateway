from dataclasses import dataclass
from fastapi import FastAPI
from typing import List, Optional, Sequence, Dict, Union, Any, Type


@dataclass
class RouteModel():
    request_method: Any
    gateway_path: str
    service_url: str
    service_path: str
    query_params: Optional[List[str]] = None
    query_required: Optional[List[bool]] = None
    form_params: Optional[List[str]] = None
    # body_params: Optional[List[str]] = None
    # override_headers: bool = True
    # response_model: Optional[Type[Any]] = None
    # status_code: Optional[int] = None
    tags: Optional[List[str]] = None
    # dependencies: Optional[Sequence[params.Depends]] = None,
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
