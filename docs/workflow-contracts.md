# CUMCM-skill JSON 契约规范

## 12 个契约清单

| # | 契约文件 | 生产者 | 消费者 | 用途 |
|---|----------|:------:|:------:|------|
| 1 | problem_analysis.json | P0 cumcm-reader | P1 | 子问题分解/题型/套路/约束/数据摘要 |
| 2 | data_plan.json | P0 data_profiler | P1/P4 | 逐字段画像/数据-问题映射 |
| 3 | sources.json | P0 external_data | P1 | 外部数据来源清单 |
| 4 | model_route.json | P1 model-selector | P2 | 选定链/候选链/三维评分/基线 |
| 5 | model-innovation.json | P2 model-innovator | P3 | 创新条目/公式链/可行性评分 |
| 6 | model-review.json | P3 model-reviewer | P4 | 五维评审结果/综合判定/风险项 |
| 7 | model_results.json | P4 solver | P5a/P5b | 每问模型/关键结果/evidence_status |
| 8 | metrics.json | P4 solver | P5a/P5b | 评价指标+基线对比 |
| 9 | conclusions.json | P4 solver | P5b | 每问核心发现+量化结论 |
| 10 | table_index.json | P4 solver | P5b | 表格索引(ID/标题/列/题注) |
| 11 | narrative-blueprint.json | P5a narrative | P5b | 核心概念/叙事主线/高光/摘要/章节递进 |
| 12 | paper_outline.json | build_paper_outline.py | P5b | 章节→小节→段落清单 |

## 通用规则

- 所有 JSON 文件使用相对路径引用
- 必含字段：schema_version, generated_by, generated_at
- Q1/Q2/Q3/Q4 作为 question_id 在各契约间保持一致
- 所有结果数据必须可追溯到 question_id
- 不允许硬编码绝对路径

## 数据流向图

```
problem_files/ → P0 → problem_analysis.json + data_plan.json + sources.json
                         ↓
                       P1 → model_route.json
                              ↓
                            P2 → model-innovation.json
                                   ↓
                                 P3 → model-review.json
                                        ↓
                                 P4 → model_results.json + metrics.json
                                       + conclusions.json + table_index.json
                                              ↓
                              P5a → narrative-blueprint.json
                                        ↓
                              P5b → paper_outline.json → final_paper_source.md
```
