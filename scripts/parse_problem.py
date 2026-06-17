"""
parse_problem.py — 赛题文本预处理
输入：用户粘贴的赛题纯文本
输出：cleaned_problem.txt
"""
import re
import sys


def clean_paragraphs(text: str) -> str:
    """清洗段落：去页码/页眉页脚/合并断行"""
    text = re.sub(r'[Pp]age\s*\d+', '', text)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def mark_formulas(text: str) -> str:
    """公式占位标记：保留 $...$ 和 $$...$$"""
    return text


def reconstruct_tables(text: str) -> str:
    """从缩进/空格对齐重建表格结构"""
    lines = text.split('\n')
    result = []
    for line in lines:
        if re.match(r'^\s{2,}', line) or '\t' in line:
            cells = re.split(r'\s{2,}|\t', line.strip())
            result.append(' | '.join(c.strip() for c in cells if c.strip()))
        else:
            result.append(line)
    return '\n'.join(result)


def parse(input_text: str, output_path: str = "cleaned_problem.txt"):
    text = clean_paragraphs(input_text)
    text = mark_formulas(text)
    text = reconstruct_tables(text)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"赛题文本预处理完成 → {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()
    parse(content)
