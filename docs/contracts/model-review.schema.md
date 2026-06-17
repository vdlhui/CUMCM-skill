# model-review.schema.md — P3→P4 契约

```json
{
  "verdict": "A_通过|B_局部修正|C_结构重调|D_推倒重来",
  "verdict_rationale": "string",
  "dimensions": {
    "方向再审": {
      "score": "绿灯|黄灯|红灯",
      "detail": "string",
      "quantitative_evidence": "string|null"
    },
    "创新可行性": {
      "score": "绿灯|黄灯|红灯",
      "detail": "string"
    },
    "完整覆盖性": {
      "score": "绿灯|黄灯|红灯",
      "detail": "string"
    },
    "可解性预判": {
      "score": "绿灯|黄灯|红灯",
      "detail": "string",
      "estimated_complexity": "string"
    },
    "数学验证": {
      "量纲一致性": "通过|警告|失败",
      "边界条件": "通过|警告|失败",
      "参数合理性": "通过|警告|失败",
      "数值稳定性预估": "通过|警告|失败"
    }
  },
  "risk_items": [
    {
      "dimension": "完整覆盖性",
      "level": "黄灯",
      "item": "Q3边界条件未预定义",
      "mitigation": "P4求解前补定义"
    }
  ],
  "routing": {
    "action": "放行P4|回环P1|回环P2",
    "target_phase": "P4",
    "carry_context": "string"
  },
  "time_sensitive_fallback": "若剩余<12h，可降级为B局部修正放行"
}
```
