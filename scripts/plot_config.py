"""
plot_config.py — CUMCM 图表全局配置
中文字体自动检测 / 5套调色板 / 色盲与灰度检测 / 出版物级保存
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# ===== 中文字体自动检测 =====
def detect_chinese_font():
    candidates = ['SimHei', 'Microsoft YaHei', 'SimSun', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC']
    available = {f.name for f in fm.fontManager.ttflist}
    for c in candidates:
        if c in available:
            return c
    return 'sans-serif'

CN_FONT = detect_chinese_font()

# ===== 全局 rcParams =====
plt.rcParams.update({
    'font.family':         'sans-serif',
    'font.sans-serif':     [CN_FONT, 'Arial', 'Helvetica', 'DejaVu Sans', 'sans-serif'],
    'font.size':           9,
    'axes.titlesize':      10,
    'axes.labelsize':      9,
    'xtick.labelsize':     8,
    'ytick.labelsize':     8,
    'legend.fontsize':     8,
    'axes.spines.right':   False,
    'axes.spines.top':     False,
    'axes.linewidth':      0.8,
    'xtick.major.width':   0.6,
    'ytick.major.width':   0.6,
    'xtick.major.size':    3.5,
    'ytick.major.size':    3.5,
    'axes.grid':           False,
    'grid.alpha':          0.3,
    'legend.frameon':      False,
    'legend.handlelength': 1.5,
    'legend.handleheight': 0.7,
    'legend.borderpad':    0.4,
    'savefig.dpi':         300,
    'savefig.bbox':        'tight',
    'savefig.pad_inches':  0.05,
    'savefig.format':      'png',
    'pdf.fonttype':        42,
    'ps.fonttype':         42,
    'text.usetex':         False,
})

# ===== 五套调色板 =====
PALETTES = {
    "contrast_3":   ["#2878B5", "#9AC9DB", "#C82423"],
    "gradient_6":   ["#8ECFC9","#FFBE7A","#FA7F6F","#82B0D2","#BEB8DC","#E7DAD2"],
    "directional":  {"positive":"#2E7D32", "negative":"#C62828", "neutral":"#78909C"},
    "spatial":      "viridis",
    "pastel_family":["#1565C0","#1976D2","#1E88E5","#42A5F5","#90CAF9"],
    "hero_highlight":{"hero":"#1565C0", "compare":"#FF8F00", "other":"#B0BEC5"},
}

# ===== 出版物级保存 =====
def save_figure(fig, filepath_base, dpi=300, formats=('png','pdf')):
    os.makedirs(os.path.dirname(filepath_base) or '.', exist_ok=True)
    for fmt in formats:
        path = f"{filepath_base}.{fmt}"
        kwargs = {'dpi': dpi} if fmt == 'png' else {}
        fig.savefig(path, **kwargs)
    plt.close(fig)

# ===== 灰度检测 =====
def grayscale_test(hex_color):
    r, g, b = int(hex_color[1:3],16), int(hex_color[3:5],16), int(hex_color[5:7],16)
    return 0.299*r + 0.587*g + 0.114*b

def is_grayscale_distinguishable(colors):
    grays = sorted([grayscale_test(c) for c in colors])
    for i in range(len(grays)-1):
        if abs(grays[i] - grays[i+1]) < 30:
            return False
    return True

# ===== 面板标签 =====
def add_panel_label(ax, label, x=-0.06, y=1.02, fontweight='bold', fontsize=10):
    ax.text(x, y, f'({label})', transform=ax.transAxes,
            fontweight=fontweight, fontsize=fontsize, va='bottom', ha='left')

# ===== 图例外置 =====
def add_legend_outside(ax, loc='upper left', bbox_to_anchor=(1.02, 1)):
    ax.legend(loc=loc, bbox_to_anchor=bbox_to_anchor)

# ===== 显著性括号 =====
def add_significance_bracket(ax, x1, x2, y, text, h=0.02, color='#333333'):
    y_bracket = y + h * 3
    ax.plot([x1, x1, x2, x2], [y+h, y_bracket, y_bracket, y+h], color=color, linewidth=0.8)
    ax.text((x1+x2)/2, y_bracket+h*0.5, text, ha='center', fontsize=8, fontweight='bold')

# ===== 最优标注 =====
def mark_optimal(ax, x, y, text='最优', color='#1565C0'):
    ax.annotate(text, xy=(x, y), xytext=(x, y + abs(y)*0.15 if y > 0 else y - abs(y)*0.15),
                ha='center', fontsize=8, fontweight='bold', color=color,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

# ===== 图宽计算 =====
def figsize_for(width_cm, aspect_ratio=0.6):
    """返回 matplotlib figsize（英寸）。width_cm: 8(单栏)或16(双栏)"""
    w_inch = width_cm / 2.54
    h_inch = w_inch * aspect_ratio
    return (w_inch, h_inch)
