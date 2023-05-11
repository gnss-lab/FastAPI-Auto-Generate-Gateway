from typing import Dict


def success_code(msg: str) -> dict[str, dict[str, str | int]]:
    return {"details": {
        "code": 0,
        "msg": msg
    }}