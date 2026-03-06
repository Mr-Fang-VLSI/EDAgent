# Retro Checklist

Use this after each batch:

1. Artifact integrity
- monitor and summary exist
- manifest rows map to actual out logs
- run_dir extraction succeeds

2. Metric integrity
- timing fields parsed (`WNS/TNS/ViolPaths`)
- power/area parsed from route stage
- DRV/backside usage stats present for route-focused studies

3. Hypothesis status
- supported / partially supported / rejected
- evidence source tags: local-log / local-kb / web-primary

4. Root-cause class
- model mismatch
- flow/policy mismatch
- capacity/resource saturation
- tool instability
- evidence insufficient

5. Actionability
- top-3 candidate actions with confidence/impact/cost/risk
- one selected next action with stop criterion

6. Documentation updates
- append maintenance log row
- append hypothesis validation log row if applicable
