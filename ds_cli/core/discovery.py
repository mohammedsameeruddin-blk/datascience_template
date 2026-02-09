from pathlib import Path
from typing import List, Optional


class ProjectDiscovery:
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.src_path = self.project_path / "src"

    # Core project detection
    def get_project_root(self) -> Optional[Path]:
        """
        Returns src/<project_name> if valid, else None
        """
        if not self.src_path.exists():
            return None

        for d in self.src_path.iterdir():
            if (
                d.is_dir()
                and (d / "dataflow").exists()
                and (d / "models").exists()
            ):
                return d

        return None

    def is_valid_project(self) -> bool:
        return self.get_project_root() is not None

    # Dataset discovery
    def get_datasets(self) -> List[str]:
        project = self.get_project_root()
        if project is None:
            return []

        datasets = set()

        preprocess_dir = project / "dataflow" / "preprocess"
        features_dir = project / "dataflow" / "features"

        if preprocess_dir.exists():
            for f in preprocess_dir.glob("*_preprocess.py"):
                datasets.add(f.stem.replace("_preprocess", ""))

        if features_dir.exists():
            for f in features_dir.glob("*_features.py"):
                datasets.add(f.stem.replace("_features", ""))

        return sorted(datasets)
    
    # Model discovery
    def get_models(self) -> List[str]:
        project_root = self.get_project_root()
        if project_root is None:
            return []

        models_dir = project_root / "models"
        if not models_dir.exists():
            return []

        models = []

        for d in models_dir.iterdir():
            if not d.is_dir():
                continue

            # minimal validity check
            if (d / "training").exists() and (d / "inference").exists():
                models.append(d.name)

        return sorted(models)

