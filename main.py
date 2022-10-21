from core import AutoRequestGeneration

if __name__ == "__main__":

    services_url = ["http://127.0.0.1:8082"]

    autoRG = AutoRequestGeneration(services_url=services_url)

    autoRG.build_routes()
