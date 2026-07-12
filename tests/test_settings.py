from pathlib import Path

import pytest
from pydantic import ValidationError

from recommender_system.config.settings import Settings


def test_settings_loads_default_values() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "ecommerce-recommender-system"
    assert settings.environment == "local"
    assert settings.random_seed == 42
    assert settings.log_level == "INFO"
    assert settings.mlflow_tracking_uri == "./mlruns"


def test_settings_accepts_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_NAME", "custom-recommender")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("RANDOM_SEED", "123")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DATA_DIR", "custom-data")
    monkeypatch.setenv("RAW_DATA_DIR", "custom-data/raw")

    settings = Settings(_env_file=None)

    assert settings.app_name == "custom-recommender"
    assert settings.environment == "test"
    assert settings.random_seed == 123
    assert settings.log_level == "DEBUG"
    assert settings.data_dir == Path("custom-data")
    assert settings.raw_data_dir == Path("custom-data/raw")


def test_random_seed_must_be_integer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RANDOM_SEED", "not-an-integer")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_environment_raises_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "staging")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_log_level_raises_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOG_LEVEL", "TRACE")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_directory_paths_are_resolved_from_root(tmp_path: Path) -> None:
    settings = Settings(
        _env_file=None,
        root_dir=tmp_path,
        data_dir=Path("datasets"),
        raw_data_dir=Path("datasets/raw"),
        processed_data_dir=Path("datasets/processed"),
        model_dir=Path("trained-models"),
        artifacts_dir=Path("outputs"),
    )

    assert settings.resolved_data_dir == tmp_path / "datasets"
    assert settings.resolved_raw_data_dir == tmp_path / "datasets/raw"
    assert settings.resolved_processed_data_dir == tmp_path / "datasets/processed"
    assert settings.resolved_model_dir == tmp_path / "trained-models"
    assert settings.resolved_artifacts_dir == tmp_path / "outputs"
