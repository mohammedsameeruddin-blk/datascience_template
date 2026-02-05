# Data Science CLI Tool

CLI tool for managing data science projects - add datasets, models, and more.

## Installation

```bash
pip install -e .
```

## Usage

### Add a New Dataset to a Project

```bash
ds-cli add-dataset /path/to/project --dataset-name my_dataset
```

If the project has multiple models, you'll be prompted to select which model to add the dataset to.
