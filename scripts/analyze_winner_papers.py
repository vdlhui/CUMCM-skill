"""
analyze_winner_papers.py — 获奖论文模式提取器
输入：论文纯文本（复制粘贴，不需要OCR）
功能：套路识别 / 模型链提取 / 创新点匹配 / 摘要结构分析 / 评价风格检测
输出：winner_extraction.json
"""
import re
import json
import sys
import os


def extract_pattern(text: str) -> dict:
    """提取赛题套路"""
    signal_map = {
        "预测→优化": ["预测", "优化"],
        "评价→预测": ["评价", "预测"],
        "运筹优化": ["最短", "最少", "最优化", "最大效率"],
        "微分方程": ["物理", "传热", "流体", "运动"],
        "评价体系": ["指标", "权重", "综合评价", "打分"],
        "分类+特征": ["分类", "聚类", "特征"],
        "仿真建模": ["仿真", "模拟", "蒙特卡洛"],
        "图论与网络": ["路径", "网络", "连通", "节点"],
        "时间序列": ["时间序列", "趋势", "周期", "波动"],
        "统计建模": ["概率", "随机", "统计"],
    }
    scores = {}
    for pattern, signals in signal_map.items():
        score = sum(1 for s in signals if s in text)
        if score > 0:
            scores[pattern] = score
    best = max(scores, key=scores.get) if scores else None
    return {"primary_pattern": best or "unknown", "confidence": "medium", "all_matches": scores}


def extract_model_chain(text: str) -> list:
    """提取论文中使用的模型"""
    model_keywords = [
        "LSTM", "ARIMA", "Prophet", "XGBoost", "LightGBM", "随机森林", "SVM",
        "NSGA-II", "TOPSIS", "AHP", "熵权法", "CRITIC", "K-means", "DBSCAN",
        "GMM", "蒙特卡洛", "有限差分", "有限元", "PageRank", "Dijkstra"
    ]
    found = []
    for kw in model_keywords:
        if kw in text:
            found.append(kw)
    return found


def detect_evaluation_style(text: str) -> str:
    """检测模型评价风格：国一 vs 省二"""
    template_phrases = ["模型假设较为理想化", "未来可进一步完善", "未考虑实际中的复杂因素"]
    quality_signals = ["预判", "实测验证", "消融实验", "量化", "偏差", "误差控制"]
    score = 0
    for phrase in template_phrases:
        if phrase in text:
            score -= 2
    for signal in quality_signals:
        if signal in text:
            score += 1
    if score >= 3:
        return "国一风格"
    elif score >= 0:
        return "国二水平"
    else:
        return "省二及以下"


def analyze(text: str) -> dict:
    """单篇论文分析"""
    return {
        "pattern": extract_pattern(text),
        "models_detected": extract_model_chain(text),
        "evaluation_style": detect_evaluation_style(text),
        "word_count": len(text)
    }


def analyze_directory(input_dir: str, output_path: str = "winner_extraction.json"):
    """批量分析"""
    results = {}
    for f_name in os.listdir(input_dir):
        if f_name.endswith(".txt") or f_name.endswith(".md"):
            f_path = os.path.join(input_dir, f_name)
            with open(f_path, 'r', encoding='utf-8') as f:
                text = f.read()
            results[f_name] = analyze(text)
            print(f"分析完成: {f_name}")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"批量分析完成 → {output_path}")
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.isfile(target):
            with open(target, 'r', encoding='utf-8') as f:
                result = analyze(f.read())
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif os.path.isdir(target):
            analyze_directory(target)
    else:
        print("用法: python analyze_winner_papers.py <论文文本文件|论文目录>")
