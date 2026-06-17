"""
chart_atlas_builder.py — CUMCM 图表参考图集生成
一键生成 18 张参考图到 assets/chart-atlas/，供 cumcm-visualizer 查阅。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
import numpy as np
from plot_config import PALETTES, save_figure, figsize_for

OUTPUT_DIR = "assets/chart-atlas" if os.path.exists("assets") else ".opencode/skills/cumcm-visualizer/assets/chart-atlas"

def _ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_atlas():
    _ensure_dir()
    print(f"生成图表参考图集 → {OUTPUT_DIR}/")

    _atlas_grouped_bar()
    _atlas_ranked_bar()
    _atlas_trend_line()
    _atlas_scatter_corr()
    _atlas_sensitivity_dual()
    _atlas_gap_annotated()
    _atlas_flowchart()
    print(f"完成：7 张参考图（18种类型中的核心7种）")


def _atlas_grouped_bar():
    cats = ['方案A','方案B','方案C','方案D']
    v1 = [85, 72, 93, 68]
    v2 = [78, 65, 88, 70]
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.5))
    x = np.arange(4); w = 0.35
    ax.bar(x-w/2, v1, w, label='场景1', color=PALETTES["contrast_3"][0], edgecolor='white')
    ax.bar(x+w/2, v2, w, label='场景2', color=PALETTES["contrast_3"][1], edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(cats)
    ax.set_title('[参考] grouped_bar — 分组柱状图', fontsize=10)
    ax.legend()
    save_figure(fig, os.path.join(OUTPUT_DIR, "atlas-01-grouped-bar"))


def _atlas_ranked_bar():
    names = ['策略A','策略B','策略C','策略D','策略E']
    vals = [95, 88, 82, 71, 55]
    errors = [3, 4, 5, 4, 6]
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.45))
    colors = [PALETTES["hero_highlight"]["hero"]] + [PALETTES["hero_highlight"]["other"]]*4
    ax.barh(names, vals, xerr=errors, color=colors, capsize=3, edgecolor='white')
    ax.set_title('[参考] ranked_bar — 水平排名柱状图', fontsize=10)
    save_figure(fig, os.path.join(OUTPUT_DIR, "atlas-02-ranked-bar"))


def _atlas_trend_line():
    x = np.linspace(0, 10, 30)
    y1 = np.sin(x)*10 + x*5 + np.random.randn(30)*2
    y2 = np.sin(x)*8 + x*4.5 + np.random.randn(30)*2
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.45))
    ax.plot(x, y1, 'o-', color=PALETTES["contrast_3"][0], markersize=3, label='方法A', linewidth=1.2)
    ax.fill_between(x, y1-3, y1+3, alpha=0.12, color=PALETTES["contrast_3"][0])
    ax.plot(x, y2, 's-', color=PALETTES["contrast_3"][2], markersize=3, label='方法B', linewidth=1.2)
    ax.fill_between(x, y2-3, y2+3, alpha=0.12, color=PALETTES["contrast_3"][2])
    ax.set_title('[参考] trend_line — 折线+置信带', fontsize=10)
    ax.legend()
    save_figure(fig, os.path.join(OUTPUT_DIR, "atlas-03-trend-line"))


def _atlas_scatter_corr():
    np.random.seed(0)
    x = np.random.randn(50)*10 + 50
    y = x*0.7 + np.random.randn(50)*8 + 10
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.48))
    ax.scatter(x, y, alpha=0.6, c='#1565C0', edgecolors='white', s=40)
    coeffs = np.polyfit(x, y, 1)
    ax.plot(sorted(x), np.polyval(coeffs, sorted(x)), '--', color='#C62828', linewidth=1.5)
    rho = 0.85
    ax.text(0.05, 0.95, f"Spearman ρ = {rho:.3f}\np < 0.001", transform=ax.transAxes, fontsize=8,
            va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.set_title('[参考] scatter_corr — 散点+回归+ρ标注', fontsize=10)
    save_figure(fig, os.path.join(OUTPUT_DIR, "atlas-04-scatter-corr"))


def _atlas_sensitivity_dual():
    fig, axes = plt.subplots(1, 2, figsize=figsize_for(16, 0.38))
    m_x = [8, 12, 16, 20, 24]
    m_y = [14, 21, 28, 35, 42]
    t_x = [500, 1000, 1500, 2000, 2500, 3000]
    t_y = [7, 14, 21, 28, 35, 42]
    axes[0].plot(m_x, m_y, 'o-', color=PALETTES["contrast_3"][0], markersize=5, linewidth=1.5)
    axes[0].set_title('(a) 对 M 的敏感性', fontsize=9)
    axes[1].plot(t_x, t_y, 's-', color=PALETTES["contrast_3"][2], markersize=5, linewidth=1.5)
    axes[1].set_title('(b) 对 T 的敏感性', fontsize=9)
    fig.suptitle('[参考] sensitivity_dual — 双面板', fontweight='bold', fontsize=10)
    save_figure(fig, os.path.join(OUTPUT_DIR, "atlas-05-sensitivity-dual"))


def _atlas_gap_annotated():
    scenarios = ['场景1','场景2','场景3','场景4']
    a = [100, 200, 300, 400]
    b = [64, 118, 180, 245]
    gaps = [(x-y)/x*100 for x,y in zip(a,b)]
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.45))
    x = np.arange(4); w = 0.3
    ax.bar(x-w/2, a, w, label='DP最优', color=PALETTES["contrast_3"][0], edgecolor='white')
    ax.bar(x+w/2, b, w, label='贪心', color='#FF8F00', edgecolor='white')
    ax.set_xticks(x); ax.set_xticklabels(scenarios)
    ax.legend()
    for i, (va, vb, gap) in enumerate(zip(a, b, gaps)):
        ax.annotate(f'差距\n{gap:.0f}%', xy=(i, (va+vb)/2), ha='center', fontweight='bold', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4', alpha=0.9))
    ax.set_title('[参考] gap_annotated — 差距标注柱状图', fontsize=10)
    save_figure(fig, os.path.join(OUTPUT_DIR, "atlas-06-gap-annotated"))


def _atlas_flowchart():
    modules = [
        {"name": "P0 读题分析", "methods": ["赛题预处理"], "key_finding": "子问题·题型·套路"},
        {"name": "P1 模型选型", "methods": ["模型链搜索"], "key_finding": "三维评分·路线决策"},
        {"name": "P2 创新优化", "methods": ["创新模式匹配"], "key_finding": "公式链·可行性评估"},
        {"name": "P3 评审闸门", "methods": ["五维量化评审"], "key_finding": "回环路由·降级"},
        {"name": "P4 求解验证", "methods": ["脚手架·调参"], "key_finding": "证据契约·门禁"},
    ]
    n = len(modules)
    fig, ax = plt.subplots(figsize=figsize_for(16, 0.25*n+0.1))
    ax.set_xlim(0, 10); ax.set_ylim(0, n+1); ax.axis('off')
    ax.plot([5,5],[0.5,n+0.5], color='#888888', linewidth=2, zorder=0)
    colors = ["#1565C0","#2E7D32","#FF8F00","#6A1B9A","#C62828"]
    for i, mod in enumerate(modules):
        y = n - i
        c = colors[i]
        box = plt.Rectangle((3.5, y-0.35), 3, 0.7, facecolor=c, edgecolor='white', alpha=0.9)
        ax.add_patch(box)
        ax.text(5, y, mod["name"], ha='center', va='center', color='white', fontsize=9, fontweight='bold')
        if mod.get("methods"):
            ax.text(3.2, y, ", ".join(mod["methods"]), ha='right', va='center', fontsize=7, color='#555')
        if mod.get("key_finding"):
            ax.text(6.8, y, mod["key_finding"], ha='left', va='center', fontsize=7, color='#333', fontweight='bold')
        if i < n-1:
            ax.annotate('', xy=(5,y-0.4), xytext=(5,y-0.7), arrowprops=dict(arrowstyle='->', color='#888888', lw=2))
    ax.set_title('[参考] flowchart — 纵向主轴线技术路线图', fontweight='bold', fontsize=10, pad=10)
    save_figure(fig, os.path.join(OUTPUT_DIR, "atlas-07-flowchart"))


if __name__ == "__main__":
    build_atlas()
