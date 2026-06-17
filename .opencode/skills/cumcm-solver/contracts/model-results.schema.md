# model-results.schema.md — P4 模型结果输出规范

```json
{
  "problem_id": "string",
  "generated_at": "ISO8601",
  "questions": {
    "Q1": {
      "model_name": "LSTM-ARIMA混合模型",
      "evidence_status": "scaffold|needs_modeling|complete",
      "key_parameters": {
        "hidden_size": 64,
        "learning_rate": 0.001,
        "其他": "值"
      },
      "key_results": {
        "train_metric": {"name": "MAE", "value": 0.035, "unit": "标准化"},
        "test_metric": {"name": "MAE", "value": 0.042, "unit": "标准化"},
        "baseline_metric": {"name": "MAE", "value": 0.078, "unit": "标准化", "baseline_model": "ARIMA"},
        "improvement_percent": 46.2
      },
      "formula_refs": ["式(12)", "式(13)"],
      "tuning_params": {"最优参数": "值来自 tuning_report.json"}
    }
  }
}
```
