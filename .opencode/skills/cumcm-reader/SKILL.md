---
name: cumcm-reader
description: CUMCM 读题与数据处理。深度解析赛题，分解子问题，识别题型与套路，提取约束与隐含假设，执行数据清洗画像，输出 problem_analysis.json 和 data_plan.json。
---

# P0：读题与数据处理

## 角色分配
- 🟢 建模手主导：赛题解析、子问题分解、套路匹配、约束/假设提取、历年对标
- 🟢 编程手主导：数据扫描、清洗、画像、外部数据获取
- 🟡 论文手辅助：记录赛题关键信息、整理问题重述素材

## 输入
- 赛题文本（粘贴内容 / 纯文本文件路径）
- 附件文件目录路径（可选）
- 已注入知识库：cumcm-pattern-library.md / cumcm-problem-archive.md / winner-paper-cases.md

## 执行步骤

### 第 1 步：赛题文本预处理
调用 `scripts/parse_problem.py`：
- 段落清洗（去页码/页眉页脚/合并断行）
- 表格结构重建（从缩进/制表符/空格对齐识别表格）
- 公式占位标记（`$...$` / `$$...$$` 标记位置）
- 输出：`parsed_problem.txt`

### 第 2 步：子问题自动分解
从 parsed_problem.txt 中：
- 识别 Q1/Q2/Q3/Q4（正则匹配："问题一/问题1/Question 1/任务1"等关键词）
- 为每个子问题提取：任务描述、输出要求、输入数据字段
- 输出到 problem_analysis.json → questions[]

### 第 3 步：任务类型推断
对每个子问题，基于关键词推断任务类型：
- "预测/预报/估计/趋势" → 预测
- "最小/最大/最优/最短/方案" → 优化
- "评价/评估/排序/打分" → 评价
- "分类/判别/识别/判断" → 分类
- "聚类/分组/划分" → 聚类
- "仿真/模拟" → 仿真
- "路径/网络/连通" → 图论
- "运动/传热/受力/流体/物理" → 微分方程
- 输出到 problem_analysis.json → questions[].task_type

### 第 4 步：约束提取
- 不等式约束：正则匹配"不超过/不大于/小于等于/≥/≤/≫/至少/至多/不少于/不低于"等
- 可行域约束："在...范围内"/"在...条件下"
- 单位口径："单位：XX"/"以 XX 为单位"
- 边界条件："假定/假设/题目给定/初始条件/边界条件"
- 每条约束标注：约束类型 + 原文出处（段落位置）
- 输出到 problem_analysis.json → constraints[]

### 第 5 步：隐含假设提取
从文本中匹配隐含假设句式：
- "根据常识" / "通常认为" / "一般情况" → 常识假设
- "不考虑" / "忽略" / "不计" → 排除性假设
- "假设" / "假定" / "设" → 显式假设
- "近似认为" / "近似为" → 近似假设
- 每条隐含假设标注：来源句式 + 置信度（高/中/低）
- 输出到 problem_analysis.json → implicit_assumptions[]

### 第 6 步：赛题套路匹配
加载 references/cumcm-pattern-library.md：
- 基于信号词表扫描 parsed_problem.txt
- 匹配 12 种套路中的 1-2 种
- 输出：套路名称 + 匹配信号词 + 置信度 + 建议模型组合
- 输出到 problem_analysis.json → pattern_match

### 第 7 步：历年赛题对标
加载 references/cumcm-problem-archive.md：
- 根据推断的任务类型查询历年赛题
- 输出：相近赛题编号 + 常用模型映射 + 获奖论文特征提示
- 输出到 problem_analysis.json → historical_benchmarks

### 第 8 步：数据源扫描（如有附件）
调用 `scripts/data_scanner.py`：
- 扫描附件目录，识别 CSV/XLSX/TXT/JSON 文件
- 每个文件输出：文件名、大小、前 5 行预览
- 输出：`scan_report.md`

### 第 9 步：数据清洗（如有数据）
调用 `scripts/data_cleaner.py`：
- 缺失值检测与填补策略（均值/中位数/众数/前向填充/模型预测填补）
- 异常值检测（IQR / Z-score / Isolation Forest）
- 异常值处理策略（剔除/截尾/标记保留，写入 evidence_status）
- 单位标准化
- 输出：`data_cleaned/` 目录

### 第 10 步：数据画像
调用 `scripts/data_profiler.py`：
- 逐字段输出：类型、count/mean/std/min/q25/q50/q75/max、缺失率、异常标记
- 字段角色推荐（因变量/自变量/时间/类别/未知）
- 数据-问题映射：每个字段标注归属子问题
- 输出：`data_plan.json`

### 第 11 步：外部数据获取（如需要）
调用 `scripts/external_data.py`：
- 根据题目数据需求匹配内置 API（国家统计局/World Bank/Open-Meteo 等）
- 优先级配置（国内建模优先国内数据源）
- 标准化口径 + 记录来源元数据
- 输出：`sources.json`

### 第 12 步：生成结构化输出
调用 `scripts/build_problem_analysis.py`：
- 将以上所有步骤的结果汇总为 problem_analysis.json
- 新增：约束-问题链接（每条约束标注影响 Q1/Q2/Q3）
- 新增：约束间矛盾检测

## 输出

| 文件 | 格式 | 内容 |
|------|------|------|
| `problem_analysis.json` | JSON | 子问题分解、题型分类、套路匹配、约束清单、隐含假设、历年对标、约束-问题链接 |
| `data_plan.json` | JSON | 逐字段画像、数据-问题映射、清洗日志 |
| `sources.json` | JSON | 外部数据来源清单、API 调用记录、口径说明 |
| `data_cleaned/` | CSV/XLSX | 清洗后数据文件 |

## 不能做的事
- 不要在此阶段推荐具体模型（那是 P1 的工作）
- 不要跳过数据清洗直接建模（不干净的数据会导致 P4 求解失败）
- 不要遗漏隐含假设（每遗漏一条 = P3 完整性黄灯）
- 不要在没有附件时强行要求数据（有些赛题只需要推导不需要数据）
