from typing import Protocol

import pandas as pd


class RecommenderModel(Protocol):
    """Contract for recommender models."""

    def fit(self, interactions: pd.DataFrame) -> None:
        """Fit the recommender using interaction data.

        Args:
            interactions: DataFrame containing user-item interactions.
        """

    def recommend(self, user_id: str, top_k: int) -> list[str]:
        """Generate product recommendations for a user.

        Args:
            user_id: User identifier.
            top_k: Maximum number of product recommendations.

        Returns:
            Ordered list of recommended item identifiers.
        """
