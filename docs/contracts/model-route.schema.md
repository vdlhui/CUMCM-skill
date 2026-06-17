# model-route.schema.md — P1→P2 契约

```json
{
  "selected_chain": {
    "chain_id": "chain16",
    "chain_structure": ["LSTM预测", "MILP优化", "灵敏度分析"],
    "three_d_assessment": {
      "expected_score": 92,
      "expected_score_rationale": "string",
      "implementation_cost": 45,
      "implementation_cost_rationale": "string",
      "risk": 20,
      "risk_rationale": "string"
    }
  },
  "chain_candidates": [
    {
      "chain_id": "string",
      "chain_structure": ["string"],
      "three_d_assessment": {
        "expected_score": 0,
        "implementation_cost": 0,
        "risk": 0
      },
      "exclusion_reason": "string|null"
    }
  ],
  "baseline_model": "ARIMA",
  "verification_plan": {
    "Q1": "滚动预测误差 + 与基线对比",
    "Q2": "优化解与随机采样对比",
    "Q3": "鲁棒性测试"
  },
  "selection_rationale": "string"
}
```
