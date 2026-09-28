# Data Science CLI Tool

CLI tool for managing data science projects — add and remove datasets and models.

## Installation

```bash
pip install -e .
```

Or as a project dependency (uv):

```bash
# pyproject.toml
"ds-cli @ git+https://github.com/<org>/datascience_template.git@<branch>"
```

After updating the version, refresh the lock and sync:

```bash
uv lock --upgrade-package ds-cli
uv sync
```

---

## Commands

### `add-dataset`

Adds a new dataset to an existing data science project. Generates the config, preprocess, and features files under the `dataflow/` directory.

```bash
ds-cli add-dataset /path/to/project --dataset-name <name>
```

| Option | Short | Required | Description |
|---|---|---|---|
| `--dataset-name` | `-d` | Yes | Name of the new dataset |

**Creates:**
- `src/<project>/dataflow/config/<dataset>_config.py`
- `src/<project>/dataflow/preprocess/<dataset>_preprocess.py`
- `src/<project>/dataflow/features/<dataset>_features.py`

---

### `remove-dataset`

Removes an existing dataset from a data science project. Deletes the corresponding config, preprocess, and features files from the `dataflow/` directory.

```bash
ds-cli remove-dataset /path/to/project --dataset-name <name>
```

| Option | Short | Required | Description |
|---|---|---|---|
| `--dataset-name` | `-d` | Yes | Name of the dataset to remove |

**Removes:**
- `src/<project>/dataflow/config/<dataset>_config.py`
- `src/<project>/dataflow/preprocess/<dataset>_preprocess.py`
- `src/<project>/dataflow/features/<dataset>_features.py`

---

### `add-model`

Adds a new model to an existing data science project. Generates the full model directory structure (config, training, inference) under `models/` using Jinja templates.

```bash
ds-cli add-model /path/to/project --model-name <name> --model-type <type>
```

| Option | Short | Required | Description |
|---|---|---|---|
| `--model-name` | `-m` | Yes | Name of the new model |
| `--model-type` | — | Yes | Model type: `Regression` or `Classification` |

**Creates:**
- `src/<project>/models/<model>/config/`
- `src/<project>/models/<model>/training/`
- `src/<project>/models/<model>/inference/`

---

### `remove-model`

Removes an existing model from a data science project. Deletes the entire model directory under `models/`.

```bash
ds-cli remove-model /path/to/project --model-name <name>
```

| Option | Short | Required | Description |
|---|---|---|---|
| `--model-name` | `-m` | Yes | Name of the model to remove |

**Removes:**
- `src/<project>/models/<model>/`

---

## Naming Rules

Dataset and model names must contain only letters, numbers, dashes (`-`), and underscores (`_`).
