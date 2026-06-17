# conclusions.schema.md — P4 结论输出规范

```json
{
  "questions": {
    "Q1": {
      "core_finding": "在基本情形下所有五种的期望净收益均为负，高级球以单次-10200洛克贝为最优",
      "quantitative_conclusion": "高级球亏损绝对值最小（-10200洛克贝/次），优于国王球的-154000洛克贝/次",
      "comparison_to_baseline": "高级球 vs 棱镜球亏损差313倍",
      "key_number": -10200,
      "key_number_unit": "洛克贝/次",
      "evidence_status": "complete",
      "formula_refs": ["式(1)", "式(2)"]
    }
  }
}
```
