from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class ModelFileGenerator:
    def __init__(self, project_root: Path):
        """
        project_root = src/<project_name>
        """
        self.project_root = project_root
        self.models_dir = project_root / "models"

        templates_dir = (
            Path(__file__).resolve().parents[1]
            / "templates"
            / "model"
        )
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def generate(self, model: str, model_type: str) -> list[Path]:
        target_dir = self.models_dir / model

        if target_dir.exists():
            raise FileExistsError(f"Model '{model}' already exists")

        context = {
            "project": self.project_name,
            "model": model,
            "model_type": model_type,
        }

        created_files = []

        for template_name in self.env.list_templates():
            if not template_name.endswith(".jinja"):
                continue

            output_path = target_dir / template_name.replace(".jinja", "")
            created_files.append(
                self._render(template_name, output_path, context)
            )

        return created_files

    def _render(self, template_name: str, output_path: Path, context: dict) -> Path:
        template = self.env.get_template(template_name)
        content = template.render(**context)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        return output_path
