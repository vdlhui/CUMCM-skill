"""
build_paper_outline.py — 自动生成论文大纲
输入：P5a narrative-blueprint.json
输出：paper_outline.json（章节→小节→段落清单）
"""
import sys
import json
import os


def build_outline(blueprint_path="paper_output/plan/narrative-blueprint.json",
                  output_path="paper_output/plan/paper_outline.json"):
    """将叙事蓝图映射到 CUMCM 标准章节结构"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 尝试读取蓝图
    blueprint = {}
    if os.path.exists(blueprint_path):
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            blueprint = json.load(f)

    outline = {
        "schema_version": "1.0",
        "generated_by": "build_paper_outline.py",
        "generated_at": "",
        "core_concept": blueprint.get("core_concept", ""),
        "chapters": [
            {
                "id": "1",
                "title": "问题重述与分析",
                "subsections": [
                    {"id": "1.1", "title": "背景说明", "key_sentences": [
                        "研究场景介绍",
                        "核心挑战说明",
                        "本文解决的具体问题"
                    ]},
                    {"id": "1.2", "title": "题目任务", "key_sentences": [
                        "Q1 任务复述",
                        "Q2 任务复述",
                        "Q3 任务复述"
                    ]},
                    {"id": "1.3", "title": "本文思路概述", "key_sentences": [
                        "建模方法论",
                        "各问递进关系",
                        "核心创新一句话"
                    ]}
                ]
            },
            {
                "id": "2",
                "title": "模型假设与符号说明",
                "subsections": [
                    {"id": "2.1", "title": "模型假设", "key_sentences": []},
                    {"id": "2.2", "title": "符号说明", "key_sentences": ["符号汇总表"]}
                ]
            },
            {
                "id": "3",
                "title": "模型建立与求解",
                "subsections": []  # 由 Agent 根据 P5a 章节递进结构填充
            },
            {
                "id": "4",
                "title": "模型评价与改进",
                "subsections": [
                    {"id": "4.1", "title": "模型优点", "key_sentences": ["优点1+证据", "优点2+证据", "优点3+证据"]},
                    {"id": "4.2", "title": "模型不足", "key_sentences": ["P3预判", "P4实测验证/证伪", "量化边界", "原因分析"]},
                    {"id": "4.3", "title": "改进方向", "key_sentences": ["改进方案1+条件", "改进方案2+条件"]},
                    {"id": "4.4", "title": "推广应用", "key_sentences": ["可迁移场景", "同类问题启示"]}
                ]
            },
            {
                "id": "附录",
                "title": "参考文献与附录",
                "subsections": []
            }
        ],
        "grading_evidence_map": blueprint.get("grading_evidence_map", {})
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(outline, f, ensure_ascii=False, indent=2)
    print(f"✅ 论文大纲 → {output_path}")
    print(f"   核心概念：{outline['core_concept']}")
    return output_path


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "paper_output/plan/narrative-blueprint.json"
    build_outline(inp)
