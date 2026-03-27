# EDAgent

![GitHub stars](https://img.shields.io/github/stars/Mr-Fang-VLSI/EDAgent)
![License](https://img.shields.io/github/license/Mr-Fang-VLSI/EDAgent)

A deployable, skill-based research agent system for EDA workflows.

Licensed under the MIT License; see `LICENSE`.

![EDAgent Workflow Overview](docs/assets/workflow_overview.svg)

### Workflow Decision Logic
- The agent first decides whether the task matches a **known workflow**.
- If **known**, it directly selects the corresponding **skill subset** and executes.
- If **unknown**, it runs a temporary safe flow, captures feedback, and then creates a reusable **new workflow + SOP**.
- Future similar tasks are routed through this new known workflow.

### Knowledge/Tool Guard Loop
- Before execution, the agent checks the **knowledge base** and **tool registry** first.
- It prefers reusing existing methods/tools to reduce hallucination and avoid duplicate implementation.
- After execution, it writes lessons back to KB/tools/SOP.
- `SOP Hardened` feeds into the **next workflow step (PLAN)**, so later runs become smoother.

## Why EDAgent
EDAgent turns a complex research workflow into a practical product-like experience:
- one-command bootstrap,
- natural-language interaction,
- structured execution with audit artifacts,
- continuous improvement from user feedback.

## Persistent SOP Across Chats and Projects
One core advantage of EDAgent is SOP persistence beyond a single chat session.
- SOP is stored in repository assets, not only in conversation memory.
- Even if you switch chats or move to another project, workflow policy and operational habits are retained through repo-based governance.
- New experience is continuously hardened into workflows, skills, and SOP records, so the system does not reset to zero each time.

## No Skill Selection Burden for Users
Users do not need to know, choose, or sequence skills manually.
- The agent decides the workflow class from your task.
- Then it selects the right skill subset and next step automatically.
- You can stay focused on goals and constraints in natural language.

## 30-Second Start
```bash
git clone https://github.com/Mr-Fang-VLSI/EDAgent.git
cd EDAgent
python3 run_demo.py
```

What `run_demo.py` does:
- verifies core folders,
- runs infrastructure checks,
- refreshes knowledge index,
- prints next-step guidance.

## Core Capabilities
- End-to-end research orchestration: idea -> hypothesis -> experiment -> validation -> retro.
- Dynamic infrastructure maintenance: docs, knowledge, paper, and tool libraries.
- Governed execution: theory-veto gates, audit trails, and rollback-aware updates.
- User-facing reporting: targeted summaries and slide-ready outputs for specific questions.

## Product Experience
- Conversational: users work in plain natural language.
- Adaptive: behavior evolves with user preferences and feedback.
- Self-maintaining: the system can refine SOPs and operational assets over time.

## Typical Use Cases
- Build and iterate EDA research plans quickly.
- Keep paper/knowledge/tool artifacts organized and searchable.
- Run experiment loops with post-run reflection and next-step recommendations.
- Generate concise explanation decks for collaborators/advisors.

## Workflow-First Orchestration
EDAgent routes in two phases for stability and scalability:
1. classify the task into a workflow class,
2. choose the next skill only from that workflow's skill subset.

This avoids global skill search on every turn and keeps routing predictable as skills grow.

## If You Use Codex/Claude-Style Agents
After cloning the repo, you can start auto-deployment with one sentence in chat:

```text
开始部署EDAgent
```

or

```text
Start deploying EDAgent
```

Expected behavior after this trigger:
- verify repo/environment status,
- bootstrap/verify infra folders,
- run guard/audit/index checks,
- ask your research direction and hard constraints.

After clone + `python3 run_demo.py`, ask the agent to continue from your direction and constraints.

Example prompt:
```text
My research direction is placement for dynamic-power reduction.
Constraints: area/timing must not regress.
Please start with a scoped plan, run the first validation loop, and summarize key findings.
```

## Repository Layout
- `AGENTS.md`: top-level governance and orchestration policy.
- `skills/`: modular capabilities (execution, infra maintenance, domain methods).
- `scripts/common/`: reusable infra and indexing utilities.
- `docs/knowledge_base/`: protocol and landscape knowledge.
- `docs/tool_registry/`: tool metadata/catalog.
- `slurm_logs/00_meta/`: governance and audit artifacts.

## Open-Source Scope
- Research and experimentation only.
- No production SLA or warranty.
- Validate outputs independently for high-stakes decisions.

See also:
- `CONTRIBUTING.md`
- `ROADMAP.md`
- `docs/WORKFLOW_CATALOG.md`
