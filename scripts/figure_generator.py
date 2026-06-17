"""
figure_generator.py — CUMCM 图表生成入口
读取 figure_placement_plan.json → 按 chart_type 分发 → 生成 → QA
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from plot_config import (PALETTES, save_figure, add_panel_label, add_legend_outside,
                          add_significance_bracket, mark_optimal, figsize_for, CN_FONT)

DATA_DIR = "paper_output/results"
OUTPUT_DIR = "paper_output/figures"


def load_placement_plan(path="paper_output/plan/figure_placement_plan.json"):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_data(source_path, json_path):
    """从 P4 JSON 文件中按路径提取数据"""
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for key in json_path.strip('.').split('.'):
        if '[' in key:
            key, idx = key.split('[')
            idx = int(idx.strip(']'))
            data = data[key][idx]
        elif key:
            data = data.get(key, data)
    return data


def generate_all(plan_path="paper_output/plan/figure_placement_plan.json"):
    """逐张生成全部图表"""
    plan = load_placement_plan(plan_path)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    index_entries = []
    qa_log = []

    for fig_spec in plan.get("figures", []):
        result = generate_one(fig_spec)
        if result:
            index_entries.append(result["index_entry"])
            qa_log.extend(result.get("qa", []))

    # 输出 figure_index.json
    index = {"figures": index_entries, "total": len(index_entries)}
    with open(os.path.join(OUTPUT_DIR, "figure_index.json"), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    # 输出 QA 日志
    with open(os.path.join(OUTPUT_DIR, "_qa_log.json"), 'w', encoding='utf-8') as f:
        json.dump(qa_log, f, ensure_ascii=False, indent=2)

    print(f"图表生成完成: {len(index_entries)} 张 → {OUTPUT_DIR}/")
    return index


def generate_one(fig_spec):
    """生成单张图表"""
    fig_id = fig_spec.get("id", "fig_unknown")
    chart_spec = fig_spec.get("chart_spec", {})
    chart_type = chart_spec.get("chart_type", "grouped_bar")
    caption = fig_spec.get("caption", "")
    width_cm = chart_spec.get("dimensions", "double_column(16cm)")
    width = 16 if "16" in str(width_cm) else 8

    filepath_base = os.path.join(OUTPUT_DIR, fig_id)
    qa = []

    try:
        if chart_type == "grouped_bar":
            _draw_grouped_bar(fig_spec, width, filepath_base)
        elif chart_type == "ranked_bar":
            _draw_ranked_bar(fig_spec, width, filepath_base)
        elif chart_type == "trend_line":
            _draw_trend_line(fig_spec, width, filepath_base)
        elif chart_type == "scatter_corr":
            _draw_scatter_corr(fig_spec, width, filepath_base)
        elif chart_type == "sensitivity_dual":
            _draw_sensitivity_dual(fig_spec, width, filepath_base)
        elif chart_type == "gap_annotated":
            _draw_gap_annotated(fig_spec, width, filepath_base)
        elif chart_type in ("heatmap", "stacked_area", "residual_diagnosis",
                           "convergence_curve", "pareto_front", "network_relation",
                           "waterfall", "solution_heatmap", "bifurcation",
                           "phase_trajectory", "subplot_comparison"):
            _draw_placeholder(fig_spec, width, filepath_base, chart_type)
        else:
            _draw_placeholder(fig_spec, width, filepath_base, chart_type)

        index_entry = {
            "id": fig_id,
            "file_png": f"figures/{fig_id}.png",
            "file_pdf": f"figures/{fig_id}.pdf",
            "caption": caption,
            "width_cm": width,
            "category": fig_spec.get("category", "data_result")
        }
        return {"index_entry": index_entry, "qa": qa}
    except Exception as e:
        print(f"  [FAIL] {fig_id}: {e}")
        return None


def _get_palette(fig_spec):
    palette_name = fig_spec.get("chart_spec", {}).get("palette", "contrast_3")
    p = PALETTES.get(palette_name, PALETTES["contrast_3"])
    if isinstance(p, dict):
        return p
    return p


def _draw_grouped_bar(fig_spec, width_cm, filepath_base):
    """分组柱状图"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    x_cats = data.get("x_categories", [])
    y_series = data.get("y_values", {})
    title = fig_spec.get("core_argument", "")

    if not x_cats or not y_series:
        print("  [WARN] grouped_bar: no data, using placeholder")
        return _draw_placeholder(fig_spec, width_cm, filepath_base, "grouped_bar")

    palette = _get_palette(fig_spec)
    n_series = len(y_series)
    n_cats = len(x_cats)

    fig, ax = plt.subplots(figsize=figsize_for(width_cm, 0.55))
    x = np.arange(n_cats)
    bar_w = 0.8 / n_series

    series_names = list(y_series.keys())
    for i, (sname, svalues) in enumerate(y_series.items()):
        color = palette[i % len(palette)] if isinstance(palette, list) else list(palette.values())[i % len(palette)]
        ax.bar(x + (i - (n_series-1)/2) * bar_w, svalues, bar_w,
               label=sname, color=color, edgecolor='white')

    ax.set_xticks(x)
    ax.set_xticklabels(x_cats, rotation=0)
    ax.set_title(title, fontweight='bold')
    if n_series > 1:
        ax.legend()
    ax.axhline(y=0, color='#888888', linestyle='--', linewidth=0.8)

    # 标注最优
    all_vals = [v for sv in y_series.values() for v in sv]
    if all_vals:
        best_val = max(all_vals) if max(all_vals) > abs(min(all_vals)) else min(all_vals)

    save_figure(fig, filepath_base)


def _draw_ranked_bar(fig_spec, width_cm, filepath_base):
    """水平排名柱状图"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    names = data.get("x_categories", [])
    values = data.get("y_values", {}).get("values", [])
    errors = data.get("error_bars", [])
    title = fig_spec.get("core_argument", "")

    if not names or not values:
        return _draw_placeholder(fig_spec, width_cm, filepath_base, "ranked_bar")

    # 按值降序排列
    sorted_idx = np.argsort(values)[::-1]
    names = [names[i] for i in sorted_idx]
    values = [values[i] for i in sorted_idx]
    if errors:
        errors = [errors[i] for i in sorted_idx]

    colors = [PALETTES["hero_highlight"]["hero"]] + [PALETTES["hero_highlight"]["other"]] * (len(names)-1)
    fig, ax = plt.subplots(figsize=figsize_for(width_cm, 0.55))
    bars = ax.barh(names, values, xerr=errors if errors else None,
                   color=colors, capsize=3, edgecolor='white')
    ax.set_title(title, fontweight='bold')
    for bar, v in zip(bars, values):
        ax.text(v + max(values)*0.02, bar.get_y()+bar.get_height()/2,
                f'{v:,.0f}', va='center', fontsize=7)
    save_figure(fig, filepath_base)


def _draw_trend_line(fig_spec, width_cm, filepath_base):
    """趋势折线图"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    title = fig_spec.get("core_argument", "")
    palette = _get_palette(fig_spec)
    x = data.get("x_values", [])
    y_series = data.get("y_series", {})

    if not x or not y_series:
        return _draw_placeholder(fig_spec, width_cm, filepath_base, "trend_line")

    fig, ax = plt.subplots(figsize=figsize_for(width_cm, 0.5))
    colors = palette if isinstance(palette, list) else list(palette.values())
    for i, (sname, sdata) in enumerate(y_series.items()):
        y = sdata.get("values", [])
        y_err = sdata.get("ci", None)
        color = colors[i % len(colors)]
        ax.plot(x, y, 'o-', color=color, label=sname, markersize=4, linewidth=1.5)
        if y_err:
            ax.fill_between(x, [a-b for a,b in zip(y,y_err)], [a+b for a,b in zip(y,y_err)],
                           alpha=0.15, color=color)
    ax.set_title(title, fontweight='bold')
    ax.legend()
    save_figure(fig, filepath_base)


def _draw_scatter_corr(fig_spec, width_cm, filepath_base):
    """散点+回归+ρ标注"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    x = data.get("x_values", [])
    y = data.get("y_values", [])
    rho = data.get("spearman_rho", None)
    p_val = data.get("p_value", None)
    title = fig_spec.get("core_argument", "")
    x_label = data.get("x_label", "X")
    y_label = data.get("y_label", "Y")

    if not x or not y:
        return _draw_placeholder(fig_spec, width_cm, filepath_base, "scatter_corr")

    fig, ax = plt.subplots(figsize=figsize_for(width_cm, 0.55))
    ax.scatter(x, y, alpha=0.6, c='#1565C0', edgecolors='white', s=40)

    # 回归线
    coeffs = np.polyfit(x, y, 1)
    x_line = np.linspace(min(x), max(x), 100)
    ax.plot(x_line, np.polyval(coeffs, x_line), '--', color='#C62828', linewidth=1.5)

    ax.set_xlabel(x_label); ax.set_ylabel(y_label)
    ax.set_title(title, fontweight='bold')

    # ρ标注框
    if rho is not None:
        text = f"Spearman ρ = {rho:.3f}"
        if p_val is not None:
            text += f"\np {'<' if p_val < 0.001 else '='} {p_val}"
        ax.text(0.05, 0.95, text, transform=ax.transAxes, fontsize=8,
                va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    save_figure(fig, filepath_base)


def _draw_sensitivity_dual(fig_spec, width_cm, filepath_base):
    """双面板敏感性分析"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    title = fig_spec.get("core_argument", "")
    panels = data.get("panels", [])
    if len(panels) < 2:
        return _draw_placeholder(fig_spec, width_cm, filepath_base, "sensitivity_dual")

    fig, axes = plt.subplots(1, 2, figsize=figsize_for(width_cm, 0.4))
    for i, (ax, panel) in enumerate(zip(axes, panels)):
        x = panel.get("x", []); y = panel.get("y", [])
        ax.plot(x, y, 'o-', color=PALETTES["contrast_3"][i], markersize=4, linewidth=1.5)
        ax.set_xlabel(panel.get("xlabel", "")); ax.set_ylabel(panel.get("ylabel", ""))
        ax.set_title(panel.get("title", ""), fontsize=9)
        add_panel_label(ax, chr(97+i))
    fig.suptitle(title, fontweight='bold', fontsize=10)
    save_figure(fig, filepath_base)


def _draw_gap_annotated(fig_spec, width_cm, filepath_base):
    """差距标注柱状图"""
    data = fig_spec.get("data_extraction", {}).get("extracted_values", {})
    scenarios = data.get("x_categories", [])
    values_a = data.get("values_a", [])  # DP最优
    values_b = data.get("values_b", [])  # 贪心
    gaps = data.get("gaps_pct", [])
    title = fig_spec.get("core_argument", "")
    if not scenarios:
        return _draw_placeholder(fig_spec, width_cm, filepath_base, "gap_annotated")

    fig, ax = plt.subplots(figsize=figsize_for(width_cm, 0.5))
    x = np.arange(len(scenarios))
    w = 0.3
    ax.bar(x - w/2, values_a, w, label='DP最优', color=PALETTES["contrast_3"][0], edgecolor='white')
    ax.bar(x + w/2, values_b, w, label='贪心', color='#FF8F00', edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(scenarios, fontsize=7)
    ax.set_title(title, fontweight='bold')
    ax.legend()

    for i, (va, vb, gap) in enumerate(zip(values_a, values_b, gaps)):
        ax.annotate(f'{gap:.1f}%', xy=(i, (va+vb)/2), ha='center', fontweight='bold', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4', alpha=0.9))
    save_figure(fig, filepath_base)


def _draw_placeholder(fig_spec, width_cm, filepath_base, chart_type="unknown"):
    """未实现图表类型的占位生成"""
    title = fig_spec.get("core_argument", f"Plot: {chart_type}")
    fig, ax = plt.subplots(figsize=figsize_for(width_cm, 0.5))
    ax.text(0.5, 0.5, f"[{chart_type}]\n具体实现待 P5c 数据填充后调用对应绘图函数",
            transform=ax.transAxes, ha='center', va='center', fontsize=10, color='#999999')
    ax.set_title(title, fontweight='bold')
    ax.set_xticks([]); ax.set_yticks([])
    save_figure(fig, filepath_base)
    print(f"  [PLACEHOLDER] {fig_spec.get('id','?')} ({chart_type})")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "paper_output/plan/figure_placement_plan.json"
    if os.path.exists(path):
        generate_all(path)
    else:
        print(f"figure_generator: {path} 不存在，跳过图表生成。")
