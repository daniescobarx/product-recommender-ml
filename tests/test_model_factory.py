import pandas as pd
import pytest

from recommender_system.models.baselines import PopularityRecommender
from recommender_system.models.factory import ModelFactory


def test_model_factory_creates_popularity_recommender() -> None:
    model = ModelFactory.create("popularity")

    assert isinstance(model, PopularityRecommender)


def test_model_factory_rejects_unknown_model() -> None:
    with pytest.raises(ValueError, match="Unknown model"):
        ModelFactory.create("unknown")


def test_popularity_recommender_returns_ranked_items() -> None:
    interactions = pd.DataFrame(
        {
            "user_id": ["u1", "u2", "u3", "u4"],
            "item_id": ["i1", "i2", "i1", "i3"],
        }
    )
    model = ModelFactory.create("popularity")

    model.fit(interactions)

    assert model.recommend(user_id="u1", top_k=2) == ["i1", "i2"]
