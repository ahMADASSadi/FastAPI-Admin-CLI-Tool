from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import List
import tempfile
import shutil
import typer

from fact.core.management.commands import validate_name, render_template
from fact.core.management.base import BaseCommand



class StartAppCommand(BaseCommand):
    help = "Create a new FastAPI app."
    
    def handle(self, args: List[str]):
        temp_dir_path = None
        
        try:
            app_name = args[0] if args else None
            if not app_name or not validate_name(app_name, entity="app"):
                typer.echo("Error: Invalid app name.")
                raise typer.Exit(code=1)

            self.template_dir = self.template_dir / "app_template"
            target_dir = Path(args[1]) if len(args) > 1 else Path.cwd() / app_name

            
            if not (Path.cwd() / "manage.py").exists():
                typer.echo(
                    "Error: manage.py not found. Make sure you're in the project root directory."
                )
                raise typer.Exit(1)

            
            if target_dir.exists():
                typer.echo(f"Error: App '{app_name}' already exists.")
                raise typer.Exit(1)

            
            with tempfile.TemporaryDirectory(prefix=f"{app_name}_") as temp_dir:
                temp_dir_path = Path(temp_dir)

                env = Environment(loader=FileSystemLoader(self.template_dir))
                
                template_files = env.list_templates()
                
                for template_file in template_files:
                    render_template(
                        env=env,
                        template_file=template_file,
                        target_dir=temp_dir_path,
                        app_name=app_name,
                    )

                shutil.move(str(temp_dir_path), str(target_dir))

            typer.echo(f"App '{app_name}' created successfully!")

        except Exception as e:
            typer.echo(f"Error: {str(e)}")
            if "temp_dir_path" in locals() and temp_dir_path.exists():
                # Clean up the temporary directory on failure
                shutil.rmtree(temp_dir_path)
            raise typer.Exit(1)