# CUMCM 图表教程

## 示例 1：分组柱状图（5种球对比）

**契约**：
- 核心论证：所有球种净收益为负，高级球亏损最小
- 类型：grouped_bar + contrast_3 配色
- 标注：最优✅标记 + 盈亏平衡虚线 + 柱顶数值

```python
from plot_config import PALETTES, save_figure, add_panel_label, CN_FONT
import matplotlib.pyplot as plt
import numpy as np

balls = ['高级球','属性球','补光球','国王球','棱镜球']
net = [-10200, -10200, -74000, -154000, -3194000]
colors = [PALETTES['hero_highlight']['hero'] if i==0 else PALETTES['hero_highlight']['other'] for i in range(5)]

fig, ax = plt.subplots(figsize=(16*0.5, 6*0.5))  # 双栏宽度
bars = ax.bar(balls, net, color=colors, edgecolor='white', width=0.6)
ax.axhline(y=0, color='#888888', linestyle='--', linewidth=0.8)
ax.set_ylabel('期望净收益 / 洛克贝')
ax.set_title('图1：基本情形下五种球的单次期望净收益', fontweight='bold')
# 标注最优
ax.annotate('最优\n-10,200', xy=(0, net[0]), xytext=(0.4, net[0]+50000),
            arrowprops=dict(arrowstyle='->', color='#1565C0'), fontsize=8, fontweight='bold', color='#1565C0')
plt.tight_layout()
save_figure(fig, 'figures/fig_01_bar_comparison')
```

---

## 示例 2：趋势折线图 + 置信带

```python
x = np.array([1,5,10,50,100,500,1000])
y = np.array(net) * x[:,None]  # N次净收益
# ... 省略数据准备 ...

fig, ax = plt.subplots(figsize=(16*0.5, 6*0.5))
for i, (name, color) in enumerate(zip(['高级球','补光球','国王球'], PALETTES['pastel_family'][:3])):
    ax.plot(x, y[:,i], 'o-', color=color, label=name, markersize=4, linewidth=1.5)
ax.set_xlabel('捕捉只数 N'); ax.set_ylabel('期望净收益 / 洛克贝')
ax.legend()
ax.set_title('图2：N只恶魔狼的期望净收益变化', fontweight='bold')
save_figure(fig, 'figures/fig_02_trend')
```

---

## 示例 3：排名水平柱状图 + 误差线

```python
fig, ax = plt.subplots(figsize=(16*0.5, 8*0.5))
names = ['国王球+高级球','国王球+属性球','国王球+补光球','国王球+国王球','补光球+属性球']
values = [281755, 282167, 280150, 272439, 57037]
errors = [2512, 2657, 2591, 2713, 3343]
colors = [PALETTES['hero_highlight']['hero']] + [PALETTES['hero_highlight']['other']]*4
bars = ax.barh(names, values, xerr=errors, color=colors, capsize=3, edgecolor='white')
ax.set_xlabel('长期平均净收益 / 洛克贝·次⁻¹')
ax.set_title('图4：25组球种组合策略排名（前5名+代表性的负收益策略）', fontweight='bold')
for bar, v in zip(bars, values):  # 柱端数值标注
    ax.text(v + max(values)*0.02, bar.get_y()+bar.get_height()/2, f'{v:,.0f}', va='center', fontsize=8)
save_figure(fig, 'figures/fig_03_rank')
```

---

## 示例 4：DP反例差距图（gap_annotated）

```python
scenarios = ['小资金\nM=200k,T=6','中等\nM=500k,T=8','大资金\nM=800k,T=10','充裕\nM=1M,T=15']
dp = [568116,1417408,2080856,2875569]
greedy = [361757,838107,1247948,1703298]
gaps = [(d-g)/d*100 for d,g in zip(dp,greedy)]

fig, ax = plt.subplots(figsize=(16*0.5, 6*0.5))
x = np.arange(4); w = 0.3
b1 = ax.bar(x-w/2, dp, w, label='DP精确最优', color='#1565C0', edgecolor='white')
b2 = ax.bar(x+w/2, greedy, w, label='贪心近似(95%CI)', color='#FF8F00', edgecolor='white')
# 标注差距百分比
for i,(d,g,gap) in enumerate(zip(dp,greedy,gaps)):
    ax.annotate(f'差距\n{gap:.1f}%', xy=(i, (d+g)/2), ha='center', fontweight='bold', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF9C4', alpha=0.9))
ax.set_xticks(x); ax.set_xticklabels(scenarios)
ax.legend(); ax.set_title('图6：DP反例——贪心策略与精确最优解的差距量化', fontweight='bold')
save_figure(fig, 'figures/fig_04_gap')
```
