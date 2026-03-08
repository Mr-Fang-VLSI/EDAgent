# Request Pattern Routing

This is the canonical request-pattern to workflow-owner mapping for the repo.

## Request Pattern -> Workflow Owner

1. "固定 checkpoint / golden / 从某阶段恢复"
- Workflow owner: `eda-stage-checkpoint-golden`
- `eda_loop_role`: `not_used`

2. "GT3 背部层策略 / CTS-PDN层分工 / 提交+监控一致性任务"
- Workflow owner: `gt3-backside-route-policy`
- `eda_loop_role`: `owner` when the task is a scoped execution batch, otherwise `not_used`

3. "模型一致性 / contract / bucketed scorecard / Gate-0/1"
- Workflow owner: `delay-model-gate-evaluator`
- `eda_loop_role`: `not_used`

4. "交互门禁 / 维护日志 / 工具复用检查"
- Workflow owner: `eda-knowledge-gate-maintainer`
- `eda_loop_role`: `not_used`

5. "需要先检索 KB 上下文 / 先查工具库可复用工具 / 给后续 skill 准备共享上下文"
- Workflow owner: `eda-context-accessor`
- `eda_loop_role`: `not_used`
- If feedback says KB should change, follow with `eda-infra-maintainer`

6. "实验前先做数据诊断 / 方法反思 / 生成下一步A-B-C建议"
- Workflow owner: `control-preflight-reflect`
- `eda_loop_role`: `not_used`

7. "背部 signal/clock cost model 规划与联网分析 / HPWL 稳定性对比 / 多设计基准扩展"
- Workflow owner: `bscost-net`
- `eda_loop_role`: `not_used`

8. "背部cost理论建模 / 优化拟合 / 稳定超越HPWL门控验证"
- Workflow owner: `bscost-theory-opt`
- `eda_loop_role`: `not_used`

9. "实验后复盘 / 失败机理分类 / 是否递归下一轮 workflow-scoped-execution 决策"
- Workflow owner: `control-postrun-retro`
- `eda_loop_role`: `not_used`

10. "从理论上判断提议是否不合理 / 是否应否决执行"
- Workflow owner: `control-theory-veto`
- `eda_loop_role`: `not_used`

11. "新建或改造 skill"
- Use: `skill-creator`

12. "安装外部 skill"
- Use: `skill-installer`

13. "缺少依据，需要联网找论文/下载论文建立证据集"
- Workflow owner: `eda-paper-fetch`
- `eda_loop_role`: `not_used`

14. "总结本地 PDF 论文并提炼结论/局限/可执行实验"
- Workflow owner: `eda-pdf-local-summary`
- `eda_loop_role`: `not_used`

15. "用 git 做版本管理 / 建立 checkpoint / 记录每个版本特点和区分点"
- Workflow owner: `git-version-control`
- `eda_loop_role`: `not_used`

16. "执行结果真假判定 / 防止假成功 / 路由结果契约化验收"
- Workflow owner: `workflow-scoped-execution`
- delegated tool: `scripts/debug/validate_execution_contract.py`
- `eda_loop_role`: `owner`

17. "提交流程前检查 PDK/LEF/DEF/SDC 兼容性"
- Workflow owner: `workflow-scoped-execution`
- delegated tool: `scripts/debug/pdk_flow_preflight.py`
- `eda_loop_role`: `owner`

18. "实验记忆库 / 约束下自动提案下一轮参数"
- Workflow owner: `workflow-scoped-execution`
- delegated tools: `scripts/common/experiment_memory.py`, `scripts/debug/propose_constrained_experiments.py`
- `eda_loop_role`: `owner`

19. "维护或发展 agent/知识库/工具库/skills 基础设施"
- Workflow owner: `eda-infra-maintainer`
- `eda_loop_role`: `not_used`
- Also run: `scripts/common/infra_stack_guard.py` and `scripts/common/skill_system_audit.py`

20. "清理知识库 / 工具库 / 日志；合并重复；删除过时；矫正命名"
- Workflow owner: `eda-artifact-hygiene-maintainer`
- `eda_loop_role`: `not_used`
- Follow with `eda-infra-maintainer` only if cleanup reveals a governance or structural policy problem

21. "我要一整条科研闭环：知识探索->文献检索->解析->idea辩论->假设实验->实现->版本管理->验证"
- Workflow owner: `workflow-research-chain`
- `eda_loop_role`: `delegated_stage` only for execution/validation stages inside the chain
- Also run: `scripts/common/init_research_chain.py` and `scripts/common/research_chain_guard.py`

22. "知识探索 / 证据缺口梳理 / 生成论文下载队列"
- Workflow owner: `control-knowledge-explorer`
- `eda_loop_role`: `not_used`

23. "新思路头脑风暴 / 正反方辩论打磨"
- Workflow owner: `eda-idea-debate-lab`
- `eda_loop_role`: `not_used`

24. "把idea变成可证伪假设与实验矩阵"
- Workflow owner: `eda-hypothesis-experiment-designer`
- `eda_loop_role`: `not_used`

25. "根据实验设计实现方法并进入版本化迭代"
- Workflow owner: `eda-method-implementer`
- additional skill: `git-version-control`
- `eda_loop_role`: `delegated_stage` only if implementation requires governed execution

26. "朝 8%功耗下降/5%频率提升目标逐步推进并门控"
- Workflow owner: `bspdn-goal-driver`
- `eda_loop_role`: `delegated_stage` when a milestone step becomes a concrete execution run
- Also run: `scripts/debug/track_bspdn_goal_progress.py`

## Selection Rules

1. Prefer the minimal set.
2. If uncertain, include `eda-knowledge-gate-maintainer` as baseline governance skill.
3. Choose one `workflow_owner_skill` first; do not default to `workflow-scoped-execution`.
4. Keep execution tools under `workflow-scoped-execution` only when `workflow-scoped-execution` is the active workflow owner or a delegated execution stage.

## Quick Routing Examples

Use these to distinguish routing, owner selection, and execution orchestration:

1. "just run this one batch"
- router: `workflow-router`
- workflow owner: `workflow-scoped-execution`
- `workflow-scoped-execution` role: `owner`

2. "do a whole research program"
- router: `workflow-router`
- workflow owner: `workflow-research-chain`
- `workflow-scoped-execution` role: `delegated_stage` only if a bounded execution stage appears later

3. "judge whether the plan is theoretically invalid"
- router: `workflow-router`
- workflow owner: `control-theory-veto`
- `workflow-scoped-execution` role: `not_used`

4. "maintain the KB/tool/skill stack"
- router: `workflow-router`
- workflow owner: `eda-infra-maintainer`
- `workflow-scoped-execution` role: `not_used`

5. "debug GT3 layer-policy assumptions and maybe run a confirming batch"
- router: `workflow-router`
- workflow owner: `gt3-backside-route-policy`
- `workflow-scoped-execution` role: `delegated_stage` only if the policy skill decides a bounded execution run is needed
