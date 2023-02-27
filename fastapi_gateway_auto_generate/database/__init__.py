from . import models

from .AddService import AddService
from .GetAllServices import GetAllServices
from .StatusService import StatusService
from .UrlService import UrlService
from .DeleteService import DeleteService
from .SetMarkDeleteSerivce import SetMarkDeleteService

__all__: list[str] = [
    "AddService",
    "GetAllServices",
    "StatusService",
    "UrlService",
    "DeleteService",
    "SetMarkDeleteService"
]
