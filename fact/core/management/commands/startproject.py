from jinja2 import Environment, FileSystemLoader
import importlib.resources
from pathlib import Path
from typing import List
import fact
import tempfile
import shutil
import typer

from fact.core.management.commands import validate_name, render_template
from fact.core.management.base import BaseCommand


class StartProjectCommand(BaseCommand):
    help = "Create a new FastAPI project."
    
    @classmethod
    def handle(cls, args: List[str]):
        try:
            # Validate the project name
            project_name = args[0] if args else None
            if not project_name or not validate_name(project_name, entity="project"):
                typer.echo("Error: Invalid project name.")
                raise typer.Exit(1)


            template_dir = importlib.resources.files(fact).joinpath('templates/project_template')
            
            target_dir = args[1] if len(args)>1 else Path.cwd() / project_name

            # Check if the project directory already exists
            if target_dir.exists():
                typer.echo(f"Error: Project '{project_name}' already exists.")
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

            typer.echo(f"Project '{project_name}' created successfully!")

        except Exception as e:
            typer.echo(f"Error: {str(e)}")
            if "temp_dir_path" in locals() and temp_dir_path.exists():
                # Clean up the temporary directory on failure
                shutil.rmtree(temp_dir_path)
            raise typer.Exit(1)