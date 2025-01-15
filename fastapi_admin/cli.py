import typer
from jinja2 import Environment, FileSystemLoader
import os

app = typer.Typer()

@app.command()
def startproject(project_name: str):
    env = Environment(loader=FileSystemLoader("fastapi_admin/project_template"))
    template_files = env.list_templates()

    os.makedirs(project_name, exist_ok=True)

    for template_file in template_files:
        template = env.get_template(template_file)
        rendered_content = template.render(project_name=project_name)
        with open(os.path.join(project_name, template_file), "w") as f:
            f.write(rendered_content)

    typer.echo(f"Project '{project_name}' created successfully!")

def main():
        """Entrypoint for the CLI."""
        app()