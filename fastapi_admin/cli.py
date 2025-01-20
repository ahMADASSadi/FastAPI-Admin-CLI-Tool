from jinja2 import Environment, FileSystemLoader
from typing import Optional
from pathlib import Path
import tempfile
import shutil
import typer
import os

from .cli_utils import render_template, validate_name


app = typer.Typer()


@app.command()
def startproject(project_name: str, project_dir: str = "."):
    try:
        # Validate the project name
        if not validate_name(project_name, entity="project"):
            raise typer.Exit(1)

        # Define paths
        template_dir = Path(__file__).parent / "templates/project_template"
        target_dir = Path(project_dir).resolve() / project_name

        # Check if the project directory already exists
        if target_dir.exists():
            typer.echo(f"Error: Project '{project_name}' already exists in '{target_dir}'.")
            raise typer.Exit(1)

        # Create a temporary directory for atomic operations
        with tempfile.TemporaryDirectory(prefix=f"{project_name}_") as temp_dir:
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
                    project_name=project_name,
                )

            # Move the temporary directory to the target directory
            shutil.move(str(temp_dir_path), str(target_dir))

        typer.echo(f"Project '{project_name}' created successfully in '{target_dir}'!")

    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        if "temp_dir_path" in locals() and temp_dir_path.exists():
            shutil.rmtree(temp_dir_path)  # Clean up the temporary directory on failure
        raise typer.Exit(1)
    
@app.command()
def startapp(app_name: str, project_name: Optional[str] = None):
    try:
        # Validate the app name
        if not validate_name(app_name):
            raise typer.Exit(1)

        # Define paths
        template_dir = Path(__file__).parent / "templates/app_template"
        target_dir = Path.cwd() / app_name

        # Check if manage.py exists
        if not (Path.cwd() / "manage.py").exists():
            typer.echo("Error: manage.py not found. Make sure you're in the project root directory.")
            raise typer.Exit(1)

        # Check if the app directory already exists
        if target_dir.exists():
            typer.echo(f"Error: app '{app_name}' already exists.")
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
                    app_name=app_name,
                    target_dir=temp_dir_path,
                    project_name=project_name,
                )
            
            shutil.move(str(temp_dir_path), str(target_dir))

        typer.echo(f"App '{app_name}' created successfully!")

    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        if "temp_dir_path" in locals() and temp_dir_path.exists():
            shutil.rmtree(temp_dir_path)  # Clean up the temporary directory on failure
        raise typer.Exit(1)

def main():
    """Entrypoint for the CLI."""
    app()
