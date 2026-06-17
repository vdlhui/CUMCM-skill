"""
evidence_gate.py — 自动化证据门禁
检查 model_results.json 中每问的 evidence_status
非零退出码 = 阻断，需修复后才能继续
"""
import sys
import json
import os


def check_evidence(results_path="paper_output/results/model_results.json"):
    """检查证据门禁"""
    if not os.path.exists(results_path):
        print(f"❌ 证据门禁：{results_path} 不存在")
        sys.exit(1)

    with open(results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data.get("questions", {})
    if not questions:
        print("❌ 证据门禁：model_results.json 中无 questions 字段")
        sys.exit(1)

    missing = []
    needs_modeling = []
    complete = []

    for qid, qdata in questions.items():
        status = qdata.get("evidence_status", "missing")
        if status == "missing":
            missing.append(qid)
        elif status == "needs_modeling" or status == "scaffold":
            needs_modeling.append(qid)
        elif status == "complete":
            complete.append(qid)

    print(f"\n{'='*50}")
    print(f"证据门禁报告")
    print(f"{'='*50}")
    print(f"✅ complete: {complete if complete else '无'}")
    print(f"⚠️  needs_modeling/scaffold: {needs_modeling if needs_modeling else '无'}")
    print(f"❌ missing: {missing if missing else '无'}")

    if missing:
        print(f"\n🚫 门禁未通过：以下问题的证据缺失：{missing}")
        print("   请确保所有问题的 model_results.json 中 evidence_status 不为 missing/scaffold。")
        sys.exit(1)

    if needs_modeling:
        print(f"\n⚠️  警告：以下问题的证据标记为 needs_modeling/scaffold：{needs_modeling}")
        print("   当前可以继续，但建议替换为真实建模结果后再提交最终稿。")
        return False

    print(f"\n✅ 证据门禁通过：所有 {len(complete)} 个问题证据完整。")
    return True


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "paper_output/results/model_results.json"
    check_evidence(path)
