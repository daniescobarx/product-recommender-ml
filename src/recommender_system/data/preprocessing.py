import pandas as pd

from recommender_system.data.interfaces import PreprocessingStrategy


class IdentityPreprocessingStrategy:
    """Preprocessing strategy that returns a defensive copy of the input data."""

    def transform(self, interactions: pd.DataFrame) -> pd.DataFrame:
        """Return interactions without changing their schema or values.

        Args:
            interactions: DataFrame containing user-item interactions.

        Returns:
            Copy of the input DataFrame.
        """
        return interactions.copy()


class RequiredColumnsPreprocessingStrategy:
    """Validate that interaction data contains the required columns."""

    def __init__(self, required_columns: set[str]) -> None:
        """Initialize the required-columns validation strategy.

        Args:
            required_columns: Columns that must exist in the interaction data.
        """
        self.required_columns = required_columns

    def transform(self, interactions: pd.DataFrame) -> pd.DataFrame:
        """Validate required columns and return a defensive copy.

        Args:
            interactions: DataFrame containing user-item interactions.

        Returns:
            Copy of the validated input DataFrame.

        Raises:
            ValueError: If one or more required columns are missing.
        """
        missing_columns = self.required_columns.difference(interactions.columns)
        if missing_columns:
            sorted_columns = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required columns: {sorted_columns}")

        return interactions.copy()


def apply_preprocessing(
    interactions: pd.DataFrame,
    strategy: PreprocessingStrategy,
) -> pd.DataFrame:
    """Apply a preprocessing strategy to interaction data.

    Args:
        interactions: DataFrame containing user-item interactions.
        strategy: Strategy responsible for transforming the data.

    Returns:
        Transformed DataFrame.
    """
    return strategy.transform(interactions)
