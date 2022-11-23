class Errors:

    @staticmethod
    def service_exists(ip: str, port: str) -> dict[str, int | str]:
        return {
            "code": 1,
            "msg": f"Service {ip}:{port} already exists"
        }
