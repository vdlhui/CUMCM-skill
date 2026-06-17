---
name: cumcm-solver
description: CUMCM 求解与代码。将模型翻译为可执行代码，按任务类型分发脚手架，自动调参，模型否决诊断，失败三分支回环，结果验证，输出论文素材包和证据契约。
---

# P4：求解与代码

## 角色分配
- 🟢 编程手主导：代码生成、求解执行、自动调参、模型否决、结果验证、素材包输出
- 🟡 建模手辅助：结果解读（建模视角）、异常值分析、关键结论提炼
- 🟢 论文手主导：并行开始写论文前 3 章初稿（问题重述 + 模型假设 + 符号说明）

## 输入
- P0 输出：problem_analysis.json / data_plan.json / data_cleaned/
- P1 输出：model_route.json（选定模型链/三维评分/基线）
- P2 输出：model-innovation.json（创新公式链）
- P3 输出：model-review.json（含风险标注列表）

## 执行步骤

### 第 1 步：脚手架分发

根据 P0 中每问的 task_type，分发对应脚手架：

| task_type | 脚手架模板 | 核心库 |
|-----------|----------|--------|
| 优化 | scaffold-templates/optimization.py | cvxpy / scipy.optimize / pulp / NSGA-II |
| 预测 | scaffold-templates/prediction.py | sklearn / statsmodels / LSTM / Prophet / XGBoost |
| 评价 | scaffold-templates/evaluation.py | AHP / TOPSIS / 熵权法 / 模糊综合评价 / CRITIC |
| 分类 | scaffold-templates/classification.py | sklearn + CatBoost / LightGBM |
| 聚类 | scaffold-templates/clustering.py | K-means / DBSCAN / 层次聚类 / GMM |
| 仿真 | scaffold-templates/simulation.py | 蒙特卡洛 / 元胞自动机 / 系统动力学 / ABM |
| 通用 | scaffold-templates/generic.py | numpy + pandas |

### 第 2 步：代码生成与首次求解

- 从脚手架复制模板 → 填入 P2 公式链 → 填入 P0 数据路径
- 参数化设计（数据路径/模型超参/输出路径均为变量）
- 运行首次求解
- 使用 `scripts/managed_marker.py`：仅覆盖 MANAGED 标记块，保留手动代码

### 第 3 步：自动调参

若首次求解结果不达标（R² < 0.7 / MAE 过大 / 收敛失败）：

```
调用 auto-tuner.py：
  - 根据模型类型加载 PRESET_PARAM_SPACES
  - 根据时间预算选择策略：
      剩余 P4 预算 > 4h → Bayesian 搜索
      剩余 P4 预算 2-4h → Random 搜索
      剩余 P4 预算 < 2h → Grid 粗搜（大步长）
  - 执行 optimize(max_trials=50, time_budget_h=剩余P4预算)
  - 输出：最优参数 + 收敛曲线 + 参数敏感度排序
```

### 第 4 步：模型否决检查

若调参后仍不达标（R² < 0.3 / 无可行解 / 严重过拟合 / 聚类轮廓系数 < 0 等），触发 model-validator.py：

```
预测任务否决检查（满足任一即否决）：
  □ R² < 0.3 → 方向性错误 → 回退 P1 备选链
  □ 残差存在明显趋势 → 遗漏系统性模式 → 换用捕捉该模式的模型
  □ 测试集误差 > 训练集误差 × 3 → 严重过拟合 → 回退 P1 更简单链
  □ 预测值全在均值附近(无波动) → 模型退化 → 检查数据预处理

优化任务否决检查：
  □ 无可行解 → 约束矛盾 → 回退 P2 修正约束
  □ 单目标 > 30min 无进展 → 规模过大 → 回退 P1 换启发式
  □ 最优解在边界 → 解依赖边界 → 回退 P2 增加鲁棒约束

评价任务否决检查：
  □ CR > 0.2(3 阶以上) → 判断矩阵不可用 → 回退 P1 换客观赋权
  □ 评价分数全集中在窄区间 → 无区分度 → 回退 P0 检查指标选择
```

否决后自动执行对应回退路由，携带否决报告。

### 第 5 步：结果验证

求解通过后，执行验证：

```
1. 量纲一致性：scripts/validation/dimensional-check.py
   - 基于 P0 输出单位体系，检查每个输出变量的物理量纲

2. 边界条件：scripts/validation/boundary-check.py
   - 在约束边界抽样 → 检查解的合法性
   - 在极端条件(0/±∞) → 检查模型行为合理性

3. 稳定性检查(by auto-tuner)：
   - 多次运行(seed=0,1,2,3,4) → 输出指标均值 ± 标准差
   - 若标准差 > 均值 × 20% → 警告数值不稳定

4. 合理性检查（人工审核提示）：
   - 负库存、负距离、概率 > 1、温度 < -273°C → 红灯提示
```

### 第 6 步：失败诊断（三分支）

若求解失败（崩溃/无解/溢出）：

```
结构性失败（无解/矛盾/物理意义不符）：
  → 回环 P2 调整模型结构
  → 携带诊断报告（哪个约束导致了矛盾？哪个变量的定义与实际不符？）

可解性失败（OOM/时间爆炸/收敛完全失败）：
  → 回环 P3 重新评审可解性
  → 携带诊断报告（实际规模 ××，预估规模 ××，差距来源是...）
  → P3 标记上次盲区

数值失败（初值敏感/震荡发散）：
  → P4 内循环
  → 换算法（Newton → 拟Newton、Explicit → Implicit）
  → 换求解器（scipy → cvxpy → gurobi）
  → 调整初始策略（随机多点 → 拉丁超立方采样）
```

### 第 7 步：论文素材包输出

求解成功且验证通过后，输出 P5a/P5b 可直接引用的素材：

```
1. model-results.json：
   - 每子问题的模型参数值、关键数值结果、公式引用（"式(12)"对应值）
   - evidence_status 标记：scaffold / needs_modeling / complete

2. metrics.json：
   - 每子问题的评价指标（MAE/RMSE/R²/AUC 等）
   - 基线模型对应指标
   - 改善幅度（百分比）

3. table-index.json：
   - 每张表格的 ID/标题/列定义/数据来源/题注建议

4. 敏感性分析报告：
   - 每个关键参数的变化范围 → 对应结果变化 → 结论判断
   - 格式："当 α 从 0.5 变化到 1.5 时，输出变化 ±X%"

5. tuning_report.json：
   - 最优参数组合 + 收敛曲线描述 + 参数敏感度排序
```

### 第 8 步：生成证据契约

调用 `scripts/build_result_contracts.py`：
- 从调参报告和求解结果自动组装 model-results.json / metrics.json / conclusions.json / table-index.json
- 所有 evidence_status 标记为 complete
- 所有指标含基线对比值
- 输出到 paper_output/results/ 和 paper_output/tables/

### 第 9 步：证据门禁

调用 `scripts/evidence_gate.py`：
- 检查 paper_output/results/model-results.json
- 每问 evidence_status 必须为 complete
- 任一问为 missing → 阻断（exit 1），返回 P4 重做该问
- 全部 complete → 放行

## 输出

| 文件 | 格式 | 内容 |
|------|------|------|
| 求解脚本 | .py/.m | q1_model.py / q2_model.py 等（含 managed marker） |
| `paper_output/results/model-results.json` | JSON | 模型参数/关键结果/公式引用/evidence_status |
| `paper_output/results/metrics.json` | JSON | 评价指标+基线对比+改善幅度 |
| `paper_output/results/conclusions.json` | JSON | 每问核心发现+量化结论 |
| `paper_output/tables/table-index.json` | JSON | 表格索引（ID/标题/列定义/题注） |
| `tuning_report.json` | JSON | 最优参数+收敛曲线+敏感性排序 |
| 验证报告 | .txt/.md | dimensional-check + boundary-check 结果 |

## 不能做的事
- 不要跳过调参直接宣布"模型最好"（除非首次结果已经达到优秀标准）
- 不要通过否决检查的模型——否决是硬标准，不是建议
- 不要在写作优先模式下运行新代码（Orchestrator 会在此模式下禁止调用 P4 新求解）
- 不要忽略 managed marker 保护手动代码
- 不要输出裸数据（没有标注、没有对比基准、没有公式引用的结果对 P5b 没用）
