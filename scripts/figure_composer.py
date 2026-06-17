"""
figure_composer.py — CUMCM 组合图引擎
4种组合模式：main+zoom / line+bar / heatmap+marginal / radar+bubble
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from plot_config import PALETTES, save_figure, add_panel_label, figsize_for


def main_plus_zoom(fig_spec, filepath_base):
    """主图+局部放大子图"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    x_main = data.get("x_main", [])
    y_main = data.get("y_main", [])
    zoom_x = data.get("zoom_x", [])
    zoom_y = data.get("zoom_y", [])
    zoom_range = data.get("zoom_range", {})  # {"x_min":, "x_max":, "y_min":, "y_max":}
    title = fig_spec.get("core_argument", "")

    fig = plt.figure(figsize=(14/2.54, 7/2.54))
    ax_main = plt.subplot(1, 2, 1)
    ax_zoom = plt.subplot(1, 2, 2)

    ax_main.plot(x_main, y_main, 'o-', color=PALETTES["contrast_3"][0], markersize=3, linewidth=1.2)
    ax_main.set_title("完整区间", fontsize=9)
    add_panel_label(ax_main, 'a')

    ax_zoom.plot(zoom_x, zoom_y, 'o-', color=PALETTES["contrast_3"][1], markersize=5, linewidth=1.5)
    if zoom_range:
        ax_zoom.set_xlim(zoom_range.get("x_min", min(zoom_x)), zoom_range.get("x_max", max(zoom_x)))
        ax_zoom.set_ylim(zoom_range.get("y_min", min(zoom_y)), zoom_range.get("y_max", max(zoom_y)))
    ax_zoom.set_title("局部放大", fontsize=9)
    add_panel_label(ax_zoom, 'b')

    fig.suptitle(title, fontweight='bold', fontsize=10)
    save_figure(fig, filepath_base)


def line_plus_bar(fig_spec, filepath_base):
    """折线+柱状双y轴"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    x = data.get("x_values", [])
    line_y = data.get("line_y", [])
    bar_y = data.get("bar_y", [])
    line_label = data.get("line_label", "趋势")
    bar_label = data.get("bar_label", "数值")
    title = fig_spec.get("core_argument", "")

    fig, ax1 = plt.subplots(figsize=figsize_for(16, 0.5))
    ax2 = ax1.twinx()

    ax1.bar(x, bar_y, alpha=0.3, color=PALETTES["pastel_family"][2], label=bar_label, edgecolor='white')
    ax2.plot(x, line_y, 'o-', color=PALETTES["contrast_3"][0], label=line_label, markersize=4, linewidth=1.5)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1+lines2, labels1+labels2, loc='upper left')

    ax1.set_title(title, fontweight='bold')
    save_figure(fig, filepath_base)


def heatmap_plus_marginal(fig_spec, filepath_base):
    """热力图+边际趋势"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    matrix = np.array(data.get("matrix", []))
    row_labels = data.get("row_labels", [])
    col_labels = data.get("col_labels", [])
    title = fig_spec.get("core_argument", "")

    if matrix.size == 0:
        return

    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=figsize_for(16, 0.6))
    gs = GridSpec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4])

    ax_heat = fig.add_subplot(gs[1, 0])
    ax_right = fig.add_subplot(gs[1, 1])
    ax_top = fig.add_subplot(gs[0, 0])

    im = ax_heat.imshow(matrix, cmap='RdBu_r', aspect='auto')
    ax_right.plot(np.mean(matrix, axis=1), range(len(row_labels)), 'k-', linewidth=1)
    ax_right.set_ylim(len(row_labels)-0.5, -0.5)
    ax_top.plot(np.mean(matrix, axis=0), 'k-', linewidth=1)
    ax_top.set_xlim(0, len(col_labels)-0.5)

    ax_heat.set_xticks(range(len(col_labels))); ax_heat.set_xticklabels(col_labels, rotation=45, ha='right', fontsize=7)
    ax_heat.set_yticks(range(len(row_labels))); ax_heat.set_yticklabels(row_labels, fontsize=7)

    fig.colorbar(im, ax=ax_right, location='right')
    fig.suptitle(title, fontweight='bold', fontsize=10)
    save_figure(fig, filepath_base)


def radar_plus_bubble(fig_spec, filepath_base):
    """雷达图+气泡图（略——雷达图实现较复杂，作为高级选项）"""
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.5))
    ax.text(0.5, 0.5, "[radar+bubble]\n雷达图+气泡图组合\n需要 polar projection + scatter",
            transform=ax.transAxes, ha='center', va='center', fontsize=10, color='#999999')
    ax.set_title(fig_spec.get("core_argument", ""), fontweight='bold')
    save_figure(fig, filepath_base)


if __name__ == "__main__":
    print("figure_composer.py — 组合图引擎")
    print("可用函数: main_plus_zoom / line_plus_bar / heatmap_plus_marginal / radar_plus_bubble")
