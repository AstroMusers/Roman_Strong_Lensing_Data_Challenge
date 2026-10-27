import numpy as np
import pytest

from challenge_data import (
    attr_val,
    augment_dataset,
    get_bool_attr_val,
    get_filter_dataset,
    normalize,
)


def test_attr_val_unwraps_only_value_description_pairs():
    pair = np.array([1.5, "arcsec"], dtype=object)
    assert attr_val({"theta_e": pair}, "theta_e") == 1.5
    array = np.array([[1.5, 2.5]])
    assert attr_val({"other": array}, "other") is array


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (True, True),
        (np.bool_(False), False),
        (" TRUE ", True),
        ("1", True),
        (b"true", True),
        (b"\xff", False),
        ("false", False),
        (0, False),
    ],
)
def test_get_bool_attr_val_preserves_metadata_conversions(value, expected):
    assert get_bool_attr_val(value) is expected


def test_get_filter_dataset_requires_one_matching_name():
    first, second = object(), object()
    group = {"exposure_F158": first, "exposure_F106": second}
    assert get_filter_dataset(group, "F158") is first
    with pytest.raises(ValueError, match="exactly one"):
        get_filter_dataset(group, "F129")
    with pytest.raises(ValueError, match="exactly one"):
        get_filter_dataset({"one_F158": first, "two_F158": second}, "F158")


def test_normalize_preserves_shape_and_maps_constant_images_to_float32():
    image = np.array([[2, 4], [6, 8]], dtype=np.int16)
    original = image.copy()
    normalized = normalize(image)
    np.testing.assert_allclose(normalized, [[0.0, 1 / 3], [2 / 3, 1.0]])
    assert normalized.dtype == np.float32
    np.testing.assert_array_equal(image, original)
    np.testing.assert_array_equal(normalize(np.ones((2, 3))), np.zeros((2, 3)))


def test_augment_dataset_returns_eight_spatial_symmetries_with_aligned_labels():
    images = np.arange(12, dtype=np.float32).reshape(1, 3, 2, 2)
    labels = np.array([0.75])

    augmented_images, augmented_labels = augment_dataset(images, labels)

    expected = []
    for rotations in range(4):
        rotated = np.rot90(images[0], rotations, axes=(1, 2))
        expected.extend((rotated, np.flip(rotated, axis=2)))
    np.testing.assert_array_equal(augmented_images, expected)
    np.testing.assert_array_equal(augmented_labels, np.full(8, 0.75))
    assert augmented_images.dtype == np.float32
    assert augmented_labels.dtype == np.float32