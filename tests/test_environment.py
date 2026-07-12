import importlib

from recommender_system.config.settings import Settings


def test_main_package_can_be_imported() -> None:
    package = importlib.import_module("recommender_system")

    assert package is not None


def test_expected_directories_are_available() -> None:
    settings = Settings(_env_file=None)

    for directory in settings.expected_directories:
        assert directory.exists()
        assert directory.is_dir()
