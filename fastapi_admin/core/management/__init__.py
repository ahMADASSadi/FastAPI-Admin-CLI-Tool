from importlib.util import spec_from_file_location, module_from_spec
from typing import Dict, Type
from pathlib import Path
import os

from fastapi_admin.core.management.base import BaseCommand


def load_commands(commands_dir: str = Path(__file__).parent/"commands") -> Dict[str, Type[BaseCommand]]:
    """
    Dynamically load all command classes from the commands folder.
    """
    commands = {}

    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            
            command_name = filename[:-3]

            module_path = os.path.join(commands_dir, filename)
            
            spec = spec_from_file_location(
                command_name, module_path)
            
            module = module_from_spec(spec)
            
            spec.loader.exec_module(module)
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseCommand)
                    and attr != BaseCommand
                ):
                    commands[command_name] = attr

    return commands

def fetch_commands(commands):
    print("Available commands:")
    
    print(f"  {'list'}: Lists all the available commands")
    
    for cmd_name, cmd_class in commands.items():
        print(f"  {cmd_name}: {cmd_class.help}")

def execute_from_command_line(argv):
    
    commands = load_commands()
    
    if not argv:
        print("Error: No subcommand provided.")
        fetch_commands(commands)
        return
    
    subcommand = argv[0]

    if subcommand in commands:
        command_class = commands[subcommand]
        command_instance = command_class()
        command_instance.handle(argv[1:])
    elif subcommand in ["list", "-l"]:
        fetch_commands(commands)
    
    else:
        print(f"Error: Unknown subcommand '{subcommand}'.")
        fetch_commands(commands)