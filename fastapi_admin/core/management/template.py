from .base import BaseCommand
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import tempfile
import shutil
import typer
from typing import List
import importlib.resources
import fastapi_admin
from typing import Optional
from pathlib import Path
import typer

app = typer.Typer()


class TemplateCommand(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_dir = importlib.resources.files(
            fastapi_admin).joinpath('templates')

    @staticmethod
    def validate_name(name: str, entity: str = "app") -> bool:
        """Validate the name to ensure it follows naming conventions."""
        if not name.isidentifier():
            typer.echo(f"Error: '{name}' is not a valid {entity} name. It must be a valid Python identifier.")
            return False
        return True

    @staticmethod
    def render_template(
        env,
        template_file: str,
        target_dir: Path,
        **context,
    ) -> None:
        """Render a template file and save it to the target directory."""
        template = env.get_template(template_file)
        rendered_content = template.render(**context)

        # Replace placeholders in the filename and handle template extensions
        target_file = template_file
        for key, value in context.items():
            target_file = target_file.replace(key, value)
        if target_file.endswith("-tpl"):
            target_file = target_file[:-4]  # Remove the "-tpl" extension

        target_path = target_dir / target_file

        # Create subdirectories as needed
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the rendered template to the target file
        with open(target_path, "w") as f:
            f.write(rendered_content)
