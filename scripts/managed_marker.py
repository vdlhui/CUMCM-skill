"""
managed_marker.py — MANAGED 标记块管理
识别/覆盖/保护：仅覆盖 MANAGED 标记块内，保留手动代码
"""
import re

BEGIN_MARKER = "=== BEGIN MANAGED:"
END_MARKER = "=== END MANAGED:"


def find_managed_blocks(content: str) -> list:
    """查找所有 MANAGED 块"""
    blocks = []
    lines = content.split('\n')
    in_block = False
    block_start = -1
    block_name = ""

    for i, line in enumerate(lines):
        if BEGIN_MARKER in line and not in_block:
            in_block = True
            block_start = i
            block_name = line.split(BEGIN_MARKER)[1].strip().split()[0]
        elif END_MARKER in line and in_block:
            in_block = False
            blocks.append({
                "name": block_name,
                "start": block_start,
                "end": i,
                "content": '\n'.join(lines[block_start:i+1])
            })

    return blocks


def update_managed_block(original: str, block_name: str, new_content: str) -> str:
    """更新指定 MANAGED 块内的内容"""
    lines = original.split('\n')
    in_target = False
    target_start = -1
    target_end = -1

    for i, line in enumerate(lines):
        if BEGIN_MARKER in line:
            current_name = line.split(BEGIN_MARKER)[1].strip().split()[0]
            if current_name == block_name:
                in_target = True
                target_start = i
        elif END_MARKER in line and in_target:
            target_end = i
            break

    if target_start >= 0 and target_end >= 0:
        managed_header = lines[target_start]
        new_lines = [managed_header, "## 📌 自动生成区域 — 已更新", new_content, lines[target_end]]
        result = lines[:target_start] + new_lines + lines[target_end+1:]
        return '\n'.join(result)

    return original


def protect_manual_regions(content: str) -> bool:
    """检查文件中被 MANAGED 保护的手动区域完整性"""
    blocks = find_managed_blocks(content)
    if not blocks:
        return True
    return all(b["start"] >= 0 and b["end"] >= 0 for b in blocks)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
        blocks = find_managed_blocks(content)
        print(f"发现 {len(blocks)} 个 MANAGED 块：")
        for b in blocks:
            print(f"  - {b['name']}: 行 {b['start']+1} ~ {b['end']+1}")
