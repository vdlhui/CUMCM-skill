# CUMCM Matplotlib 运行时配置

以下代码片段必须在每个 Python 绘图脚本的开头执行。

```python
import matplotlib
matplotlib.use('Agg')  # 无头渲染，服务器环境必需

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ===== 中文字体自动检测 =====
def detect_chinese_font():
    import matplotlib.font_manager as fm
    candidates = ['SimHei', 'Microsoft YaHei', 'SimSun', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC']
    available = {f.name for f in fm.fontManager.ttflist}
    for c in candidates:
        if c in available:
            return c
    return 'sans-serif'  # 降级

CN_FONT = detect_chinese_font()

# ===== 全局 rcParams =====
plt.rcParams.update({
    # 字体
    'font.family':         'sans-serif',
    'font.sans-serif':     [CN_FONT, 'Arial', 'Helvetica', 'DejaVu Sans', 'sans-serif'],
    'font.size':           9,           # 基准字号（其他字号相对此缩放）
    'axes.titlesize':      10,          # 图标题
    'axes.labelsize':      9,           # 轴标签
    'xtick.labelsize':     8,           # 刻度
    'ytick.labelsize':     8,
    'legend.fontsize':     8,

    # 坐标轴
    'axes.spines.right':   False,       # 右脊线关闭
    'axes.spines.top':     False,       # 上脊线关闭
    'axes.linewidth':      0.8,
    'xtick.major.width':   0.6,
    'ytick.major.width':   0.6,
    'xtick.major.size':    3.5,
    'ytick.major.size':    3.5,

    # 网格
    'axes.grid':           False,       # 默认无网格
    'grid.alpha':          0.3,

    # 图例
    'legend.frameon':      False,       # 无图例边框
    'legend.handlelength': 1.5,
    'legend.handleheight': 0.7,
    'legend.borderpad':    0.4,

    # 导出
    'savefig.dpi':         300,
    'savefig.bbox':        'tight',
    'savefig.pad_inches':  0.05,
    'savefig.format':      'png',

    # PDF 可编辑文字
    'pdf.fonttype':        42,
    'ps.fonttype':          42,

    # 数学公式（仅在需要时启用，增加渲染时间）
    'text.usetex':         False,
})

# ===== CUMCM 5套调色板 =====
PALETTES = {
    "contrast_3":   ["#2878B5", "#9AC9DB", "#C82423"],                     # 通用对比（2-3组）
    "gradient_6":   ["#8ECFC9","#FFBE7A","#FA7F6F","#82B0D2","#BEB8DC","#E7DAD2"], # 多组渐变
    "directional":  {"positive":"#2E7D32", "negative":"#C62828", "neutral":"#78909C"},
    "spatial":      "viridis",                                              # 地理/空间
    "pastel_family": ["#1565C0","#1976D2","#1E88E5","#42A5F5","#90CAF9"],  # 同色系深浅
    "hero_highlight": {"hero":"#1565C0", "compare":"#FF8F00", "other":"#B0BEC5"},
}

# ===== 出版物级保存函数 =====
def save_figure(fig, filepath_base, dpi=300, formats=('png','pdf')):
    """
    保存图表为指定格式。
    filepath_base: 不含扩展名的路径（如 'figures/fig_01'）
    formats: 输出格式元组
    """
    import os
    os.makedirs(os.path.dirname(filepath_base) or '.', exist_ok=True)
    for fmt in formats:
        path = f"{filepath_base}.{fmt}"
        kwargs = {'dpi': dpi} if fmt == 'png' else {}
        fig.savefig(path, **kwargs)
    plt.close(fig)

# ===== 色盲检测辅助函数 =====
def grayscale_test(hex_color):
    """返回颜色的灰度感知亮度（0-255）"""
    r, g, b = int(hex_color[1:3],16), int(hex_color[3:5],16), int(hex_color[5:7],16)
    return 0.299*r + 0.587*g + 0.114*b

def is_grayscale_distinguishable(colors):
    """检查一组颜色在灰度下是否可区分（相邻两色亮度差≥30）"""
    grays = [grayscale_test(c) for c in colors]
    for i in range(len(grays)-1):
        if abs(grays[i] - grays[i+1]) < 30:
            return False
    return True

# ===== 面板标签 =====
def add_panel_label(ax, label, x=-0.08, y=1.05, fontweight='bold', fontsize=10):
    """在子图左上角添加 (a) (b) (c) 标签"""
    ax.text(x, y, f'({label})', transform=ax.transAxes,
            fontweight=fontweight, fontsize=fontsize, va='bottom', ha='left')

# ===== 图例优化 =====
def add_legend_outside(ax, loc='upper left', bbox_to_anchor=(1.02, 1)):
    """将图例放在图外右侧"""
    ax.legend(loc=loc, bbox_to_anchor=bbox_to_anchor)
