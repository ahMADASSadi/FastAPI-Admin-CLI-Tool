from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import tempfile
import shutil
import typer
from typing import List
import importlib.resources
import fastapi_admin

from fastapi_admin.core.management.commands import validate_name, render_template, app
from fastapi_admin.core.management.base import BaseCommand
from fastapi_admin.core.management.template import TemplateCommand


# class StartAppCommand(BaseCommand):
#     help = "Create a new FastAPI app."

#     @classmethod
#     def handle(cls, args: List[str]):
#         try:
#             # Validate the app name
#             app_name = args[0] if args else None
#             if not app_name or not validate_name(app_name, entity="app"):
#                 typer.echo("Error: Invalid app name.")
#                 raise typer.Exit(1)

#             # Define paths
#             template_dir = importlib.resources.files(fastapi_admin).joinpath('templates/app_template')
#             target_dir = args[1] if len(args)>1 else Path.cwd() / app_name

#             # Check if manage.py exists
#             if not (Path.cwd() / "manage.py").exists():
#                 typer.echo(
#                     "Error: manage.py not found. Make sure you're in the project root directory."
#                 )
#                 raise typer.Exit(1)

#             # Check if the app directory already exists
#             if target_dir.exists():
#                 typer.echo(f"Error: App '{app_name}' already exists.")
#                 raise typer.Exit(1)

#             # Create a temporary directory for atomic operations
#             with tempfile.TemporaryDirectory(prefix=f"{app_name}_") as temp_dir:
#                 temp_dir_path = Path(temp_dir)

#                 # Load the template environment
#                 env = Environment(loader=FileSystemLoader(template_dir))
#                 template_files = env.list_templates()

#                 # Render and save each template file in the temporary directory
#                 for template_file in template_files:
#                     render_template(
#                         env=env,
#                         template_file=template_file,
#                         target_dir=temp_dir_path,
#                         app_name=app_name,
#                     )

#                 # Move the temporary directory to the target directory
#                 shutil.move(str(temp_dir_path), str(target_dir))

#             typer.echo(f"App '{app_name}' created successfully!")

#         except Exception as e:
#             typer.echo(f"Error: {str(e)}")
#             if "temp_dir_path" in locals() and temp_dir_path.exists():
#                 # Clean up the temporary directory on failure
#                 shutil.rmtree(temp_dir_path)
#             raise typer.Exit(1)

import argparse

class StartAppCommand(TemplateCommand):
    help = "Create a new FastAPI app."
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name',
            type=str,
            help='Name of the new FastAPI app.'
        )
        parser.add_argument(
            'target_dir',
            nargs='?',
            type=Path,
            default=None,
            help='Optional target directory for the new app.'
        )
    def handle(self, args: List[str]):
        parser = argparse.ArgumentParser(description=self.help)
        self.add_arguments(parser)
        parsed_args = parser.parse_args(args)

        app_name = parsed_args.app_name
        target_dir = parsed_args.target_dir or Path.cwd() / app_name

        try:
            # Validate the app name
            if not self.validate_name(app_name, entity="app"):
                raise typer.Exit(1)

            # Check if manage.py exists
            if not (Path.cwd() / "manage.py").exists():
                typer.echo(
                    "Error: manage.py not found. Make sure you're in the project root directory."
                )
                raise typer.Exit(1)

            # Check if the app directory already exists
            if target_dir.exists():
                typer.echo(f"Error: App '{app_name}' already exists.")
                raise typer.Exit(1)

            # Create a temporary directory for atomic operations
            with tempfile.TemporaryDirectory(prefix=f"{app_name}_") as temp_dir:
                temp_dir_path = Path(temp_dir)

                # Load the template environment
                template_dir = self.template_dir / 'app_template'
                env = Environment(loader=FileSystemLoader(template_dir))
                template_files = env.list_templates()

                # Render and save each template file in the temporary directory
                for template_file in template_files:
                    render_template(
                        env=env,
                        template_file=template_file,
                        target_dir=temp_dir_path,
                        app_name=app_name,
                    )

                # Move the temporary directory to the target directory
                shutil.move(str(temp_dir_path), str(target_dir))

            typer.echo(f"App '{app_name}' created successfully!")

        except Exception as e:
            typer.echo(f"Error: {str(e)}")
            raise typer.Exit(1)