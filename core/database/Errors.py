class Errors:

    @staticmethod
    def any_error(msg: str) -> dict[str, int | str]:
        return {
            "code": -1,
            "msg": msg
        }

    @staticmethod
    def service_exists(ip: str, port: str) -> dict[str, int | str]:
        return {
            "code": 1,
            "msg": f"Service {ip}:{port} already exists"
        }

    @staticmethod
    def no_services_found() -> dict[str, int | str]:
        return {
            "code": 2,
            "msg": f"Not a single service has been created yet"
        }

    @staticmethod
    def page_not_found() -> dict[str, int | str]:
        return {
            "code": 3,
            "msg": f"Page not found"
        }
