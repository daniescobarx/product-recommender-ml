from pathlib import Path


def test_required_project_directories_exist() -> None:
    required_directories = [
        "src",
        "tests",
        "data",
        "data/raw",
        "data/interim",
        "data/processed",
        "models",
        "configs",
    ]

    for directory in required_directories:
        assert Path(directory).is_dir()


def test_required_project_files_exist() -> None:
    required_files = [
        "pyproject.toml",
        ".gitignore",
        ".pre-commit-config.yaml",
        "README.md",
        "src/recommender_system/__init__.py",
        "src/recommender_system/config/__init__.py",
        "src/recommender_system/config/settings.py",
        "src/recommender_system/data/__init__.py",
        "src/recommender_system/data/interfaces.py",
        "src/recommender_system/data/preprocessing.py",
        "src/recommender_system/models/__init__.py",
        "src/recommender_system/models/interfaces.py",
        "src/recommender_system/models/factory.py",
        "src/recommender_system/models/baselines.py",
        "src/recommender_system/evaluation/__init__.py",
        "src/recommender_system/evaluation/metrics.py",
    ]

    for file_path in required_files:
        assert Path(file_path).is_file()
