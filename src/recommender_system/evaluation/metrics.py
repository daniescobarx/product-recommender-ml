def precision_at_k(
    recommended_items: list[str],
    relevant_items: set[str],
    k: int,
) -> float:
    """Compute precision at K for one recommendation list.

    Args:
        recommended_items: Ordered recommended item identifiers.
        relevant_items: Set of item identifiers considered relevant.
        k: Evaluation cutoff.

    Returns:
        Precision at K score.

    Raises:
        ValueError: If k is less than one.
    """
    if k < 1:
        raise ValueError("k must be greater than zero.")

    if not recommended_items:
        return 0.0

    top_k_items = recommended_items[:k]
    hit_count = len(set(top_k_items).intersection(relevant_items))
    return hit_count / k
