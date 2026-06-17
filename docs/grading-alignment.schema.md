# grading-alignment.schema.md — 评分点-证据映射表

```json
{
  "mappings": [
    {
      "grading_dimension": "模型创新性",
      "weight": 7,
      "target_section": "4.2",
      "evidence_source": "P2 model-innovation.json",
      "evidence_content": "消融实验确认注意力独立贡献R²+0.06",
      "presentation_strategy": "缺陷驱动：先展示标准LSTM的不足，再引入创新"
    },
    {
      "grading_dimension": "求解正确性",
      "weight": 5,
      "target_section": "4.3",
      "evidence_source": "P4 metrics.json",
      "evidence_content": "表3：MAE=0.042 vs 基线ARIMA MAE=0.078，改善46.2%",
      "presentation_strategy": "三线表+对比柱状图+一句话分析差异来源"
    },
    {
      "grading_dimension": "模型真实性",
      "weight": 4,
      "target_section": "5",
      "evidence_source": "P3 model-review.json + P4 tuning_report.json",
      "evidence_content": "P3预判α敏感性→P4实测确认：α偏离15%时误差膨胀至23%",
      "presentation_strategy": "国一评价风格：预判vs实测对比+量化边界+改进路径"
    }
  ]
}
```
