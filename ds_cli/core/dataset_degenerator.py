from pathlib import Path


class DatasetFileDegenerator:
    def __init__(self, project_root: Path):
        """
        project_root = src/<project_name>
        """
        self.project_root = project_root
        self.config_dir = project_root / "dataflow" / "config"
        self.preprocess_dir = project_root / "dataflow" / "preprocess"
        self.features_dir = project_root / "dataflow" / "features"

    def degenerate(self, dataset_name: str) -> list[Path]:
        removed_files: list[Path] = []

        candidates = [
            self.config_dir / f"{dataset_name}_config.py",
            self.preprocess_dir / f"{dataset_name}_preprocess.py",
            self.features_dir / f"{dataset_name}_features.py",
        ]

        for path in candidates:
            if path.exists():
                removed_files.append(path)
                path.unlink()

        return removed_files
