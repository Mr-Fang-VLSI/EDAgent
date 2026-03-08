# Model-Gap Patterns

## Pattern A: short-net-heavy backside usage
Signal:
- short_share_in_back high, long capture weak
Likely cause:
- router congestion spillover / policy artifact dominates
Action:
- add judgment model; constrain backside candidacy by criticality + net-length + capacity

## Pattern B: backside usage increases but timing worsens
Signal:
- more backside nets, WNS/TNS degrade
Likely cause:
- naive selection includes timing-sensitive nets or high via/access overhead
Action:
- add slack budget gate and via-risk penalty

## Pattern C: reroute report claims routed, DEF shows none/minimal
Signal:
- metadata says routed but geometric occupancy absent
Likely cause:
- script/report mismatch or fallback no-op
Action:
- add hard post-check based on routed DEF layer occupancy
