from functools import lru_cache
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "dev", "test", "prod"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def _project_root() -> Path:
    """Return the repository root inferred from the src layout."""
    return Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env files.

    Attributes:
        app_name: Human-readable application name.
        environment: Runtime environment identifier.
        random_seed: Seed used to make experiments reproducible.
        data_dir: Base directory for project datasets.
        raw_data_dir: Directory containing immutable raw datasets.
        processed_data_dir: Directory containing model-ready datasets.
        model_dir: Directory used to store trained model files.
        artifacts_dir: Directory used to store generated artifacts.
        log_level: Minimum logging level for application logs.
        mlflow_tracking_uri: MLflow tracking URI reserved for the MLOps stage.
        mlflow_experiment_name: MLflow experiment name reserved for the MLOps stage.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "ecommerce-recommender-system"
    environment: Environment = "local"
    random_seed: int = Field(default=42, ge=0)

    data_dir: Path = Path("data")
    raw_data_dir: Path = Path("data/raw")
    processed_data_dir: Path = Path("data/processed")
    model_dir: Path = Path("models")
    artifacts_dir: Path = Path("artifacts")

    log_level: LogLevel = "INFO"
    mlflow_tracking_uri: str = "./mlruns"
    mlflow_experiment_name: str = "ecommerce-recommender-local"

    root_dir: Path = Field(default_factory=_project_root, exclude=True)

    @field_validator("app_name", "mlflow_tracking_uri", "mlflow_experiment_name")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        """Validate that string settings are not blank.

        Args:
            value: String value loaded by Pydantic Settings.

        Returns:
            The stripped string value.

        Raises:
            ValueError: If the value is empty after trimming whitespace.
        """
        value = value.strip()
        if not value:
            msg = "Setting cannot be blank."
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def validate_directories(self) -> Self:
        """Validate directory settings before the application uses them.

        Returns:
            The validated settings instance.

        Raises:
            ValueError: If any directory setting is empty.
        """
        for field_name in (
            "data_dir",
            "raw_data_dir",
            "processed_data_dir",
            "model_dir",
            "artifacts_dir",
        ):
            path = getattr(self, field_name)
            if not str(path).strip():
                msg = f"{field_name} cannot be empty."
                raise ValueError(msg)
        return self

    def resolve_path(self, path: Path) -> Path:
        """Resolve a path against the project root when it is relative.

        Args:
            path: Relative or absolute path to resolve.

        Returns:
            Absolute normalized path.
        """
        expanded_path = path.expanduser()
        if expanded_path.is_absolute():
            return expanded_path.resolve()
        return (self.root_dir / expanded_path).resolve()

    @property
    def resolved_data_dir(self) -> Path:
        """Return the absolute data directory path."""
        return self.resolve_path(self.data_dir)

    @property
    def resolved_raw_data_dir(self) -> Path:
        """Return the absolute raw data directory path."""
        return self.resolve_path(self.raw_data_dir)

    @property
    def resolved_processed_data_dir(self) -> Path:
        """Return the absolute processed data directory path."""
        return self.resolve_path(self.processed_data_dir)

    @property
    def resolved_model_dir(self) -> Path:
        """Return the absolute model directory path."""
        return self.resolve_path(self.model_dir)

    @property
    def resolved_artifacts_dir(self) -> Path:
        """Return the absolute artifacts directory path."""
        return self.resolve_path(self.artifacts_dir)

    @property
    def expected_directories(self) -> tuple[Path, ...]:
        """Return directories expected to exist during local development."""
        return (
            self.resolved_data_dir,
            self.resolved_raw_data_dir,
            self.resolved_processed_data_dir,
            self.resolved_model_dir,
            self.resolved_artifacts_dir,
        )


@lru_cache
def get_settings() -> Settings:
    """Create cached application settings.

    Returns:
        Settings instance loaded from environment variables and .env.
    """
    return Settings()
