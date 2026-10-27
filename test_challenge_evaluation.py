import numpy as np
import torch
import matplotlib.pyplot as plt

from challenge_evaluation import (
    attach_physical_properties,
    get_worst_predictions,
    plot_worst_images,
    print_worst_summary,
    run_two_stage_pipeline,
    snr_stratified_sample,
)


def test_snr_stratified_sample_spans_snr_order():
    np.testing.assert_array_equal(
        snr_stratified_sample(np.array([100.0, 10.0, 50.0, 20.0]), 3),
        [1, 2, 0],
    )


def test_get_worst_predictions_preserves_order_and_supports_holdout_ids():
    predictions = np.array([0.2, 0.1, 1.4])  # [arcsec]
    truths = np.array([0.0, 0.7, 1.0])  # [arcsec]
    indices = np.array([10, 11, 12])

    result = get_worst_predictions(predictions, truths, indices)
    assert list(result.columns) == [
        "test_pos", "orig_idx", "pred", "truth", "abs_error", "signed_error"
    ]
    np.testing.assert_array_equal(result["test_pos"], [1, 2, 0])
    np.testing.assert_array_equal(result["orig_idx"], [11, 12, 10])

    holdout = get_worst_predictions(
        predictions, truths, np.array([1001, 1002, 1003]),
        position_column="holdout_pos", index_column="uid",
    )
    assert "holdout_pos" in holdout and "uid" in holdout
    assert "test_pos" not in holdout and "orig_idx" not in holdout


def test_attach_physical_properties_aligns_by_original_index():
    worst = get_worst_predictions(
        np.array([0.8, 1.1]), np.array([1.0, 1.0]), np.array([1, 0])  # [arcsec]
    )
    result = attach_physical_properties(
        worst,
        labels=np.array([1.0, 2.0]),  # [arcsec]
        snr_values=np.array([30.0, 10.0]),
        system_names=np.array(["second", "first"]),
    )
    assert result is worst
    np.testing.assert_array_equal(result["theta_e_true"], [2.0, 1.0])
    np.testing.assert_array_equal(result["snr"], [10.0, 30.0])
    assert result["system_name"].tolist() == ["first", "second"]
    np.testing.assert_allclose(result["pct_error"], [20.0, 10.0])


def test_print_worst_summary_includes_system_names(capsys):
    worst = get_worst_predictions(
        np.array([1.2]), np.array([1.0]), np.array([3])  # [arcsec]
    )
    worst["system_name"] = ["lens-3"]

    print_worst_summary(worst, n_show=1)

    assert "lens-3" in capsys.readouterr().out


def test_plot_worst_images_uses_indexed_previews_and_hides_empty_axes(monkeypatch):
    worst = get_worst_predictions(
        np.array([0.8, 1.1]), np.array([1.0, 1.0]), np.array([1, 0])  # [arcsec]
    )
    previews = np.zeros((2, 4, 4, 3), dtype=np.float32)
    figures = []
    monkeypatch.setattr(plt, "show", lambda: figures.append(plt.gcf()))

    plot_worst_images(worst, previews, n_show=2, cols=3)

    assert len(figures) == 1
    assert len(figures[0].axes) == 3
    assert figures[0].axes[0].get_title().startswith('pred=0.800')
    assert not figures[0].axes[2].axison
    plt.close(figures[0])


def test_two_stage_pipeline_batches_and_regresses_only_predicted_lenses():
    class Classifier:
        def __init__(self):
            self.evaluated = False

        def eval(self):
            self.evaluated = True

        def __call__(self, batch):
            return batch[:, 0, 0, 0]

    class Regressor:
        def __init__(self):
            self.evaluated = False
            self.batch_sizes = []

        def eval(self):
            self.evaluated = True

        def __call__(self, batch):
            self.batch_sizes.append(len(batch))
            return 10.0 * batch[:, 0, 0, 0]

    images = torch.tensor([-1.0, 1.0, 0.0, 2.0, -2.0]).reshape(5, 1, 1, 1)
    classifier = Classifier()
    regressor = Regressor()

    predicted_lenses, predicted_radii = run_two_stage_pipeline(
        images, classifier, regressor, "cpu", batch_size=2
    )

    np.testing.assert_array_equal(predicted_lenses, [0.0, 1.0, 0.0, 1.0, 0.0])
    np.testing.assert_allclose(predicted_radii[[1, 3]], [10.0, 20.0])  # [arcsec]
    assert np.isnan(predicted_radii[[0, 2, 4]]).all()
    assert classifier.evaluated and regressor.evaluated
    assert regressor.batch_sizes == [1, 1]