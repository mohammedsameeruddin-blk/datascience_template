import shutil
from pathlib import Path


class ModelFileDegenerator:
    def __init__(self, project_root: Path):
        """
        project_root = src/<project_name>
        """
        self.project_root = project_root
        self.models_dir = project_root / "models"

    def degenerate(self, model_name: str) -> list[Path]:
        removed_files: list[Path] = []

        model_dir = self.models_dir / model_name
        if model_dir.exists():
            removed_files = [f for f in model_dir.rglob("*") if f.is_file()]
            shutil.rmtree(model_dir)

        return removed_files
