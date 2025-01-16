import typer
from jinja2 import Environment, FileSystemLoader
import os

app = typer.Typer()

@app.command()
def startproject(project_name: str):
    # Define the template directory
    template_dir = os.path.join(os.path.dirname(__file__), "templates/project_template")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Debugging output
    print("Template directory:", template_dir)
    template_files = env.list_templates()
    print("Template files:", template_files)

    # Ensure the project directory exists
    os.makedirs(project_name, exist_ok=True)

    for template_file in template_files:
        template = env.get_template(template_file)
        rendered_content = template.render(project_name=project_name)
        
        # Replace 'project_name' in the file path with the actual project name
        target_path = os.path.join(project_name, template_file.replace("project_name", project_name))
        
        # Replace the file extension from .py-tpl to .py (or others as needed)
        if target_path.endswith("-tpl"):
            target_path = target_path.replace("-tpl", "")
        
        # Create subdirectories as needed
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Write the rendered template to the target file
        with open(target_path, "w") as f:
            f.write(rendered_content)

    typer.echo(f"Project '{project_name}' created successfully!")


@app.command()
def startapp(app_name:str):
    template_dir = os.path.join(os.path.dirname(__file__), "templates/app_template")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Debugging output
    print("Template directory:", template_dir)
    template_files = env.list_templates()
    print("Template files:", template_files)

    # Ensure the project directory exists
    os.makedirs(app_name, exist_ok=True)
    
    for template_file in template_files:
        template = env.get_template(template_file)
        rendered_content = template.render(app_name=app_name)
        
        # Replace 'app_name' in the file path with the actual project name
        target_path = os.path.join(app_name, template_file.replace("app_name", app_name))
        
        # Replace the file extension from .py-tpl to .py (or others as needed)
        if target_path.endswith("-tpl"):
            target_path = target_path.replace("-tpl", "")
        
        # Create subdirectories as needed
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Write the rendered template to the target file
        with open(target_path, "w") as f:
            f.write(rendered_content)

    typer.echo(f"App '{app_name}' created successfully!")
    
def main():
    """Entrypoint for the CLI."""
    app()
