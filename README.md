# CUMCM-skill — 数学建模竞赛论文生成系统

> **面向全国大学生数学建模竞赛（CUMCM）的 AI Agent 工作流。输入赛题，输出冲击国奖水平的完整论文。**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Platform](https://img.shields.io/badge/platform-OpenCode-green.svg)](https://opencode.ai)

---

## 关于作者

大家好，我是一名来自河南的普通双非大一本科生，目前正在备赛数学建模国赛。在准备过程中，我体会到一套系统的建模工作流对竞赛的帮助有多大，于是在学习 AI Agent 的过程中，边学边做了这个项目。

CUMCM-skill 还有很多不完善的地方，我会持续慢慢更新。如果你有任何想法、建议，或者想一起交流数学建模和 AI Agent，欢迎发邮件给我：**zhangjiahao@stu.qut.edu.cn**。

---

## 快速开始

```bash
# 把这个文件夹放到项目根目录（或全局 .opencode/ 下），然后直接说话：
帮我做这道题：[粘贴赛题]

# 或用斜杠命令
/cumcm [赛题文件路径]

# 全自动化模式
/cumcm auto [赛题文件路径]
```

**不需要记任何 @ 前缀或精确命令名。** 你只需要说"开始建模"，或直接把赛题扔进来——系统会自动识别并启动流水线。

---

## CUMCM-skill 是什么

一套完整的数学建模竞赛论文自动生成系统。它不像大多数建模 Agent 那样简单地"读题 → 推荐几个模型 → 写代码 → 写论文"，而是一个拥有**回环机制、模型评审闸门、叙事设计引擎和时间管理控制器**的工业级工作流。

**本质上是把数学建模竞赛指导老师的经验固化为可执行的 AI 流水线。**

---

## 九阶段流水线

```
[赛题] → P0 读题 → P1 选模 → P2 创新 → P3 评审 → P4 求解 → P5a 叙事 → P5b 纯文本写作 → P5c 插图方案 → [论文稿]

                               ↑回环             ↑修正回环          ↑失败诊断回环(三分支)
```

|  阶段   | 名称           | 核心职责                                                     |
| :-----: | -------------- | ------------------------------------------------------------ |
| **P0**  | 读题与数据处理 | 赛题多格式解析、子问题自动分解（Q1/Q2/Q3/Q4）、12 种赛题套路识别、数据自动清洗画像、隐含假设提取、外部数据获取 |
| **P1**  | 模型方向选型   | 80+ 模型目录 + 45 条模型链库 + 历年获奖成功率统计 + 决策树匹配 + 三维评分（预期得分×实现成本×风险）+ 排除"死亡组合" |
| **P2**  | 模型创新优化   | 22 种创新模式库（数据/模型结构/约束假设/求解算法/评价验证五大来源）+ 完整公式链推导 + 四维可行性评估 + 5 种反模式规避 |
| **P3**  | 模型评审闸门   | 五维量化评审（方向再审/创新可行性/完整覆盖性/可解性预判/数学验证）+ 红/黄/绿灯阈值判定 + 精确回环路由 + A/B/C/D 四级时间敏感降级 |
| **P4**  | 求解与代码     | 7 种任务类型脚手架自动分发 + auto-tuner 自动调参（Bayesian/Random/Grid）+ model-validator 模型否决 + 三分支失败诊断回环 + 证据契约自动生成 + 证据门禁 |
| **P5a** | 叙事设计       | 论文核心概念提炼 + 叙事主线设计（150 字）+ 高光布局（3 个评委必看亮点）+ 摘要漏斗（550-700 字）+ 国一等奖风格库匹配 |
| **P5b** | 纯文本写作     | 7 条评审友好规范（导航句/解释锚点/图表自明/段落≤150 字/术语一致性/节间递进/结果引导）+ 微单元覆盖性检查 + 反模板句硬检查 + GB/T 7714 参考文献 |
| **P5c** | 插图方案设计   | 扫描纯文本 → 识别"值得配图的论证段落" → 为每张图制定 7 点契约 → 18 种图表类型匹配 → 输出完整插图生成方案 |
|    ⚙️    | 图表生成       | 读方案 → 分组柱状图/排名图/折线置信带/散点相关性图/双面板敏感性图/差距标注图/逻辑框架图 → 12 项 QA 自检 → PNG（300DPI）+ PDF 双格式输出 |

---

## 为什么它强于其他数学建模 Agent

| 维度     |          普通建模 Agent           |                         CUMCM-skill                          |
| -------- | :-------------------------------: | :----------------------------------------------------------: |
| 流程结构 | 线性：读题→推荐模型→写代码→写论文 |                 **九阶段有向图 + 多级回环**                  |
| 模型选择 |          推荐 1-2 个模型          | **80+ 模型目录 + 45 条模型链 + 成功率统计 + 三维风险收益评分** |
| 创新能力 |                无                 |          **22 种创新模式 + 公式推导 + 反模式规避**           |
| 评审机制 |                无                 |       **五维量化评审闸门 + 红/黄/绿灯 + 精确回环路由**       |
| 求解深度 |           基础代码生成            | **7 种任务脚手架 + auto-tuner 自动调参 + model-validator 模型否决 + 三分支失败诊断** |
| 时间管理 |                无                 | **四模式自动降级（完整>36h/效率 24-36h/保守 12-24h/写作优先<12h）** |
| 叙事设计 |                无                 |   **独立叙事阶段：核心概念→高光布局→摘要漏斗→国一风格库**    |
| 论文质量 |           "实验结果"式            |    **导航句/解释锚点/反模板句硬检查/引用对话/微单元覆盖**    |
| 可视化   |           简单默认样式            |    **18 种图表类型 + 5 套配色 + 7 点图表契约 + 12 项 QA**    |

---

## 核心机制详解

### 1. 回环系统

CUMCM-skill 是市面极少数拥有"自我纠错"能力的建模 Agent：

- **P3 评审闸门**：五维量化评审（红/黄/绿灯）。红灯 → 精确回退到对应的 P1 或 P2 阶段重新选模/创新
- **P4 失败诊断**：三分支回环——结构性问题→P2 / 可解性漏判→P3 / 数值不稳定→P4 内循环
- **模型否决**：区分"调参不足"和"方向性错误"。R²<0.3 时直接否决模型，回退备选方案

### 2. 时间管理控制器

72 小时竞赛时间自动分配：

```
剩余 > 36h  → 完整模式：允许深度学习、大规模仿真、≥5 候选对比
剩余 24-36h → 效率模式：禁止从头训练深度学习、收敛候选≤3
剩余 12-24h → 保守模式：仅线性/统计/经典 ML、禁止回环、禁止新增创新
剩余 < 12h  → 写作优先：停止一切建模、全部精力投入论文写作
```

### 3. 三人角色协调器

模拟真实团队的三人分工：

- **建模手**：主导 P0/P1/P2/P3（问题分析、模型选型、创新推导、模型评审）
- **编程手**：主导 P0（数据部分）/P4（数据清洗、代码实现、求解调参、结果验证）
- **论文手**：主导 P5a/P5b/P5c（叙事设计、论文写作、插图方案）

每阶段有明确的主/辅角色分配，GCD（全局上下文文档）追踪每人完成状态。

### 4. 全局上下文文档（GCD）

六维结构化状态视图：

- 阶段状态矩阵（P0~P5c：进度 / 时间戳 / 耗时 / 输出摘要）
- 证据状态矩阵（8 要素×9 阶段：scaffold / needs_modeling / complete）
- 风险标注表（来源 / 等级 / 内容）
- 回环历史表（# / 时间 / 从 / 到 / 原因）
- 时间追踪行（已用 / 剩余 / 当前模式 / 阶段预算）
- 角色任务矩阵（建模手 / 编程手 / 论文手 每阶段完成状态）

### 5. 双门禁体系

- **证据门禁（P4）**：自动检查 model_results.json 中每问的 evidence_status。任一问为 "missing" → 阻断（exit 1）
- **格式门禁（P5b）**：自动检查字数（≥8000 字）、标题层级（1/1.1/1.1.1 完整）、图表引用、摘要字数、参考文献数量、反模板句（"模型假设理想化"等→红灯阻断）

---

## 项目结构

```
CUMCM-skill/
├── AGENTS.md                    # 项目总说明 + 自然语言触发规则
├── README.md                    # 本文件
├── .gitignore
│
├── .opencode/
│   ├── commands/
│   │   └── cumcm.md             # /cumcm 斜杠命令（启动/自动/状态/恢复）
│   └── skills/
│       ├── cumcm-orchestrator/   # 主控器：状态机 + GCD + 路由 + 时间 + 角色
│       ├── cumcm-reader/         # P0 读题与数据处理
│       ├── cumcm-model-selector/ # P1 模型方向选型
│       ├── cumcm-model-innovator/# P2 模型创新优化
│       ├── cumcm-model-reviewer/ # P3 模型评审闸门
│       ├── cumcm-solver/         # P4 求解与代码（含脚手架/调参器/否决器）
│       ├── cumcm-narrative/      # P5a 叙事设计
│       ├── cumcm-writer/         # P5b 论文写作
│       ├── cumcm-figure-planner/ # P5c 插图方案设计
│       ├── cumcm-visualizer/     # 图表生成引擎（含 18 种图表类型+配色库）
│       └── cumcm-micro-units/    # 微单元覆盖性检查库
│
├── docs/
│   └── contracts/                # 阶段间 JSON 契约 schema（12 个）
│
├── references/                   # 知识库（按阶段自动注入）
│   ├── common-model-catalog.md           # 80+ 模型目录
│   ├── model-innovation-patterns.md      # 22 种创新模式
│   ├── model-chain-patterns.md           # 45 条模型链库
│   ├── cumcm-grading-guide.md            # 国赛评分标准
│   ├── cumcm-pattern-library.md          # 12 种赛题套路
│   ├── cumcm-problem-archive.md          # 历年赛题索引
│   ├── winner-style-library.md           # 国一论文风格库
│   ├── winner-paper-cases.md             # 获奖论文案例
│   └── model-success-rates.md            # 模型获奖成功率统计
│
├── scripts/                      # 自动化算法包
│   ├── parse_problem.py          # 赛题文本预处理
│   ├── data_scanner.py           # 附件目录扫描
│   ├── data_cleaner.py           # 多策略异常检测+清洗
│   ├── data_profiler.py          # 逐字段画像+角色推断
│   ├── external_data.py          # 外部数据 API 获取
│   ├── build_problem_analysis.py # 自动生成 problem_analysis.json
│   ├── build_model_route.py      # 自动生成 model_route.json
│   ├── build_result_contracts.py # 证据契约自动生成
│   ├── build_paper_outline.py    # 自动生成论文大纲
│   ├── managed_marker.py         # MANAGED 标记块管理
│   ├── evidence_gate.py          # 自动化证据门禁
│   ├── check_paper_format.py     # 内容格式门禁
│   ├── run_pipeline.py           # 全流程一键串联
│   ├── solve_template.py         # Python 求解骨架
│   ├── solve_template.m          # MATLAB 求解骨架
│   ├── plot_config.py            # 图表全局配置（中文字体+5 套配色+色盲检测）
│   ├── figure_generator.py       # 图表生成入口（7 种核心类型）
│   ├── figure_composer.py        # 组合图引擎（4 种组合模式）
│   ├── logical_figure_generator.py # 逻辑框架图生成
│   ├── chart_atlas_builder.py    # 参考图集一键生成
│   ├── analyze_winner_papers.py  # 获奖论文模式提取器
│   └── validation/               # 求解结果验证脚本
│       ├── dimensional-check.py  # 量纲一致性
│       └── boundary-check.py     # 边界条件验证
│
└── templates/
    └── latex/                     # LaTeX 论文模板
        ├── cumcm-paper.tex
        ├── abstract-env.tex
        └── figure-table-macros.tex
```

---

## 使用方式

### 交互式（初学/试跑）

```bash
# 直接说话
帮我做这道题：[粘贴赛题全文]

# 斜杠命令
/cumcm [赛题文件路径]
```

启动后系统逐阶段推进，每阶段可审阅、介入、触发回环。

### 自动化（熟练用户）

```bash
/cumcm auto [赛题文件路径]
```

一键执行全流程。仅在证据门禁阻塞时暂停等待介入。

### 脚本模式（调试）

```bash
python scripts/run_pipeline.py --problem "赛题文件路径"
```

### 断点恢复

```bash
/cumcm resume
```

---

## 输出物

运行完成后在 `paper_output/` 下生成：

```
paper_output/
├── plan/                         # 建模方案
│   ├── problem_analysis.json     # 问题分析
│   ├── model_route.json          # 模型路线
│   ├── model-innovation.json     # 创新方案
│   ├── model-review.json         # 评审结果
│   ├── narrative-blueprint.json  # 叙事蓝图
│   ├── figure_placement_plan.json# 插图方案
│   └── paper_outline.json        # 论文大纲
├── results/                      # 求解结果
│   ├── model_results.json        # 模型结果
│   ├── metrics.json              # 评价指标
│   └── conclusions.json          # 核心结论
├── tables/                       # 表格导出
├── figures/                      # 图表（PNG 300DPI + PDF 矢量）
├── code/                         # 生成的可执行代码
└── final_paper_source.md         # 最终论文正文
```

---

## 致谢与参考

本项目在开发过程中参考了以下优秀开源项目：

- **[MathModel-Skill](https://github.com/yushui2022/MathModel-Skill)**  
  自动化数据处理 pipeline（data_scanner / cleaner / profiler）、证据契约协议（model_results.json / metrics.json / conclusions.json）、双门禁体系（evidence_gate.py + check_paper_format.py）、微单元 Prompt 库和全流程自动化等工程化设计

- **[nature-skills](https://github.com/Yuan1z0825/nature-skills)**  
  图表契约理念（contract.md）、静态/动态分离架构（manifest.yaml）、调色板体系（5 套场景化配色方案 + 色盲友好检测）、QA 检查清单和完整的可视化设计哲学

CUMCM-skill 的三大核心差异化创新——**P3 模型评审闸门**（量化级红/黄/绿灯判定 + 精确回环路由）、**P5a 叙事设计引擎**（核心概念提炼 + 高光布局 + 摘要漏斗 + 国一风格库）和**P5c "先文后图"插图方案工作流**（纯文本→识别论证段落→制定图表契约→自动化生成）——为独立开发。

---

