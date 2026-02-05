from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def to_class_name(dataset_name: str) -> str:
    """
    titanic_v2 → TitanicV2
    customer-churn → CustomerChurn
    """
    return "".join(word.capitalize() for word in dataset_name.replace("-", "_").split("_"))


class DatasetFileGenerator:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.preprocess_dir = project_root / "dataflow" / "preprocess"
        self.features_dir = project_root / "dataflow" / "features"

        templates_dir = Path(__file__).resolve().parents[1] / "templates" / "dataset"
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def generate(self, dataset_name: str) -> list[Path]:
        dataset_class = to_class_name(dataset_name)

        context = {
            "dataset_name": dataset_name,
            "dataset_class": dataset_class,
        }

        created_files = []

        # preprocess
        created_files.append(
            self._render(
                "preprocess.py.jinja",
                self.preprocess_dir / f"{dataset_name}_preprocess.py",
                context,
            )
        )

        # features
        created_files.append(
            self._render(
                "features.py.jinja",
                self.features_dir / f"{dataset_name}_features.py",
                context,
            )
        )

        return created_files

    def _render(self, template_name: str, output_path: Path, context: dict) -> Path:
        template = self.env.get_template(template_name)
        content = template.render(**context)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        return output_path
