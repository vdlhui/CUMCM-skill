---
name: cumcm-visualizer
description: CUMCM 图表生成。读取 P5c 输出的 figure_placement_plan.json，逐张生成符合国赛一等奖标准的插图（逻辑框架图+数据结果图）。输出 PNG(300DPI)+PDF 双格式到 figures/ 目录，并更新 figure_index.json。
---

# cumcm-visualizer：图表生成引擎

## 输入
- P5c 输出：`figure_placement_plan.json`（每张图的完整方案）

## 工作流

### 第 1 步：加载核心契约

```
1. 读取 static/core/contract.md   → 确认每张图满足7点契约
2. 读取 static/core/stance.md     → 加载视觉立场（配色/字体/标注策略）
3. 读取 static/fragments/backend/python.md → 加载 matplotlib rcParams
```

### 第 2 步：逐张生成

```
for each figure in figure_placement_plan.json:
  1. 确认 chart_type → 查 references/chart-types.md 找到对应模板
  2. 确认 data_extraction → 从 P4 输出文件提取 x/y/误差数据
  3. 确认 palette → 从 references/palette.md 加载对应配色
  4. 调用 scripts/figure_generator.py 或 scripts/figure_composer.py
  5. 生成 PNG(300DPI) + PDF 双格式 → 保存到 figures/
```

### 第 3 步：生成逻辑框架图

```
for each logical_framework_figure in figure_placement_plan.json:
  1. 根据 figure_type (flowchart/mechanism_diagram/mind_map/algorithm_flow)
  2. 调用 scripts/logical_figure_generator.py
  3. 生成简化版排版图 → 保存到 figures/
```

### 第 4 步：QA 自检

```
对每张生成的图，执行 references/qa-checklist.md 的 8 项检查：
  1. 核心论证：图标题包含一句结论（不是"关系图"）
  2. 自明性：不看正文，只看图+标题+轴标签能理解
  3. 误差/不确定度：所有柱/点/线含误差线或置信带
  4. 统计标注：关键对比标注显著性
  5. 中文可读：无豆腐块(□□□)，字体≥8pt
  6. 颜色功能：≤4色，灰度打印可分辨
  7. 导出完整：PNG(300DPI) + PDF 同时生成
  8. 数据可溯：文件名对应 P4 数据来源
```

### 第 5 步：输出 figure_index.json

```json
{
  "figures": [
    {
      "id": "fig_01",
      "file_png": "figures/fig_01.png",
      "file_pdf": "figures/fig_01.pdf",
      "caption": "图1：...",
      "width_cm": 16,
      "category": "data_result"
    }
  ]
}
```

## 输出

| 文件 | 格式 | 内容 |
|------|------|------|
| `figures/*.png` | PNG 300DPI | 每张图的光栅版本 |
| `figures/*.pdf` | PDF 矢量 | 每张图的矢量版本 |
| `figure_index.json` | JSON | 图表索引（ID/文件路径/图注/尺寸） |

## 不能做的事
- 不要跳过 QA 自检——每张图必须通过 8 项检查才能输出
- 不要在数据不足时"编造"图表——数据缺失应报告而非伪造
- 不要让图注写成"图X：关系图"——必须写结论性描述
- 不要超过 4 种颜色——克制是高级感的前提
- 不要生成无误差线的柱状图——凡有均值必带误差
