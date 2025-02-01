import importlib.resources
from pathlib import Path
from typing import List

import fastapi_admin

class BaseCommand:
    help: str = ""
    template_dir: Path = importlib.resources.files(
        fastapi_admin).joinpath('templates')

    def handle(self, args: List[str]):
        """
        This method must be implemented by all subclasses.
        It contains the logic to execute the command.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'handle' method.")
