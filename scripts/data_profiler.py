"""
data_profiler.py — 数据画像
输出：data_plan.json（逐字段画像+数据-问题映射）
"""
import os
import sys
import json
import numpy as np
import pandas as pd


def profile_series(series, field_name, source_file):
    """单字段画像"""
    profile = {
        "field": field_name,
        "source_file": source_file,
        "dtype": str(series.dtype),
        "missing_ratio": round(series.isnull().sum() / len(series), 4) if len(series) > 0 else 0,
        "role": infer_role(field_name)
    }
    if pd.api.types.is_numeric_dtype(series):
        clean = series.dropna()
        if len(clean) > 0:
            profile["stats"] = {
                "count": int(len(clean)),
                "mean": round(float(clean.mean()), 4),
                "std": round(float(clean.std()), 4),
                "min": round(float(clean.min()), 4),
                "q25": round(float(clean.quantile(0.25)), 4),
                "q50": round(float(clean.quantile(0.50)), 4),
                "q75": round(float(clean.quantile(0.75)), 4),
                "max": round(float(clean.max()), 4)
            }
            # 异常值标记
            Q1, Q3 = clean.quantile(0.25), clean.quantile(0.75)
            IQR = Q3 - Q1
            outliers = (clean < Q1 - 1.5 * IQR) | (clean > Q3 + 1.5 * IQR)
            profile["outlier_count"] = int(outliers.sum())
            profile["outlier_method"] = "IQR × 1.5"
    return profile


def infer_role(field_name: str) -> str:
    """基于关键词推断字段角色"""
    name_lower = field_name.lower()
    if any(kw in name_lower for kw in ["目标", "输出", "结果", "因变量", "y_", "target", "label"]):
        return "dependent"
    if any(kw in name_lower for kw in ["因素", "输入", "特征", "自变量", "x_", "feature"]):
        return "independent"
    if any(kw in name_lower for kw in ["时间", "日期", "month", "year", "date", "time"]):
        return "temporal"
    if any(kw in name_lower for kw in ["类别", "类型", "分组", "category", "class", "type"]):
        return "categorical"
    return "unknown"


def profile_files(data_dir, output_path="data_plan.json"):
    profiles = []
    for f_name in os.listdir(data_dir):
        f_path = os.path.join(data_dir, f_name)
        try:
            ext = os.path.splitext(f_name)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(f_path)
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(f_path)
            else:
                continue
            for col in df.columns:
                profiles.append(profile_series(df[col], col, f_name))
        except Exception as e:
            profiles.append({"field": "ERROR", "source_file": f_name, "error": str(e)})

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"field_profiles": profiles, "question_mapping": {}}, f, ensure_ascii=False, indent=2)
    print(f"数据画像完成 → {output_path} ({len(profiles)} 个字段)")
    return output_path


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "data_cleaned"
    profile_files(target)
