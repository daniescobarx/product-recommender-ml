import pandas as pd
import pytest

from recommender_system.data.preprocessing import (
    IdentityPreprocessingStrategy,
    RequiredColumnsPreprocessingStrategy,
    apply_preprocessing,
)


def test_identity_preprocessing_returns_copy_with_same_values() -> None:
    interactions = pd.DataFrame({"user_id": ["u1"], "item_id": ["i1"]})
    strategy = IdentityPreprocessingStrategy()

    transformed = apply_preprocessing(interactions, strategy)

    assert transformed.equals(interactions)
    assert transformed is not interactions


def test_required_columns_strategy_accepts_valid_schema() -> None:
    interactions = pd.DataFrame({"user_id": ["u1"], "item_id": ["i1"]})
    strategy = RequiredColumnsPreprocessingStrategy({"user_id", "item_id"})

    transformed = strategy.transform(interactions)

    assert transformed.equals(interactions)


def test_required_columns_strategy_rejects_missing_columns() -> None:
    interactions = pd.DataFrame({"user_id": ["u1"]})
    strategy = RequiredColumnsPreprocessingStrategy({"user_id", "item_id"})

    with pytest.raises(ValueError, match="Missing required columns: item_id"):
        strategy.transform(interactions)
