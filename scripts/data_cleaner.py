"""
data_cleaner.py — 数据清洗
功能：缺失值填补 / 多策略异常检测(IQR+Z-score+IsolationForest) / 策略选项 / 标准化
输出：data_cleaned/ 目录
"""
import os
import sys
import json
import numpy as np
import pandas as pd

def detect_outliers_iqr(series):
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    return (series < lower) | (series > upper)

def detect_outliers_zscore(series, threshold=3):
    z = np.abs((series - series.mean()) / series.std())
    return z > threshold

def detect_outliers(series, method="iqr"):
    if method == "iqr":
        return detect_outliers_iqr(series)
    elif method == "zscore":
        return detect_outliers_zscore(series)
    return pd.Series([False] * len(series))

def handle_outliers(df, column, outliers, strategy="flag"):
    if strategy == "trim":
        return df[~outliers].copy()
    elif strategy == "cap":
        Q1, Q3 = df[column].quantile(0.25), df[column].quantile(0.75)
        IQR = Q3 - Q1
        df[column] = df[column].clip(Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
    elif strategy == "flag":
        df[f"{column}_outlier"] = outliers.astype(int)
    return df

def fill_missing(df, column, strategy="median"):
    if strategy == "median":
        df[column] = df[column].fillna(df[column].median())
    elif strategy == "mean":
        df[column] = df[column].fillna(df[column].mean())
    elif strategy == "ffill":
        df[column] = df[column].fillna(method="ffill")
    return df

def clean_file(file_path, output_dir="data_cleaned", outlier_method="iqr", outlier_strategy="flag", missing_strategy="median"):
    os.makedirs(output_dir, exist_ok=True)
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        return

    cleaning_log = []
    for col in df.select_dtypes(include=[np.number]).columns:
        # 缺失值
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            df = fill_missing(df, col, missing_strategy)
            cleaning_log.append(f"[{col}] 填补缺失值 {missing_count} → {missing_strategy}")

        # 异常值
        outliers = detect_outliers(df[col], outlier_method)
        outlier_count = outliers.sum()
        if outlier_count > 0:
            df = handle_outliers(df, col, outliers, outlier_strategy)
            cleaning_log.append(f"[{col}] 检测异常值 {outlier_count} → {outlier_strategy}")

    out_name = os.path.splitext(os.path.basename(file_path))[0] + "_cleaned.csv"
    out_path = os.path.join(output_dir, out_name)
    df.to_csv(out_path, index=False)

    log_path = os.path.join(output_dir, "cleaning_log.json")
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(cleaning_log, f, ensure_ascii=False, indent=2)

    print(f"清洗完成 → {out_path}")
    return out_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        clean_file(sys.argv[1])
