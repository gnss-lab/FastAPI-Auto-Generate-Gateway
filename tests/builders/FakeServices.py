from typing import Any

from fastapi_gateway_auto_generate.database.models import Services
from faker import Faker

class FakeServices():
    def __init__(self) -> None:
        self.fake = Faker()
        self.service = {}

    def with_domain(self) -> "FakeServices":
        self.service["domain"] = f"http://{self.fake.ipv4()}"
        return self

    def with_port(self) -> "FakeServices":
        self.service["port"] = self.fake.port_number()
        return self

    def with_name(self) -> "FakeServices":
        self.service["name"] = self.fake.domain_word()
        return self

    def build(self) -> dict:
        return self.service
