# CUMCM-skill 启动提示词

## 交互式模式（推荐新手）

```
@cumcm-orchestrator 启动 [粘贴赛题内容]

@cumcm-orchestrator 启动 problem_files/2024A.pdf
```

## 自动化模式（一键执行）

```
@cumcm-orchestrator 自动 problem_files/2024A.pdf
```

## 断点恢复

```
@cumcm-orchestrator 恢复
```

## 只做某一阶段

```
@cumcm-reader 分析赛题 problem_files/题目.pdf
@cumcm-model-selector 基于上一阶段输出选模型方向
@cumcm-model-innovator 对选定模型做针对性创新优化
@cumcm-model-reviewer 评审当前模型方案
@cumcm-solver 求解当前模型
@cumcm-narrative 设计论文叙事
@cumcm-writer 开始逐节写作
```

## 查看当前状态

```
查看 GCD 上下文文档
```

## 回环控制

```
@cumcm-orchestrator 回环到 P1（原因：评审发现方向性问题）
@cumcm-orchestrator 回环到 P2（原因：创新推导有漏洞）
```

## 常用检查命令

```
# 证据门禁
python scripts/evidence_gate.py paper_output/results/model_results.json

# 格式门禁
python scripts/check_paper_format.py paper_output/final_paper_source.md

# 全流程
python scripts/run_pipeline.py --problem "problem_files/题目.pdf"

# 数据画像
python scripts/data_profiler.py data_cleaned/
```

## 输出目录初始化

首次运行时自动创建 `paper_output/` 目录结构：

```
paper_output/
├── plan/              # 契约文件（model_route.json 等）
├── results/           # 求解结果（model_results.json 等）
├── tables/            # 表格导出
├── data_cleaned/      # 清洗后数据
└── final_paper_source.md  # 最终论文稿
```
