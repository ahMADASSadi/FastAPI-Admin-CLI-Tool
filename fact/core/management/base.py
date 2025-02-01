import importlib.resources
from pathlib import Path
from typing import List

import fact

class BaseCommand:
    help: str = ""
    template_dir: Path = importlib.resources.files(
        fact).joinpath('templates')

    def handle(self, args: List[str]):
        """
        This method must be implemented by all subclasses.
        It contains the logic to execute the command.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'handle' method.")
