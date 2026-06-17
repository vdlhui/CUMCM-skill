"""
solve_template.py — 通用 Python 求解骨架
参数化设计 / 错误处理 / 运行日志 / 关键数值落盘
"""
import os
import json
import time
import numpy as np
import pandas as pd
import sys

LOG = []

def log(msg: str):
    entry = f"[{time.strftime('%H:%M:%S')}] {msg}"
    LOG.append(entry)
    print(entry)


def load_data(data_dir: str = "data_cleaned"):
    """加载 P0 清洗后的数据"""
    log(f"加载数据: {data_dir}")
    data = {}
    if os.path.exists(data_dir):
        for f_name in os.listdir(data_dir):
            if f_name.endswith(".csv"):
                key = os.path.splitext(f_name)[0]
                data[key] = pd.read_csv(os.path.join(data_dir, f_name))
                log(f"  已加载: {f_name} ({len(data[key])} 行)")
    return data


def save_results(results: dict, output_dir: str = "output"):
    """保存结果"""
    os.makedirs(output_dir, exist_ok=True)
    for key, value in results.items():
        if isinstance(value, (pd.DataFrame, pd.Series)):
            value.to_csv(os.path.join(output_dir, f"{key}.csv"), index=False)
        elif isinstance(value, dict):
            with open(os.path.join(output_dir, f"{key}.json"), 'w', encoding='utf-8') as f:
                json.dump(value, f, ensure_ascii=False, indent=2)
    log(f"结果已保存到: {output_dir}")
    with open(os.path.join(output_dir, "run_log.json"), 'w', encoding='utf-8') as f:
        json.dump(LOG, f, ensure_ascii=False, indent=2)


def main():
    log("=== CUMCM 求解开始 ===")
    try:
        data = load_data()
        # === BEGIN MANAGED: modeling ===
        # 📌 在此区域填入模型逻辑
        results = {}
        # === END MANAGED: modeling ===
        save_results(results)
        log("=== 求解完成 ===")
    except Exception as e:
        log(f"!!! 求解失败: {e}")
        raise


if __name__ == "__main__":
    main()
