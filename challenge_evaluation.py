"""Shared evaluation helpers for Roman lens challenge notebooks."""

import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt


def snr_stratified_sample(snr_values, n_show):
    """Select indices spanning the measured SNR range from low to high."""
    order = np.argsort(snr_values)
    pick_positions = np.linspace(0, len(order) - 1, n_show).round().astype(int)
    return order[pick_positions]


def get_worst_predictions(
    predictions,
    truths,
    source_indices,
    n_worst=25,
    *,
    position_column="test_pos",
    index_column="orig_idx",
):
    """Return a table of the largest absolute errors and their source indices."""
    abs_errors = np.abs(predictions - truths)
    worst_order = np.argsort(abs_errors)[::-1][:n_worst]
    return pd.DataFrame(
        {
            position_column: worst_order,
            index_column: source_indices[worst_order],
            "pred": predictions[worst_order],
            "truth": truths[worst_order],
            "abs_error": abs_errors[worst_order],
            "signed_error": (predictions - truths)[worst_order],
        }
    )


def attach_physical_properties(worst_df, labels, snr_values=None, system_names=None):
    """Add label-indexed radius, SNR, and system names to worst-error rows."""
    indices = worst_df["orig_idx"].values
    worst_df["theta_e_true"] = labels[indices]
    if snr_values is not None:
        worst_df["snr"] = snr_values[indices]
    if system_names is not None:
        worst_df["system_name"] = system_names[indices]
    worst_df["pct_error"] = 100 * worst_df["abs_error"] / worst_df["truth"]
    return worst_df


def print_worst_summary(worst_df, n_show=25):
    """Print a compact summary of the highest-error predictions."""
    priority_columns = [
        "system_name", "orig_idx", "truth", "pred", "abs_error", "pct_error",
        "theta_e_true", "snr",
    ]
    columns = [name for name in priority_columns if name in worst_df.columns]
    columns.extend(
        name for name in worst_df.columns
        if name not in columns and name not in ("test_pos", "signed_error")
    )
    print(f"\n── Worst {n_show} Predictions by Absolute Error ───────────────────────")
    print(worst_df[columns].head(n_show).to_string(index=False, float_format="%.4f"))
    if "theta_e_true" in worst_df.columns:
        values = worst_df["theta_e_true"].head(n_show)
        print(f"\nWorst-{n_show} theta_e stats:")
        print(
            f"  mean={values.mean():.3f}  median={values.median():.3f}  "
            f"min={values.min():.3f}  max={values.max():.3f}"
        )


def plot_worst_images(worst_df, rgb_previews, n_show=12, cols=3, panel_size=5):
    """Show RGB previews for the highest-error predictions."""
    n_show = min(n_show, len(worst_df))
    rows = int(np.ceil(n_show / cols))
    figure, axes = plt.subplots(
        rows, cols, figsize=(panel_size * cols, panel_size * rows)
    )
    axes = np.atleast_1d(axes).flatten()
    for index, (_, row) in enumerate(worst_df.head(n_show).iterrows()):
        original_index = int(row["orig_idx"])
        snr_text = f"  snr={row['snr']:.1f}" if "snr" in worst_df.columns else ""
        error_text = f"  err={row['pct_error']:.1f}%" if "pct_error" in worst_df.columns else ""
        axes[index].imshow(rgb_previews[original_index])
        axes[index].axis("off")
        axes[index].set_title(
            f"pred={row['pred']:.3f}\"  true={row['truth']:.3f}\"{error_text}{snr_text}",
            fontsize=10,
        )
    for axis in axes[n_show:]:
        axis.axis("off")
    figure.suptitle("Worst Predictions – Combined Lupton RGB (F158/F129/F106)", fontsize=14, y=1.01)
    figure.tight_layout()
    plt.show()


def run_two_stage_pipeline(
    images_tensor,
    classifier,
    regressor,
    device,
    threshold=0.5,
    batch_size=256,
):
    """Classify image batches and regress only the images predicted as lenses."""
    classifier.eval()
    regressor.eval()
    all_is_lens = []
    all_theta_e = []
    with torch.no_grad():
        for start in range(0, len(images_tensor), batch_size):
            batch = images_tensor[start:start + batch_size].to(device)
            probabilities = torch.sigmoid(classifier(batch))
            pred_is_lens = (probabilities > threshold).float()
            pred_theta_e = torch.full((len(batch),), float("nan"), device=device)
            lens_mask = pred_is_lens == 1
            if lens_mask.any():
                pred_theta_e[lens_mask] = regressor(batch[lens_mask])
            all_is_lens.append(pred_is_lens.cpu().numpy())
            all_theta_e.append(pred_theta_e.cpu().numpy())
    return np.concatenate(all_is_lens), np.concatenate(all_theta_e)