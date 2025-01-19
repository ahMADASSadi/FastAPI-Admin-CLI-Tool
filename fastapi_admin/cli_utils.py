from typing import Optional
from pathlib import Path
import typer


def validate_app_name(app_name: str) -> bool:
    """Validate the app name to ensure it follows naming conventions."""
    if not app_name.isidentifier():
        typer.echo(f"Error: '{
                   app_name}' is not a valid app name. It must be a valid Python identifier.")
        return False
    return True


def render_template(
    env,
    template_file: str,
    app_name: str,
    target_dir: Path,
    project_name: Optional[str] = None,
) -> None:
    """Render a template file and save it to the target directory."""
    template = env.get_template(template_file)
    rendered_content = template.render(
        app_name=app_name, project_name=project_name)

    # Replace "app_name" in the filename and handle template extensions
    target_file = template_file.replace("app_name", app_name)
    if target_file.endswith("-tpl"):
        target_file = target_file[:-4]  # Remove the "-tpl" extension

    target_path = target_dir / target_file

    # Create subdirectories as needed
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the rendered template to the target file
    with open(target_path, "w") as f:
        f.write(rendered_content)