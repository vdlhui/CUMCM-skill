"""
data_scanner.py — 附件目录扫描
输出：scan_report.md
"""
import os
import sys

def scan_directory(dir_path: str) -> dict:
    """扫描目录，识别 CSV/XLSX/TXT/JSON 文件"""
    files_info = []
    for root, dirs, files in os.walk(dir_path):
        for f_name in files:
            ext = os.path.splitext(f_name)[1].lower()
            if ext in ['.csv', '.xlsx', '.txt', '.json']:
                f_path = os.path.join(root, f_name)
                size_kb = os.path.getsize(f_path) / 1024
                files_info.append({
                    "name": f_name,
                    "ext": ext,
                    "path": f_path,
                    "size_kb": round(size_kb, 1)
                })
    return {"total_files": len(files_info), "files": files_info}

def generate_report(scan_result: dict, output_path: str = "scan_report.md"):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# 附件扫描报告\n\n共 {scan_result['total_files']} 个文件\n\n")
        for item in scan_result["files"]:
            f.write(f"- **{item['name']}** ({item['ext']}, {item['size_kb']} KB)\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    report = scan_directory(target)
    generate_report(report)
    print(f"扫描完成 → {report['total_files']} 个文件")
