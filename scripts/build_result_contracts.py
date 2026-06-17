"""
build_result_contracts.py — 自动生成 P4 证据契约
从 P4 输出组装 model_results.json + metrics.json + conclusions.json + table_index.json
"""
import sys
import json
import os


def build_model_results(results_data, output_path="paper_output/results/model_results.json"):
    """从求解结果组装 model_results.json"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    contract = {
        "schema_version": "1.0",
        "generated_by": "build_result_contracts.py",
        "generated_at": "",
        "questions": results_data
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)
    print(f"✅ model_results.json → {output_path}")
    return output_path


def build_metrics(metrics_data, output_path="paper_output/results/metrics.json"):
    """从评价指标组装 metrics.json"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    contract = {
        "schema_version": "1.0",
        "generated_by": "build_result_contracts.py",
        "generated_at": "",
        "questions": metrics_data
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)
    print(f"✅ metrics.json → {output_path}")
    return output_path


def build_conclusions(conclusions_data, output_path="paper_output/results/conclusions.json"):
    """从结论组装 conclusions.json"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    contract = {
        "schema_version": "1.0",
        "generated_by": "build_result_contracts.py",
        "generated_at": "",
        "questions": conclusions_data
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)
    print(f"✅ conclusions.json → {output_path}")
    return output_path


def build_table_index(tables_data, output_path="paper_output/tables/table_index.json"):
    """从表格数据组装 table_index.json"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    contract = {
        "schema_version": "1.0",
        "generated_by": "build_result_contracts.py",
        "generated_at": "",
        "tables": tables_data
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(contract, f, ensure_ascii=False, indent=2)
    print(f"✅ table_index.json → {output_path}")
    return output_path


if __name__ == "__main__":
    print("build_result_contracts.py — 由 P4 求解完成后调用")
    print("预期从 P4 输出目录读取结果并组装为证据契约")
    print("可用函数：build_model_results / build_metrics / build_conclusions / build_table_index")
