"""File generation utilities for creating new dataset files"""

from pathlib import Path
from typing import List, Dict
import shutil


class DatasetFileGenerator:
    """Generates new dataset files by copying from templates"""

    def __init__(self, model_path: Path):
        self.model_path = Path(model_path)

    def generate_dataset_files(self, template_dataset: str, new_dataset: str) -> List[Path]:
        """
        Generate new dataset files by copying from template dataset
        
        Args:
            template_dataset: Name of the existing dataset to use as template
            new_dataset: Name of the new dataset to create
            
        Returns:
            List of created file paths
        """
        created_files = []

        # Copy preprocess file
        template_preprocess = self.model_path / "data" / f"{template_dataset}_preprocess.py"
        if template_preprocess.exists():
            new_preprocess = self.model_path / "data" / f"{new_dataset}_preprocess.py"
            shutil.copy(template_preprocess, new_preprocess)
            created_files.append(new_preprocess)

        # Copy features file
        template_features = self.model_path / "features" / f"{template_dataset}_features.py"
        if template_features.exists():
            new_features = self.model_path / "features" / f"{new_dataset}_features.py"
            shutil.copy(template_features, new_features)
            created_files.append(new_features)

        return created_files

    def update_file_references(self, file_path: Path, old_dataset: str, new_dataset: str) -> None:
        """
        Update internal references in generated files
        
        Args:
            file_path: Path to the file to update
            old_dataset: Old dataset keyword to replace
            new_dataset: New dataset keyword to replace with
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace dataset keyword in comments and strings
        updated_content = content.replace(old_dataset, new_dataset)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
