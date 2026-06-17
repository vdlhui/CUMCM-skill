"""
dimensional-check.py — 量纲一致性自动检查
验证输出/中间变量/参数的物理量纲
"""
import sys


KNOWN_UNITS = {
    "长度": ["m", "km", "cm", "mm"],
    "时间": ["s", "min", "h", "day"],
    "质量": ["kg", "g", "t"],
    "温度": ["°C", "K", "F"],
    "速度": ["m/s", "km/h"],
    "力": ["N", "kN"],
    "能量": ["J", "kJ", "kWh"],
    "功率": ["W", "kW"],
    "压力": ["Pa", "kPa", "MPa", "atm"],
    "频率": ["Hz", "kHz"],
    "无量纲": ["—", "-", "无", "无量纲"]
}


def check(declarations: list) -> dict:
    """检查变量声明列表的量纲一致性"""
    issues = []
    for item in declarations:
        unit = item.get("unit", "")
        quantity = item.get("quantity", "")
        var = item.get("variable", "")

        if unit and quantity:
            expected_units = KNOWN_UNITS.get(quantity, [])
            if expected_units and unit not in expected_units:
                issues.append({
                    "variable": var,
                    "declared_unit": unit,
                    "expected_units": expected_units,
                    "severity": "error"
                })

    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "checked_count": len(declarations)
    }


if __name__ == "__main__":
    # 示例：从命令行接收变量声明
    print("量纲一致性检查器")
    print("请确保模型中所有数值变量声明了物理量和单位")
    print("支持的物理量：", list(KNOWN_UNITS.keys()))
