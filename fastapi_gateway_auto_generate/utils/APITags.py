from enum import Enum


class APITags(str, Enum):
    AUTO_GENERATE = "x-auto-generate-in-api-gateway"
    ENABLE_AUTH = "x-enable-auth-in-api-gateway"
    LARGE_FILE = "x-large-file"
