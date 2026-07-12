import pandas as pd


class PopularityRecommender:
    """Recommend globally popular items from historical interactions."""

    def __init__(
        self,
        item_column: str = "item_id",
        interaction_weight_column: str | None = None,
    ) -> None:
        """Initialize the popularity recommender.

        Args:
            item_column: Column containing item identifiers.
            interaction_weight_column: Optional column with interaction weights.
        """
        self.item_column = item_column
        self.interaction_weight_column = interaction_weight_column
        self._ranked_items: list[str] = []

    def fit(self, interactions: pd.DataFrame) -> None:
        """Rank items by interaction frequency or total interaction weight.

        Args:
            interactions: DataFrame containing user-item interactions.

        Raises:
            ValueError: If required columns are missing.
        """
        self._validate_columns(interactions)

        if self.interaction_weight_column is None:
            item_scores = interactions[self.item_column].value_counts()
        else:
            item_scores = interactions.groupby(self.item_column)[
                self.interaction_weight_column
            ].sum()

        ranked_index = item_scores.sort_values(ascending=False).index
        self._ranked_items = [str(item_id) for item_id in ranked_index]

    def recommend(self, user_id: str, top_k: int) -> list[str]:
        """Return the most popular items.

        Args:
            user_id: User identifier. The popularity baseline does not
                personalize recommendations yet.
            top_k: Maximum number of recommendations.

        Returns:
            Ordered list of recommended item identifiers.

        Raises:
            ValueError: If top_k is less than one.
        """
        if top_k < 1:
            raise ValueError("top_k must be greater than zero.")

        return self._ranked_items[:top_k]

    def _validate_columns(self, interactions: pd.DataFrame) -> None:
        """Validate that required model columns are present.

        Args:
            interactions: DataFrame containing user-item interactions.

        Raises:
            ValueError: If the item or weight columns are missing.
        """
        required_columns = {self.item_column}
        if self.interaction_weight_column is not None:
            required_columns.add(self.interaction_weight_column)

        missing_columns = required_columns.difference(interactions.columns)
        if missing_columns:
            sorted_columns = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required columns: {sorted_columns}")
