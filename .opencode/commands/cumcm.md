---
name: cumcm
description: 数学建模竞赛论文生成系统——交互式启动/自动化执行/进度查看/断点恢复
argument: 启动模式（可选：auto）+ 赛题内容或文件路径
---

# /cumcm — CUMCM 数学建模快捷入口

当用户输入 `/cumcm` 时，执行以下逻辑：

## 无参数 或 直接跟赛题

```
/cumcm [赛题粘贴内容]
/cumcm problem_files/2024A.pdf
```

→ 加载 cumcm-orchestrator，以交互式模式启动流水线。

---

## auto 模式

```
/cumcm auto [赛题内容或路径]
```

→ 加载 cumcm-orchestrator，以自动化一键执行模式启动流水线。仅在门禁阻塞时暂停等待介入。

---

## status

```
/cumcm status
```

→ 加载 cumcm-orchestrator，输出 GCD 当前进度：
  - 各阶段完成状态
  - 当前时间模式
  - 已注入知识库
  - 风险标注一览
  - 回环历史

---

## resume

```
/cumcm resume
```

→ 读取 runtime-log，从断点恢复上次进度。
