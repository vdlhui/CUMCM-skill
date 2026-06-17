"""
build_problem_analysis.py — 自动生成 problem_analysis.json
从 cleaned_problem.txt → 子问题分解 + 任务类型推断 + 约束提取 + 隐含假设 + 套路匹配
"""
import re
import json
import sys


def extract_questions(text: str) -> list:
    """提取 Q1/Q2/Q3"""
    questions = []
    pattern = re.compile(r'(问题\s*[一二三四1-4]|Q[1-4]|任务\s*[一二三四1-4])', re.IGNORECASE)
    parts = pattern.split(text)
    current_q = None
    for part in parts:
        if pattern.match(part):
            if current_q:
                questions.append(current_q)
            current_q = {"id": part.strip(), "description": "", "task_type": "", "data_fields_used": []}
        elif current_q:
            current_q["description"] += part.strip() + " "
    if current_q:
        questions.append(current_q)

    for q in questions:
        desc = q.get("description", "")
        if re.search(r'预测|预报|估计|趋势', desc):
            q["task_type"] = "prediction"
        elif re.search(r'最小|最大|最优|最短|方案|规划', desc):
            q["task_type"] = "optimization"
        elif re.search(r'评价|评估|排序|打分', desc):
            q["task_type"] = "evaluation"
        elif re.search(r'分类|判别|识别', desc):
            q["task_type"] = "classification"
        elif re.search(r'聚类|分组|划分', desc):
            q["task_type"] = "clustering"
        elif re.search(r'仿真|模拟', desc):
            q["task_type"] = "simulation"
        else:
            q["task_type"] = "unknown"
    return questions


def extract_constraints(text: str) -> list:
    """提取约束"""
    constraints = []
    patterns = [
        (r'不[得应能可]?[超过大于低于少于]+[^\n。]+', 'inequality'),
        (r'[在处于]+[^\n。]*?范围[内中下][^\n。]*', 'boundary'),
        (r'单位[：:][^\n]+', 'unit'),
    ]
    for pat, ctype in patterns:
        for match in re.finditer(pat, text):
            constraints.append({"type": ctype, "expression": match.group().strip(), "source": f"原文匹配: {pat}"})
    return constraints


def extract_implicit_assumptions(text: str) -> list:
    """提取隐含假设"""
    assumptions = []
    patterns = [
        (r'[根据通常一般]常[识理]', '常识假设', 'medium'),
        (r'不[考虑计][^\n。]{0,20}', '排除性假设', 'high'),
        (r'假设|假定|设[^\n。]*', '显式假设', 'high'),
        (r'近似[认为为]', '近似假设', 'medium'),
    ]
    for pat, stype, confidence in patterns:
        for match in re.finditer(pat, text):
            assumptions.append({
                "statement": match.group().strip(),
                "source_pattern": pat,
                "confidence": confidence
            })
    return assumptions


def build(input_path="cleaned_problem.txt", output_path="problem_analysis.json"):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    analysis = {
        "problem_id": "",
        "questions": extract_questions(text),
        "constraints": extract_constraints(text),
        "implicit_assumptions": extract_implicit_assumptions(text),
        "data_summary": {"total_files": 0, "total_records": 0, "highest_missing_field": "", "outlier_fields": []}
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"问题分析完成 → {output_path}")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "cleaned_problem.txt"
    build(inp)
