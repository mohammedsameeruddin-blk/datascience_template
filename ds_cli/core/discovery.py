"""Project discovery utilities for analyzing data science project structure"""

from pathlib import Path
from typing import List, Dict, Set, Optional
import json


class ProjectDiscovery:
    """Discovers project structure and existing datasets/models"""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.src_path = self.project_path / "src"

    def is_valid_project(self) -> bool:
        """Check if the directory is a valid data science project"""
        # return (self.src_path.exists() and 
        #         (self.src_path / "*/models").exists())
        return any(
            d.is_dir() and (d / "models").exists()
            for d in self.src_path.iterdir()
        )

    def get_project_name(self) -> Optional[str]:
        """Extract project name from directory structure"""
        # if not self.src_path.exists():
        #     return None
        # subdirs = [d for d in self.src_path.iterdir() if d.is_dir()]
        # return subdirs[0].name if subdirs else None

        for d in self.src_path.iterdir():
            if d.is_dir() and (d / "models").exists():
                return d.name
        return None

    def get_models(self) -> List[str]:
        """Get list of available models in the project"""
        models_dir = self.src_path / self.get_project_name() / "models"
        if not models_dir.exists():
            return []
        
        return [d.name for d in models_dir.iterdir() if d.is_dir()]

    def get_datasets_for_model(self, model_name: str) -> List[str]:
        """Get list of datasets for a specific model by analyzing existing files"""
        datasets = set()
        model_path = self.src_path / self.get_project_name() / "models" / model_name

        # Check data directory for dataset-specific files
        data_dir = model_path / "data"
        if data_dir.exists():
            for file in data_dir.glob("*_preprocess.py"):
                # Extract dataset keyword from filename
                dataset_name = file.stem.replace("_preprocess", "")
                datasets.add(dataset_name)

        # Check features directory
        features_dir = model_path / "features"
        if features_dir.exists():
            for file in features_dir.glob("*_features.py"):
                dataset_name = file.stem.replace("_features", "")
                datasets.add(dataset_name)

        return sorted(list(datasets))

    def get_dataset_template_files(self, model_name: str, dataset_name: str) -> Dict[str, Path]:
        """Find all dataset-specific files for a given model and dataset"""
        model_path = self.src_path / self.get_project_name() / "models" / model_name
        template_files = {}

        # Data preprocessing file
        preprocess_file = model_path / "data" / f"{dataset_name}_preprocess.py"
        if preprocess_file.exists():
            template_files["preprocess"] = preprocess_file

        # Features file
        features_file = model_path / "features" / f"{dataset_name}_features.py"
        if features_file.exists():
            template_files["features"] = features_file

        return template_files

    def get_all_dataset_files(self, model_name: str, dataset_name: str) -> Dict[str, Path]:
        """Get all files related to a dataset for a model"""
        files = self.get_dataset_template_files(model_name, dataset_name)
        return files
