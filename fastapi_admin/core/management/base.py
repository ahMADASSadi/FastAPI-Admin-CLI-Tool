from typing import List
import argparse


class BaseCommand:
    help: str = ""

    def handle(self, args: List[str]):
        """
        This method must be implemented by all subclasses.
        It contains the logic to execute the command.
        """
        raise NotImplementedError("Subclasses must implement the 'handle' method.")

    def add_arguments(self, parser: argparse.ArgumentParser):
        """
        This method can be implemented by subclasses to add custom arguments to the command.
        """
        pass

