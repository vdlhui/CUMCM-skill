# figure-placement.schema.md — P5c 插图方案契约

```json
{
  "schema_version": "1.0",
  "generated_by": "P5c cumcm-figure-planner",
  "generated_at": "ISO8601",

  "figures": [
    {
      "id": "fig_01",
      "category": "data_result",
      "priority": "high|medium",
      
      "placement": {
        "section": "3.1.3",
        "sentence_hint": "关键句子的前20个字，用于定位"
      },
      
      "core_argument": "这张图在证明什么？一句话结论——将用于图标题",
      
      "chart_spec": {
        "chart_type": "grouped_bar|ranked_bar|trend_line|scatter_corr|sensitivity_dual|gap_annotated|heatmap|radar|stacked_area|residual_diagnosis|convergence_curve|pareto_front|network_relation|waterfall|solution_heatmap|bifurcation|phase_trajectory|subplot_comparison",
        "palette": "contrast_3|gradient_6|directional|spatial|pastel_family",
        "composite_mode": "none|main_plus_zoom|line_plus_bar|heatmap_plus_marginal|radar_plus_bubble",
        "dimensions": "single_column(8cm)|double_column(16cm)"
      },
      
      "data_extraction": {
        "source_files": ["paper_output/results/model_results.json"],
        "x_path": "questions.Q1.key_categories[]",
        "y_paths": {
          "series_1": {"source": "paper_output/results/metrics.json", "path": "questions.Q1[0].value", "label": "MAE"}
        },
        "error_bars": {"source": "paper_output/results/metrics.json", "path": "questions.Q1[0].ci95"}
      },
      
      "annotations": {
        "reference_lines": [{"value": 0, "style": "dashed", "label": "盈亏平衡线"}],
        "star_markers": [{"target": "最优柱", "text": "最优"}],
        "significance_brackets": [],
        "threshold_arrows": []
      },
      
      "caption": "图X：结论先行+关键数据支撑+与论文论点的关联（支撑§X.X论证）"
    }
  ],
  
  "logical_framework_figures": [
    {
      "id": "fig_flow_01",
      "category": "logical_framework",
      "figure_type": "flowchart|mechanism_diagram|mind_map|algorithm_flow",
      "placement": {"section": "1.3"},
      "core_argument": "展示从Q1到Q4的递进式建模范式",
      "layout_style": "vertical_spine|center_radial|step_progression",
      "modules": [
        {"name": "Q1 期望值基准", "color_zone": "blue", "methods": ["期望值解析"], "key_finding": "全亏损基准"},
        {"name": "Q2 全概率扩展", "color_zone": "green", "methods": ["全概率推导+E[M]MC"], "key_finding": "总倍率22.63"},
        {"name": "Q3 随机过程仿真", "color_zone": "orange", "methods": ["MC仿真+统计检验"], "key_finding": "死磕3.65倍"},
        {"name": "Q4 DP反证贪心", "color_zone": "purple", "methods": ["小规模DP反例+改进贪心"], "key_finding": "差距36-41%"}
      ]
    }
  ],
  
  "figure_count": {
    "data_result": 0,
    "logical_framework": 0
  }
}
```
