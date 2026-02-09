"""Command for adding a new model to a project"""

from pathlib import Path
import click
from colorama import Fore, Style

from ds_cli.core.discovery import ProjectDiscovery
from ds_cli.core.model_generator import ModelFileGenerator


@click.command(name="add-model")
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--model-name", "-m", required=True, help="Name of the new model")
@click.option(
    "--model-type",
    required=True,
    type=click.Choice(["Regression", "Classification"], case_sensitive=True),
    help="Select the model type",
)
def add_model(project_path: str, model_name: str, model_type: str):
    """Add a new model to a data science project"""

    project_path = Path(project_path)
    discovery = ProjectDiscovery(project_path)

    # Validate project
    if not discovery.is_valid_project():
        click.echo(
            f"{Fore.RED}Error: {project_path} is not a valid data science project{Style.RESET_ALL}"
        )
        raise click.Abort()

    project_root = discovery.get_project_root()

    click.echo(f"{Fore.CYAN}Analyzing project structure...{Style.RESET_ALL}")
    click.echo(f"{Fore.GREEN}✓ Project: {project_root.name}{Style.RESET_ALL}\n")

    # Existing models (for collision check only)
    existing_models = discovery.get_models()

    click.echo(
        f"{Fore.CYAN}Existing models: "
        f"{', '.join(existing_models) if existing_models else 'None'}"
        f"{Style.RESET_ALL}\n"
    )
    
    if model_name in existing_models:
        click.echo(
            f"{Fore.RED}Error: Model '{model_name}' already exists{Style.RESET_ALL}"
        )
        raise click.Abort()

    generator = ModelFileGenerator(project_root)

    click.echo(
        f"{Fore.CYAN}Creating model '{model_name}' ({model_type})...{Style.RESET_ALL}"
    )
    created_files = generator.generate(model_name, model_type)

    # Report results
    click.echo(
        f"\n{Fore.GREEN}✓ Successfully created new model: {model_name}{Style.RESET_ALL}\n"
    )
    click.echo(f"{Fore.GREEN}Created files:{Style.RESET_ALL}")
    for file_path in created_files:
        click.echo(f"  • {file_path.relative_to(project_path)}")

    click.echo(f"\n{Fore.YELLOW}Next steps:{Style.RESET_ALL}")
    click.echo("  1. Review the generated files")
    click.echo("  2. Use the model in training/inference")