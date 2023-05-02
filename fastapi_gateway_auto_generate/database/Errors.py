class Errors:

    @staticmethod
    def any_error(msg: str) -> dict[str, int | str]:
        return {
            "code": -1,
            "msg": msg
        }

    @staticmethod
    def service_exists(name: str) -> dict[str, int | str]:
        return {
            "code": 1,
            "msg": f"The \"{name}\" service already exists."
        }

    @staticmethod
    def not_single_service() -> dict[str, int | str]:
        return {
            "code": 2,
            "msg": f"Not a single service has been created yet."
        }

    @staticmethod
    def no_services_found(id: int) -> dict[str, int | str]:
        return {
            "code": 3,
            "msg": f"The service with id {id} was not found."
        }

    @staticmethod
    def page_not_found() -> dict[str, int | str]:
        return {
            "code": 4,
            "msg": f"Page not found."
        }

    @staticmethod
    def deletion_already_marked(id: int) -> dict[str, int | str]:
        return {
            "code": 5,
            "msg": f"Service {id} has already been marked as deleted."
        }