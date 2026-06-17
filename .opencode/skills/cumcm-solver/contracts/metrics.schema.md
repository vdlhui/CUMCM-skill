# metrics.schema.md — P4 评价指标输出规范

```json
{
  "questions": {
    "Q1": [
      {
        "metric": "MAE",
        "value": 0.042,
        "unit": "标准化",
        "benchmark_value": 0.078,
        "benchmark_model": "ARIMA",
        "improvement_percent": 46.2
      },
      {
        "metric": "RMSE",
        "value": 0.058,
        "unit": "标准化",
        "benchmark_value": 0.095,
        "benchmark_model": "ARIMA",
        "improvement_percent": 38.9
      },
      {
        "metric": "R²",
        "value": 0.91,
        "unit": "—",
        "benchmark_value": 0.82,
        "benchmark_model": "ARIMA",
        "improvement_percent": 11.0
      }
    ]
  }
}
```
