"""
model-validator.py — CUMCM 模型否决器

区分"调参不足"与"方向性错误"的硬标准。
调参是优化同一个模型，否决是判断"这个模型根本不适用于这道题"。

否决 → 自动回退路由（回退 P1 备选链 / P2 移除创新 / P0 检查数据）
"""

# === 预测任务否决标准 ===
PREDICTION_REJECTION_RULES = {
    "R2_too_low": {
        "threshold": 0.3,
        "verdict": "否决 - 方向性错误",
        "cause": "模型对数据结构几乎没有解释力（R² < 0.3）",
        "action": "回退 P1 备选链"
    },
    "residual_trend": {
        "verdict": "否决 - 遗漏系统性模式",
        "cause": "残差存在明显趋势（周期性/趋势性/变点），模型未捕捉",
        "action": "换用捕捉该模式的模型（如 LSTM → Prophet+变点检测，XGBoost → 时序分解+LSTM）"
    },
    "severe_overfit": {
        "threshold_ratio": 3.0,
        "verdict": "否决 - 严重过拟合",
        "cause": "测试集误差 > 训练集误差 × 3",
        "action": "回退 P1 更简单的模型链"
    },
    "degenerate_prediction": {
        "verdict": "否决 - 模型退化",
        "cause": "预测值全在历史均值附近，未学习到有效模式",
        "action": "检查数据预处理是否过度平滑，或模型结构过于简单"
    }
}

# === 优化任务否决标准 ===
OPTIMIZATION_REJECTION_RULES = {
    "infeasible": {
        "verdict": "否决 - 约束矛盾",
        "cause": "无可行解，约束存在矛盾或可行域为空",
        "action": "回退 P2 检查约束建模，或回退 P1 换用松弛/启发式"
    },
    "boundary_dependent": {
        "threshold_pct": 30,
        "verdict": "否决 - 解依赖边界",
        "cause": "最优解在边界上，放宽边界 5% 后解突变 > 30%",
        "action": "回退 P2 增加鲁棒性约束"
    },
    "timeout": {
        "threshold_min": 30,
        "verdict": "否决 - 规模过大",
        "cause": "单目标优化 > 30min 无进展",
        "action": "回退 P1 换用启发式/分解方法"
    }
}

# === 评价任务否决标准 ===
EVALUATION_REJECTION_RULES = {
    "cr_too_high": {
        "threshold": 0.2,
        "min_order": 3,
        "verdict": "否决 - 判断矩阵不可用",
        "cause": "一致性比率 CR > 0.2（3 阶以上），判断矩阵存在严重矛盾",
        "action": "回退 P1 换用客观赋权法（CRITIC/熵权法）"
    },
    "ranking_unstable": {
        "threshold_pct": 30,
        "verdict": "否决 - 评价结果不稳定",
        "cause": "TOPSIS 排序对权重扰动 ±10% 的敏感性 > 30% 排名变化",
        "action": "回退 P2 增加组合赋权 / 换用灰色关联分析"
    },
    "no_discrimination": {
        "threshold_cv_pct": 5,
        "verdict": "否决 - 评价体系无区分度",
        "cause": "评价分数全部集中在窄区间（变异系数 < 5%）",
        "action": "回退 P0 检查指标选择是否过于同质化"
    }
}

# === 分类/聚类任务否决标准 ===
CLASSIFICATION_REJECTION_RULES = {
    "accuracy_too_low": {
        "threshold_pct": 10,
        "verdict": "否决 - 方向性错误",
        "cause": "准确率 < 随机猜测 + 10%，特征与标签基本无关联",
        "action": "回退 P0 检查特征工程，或回退 P1 换用无监督方法"
    }
}

CLUSTERING_REJECTION_RULES = {
    "silhouette_negative": {
        "verdict": "否决 - 数据无聚类结构",
        "cause": "轮廓系数 < 0",
        "action": "回退 P1 换用密度估计/异常检测视角重新建模"
    },
    "db_index_high": {
        "threshold": 2.0,
        "verdict": "否决 - 数据无自然聚类倾向",
        "cause": "所有聚类方法的 Davies-Bouldin 指数均 > 2.0",
        "action": "回退 P1 考虑连续建模替代离散聚类"
    }
}


def check_prediction_rejection(metrics: dict) -> dict:
    """检查预测任务是否应被否决"""
    if metrics.get("R2", 1.0) < PREDICTION_REJECTION_RULES["R2_too_low"]["threshold"]:
        return PREDICTION_REJECTION_RULES["R2_too_low"]
    if metrics.get("test_train_error_ratio", 1.0) > PREDICTION_REJECTION_RULES["severe_overfit"]["threshold_ratio"]:
        return PREDICTION_REJECTION_RULES["severe_overfit"]
    return {"verdict": "pass"}


def check_optimization_rejection(metrics: dict) -> dict:
    """检查优化任务是否应被否决"""
    if metrics.get("feasible", True) == False:
        return OPTIMIZATION_REJECTION_RULES["infeasible"]
    if metrics.get("solve_time_min", 0) > OPTIMIZATION_REJECTION_RULES["timeout"]["threshold_min"]:
        return OPTIMIZATION_REJECTION_RULES["timeout"]
    return {"verdict": "pass"}


def check_evaluation_rejection(metrics: dict) -> dict:
    """检查评价任务是否应被否决"""
    if metrics.get("CR", 0) > EVALUATION_REJECTION_RULES["cr_too_high"]["threshold"] and metrics.get("matrix_order", 0) >= 3:
        return EVALUATION_REJECTION_RULES["cr_too_high"]
    if metrics.get("score_cv_pct", 100) < EVALUATION_REJECTION_RULES["no_discrimination"]["threshold_cv_pct"]:
        return EVALUATION_REJECTION_RULES["no_discrimination"]
    return {"verdict": "pass"}


def check_clustering_rejection(metrics: dict) -> dict:
    """检查聚类任务是否应被否决"""
    if metrics.get("silhouette_score", 1.0) < 0:
        return CLUSTERING_REJECTION_RULES["silhouette_negative"]
    return {"verdict": "pass"}


def validate(task_type: str, metrics: dict) -> dict:
    """模型否决主入口"""
    checkers = {
        "prediction": check_prediction_rejection,
        "optimization": check_optimization_rejection,
        "evaluation": check_evaluation_rejection,
        "classification": check_prediction_rejection,
        "clustering": check_clustering_rejection,
        "simulation": lambda m: {"verdict": "pass"},
        "generic": lambda m: {"verdict": "pass"}
    }
    checker = checkers.get(task_type, lambda m: {"verdict": "pass"})
    result = checker(metrics)
    return result
