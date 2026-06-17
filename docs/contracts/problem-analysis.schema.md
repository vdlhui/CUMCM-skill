# problem-analysis.schema.md — P0→P1 契约

## 必填字段

```json
{
  "problem_id": "string",
  "problem_description_short": "string",
  "questions": [
    {
      "id": "Q1",
      "description": "string",
      "task_type": "prediction|optimization|evaluation|classification|clustering|simulation|graph_theory|differential_equation",
      "output_requirement": "string",
      "data_fields_used": ["字段1", "字段2"]
    }
  ],
  "constraints": [
    {
      "type": "inequality|boundary|unit|explicit",
      "expression": "string",
      "source": "string",
      "related_questions": ["Q1"]
    }
  ],
  "implicit_assumptions": [
    {
      "statement": "string",
      "source_pattern": "string",
      "confidence": "high|medium|low",
      "related_questions": ["Q1"]
    }
  ],
  "pattern_match": {
    "primary_pattern": "string",
    "secondary_pattern": "string|null",
    "confidence": "high|medium|low",
    "signal_words_matched": ["预测", "优化"],
    "suggested_model_combos": ["LSTM+NSGA-II"]
  },
  "historical_benchmarks": [
    {
      "year": "2023",
      "problem": "B",
      "similarity": "string",
      "winning_models": ["string"]
    }
  ],
  "data_summary": {
    "total_files": 0,
    "total_records": 0,
    "highest_missing_field": "string",
    "outlier_fields": []
  }
}
```
