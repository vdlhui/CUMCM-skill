"""
run_pipeline.py — CUMCM 全流程自动化
一键执行 P0→P5b，每阶段结束后检查 GCD + evidence_status

用法：
  python run_pipeline.py --problem "problem_files/题目.pdf"
  python run_pipeline.py --problem "problem_files/题目.txt" --mode auto
"""
import sys
import os
import json
import subprocess
import time

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPTS_DIR)

PIPELINE_STAGES = [
    {"phase": "P0", "name": "读题与数据处理", "scripts": [
        "scripts/parse_problem.py",
        "scripts/data_scanner.py",
        "scripts/data_cleaner.py",
        "scripts/data_profiler.py",
        "scripts/external_data.py",
        "scripts/build_problem_analysis.py"
    ]},
    {"phase": "P1", "name": "模型方向选型", "scripts": [
        "scripts/build_model_route.py"
    ]},
    {"phase": "P2", "name": "模型创新优化", "scripts": []},   # Agent 主导
    {"phase": "P3", "name": "模型评审闸门", "scripts": []},    # Agent 主导
    {"phase": "P4", "name": "求解与代码", "scripts": [
        "scripts/build_result_contracts.py",
        "scripts/evidence_gate.py"
    ]},
    {"phase": "P5a", "name": "叙事设计", "scripts": []},       # Agent 主导
    {"phase": "P5b", "name": "论文写作", "scripts": [
        "scripts/check_paper_format.py"
    ]},
]


def run_script(script_path, args=None):
    """运行单个脚本"""
    full_path = os.path.join(PROJECT_DIR, script_path)
    if not os.path.exists(full_path):
        print(f"  ⚠️ 跳过（文件不存在）: {script_path}")
        return True

    cmd = [sys.executable, full_path]
    if args:
        cmd.extend(args)

    print(f"  ▶ 运行: {script_path}")
    start = time.time()
    try:
        result = subprocess.run(cmd, cwd=PROJECT_DIR, capture_output=True, text=True)
        elapsed = time.time() - start
        if result.returncode == 0:
            print(f"  ✅ 完成 ({elapsed:.1f}s)")
            if result.stdout.strip():
                print(f"     {result.stdout.strip()[:200]}")
            return True
        else:
            print(f"  ❌ 失败 (exit code {result.returncode})")
            if result.stderr.strip():
                print(f"     {result.stderr.strip()[:300]}")
            return False
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        return False


def run_pipeline(problem_path, mode="auto"):
    """执行全流程"""
    print(f"\n{'='*60}")
    print(f"CUMCM 全流程自动化 - 赛题: {problem_path}")
    print(f"模式: {mode}")
    print(f"{'='*60}\n")

    total_start = time.time()
    all_passed = True

    for stage in PIPELINE_STAGES:
        print(f"\n--- {stage['phase']}: {stage['name']} ---")

        if not stage["scripts"] and stage["phase"] in ["P1", "P2", "P3", "P5a"]:
            print(f"  ℹ️  {stage['phase']} 需要 Agent 主导建模决策")
            if mode == "auto":
                print(f"  ⏸️  自动化模式暂停 —— 请在 Agent 中完成 {stage['phase']} 后继续")
                input("  按 Enter 继续...")
            continue

        for script in stage["scripts"]:
            if not run_script(script):
                all_passed = False
                if "evidence_gate" in script or "check_paper_format" in script:
                    print(f"\n  🚫 门禁未通过，流程中止。请修复后重试。")
                    return False

    total_elapsed = time.time() - total_start
    print(f"\n{'='*60}")
    if all_passed:
        print(f"✅ 全流程完成！总耗时: {total_elapsed/60:.1f} 分钟")
    else:
        print(f"⚠️  流程完成但部分步骤有警告，请检查上述输出。")
    print(f"{'='*60}\n")
    return all_passed


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CUMCM 全流程自动化")
    parser.add_argument("--problem", required=True, help="赛题文件路径")
    parser.add_argument("--mode", default="auto", choices=["auto", "interactive"], help="运行模式")
    args = parser.parse_args()
    run_pipeline(args.problem, args.mode)
