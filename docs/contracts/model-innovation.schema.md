# model-innovation.schema.md — P2→P3 契约

```json
{
  "innovations": [
    {
      "id": "INNOV-1",
      "innovation_mode": "INN-06|INN-05|...",
      "deficiency_addressed": "string",
      "standard_formula": {"id": "式(5)", "latex": "..."},
      "innovation_formula": {"id": "式(8)", "latex": "...", "meaning": "string"},
      "feasibility_scores": {
        "贴题性": 5,
        "可解释性": 4,
        "数据支撑": 5,
        "可复现性": 4
      },
      "assumptions_required": ["string"],
      "verification_required": ["消融实验", "string"],
      "anti_pattern_scan": {
        "ANTI-01": "pass",
        "ANTI-02": "pass",
        "ANTI-03": "pass",
        "ANTI-04": "pass",
        "ANTI-05": "pass"
      }
    }
  ],
  "self_assessment": {
    "innovation_level": "增量改进|方法迁移|结构创新",
    "estimated_independent_contribution": "R²+0.06",
    "contribution_rationale": "string"
  }
}
```
