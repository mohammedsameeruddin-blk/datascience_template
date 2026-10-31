# Datascience Template

A [Copier](https://copier.readthedocs.io/) template for bootstrapping data science projects at Blackstraw. It provides a standardised project scaffold covering data preprocessing, featurization, model training, inference, and hyperparameter tuning.

## Requirements

- [Copier](https://copier.readthedocs.io/) v9+
- [uv](https://docs.astral.sh/uv/)

```bash
uv tool install copier
```

## Naming Convention

Your project directory **must** be named with a `ds_` prefix:

```
ds_<project_name>
```

Example: `ds_store_sales`, `ds_customer_churn`, `ds_fraud_detection`

## Creating a New Project

Run this command from your workspace (the parent directory where you want the project to live):

```bash
copier copy git@github.com:mohammedsameeruddin-blk/datascience_template.git ds_<project_name> --trust
```

Example:

```bash
copier copy git@github.com:mohammedsameeruddin-blk/datascience_template.git ds_store_sales --trust
```

### Questions You Will Be Asked

| Question | Description | Example |
|---|---|---|
| `project` | DS project name (no `ds_` prefix) | `store_sales` |
| `model` | Model name | `sales_forecast` |
| `dataset_keyword` | Dataset keyword for preprocessing and featurization | `oil_stores` |
| `model_type` | Select `Regression` or `Classification` | `Regression` |
| `author_email` | Your email address | `you@blackstraw.ai` |

### After Creation

```bash
cd ds_<project_name>

# Install dependencies
uv sync

# Initialise git
git init
git checkout -b main
git add .
git commit -m "chore: initial project scaffold from template"
```

## Updating an Existing Project

When a new template version is released, run this from inside your project directory:

```bash
copier update --vcs-ref <version> --trust
```

Example:

```bash
copier update --vcs-ref v1.1.0 --trust
```

Then review and commit the changes:

```bash
git diff
git add .
git commit -m "chore: update project scaffold to <version>"
```

## Project Structure

```
ds_<project_name>/
├── src/
│   └── <project>/
│       ├── common_utils/
│       ├── dataflow/
│       │   ├── config/
│       │   ├── features/
│       │   │   └── transformers/
│       │   └── preprocess/
│       └── models/
│           └── <model>/
│               ├── config/
│               ├── inference/
│               └── training/
│                   ├── evaluation/
│                   └── hypertuning/
├── pyproject.toml
├── README.md
└── .copier-answers.yml
```

## Template Versions

| Version | Notes |
|---|---|
| `v1.0.0` | Initial release — restructured template, naming validation, `copier update` support |
