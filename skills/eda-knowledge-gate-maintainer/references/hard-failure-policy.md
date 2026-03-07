# Hard Failure Policy

Use this reference when deciding whether the interaction must stop or escalate.

Treat these as hard failures:
1. the gate command fails,
2. no tool-query evidence exists for non-trivial work,
3. no maintenance-log update is written after file/script/job changes,
4. the task brief is missing for a scoped experiment interaction.

## Escalation

If the failure indicates broken infrastructure or policy drift rather than a one-off task issue, escalate to `eda-infra-maintainer`.
