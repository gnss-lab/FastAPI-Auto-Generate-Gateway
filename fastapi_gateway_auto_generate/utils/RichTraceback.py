import sys
from rich.console import Console


class RichTraceback:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.console = Console()

    def console_call_exception(self):
        self.console.print_exception(show_locals=True)
        sys.exit(1)
