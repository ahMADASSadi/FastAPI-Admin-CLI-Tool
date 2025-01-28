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


class StartAppCommand(BaseCommand):
    help_text = "Create a new FastAPI app."

    @classmethod
    def handle(cls, args: List[str]):
        try:
            # Validate the app name
            app_name = args[0] if args else None
            if not app_name or not validate_name(app_name, entity="app"):
                typer.echo("Error: Invalid app name.")
                raise typer.Exit(1)

            # Define paths
            template_dir = importlib.resources.files(fastapi_admin).joinpath('templates/app_template')
            target_dir = Path.cwd() / app_name

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
            if "temp_dir_path" in locals() and temp_dir_path.exists():
                # Clean up the temporary directory on failure
                shutil.rmtree(temp_dir_path)
            raise typer.Exit(1)
