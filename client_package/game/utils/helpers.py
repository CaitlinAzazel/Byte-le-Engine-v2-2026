def clamp(value: int, minimum: int, maximum: int) -> int:
    return min(maximum, max(minimum, value))

def flip_dict[K, V](d: dict[K, V]) -> dict[V, K]:
    return {v: k for k, v in d.items()}
