# narrative-blueprint.schema.md — P5a→P5b 契约

```json
{
  "abstract_template": "A_问题穿透型|B_数据驱动型|C_指标驱动型",
  "innovation_presentation": "A_缺陷驱动型|B_洞察驱动型",
  "core_concept": "动态耦合温度预测网络",
  "narrative_mainline": "string (150字)",
  "highlights": [
    {
      "id": 1,
      "section": "4.2",
      "content": "注意力权重可视化（式8-9的热力图）",
      "why_compelling": "直观展示模型抓住了题目中的关键转折点"
    },
    {
      "id": 2,
      "section": "4.3",
      "content": "耦合损失函数对比实验（表3）",
      "why_compelling": "量化说明联合优化优于分开训练——消融实验"
    }
  ],
  "abstract_long": "string (550-700字)",
  "abstract_short": "string (300字)",
  "chapter_structure": [
    {
      "chapter": 3,
      "title": "模型建立",
      "subsections": [
        {"id": "3.1", "title": "核心概念引入+基础模型建立", "progression": "引入"},
        {"id": "3.2", "title": "关键创新点展开", "progression": "展开"},
        {"id": "3.3", "title": "框架在Q1的验证", "progression": "验证"},
        {"id": "3.4", "title": "框架拓展到Q2", "progression": "拓展"},
        {"id": "3.5", "title": "框架在Q3的最终验证", "progression": "整合"}
      ]
    }
  ],
  "grading_evidence_map": {
    "模型创新性": {"section": "4.2", "evidence": "消融实验确认注意力独立贡献R²+0.06"},
    "求解正确性": {"section": "4.3", "evidence": "表3：MAE=0.042 vs 基线0.078"},
    "模型真实性": {"section": "5", "evidence": "P3预判的敏感性在实测中确认"}
  },
  "self_review": {
    "核心概念贯穿": "通过",
    "叙事递进": "通过",
    "摘要独立可读": "通过",
    "摘要模板匹配": "通过",
    "创新呈现一致": "通过",
    "反模板句检查": "通过"
  }
}
```
