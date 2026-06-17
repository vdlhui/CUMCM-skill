"""
logical_figure_generator.py — CUMCM 逻辑框架图生成
4种类型：技术路线图/模型机理图/问题分解思维导图/算法流程图
生成方式：TikZ 文字描述 + matplotlib 简化版排版图
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from plot_config import PALETTES, save_figure, figsize_for, CN_FONT


def draw_flowchart(modules, title, filepath_base):
    """纵向主轴线技术路线图"""
    n = len(modules)
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.22 * n + 0.1))
    ax.set_xlim(0, 10); ax.set_ylim(0, n + 1)
    ax.axis('off')

    # 主轴线
    ax.plot([5, 5], [0.5, n + 0.5], color='#888888', linewidth=2, zorder=0)

    colors = ["#1565C0", "#2E7D32", "#FF8F00", "#6A1B9A"]
    for i, mod in enumerate(modules):
        y = n - i
        color = colors[i % len(colors)]

        # 主模块框
        box = mpatches.FancyBboxPatch((3.5, y-0.35), 3, 0.7,
                                       boxstyle="round,pad=0.1", facecolor=color, edgecolor='white', alpha=0.9)
        ax.add_patch(box)
        ax.text(5, y, mod.get("name", f"模块{i+1}"), ha='center', va='center',
                color='white', fontsize=9, fontweight='bold')

        # 左侧方法
        methods = mod.get("methods", [])
        if methods:
            ax.text(3.2, y, ", ".join(methods), ha='right', va='center', fontsize=7, color='#555555')

        # 右侧发现
        finding = mod.get("key_finding", "")
        if finding:
            ax.text(6.8, y, finding, ha='left', va='center', fontsize=7, color='#333333', fontweight='bold')

        # 箭头（除最后一个）
        if i < n - 1:
            ax.annotate('', xy=(5, y-0.4), xytext=(5, y-0.7),
                        arrowprops=dict(arrowstyle='->', color='#888888', lw=2))

    ax.set_title(title, fontweight='bold', fontsize=11, pad=10)
    save_figure(fig, filepath_base)


def draw_mechanism_diagram(layers, title, filepath_base):
    """模型层级结构图"""
    n = len(layers)
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.3 * n + 0.1))
    ax.set_xlim(0, 10); ax.set_ylim(0, n + 1)
    ax.axis('off')

    colors = ["#1565C0", "#2E7D32", "#FF8F00", "#6A1B9A"]
    for i, layer in enumerate(layers):
        y = n - i
        color = colors[i % len(colors)]
        box = mpatches.FancyBboxPatch((1, y-0.3), 8, 0.6,
                                       boxstyle="round,pad=0.1", facecolor=color, edgecolor='white', alpha=0.85)
        ax.add_patch(box)
        ax.text(5, y, f"{layer.get('name','')}  {layer.get('desc','')}",
                ha='center', va='center', color='white', fontsize=9, fontweight='bold')

    ax.set_title(title, fontweight='bold', fontsize=11, pad=10)
    save_figure(fig, filepath_base)


def draw_mind_map(root, children, title, filepath_base):
    """简化思维导图（层级文本）"""
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.axis('off')

    # 根节点
    ax.text(1, 3, root, ha='center', va='center', fontsize=11, fontweight='bold', color='#1565C0',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2))

    for i, child in enumerate(children):
        y = 5 - i * 1.2
        ax.text(5, y, child.get("name", ""), ha='center', va='center', fontsize=9, fontweight='bold', color='white',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1565C0', alpha=0.85))
        # 子项
        sub_items = child.get("items", [])
        for j, sub in enumerate(sub_items):
            sx = 5 + 2.5 + (j - len(sub_items)/2 + 0.5) * 1.8
            ax.text(sx, y, sub, ha='center', va='center', fontsize=7, color='#333333',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#F5F5F5', edgecolor='#CCCCCC'))

    ax.set_title(title, fontweight='bold', fontsize=11, pad=10)
    save_figure(fig, filepath_base)


def generate_logical_figures(plan_path="paper_output/plan/figure_placement_plan.json"):
    """生成所有逻辑框架图"""
    import json
    if not os.path.exists(plan_path):
        print(f"logical_figure_generator: {plan_path} 不存在，跳过。")
        return
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    output_dir = "paper_output/figures"
    os.makedirs(output_dir, exist_ok=True)

    for fig_spec in plan.get("logical_framework_figures", []):
        fig_id = fig_spec.get("id", "fig_flow")
        figure_type = fig_spec.get("figure_type", "flowchart")
        title = fig_spec.get("core_argument", "")
        filepath_base = os.path.join(output_dir, fig_id)

        if figure_type == "flowchart":
            draw_flowchart(fig_spec.get("modules", []), title, filepath_base)
        elif figure_type == "mechanism_diagram":
            draw_mechanism_diagram(fig_spec.get("layers", []), title, filepath_base)
        elif figure_type == "mind_map":
            draw_mind_map(fig_spec.get("root", ""), fig_spec.get("children", []), title, filepath_base)
        elif figure_type == "algorithm_flow":
            modules = fig_spec.get("modules", [])
            draw_flowchart(modules, title, filepath_base)

        print(f"  [LOGICAL] {fig_id} → {filepath_base}.png/pdf")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "paper_output/plan/figure_placement_plan.json"
    generate_logical_figures(path)
