"""
boundary-check.py — 边界条件自动验证
检查约束上下界/可行域内抽样点合法性
"""
import sys
import json


def check_constraint_bounds(constraints: list, solution: dict) -> dict:
    """检查解是否满足所有约束"""
    violations = []
    for i, c in enumerate(constraints):
        var = c.get("variable")
        lower = c.get("lower_bound")
        upper = c.get("upper_bound")
        if var and var in solution:
            val = solution[var]
            if lower is not None and val < lower:
                violations.append({
                    "constraint_id": i,
                    "variable": var,
                    "value": val,
                    "bound": lower,
                    "type": "lower_bound_violation"
                })
            if upper is not None and val > upper:
                violations.append({
                    "constraint_id": i,
                    "variable": var,
                    "value": val,
                    "bound": upper,
                    "type": "upper_bound_violation"
                })

    return {
        "passed": len(violations) == 0,
        "violations": violations,
        "total_constraints": len(constraints)
    }


def check_physical_limits(solution: dict) -> dict:
    """检查物理不可能值"""
    checks = [
        ("probability_range", lambda v: 0 <= v <= 1),
        ("temperature_min", lambda v: v > -273.15),
        ("non_negative_distance", lambda v: v >= 0),
        ("non_negative_mass", lambda v: v >= 0),
    ]

    issues = []
    for var, val in solution.items():
        for check_name, check_fn in checks:
            if not check_fn(val):
                issues.append({
                    "variable": var,
                    "value": val,
                    "check": check_name,
                    "severity": "error"
                })

    return {
        "passed": len(issues) == 0,
        "issues": issues
    }


if __name__ == "__main__":
    print("边界条件验证器")
    print("调用 check_constraint_bounds(constraints, solution) 验证约束上下界")
    print("调用 check_physical_limits(solution) 验证物理不可能值")
