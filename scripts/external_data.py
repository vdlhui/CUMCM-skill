"""
external_data.py — 外部数据获取
内置数据源优先级：国内建模优先 → 国家统计局 > 地方统计局 > 国际组织
输出：sources.json
"""
import json
import sys

DATA_SOURCE_PRIORITY = {
    "国内宏观": ["国家统计局 API", "各省统计年鉴"],
    "国际宏观": ["World Bank API", "IMF Data API"],
    "天气环境": ["Open-Meteo API", "中国气象局"],
    "地理空间": ["天地图 API", "OpenStreetMap Nominatim"],
}


def resolve_source(query_type: str) -> str:
    """根据查询类型返回推荐数据源"""
    sources = DATA_SOURCE_PRIORITY.get(query_type, [])
    if not sources:
        for k, v in DATA_SOURCE_PRIORITY.items():
            if query_type in k:
                sources = v
                break
    return sources[0] if sources else "无匹配数据源"


def generate_sources_log(requests: list, output_path="sources.json"):
    """生成外部数据来源清单"""
    log = {
        "requests": requests,
        "note": "外部数据获取记录。如 API 不可用，应使用本地数据替代并标注。"
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"外部数据记录完成 → {output_path}")


if __name__ == "__main__":
    # 示例：接收数据需求描述
    if len(sys.argv) > 1:
        query = sys.argv[1]
        source = resolve_source(query)
        print(f"查询类型：{query} → 推荐数据源：{source}")
    else:
        print("可用数据源：")
        for k, v in DATA_SOURCE_PRIORITY.items():
            print(f"  {k}: {', '.join(v)}")
