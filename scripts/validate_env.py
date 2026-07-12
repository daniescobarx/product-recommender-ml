from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType

MIN_PYTHON_VERSION = (3, 11)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
MAIN_DEPENDENCIES = (
    "numpy",
    "pandas",
    "pydantic",
    "pydantic_settings",
    "sklearn",
    "torch",
    "dotenv",
    "typer",
)


def configure_import_path() -> None:
    """Ensure the src layout is importable when the package is not installed."""
    src_path = str(SRC_DIR)
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


def check_python_version() -> None:
    """Validate the active Python interpreter version.

    Raises:
        RuntimeError: If the interpreter version is not supported.
    """
    current_version = sys.version_info[:2]
    if current_version < MIN_PYTHON_VERSION:
        expected = ".".join(str(part) for part in MIN_PYTHON_VERSION)
        current = ".".join(str(part) for part in current_version)
        msg = f"Python {expected}+ is required. Current version: {current}."
        raise RuntimeError(msg)


def import_module(module_name: str) -> ModuleType:
    """Import a module and wrap errors with a clearer message.

    Args:
        module_name: Module name to import.

    Returns:
        Imported Python module.

    Raises:
        RuntimeError: If the module cannot be imported.
    """
    try:
        return importlib.import_module(module_name)
    except ImportError as exc:
        msg = f"Required dependency '{module_name}' could not be imported."
        raise RuntimeError(msg) from exc


def check_dependencies() -> None:
    """Validate that main runtime dependencies can be imported."""
    for module_name in MAIN_DEPENDENCIES:
        import_module(module_name)


def check_package_import() -> None:
    """Validate that the main project package can be imported."""
    import_module("recommender_system")


def check_settings() -> None:
    """Validate that settings load and contain required values.

    Raises:
        RuntimeError: If settings are inconsistent.
    """
    from recommender_system.config.settings import Settings

    settings = Settings()
    if not isinstance(settings.random_seed, int):
        msg = "RANDOM_SEED must be loaded as an integer."
        raise RuntimeError(msg)

    for directory in settings.expected_directories:
        directory.mkdir(parents=True, exist_ok=True)
        if not directory.is_dir():
            msg = f"Expected directory is not available: {directory}"
            raise RuntimeError(msg)


def run_checks() -> list[str]:
    """Run all environment checks.

    Returns:
        Human-readable success messages for completed checks.
    """
    checks = (
        ("Python version is supported", check_python_version),
        ("Runtime dependencies import correctly", check_dependencies),
        ("Package recommender_system imports correctly", check_package_import),
        ("Settings load and directories are available", check_settings),
    )
    messages: list[str] = []
    for message, check in checks:
        check()
        messages.append(message)
    return messages


def main() -> int:
    """Run the environment validation command.

    Returns:
        Process exit code. Zero means success; non-zero means validation failed.
    """
    configure_import_path()
    try:
        messages = run_checks()
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    for message in messages:
        print(f"[OK] {message}")
    print("[OK] Environment is ready for development.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
