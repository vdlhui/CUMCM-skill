# table-index.schema.md — P4 表格索引输出规范

```json
{
  "tables": [
    {
      "id": "table1",
      "title": "各模型预测误差对比",
      "format": "三线表",
      "columns": ["模型", "MAE", "RMSE", "R²"],
      "source_question": "Q1",
      "file": "tables/table1.csv",
      "caption": "表1：LSTM-ARIMA混合模型与基线模型在测试集上的预测误差对比",
      "key_finding": "混合模型在所有三项指标上均显著优于基线ARIMA"
    }
  ]
}
```
