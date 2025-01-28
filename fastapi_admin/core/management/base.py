from typing import List
import typer

class BaseCommand:
    help_text: str = "No help text available."

    @classmethod
    def handle(cls, args: List[str]):
        """
        This method must be implemented by all subclasses.
        It contains the logic to execute the command.
        """
        raise NotImplementedError("Subclasses must implement the 'handle' method.")