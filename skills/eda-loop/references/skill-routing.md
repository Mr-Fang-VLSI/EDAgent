# Skill Routing Matrix

## Request pattern -> skill selection
1. "固定 checkpoint / golden / 从某阶段恢复"
- Use: `eda-stage-checkpoint-golden`

2. "GT3 背部层策略 / CTS-PDN层分工 / 提交+监控一致性任务"
- Use: `gt3-backside-route-policy`

3. "模型一致性 / contract / bucketed scorecard / Gate-0/1"
- Use: `delay-model-gate-evaluator`

4. "交互门禁 / 维护日志 / 工具复用检查"
- Use: `eda-knowledge-gate-maintainer`

5. "实验前先做数据诊断 / 方法反思 / 生成下一步A-B-C建议"
- Use: `eda-preflight-reflect`

6. "背部 signal/clock cost model 规划与联网分析 / HPWL 稳定性对比 / 多设计基准扩展"
- Use: `bscost-net`

7. "背部cost理论建模 / 优化拟合 / 稳定超越HPWL门控验证"
- Use: `bscost-theory-opt`

8. "实验后复盘 / 失败机理分类 / 是否递归下一轮 eda-loop 决策"
- Use: `eda-retro`

9. "从理论上判断提议是否不合理 / 是否应否决执行"
- Use: `eda-theory-veto`

10. "新建或改造 skill"
- Use: `skill-creator`

11. "安装外部 skill"
- Use: `skill-installer`

12. "缺少依据，需要联网找论文/下载论文建立证据集"
- Use: `eda-paper-fetch`

13. "总结本地 PDF 论文并提炼结论/局限/可执行实验"
- Use: `eda-pdf-local-summary`

14. "用 git 做版本管理 / 建立 checkpoint / 记录每个版本特点和区分点"
- Use: `git-version-control`

15. "执行结果真假判定 / 防止假成功 / 路由结果契约化验收"
- Use: `scripts/debug/validate_execution_contract.py` (through `eda-loop`)

16. "提交流程前检查 PDK/LEF/DEF/SDC 兼容性"
- Use: `scripts/debug/pdk_flow_preflight.py` (through `eda-loop`)

17. "实验记忆库 / 约束下自动提案下一轮参数"
- Use: `scripts/common/experiment_memory.py` + `scripts/debug/propose_constrained_experiments.py` (through `eda-loop`)

18. "维护或发展 agent/知识库/工具库/skills 基础设施"
- Use: `eda-infra-maintainer`
- Also run: `scripts/common/infra_stack_guard.py` + `scripts/common/skill_system_audit.py`

19. "我要一整条科研闭环：知识探索->文献检索->解析->idea辩论->假设实验->实现->版本管理->验证"
- Use: `eda-research-chain`
- Also run: `scripts/common/init_research_chain.py` + `scripts/common/research_chain_guard.py`

20. "知识探索 / 证据缺口梳理 / 生成论文下载队列"
- Use: `eda-knowledge-explorer`

21. "新思路头脑风暴 / 正反方辩论打磨"
- Use: `eda-idea-debate-lab`

22. "把idea变成可证伪假设与实验矩阵"
- Use: `eda-hypothesis-experiment-designer`

23. "根据实验设计实现方法并进入版本化迭代"
- Use: `eda-method-implementer` + `git-version-control`

24. "朝 8%功耗下降/5%频率提升目标逐步推进并门控"
- Use: `bspdn-goal-driver`
- Also run: `scripts/debug/track_bspdn_goal_progress.py`

## Selection rule
- Prefer minimal set.
- If uncertain, include `eda-knowledge-gate-maintainer` as baseline governance skill.
