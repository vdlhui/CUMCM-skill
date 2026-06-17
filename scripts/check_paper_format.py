"""
check_paper_format.py — 内容格式门禁
检查项：字数/标题层级/图表引用/摘要字数/参考文献/反模板句
只检查内容质量，不做字体/页边距/页眉等排版检查
"""
import sys
import re
import os

FORBIDDEN_PHRASES = [
    "模型假设较为理想化",
    "未考虑实际中的复杂因素",
    "未来可进一步完善",
    "由于时间有限",
]


def count_chinese_chars(text):
    """统计中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def check_paper_format(paper_path="paper_output/final_paper_source.md"):
    """执行格式门禁"""
    if not os.path.exists(paper_path):
        print(f"[FAIL] 格式门禁：{paper_path} 不存在")
        sys.exit(1)

    with open(paper_path, 'r', encoding='utf-8') as f:
        text = f.read()

    issues = []
    warnings = []

    # 1. 字数检查
    char_count = count_chinese_chars(text)
    if char_count < 8000:
        issues.append(f"正文字数 {char_count} < 8000，内容不足")
    elif char_count < 10000:
        warnings.append(f"正文字数 {char_count}，建议 ≥ 10000 字")
    elif char_count > 15000:
        warnings.append(f"正文字数 {char_count} > 15000，建议精简")
    else:
        print(f"[PASS] 正文字数：{char_count} 字（合理范围）")

    # 2. 标题层级检查
    has_h1 = bool(re.search(r'^#{1,2} \d+\.?\s', text, re.MULTILINE))
    has_h2 = bool(re.search(r'^#{2,3} \d+\.\d+\.?\s', text, re.MULTILINE))
    has_h3 = bool(re.search(r'^#{3,4} \d+\.\d+\.\d+\.?\s', text, re.MULTILINE))
    if not has_h1:
        issues.append("缺少一级标题（如 '## 1 问题重述'）")
    if not has_h2:
        issues.append("缺少二级标题（如 '### 1.1 背景说明'）")
    if not has_h3:
        warnings.append("缺少三级标题，建议有 5.1.1 级别子节")
    else:
        print("[PASS] 标题层级：完整")

    # 3. 图表引用检查
    figure_refs = re.findall(r'图\s*\d+|Figure\s*\d+|fig\w*\.\s*\d+', text)
    table_refs = re.findall(r'表\s*\d+|Table\s*\d+', text)
    if not figure_refs:
        warnings.append("正文中未发现图表引用")
    else:
        print(f"[PASS] 图表引用：图 {len(set(figure_refs))} 处，表 {len(set(table_refs))} 处")

    # 4. 摘要字数
    abstract_match = re.search(r'##\s*摘要.*?(?=##\s*\d)', text, re.DOTALL)
    if abstract_match:
        abstract_chars = count_chinese_chars(abstract_match.group())
        if abstract_chars < 400:
            issues.append(f"摘要 {abstract_chars} 字 < 400，内容不足")
        elif abstract_chars > 800:
            warnings.append(f"摘要 {abstract_chars} 字 > 800，建议控制在 550-700 字")
        else:
            print(f"[PASS] 摘要字数：{abstract_chars} 字")
    else:
        issues.append("未找到摘要章节")

    # 5. 参考文献
    ref_section = re.search(r'##\s*(参考文献|References).*', text, re.DOTALL)
    if not ref_section:
        issues.append("缺少参考文献章节")
    else:
        ref_items = re.findall(r'\[\d+\]', ref_section.group())
        if len(ref_items) < 5:
            issues.append(f"参考文献仅 {len(ref_items)} 条，要求 ≥ 5 条")
        else:
            print(f"[PASS] 参考文献：{len(ref_items)} 条")

    # 6. 反模板句检查
    found_forbidden = []
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text:
            found_forbidden.append(phrase)
    if found_forbidden:
        issues.append(f"发现反模板句：{found_forbidden}")
    else:
        print("[PASS] 反模板句检查：通过")

    # 汇总
    print(f"\n{'='*50}")
    if issues:
        print(f"[FAIL] 格式门禁未通过 ({len(issues)} 项错误)：")
        for i in issues:
            print(f"  [FAIL] {i}")
        sys.exit(1)
    else:
        if warnings:
            print(f"[WARN]  格式门禁通过（{len(warnings)} 项警告）：")
            for w in warnings:
                print(f"  [WARN]  {w}")
        else:
            print("✅ 格式门禁通过：全部检查项合格。")
    print(f"{'='*50}\n")
    return len(issues) == 0


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "paper_output/final_paper_source.md"
    check_paper_format(path)
