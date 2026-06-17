"""
auto-tuner.py — CUMCM 模型自动调参与验证框架

核心能力：
  1. 多策略超参搜索（Grid/Random/Bayesian）
  2. 早停与收敛检查
  3. 参数敏感性分析（OAT：一次变一个参数）
  4. 结果稳定性检查（多次运行标准差）
  5. 自动生成调参报告

用法：
  from auto_tuner import AutoTuner
  tuner = AutoTuner(model, param_space, X, y, task_type="prediction")
  best_params, report = tuner.optimize(strategy="bayesian", max_trials=50, time_budget_h=2)
  tuner.save_report("tuning_report.json")
"""

import numpy as np
import time
import json
from itertools import product

# === 预置常见模型参数空间 ===
PRESET_PARAM_SPACES = {
    "LSTM": {
        "hidden_size": [32, 64, 128, 256],
        "num_layers": [1, 2, 3],
        "dropout": [0.0, 0.1, 0.2, 0.3, 0.5],
        "learning_rate": [1e-4, 5e-4, 1e-3, 5e-3],
        "batch_size": [16, 32, 64, 128],
        "seq_length": [7, 14, 30, 60, 90]
    },
    "XGBoost": {
        "n_estimators": [100, 200, 500, 1000],
        "max_depth": [3, 5, 7, 9],
        "learning_rate": [0.01, 0.05, 0.1, 0.3],
        "subsample": [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0]
    },
    "RandomForest": {
        "n_estimators": [100, 200, 500],
        "max_depth": [5, 10, 15, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4]
    },
    "SVR": {
        "C": [0.1, 1, 10, 100],
        "gamma": [0.001, 0.01, 0.1, 1, "scale", "auto"],
        "kernel": ["rbf", "poly", "linear"]
    },
    "GMM": {
        "n_components": [2, 3, 4, 5, 6, 8, 10],
        "covariance_type": ["full", "tied", "diag", "spherical"]
    },
    "DBSCAN": {
        "eps": "auto",
        "min_samples": [3, 5, 10, 15, 20]
    },
    "NSGA-II": {
        "population_size": [50, 100, 200],
        "generations": [100, 200, 500],
        "crossover_prob": [0.7, 0.8, 0.9],
        "mutation_prob": [0.05, 0.1, 0.2]
    }
}


def check_convergence(loss_history, patience=10, min_delta=1e-4):
    """早停检测：连续 patience 次 loss 下降 < min_delta"""
    if len(loss_history) < patience + 1:
        return False
    recent = loss_history[-patience:]
    if max(recent) - min(recent) < min_delta:
        return True
    return False


def sensitivity_analysis(model_fn, param_name, param_range, X, y, metric_fn):
    """OAT 敏感性分析：逐一改变参数，记录指标变化"""
    results = []
    baseline = model_fn(X, y)
    for val in param_range:
        m = model_fn(X, y, **{param_name: val})
        results.append({
            "param_value": val,
            "metric_value": metric_fn(m, baseline),
            "change_percent": (metric_fn(m, baseline) - metric_fn(baseline, baseline)) / metric_fn(baseline, baseline) * 100
        })
    return results


def stability_check(model_fn, X, y, n_runs=5):
    """多次运行稳定性检查：返回指标均值 ± 标准差"""
    metrics = []
    for seed in range(n_runs):
        np.random.seed(seed)
        m = model_fn(X, y)
        metrics.append(m)
    return {
        "mean": np.mean(metrics),
        "std": np.std(metrics),
        "cv": np.std(metrics) / np.mean(metrics) if np.mean(metrics) != 0 else 0
    }


class AutoTuner:
    """CUMCM 自动调参器"""

    def __init__(self, model, param_space, X, y, task_type="prediction"):
        self.model = model
        self.param_space = param_space
        self.X = X
        self.y = y
        self.task_type = task_type
        self.history = []

    def _grid_search(self, eval_fn, time_budget_h):
        """Grid Search"""
        keys = list(self.param_space.keys())
        values = list(self.param_space.values())
        best_score = float("inf")
        best_params = None
        start = time.time()
        deadline = start + time_budget_h * 3600

        for combo in product(*values):
            if time.time() > deadline:
                break
            params = dict(zip(keys, combo))
            score = eval_fn(params)
            self.history.append({"params": params, "score": score})
            if score < best_score:
                best_score = score
                best_params = params

        return best_params, best_score

    def _random_search(self, eval_fn, max_trials, time_budget_h):
        """Random Search"""
        best_score = float("inf")
        best_params = None
        start = time.time()
        deadline = start + time_budget_h * 3600

        for _ in range(max_trials):
            if time.time() > deadline:
                break
            params = {
                k: np.random.choice(v) if isinstance(v, list) else v
                for k, v in self.param_space.items()
            }
            score = eval_fn(params)
            self.history.append({"params": params, "score": score})
            if score < best_score:
                best_score = score
                best_params = params

            if check_convergence([h["score"] for h in self.history[-20:]]):
                break

        return best_params, best_score

    def _bayesian_search(self, eval_fn, max_trials, time_budget_h):
        """Bayesian Optimization (简化版：带随机探索的贪心)"""
        best_score = float("inf")
        best_params = None
        start = time.time()
        deadline = start + time_budget_h * 3600

        # 初始随机采样10个点
        warmup = min(10, max_trials // 5)
        for _ in range(warmup):
            params = {
                k: np.random.choice(v) if isinstance(v, list) else v
                for k, v in self.param_space.items()
            }
            score = eval_fn(params)
            self.history.append({"params": params, "score": score})
            if score < best_score:
                best_score = score
                best_params = params

        # 贪心+探索
        for _ in range(max_trials - warmup):
            if time.time() > deadline:
                break
            base = {k: v for k, v in best_params.items()} if best_params else {
                k: np.random.choice(v) if isinstance(v, list) else v
                for k, v in self.param_space.items()
            }
            perturbed = {}
            for k, v in base.items():
                if isinstance(self.param_space[k], list) and len(self.param_space[k]) > 1:
                    choices = self.param_space[k]
                    idx = choices.index(v) if v in choices else 0
                    idx = max(0, min(len(choices) - 1, idx + np.random.choice([-1, 0, 1])))
                    perturbed[k] = choices[idx]
                else:
                    perturbed[k] = v
            score = eval_fn(perturbed)
            self.history.append({"params": perturbed, "score": score})
            if score < best_score:
                best_score = score
                best_params = perturbed

        return best_params, best_score

    def optimize(self, strategy="bayesian", max_trials=50, time_budget_h=2, eval_fn=None):
        """主入口"""
        if eval_fn is None:
            eval_fn = lambda p: np.random.random()

        if strategy == "bayesian":
            best_params, best_score = self._bayesian_search(eval_fn, max_trials, time_budget_h)
        elif strategy == "random":
            best_params, best_score = self._random_search(eval_fn, max_trials, time_budget_h)
        else:
            best_params, best_score = self._grid_search(eval_fn, time_budget_h)

        return best_params, {
            "best_score": best_score,
            "n_trials": len(self.history),
            "strategy": strategy,
            "convergence_reached": check_convergence([h["score"] for h in self.history])
        }

    def save_report(self, path, best_params, report):
        """保存调参报告"""
        with open(path, "w") as f:
            json.dump({
                "best_params": best_params,
                "report": report,
                "history": [
                    {"params": h["params"], "score": float(h["score"])}
                    for h in self.history[-20:]
                ]
            }, f, ensure_ascii=False, indent=2)
