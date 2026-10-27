"""Shared readers and image transforms for the Roman lens challenge."""

import numpy as np


def attr_val(attrs, key):
    """Return the value from a value-description attribute pair."""
    value = attrs[key]
    if isinstance(value, np.ndarray) and value.shape == (2,):
        return value[0]
    return value


def get_bool_attr_val(raw_value):
    """Interpret boolean metadata stored as booleans, strings, or bytes."""
    if isinstance(raw_value, bytes):
        raw_value = raw_value.decode("utf-8", errors="replace")
    if isinstance(raw_value, str):
        return raw_value.strip().lower() in ("true", "1")
    return bool(raw_value)


def get_filter_dataset(group, filter_name):
    """Return the unique dataset whose name ends in the requested filter."""
    matches = [key for key in group.keys() if key.endswith(f"_{filter_name}")]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one key ending in _{filter_name}, found {matches}"
        )
    return group[matches[0]]


def normalize(image):
    """Scale one image to float32 in [0, 1], mapping constants to zero."""
    minimum, maximum = image.min(), image.max()
    if maximum - minimum == 0:
        return np.zeros_like(image, dtype=np.float32)
    return ((image - minimum) / (maximum - minimum)).astype(np.float32)


def augment_dataset(images, labels):
    """Return all eight rotations/reflections of channel-first images."""
    augmented_images = []
    augmented_labels = []
    for image, label in zip(images, labels):
        for rotations in range(4):
            rotated = np.rot90(image, rotations, axes=(1, 2))
            augmented_images.append(rotated.copy())
            augmented_labels.append(label)
            augmented_images.append(np.flip(rotated, axis=2).copy())
            augmented_labels.append(label)
    return (
        np.array(augmented_images, dtype=np.float32),
        np.array(augmented_labels, dtype=np.float32),
    )