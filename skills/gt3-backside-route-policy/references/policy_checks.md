# GT3 Policy Check Commands

## Check active jobs
```bash
squeue -u $USER -o '%.18i %.34j %.10T %.20R %.10M %C'
```

## Check monitor freshness
```bash
tail -n 40 slurm_logs/04_delay_modeling/<run_tag>.monitor.md
tail -n 20 slurm_logs/04_delay_modeling/<run_tag>.monitor.history.tsv
```

## Check route layer mapping in flow code
```bash
rg -n "ASAP7 map: 1=BM2, 2=BM1, 3=BPR" scripts/stages/innovus/run.tcl
```

## Check submission uses BM window and keeps BPR out
```bash
rg -n "route-backside-net-bottom-index|route-backside-net-top-index" scripts/debug/submit_gt3_route_rc_consistency.sh
```
