from collections.abc import Callable
from typing import Any

from recommender_system.models.baselines import PopularityRecommender
from recommender_system.models.interfaces import RecommenderModel

ModelBuilder = Callable[..., RecommenderModel]


class ModelFactory:
    """Factory responsible for creating recommender model instances."""

    _registry: dict[str, ModelBuilder] = {
        "popularity": PopularityRecommender,
    }

    @classmethod
    def create(cls, model_name: str, **kwargs: Any) -> RecommenderModel:
        """Create a recommender model by name.

        Args:
            model_name: Registered recommender model name.
            **kwargs: Model-specific initialization arguments.

        Returns:
            Recommender model instance.

        Raises:
            ValueError: If the requested model is not registered.
        """
        normalized_name = model_name.lower().strip()
        try:
            builder = cls._registry[normalized_name]
        except KeyError as error:
            available_models = ", ".join(sorted(cls._registry))
            raise ValueError(
                f"Unknown model '{model_name}'. Available models: {available_models}"
            ) from error

        return builder(**kwargs)

    @classmethod
    def register(cls, model_name: str, builder: ModelBuilder) -> None:
        """Register a model builder.

        Args:
            model_name: Name used to instantiate the model.
            builder: Callable that returns a recommender model.

        Raises:
            ValueError: If model_name is empty.
        """
        normalized_name = model_name.lower().strip()
        if not normalized_name:
            raise ValueError("model_name must not be empty.")

        cls._registry[normalized_name] = builder

    @classmethod
    def available_models(cls) -> tuple[str, ...]:
        """List registered model names.

        Returns:
            Sorted tuple with available model names.
        """
        return tuple(sorted(cls._registry))
