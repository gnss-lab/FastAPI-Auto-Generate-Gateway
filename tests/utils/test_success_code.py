import pytest
from fastapi_gateway_auto_generate.utils import success_code


@pytest.mark.parametrize("msg, expected_output", [
    ("Success", {"details": {"code": 0, "msg": "Success"}}),
    ("Test", {"details": {"code": 0, "msg": "Test"}}),
    ("", {"details": {"code": 0, "msg": ""}})
])
def test_success_code_returns_expected_output(msg: str, expected_output: dict[str, dict[str, str | int]]):
    assert success_code(msg) == expected_output


def test_success_code_returns_dict():
    assert isinstance(success_code("Success"), dict)


def test_success_code_returns_valid_keys():
    output = success_code("Success")
    assert "details" in output
    assert "code" in output["details"]
    assert "msg" in output["details"]