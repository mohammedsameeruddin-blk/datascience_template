"""Command for removing an existing dataset from a project"""

from pathlib import Path
import re
import click
from colorama import Fore, Style

from ds_cli.core.discovery import ProjectDiscovery
from ds_cli.core.dataset_degenerator import DatasetFileDegenerator


@click.command(name="remove-dataset")
@click.argument("project_path", type=click.Path(exists=True))
@click.option(
    "--dataset-name", "-d", required=True, help="Name of the dataset to remove"
)
def remove_dataset(project_path: str, dataset_name: str):
    """Remove an existing dataset from a data science project"""

    # Validate dataset name format
    if not dataset_name or re.search(r"[^a-zA-Z0-9_-]", dataset_name):
        click.echo(
            f"{Fore.RED}Error: Dataset name must contain only letters, numbers, dashes and underscores.{Style.RESET_ALL}"
        )
        raise click.Abort()

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

    existing_datasets = discovery.get_datasets()

    click.echo(
        f"{Fore.CYAN}Existing datasets: "
        f"{', '.join(existing_datasets) if existing_datasets else 'None'}"
        f"{Style.RESET_ALL}\n"
    )

    if dataset_name not in existing_datasets:
        click.echo(
            f"{Fore.RED}Error: Dataset '{dataset_name}' does not exist{Style.RESET_ALL}"
        )
        raise click.Abort()

    degenerator = DatasetFileDegenerator(project_root)

    click.echo(f"{Fore.CYAN}Removing dataset files...{Style.RESET_ALL}")
    removed_files = degenerator.degenerate(dataset_name)

    click.echo(
        f"\n{Fore.GREEN}✓ Successfully removed dataset: {dataset_name}{Style.RESET_ALL}\n"
    )
    click.echo(f"{Fore.GREEN}Removed files:{Style.RESET_ALL}")
    for file_path in removed_files:
        click.echo(f"  • {file_path.relative_to(project_path)}")
