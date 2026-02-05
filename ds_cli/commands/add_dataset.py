"""Command for adding a new dataset to a model"""

from pathlib import Path
import click
from colorama import Fore, Style
from ds_cli.core.discovery import ProjectDiscovery
from ds_cli.core.generator import DatasetFileGenerator


@click.command(name="add-dataset")
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--dataset-name", "-d", default=None, help="Name of the new dataset")
@click.option("--model", "-m", default=None, help="Target model (required for multi-model projects)")
def add_dataset(project_path: str, dataset_name: str, model: str):
    """Add a new dataset to an existing model in your data science project"""
    
    project_path = Path(project_path)
    discovery = ProjectDiscovery(project_path)

    # Validate project
    if not discovery.is_valid_project():
        click.echo(f"{Fore.RED}Error: {project_path} is not a valid data science project{Style.RESET_ALL}")
        raise click.Abort()

    click.echo(f"{Fore.CYAN}Analyzing project structure...{Style.RESET_ALL}")

    # Get project and models info
    project_name = discovery.get_project_name()
    models = discovery.get_models()

    if not models:
        click.echo(f"{Fore.RED}Error: No models found in project{Style.RESET_ALL}")
        raise click.Abort()

    click.echo(f"{Fore.GREEN}✓ Project: {project_name}{Style.RESET_ALL}")
    click.echo(f"{Fore.GREEN}✓ Found {len(models)} model(s): {', '.join(models)}{Style.RESET_ALL}\n")

    # Handle model selection
    if len(models) == 1:
        target_model = models[0]
        click.echo(f"{Fore.CYAN}Single model detected: {target_model}{Style.RESET_ALL}")
    else:
        if model is None:
            click.echo(f"{Fore.YELLOW}Multiple models found. Please select:{Style.RESET_ALL}")
            for i, m in enumerate(models, 1):
                click.echo(f"  {i}. {m}")
            choice = click.prompt("Enter model number", type=click.IntRange(1, len(models)))
            target_model = models[choice - 1]
        else:
            if model not in models:
                click.echo(f"{Fore.RED}Error: Model '{model}' not found{Style.RESET_ALL}")
                raise click.Abort()
            target_model = model

    click.echo(f"{Fore.GREEN}✓ Target model: {target_model}{Style.RESET_ALL}\n")

    # Get existing datasets
    existing_datasets = discovery.get_datasets_for_model(target_model)
    click.echo(f"{Fore.CYAN}Existing datasets: {', '.join(existing_datasets) if existing_datasets else 'None'}{Style.RESET_ALL}\n")

    # Get new dataset name
    if dataset_name is None:
        dataset_name = click.prompt("Enter new dataset name")

    if dataset_name in existing_datasets:
        click.echo(f"{Fore.RED}Error: Dataset '{dataset_name}' already exists{Style.RESET_ALL}")
        raise click.Abort()

    # Select template dataset
    if not existing_datasets:
        click.echo(f"{Fore.RED}Error: No existing datasets to use as template{Style.RESET_ALL}")
        raise click.Abort()

    if len(existing_datasets) == 1:
        template_dataset = existing_datasets[0]
        click.echo(f"{Fore.CYAN}Using '{template_dataset}' as template{Style.RESET_ALL}\n")
    else:
        click.echo(f"{Fore.YELLOW}Select template dataset:{Style.RESET_ALL}")
        for i, ds in enumerate(existing_datasets, 1):
            click.echo(f"  {i}. {ds}")
        choice = click.prompt("Enter dataset number", type=click.IntRange(1, len(existing_datasets)))
        template_dataset = existing_datasets[choice - 1]

    # Generate files
    model_path = project_path / "src" / project_name / "models" / target_model
    generator = DatasetFileGenerator(model_path)

    click.echo(f"{Fore.CYAN}Creating dataset files...{Style.RESET_ALL}")
    created_files = generator.generate_dataset_files(template_dataset, dataset_name)

    # Update file references
    for file_path in created_files:
        generator.update_file_references(file_path, template_dataset, dataset_name)

    # Report results
    click.echo(f"\n{Fore.GREEN}✓ Successfully created new dataset: {dataset_name}{Style.RESET_ALL}\n")
    click.echo(f"{Fore.GREEN}Created files:{Style.RESET_ALL}")
    for file_path in created_files:
        click.echo(f"  • {file_path.relative_to(project_path)}")

    click.echo(f"\n{Fore.YELLOW}Next steps:{Style.RESET_ALL}")
    click.echo(f"  1. Review and update the created files if needed")
    click.echo(f"  2. Update any configuration files that reference datasets")
    click.echo(f"  3. Add the new dataset to your training/evaluation scripts")
