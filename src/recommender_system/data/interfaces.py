from typing import Protocol

import pandas as pd


class PreprocessingStrategy(Protocol):
    """Contract for data preprocessing strategies."""

    def transform(self, interactions: pd.DataFrame) -> pd.DataFrame:
        """Transform interaction data.

        Args:
            interactions: DataFrame containing user-item interactions.

        Returns:
            Transformed DataFrame ready for the next pipeline stage.
        """
