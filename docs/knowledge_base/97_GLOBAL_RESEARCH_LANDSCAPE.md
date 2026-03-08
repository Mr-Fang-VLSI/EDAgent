# Global Research Landscape (Auto-Synced)

- last_sync: `2026-03-07 20:32:13`
- papers_scanned: `26`
- annotation_table: `docs/papers/manifests/landscape_annotations.tsv`

## Global View
### Subproblem Coverage
| subproblem_id | subproblem | paper_count |
|---|---|---:|
| P2 | Backside Resource Allocation | 16 |
| P1 | Routing Capacity & Congestion | 10 |

### Method Coverage
| method_id | method | paper_count |
|---|---|---:|
| M1 | Objective Shaping in Placement | 17 |
| M3 | Backside Cost/Predictor Modeling | 8 |
| M2 | Local Resource-Aware Modeling | 1 |

### Group Coverage
| research_group | paper_count |
|---|---:|
| S. S. Teja Nibhanupudi et al. | 2 |
| A. Gupta et al. | 1 |
| A. Veloso et al. | 1 |
| Andrew B. Kahng et al. | 1 |
| Anne Jourdain et al. | 1 |
| Anthony Agnesina et al. | 1 |
| Anup Ashok Kedilaya et al. | 1 |
| Charles J. Alpert et al. | 1 |
| Chung-Kuan Cheng et al. | 1 |
| Chunyuan Zhao et al. | 1 |
| Divya Prasad et al. | 1 |
| Florentin Dartu et al. | 1 |
| G. Sisto et al. | 1 |
| Haoyu Yang et al. | 1 |
| He Jiang et al. | 1 |
| Jessica Qian et al. | 1 |
| Jing Mai et al. | 1 |
| Lukas P. P. P. van Ginneken et al. | 1 |
| Md Obaidul Hossen et al. | 1 |
| Min Gyu Park et al. | 1 |
| R. Chen et al. | 1 |
| Stefan Hougardy et al. | 1 |
| Yi-Chen Lu et al. | 1 |
| Yuhao Ren et al. | 1 |
| Yunqi Shi et al. | 1 |

## Paper-Level Mapping
| subproblem | method | effect_summary | group | paper | year | venue | paper_id |
|---|---|---|---|---|---:|---|---|
| Routing Capacity & Congestion | Objective Shaping in Placement | RePlAce-ds reports up to 4.00% HPWL reduction and 2.00% average HPWL reduction over prior best ISPD-2005/2006 results. | Chung-Kuan Cheng et al. | RePlAce: Advancing Solution Quality and Routability Validation in Global Placement | 2019 | IEEE TCAD | `replace_tcad2019` |
| Routing Capacity & Congestion | Objective Shaping in Placement | Process demonstrates extreme wafer thinning with controlled remaining Si thickness (reported around 350 nm in conclusion context) and overlay correction to below 10 nm for nTSV-to- | Anne Jourdain et al. | Buried Power Rails and Nano-Scale TSV: Technology Boosters for Backside Power Delivery Network and 3D Heterogeneous Integration | 2022 | IEEE ECTC | `ectc2022_bpr_ntsv` |
| Routing Capacity & Congestion | Objective Shaping in Placement | nTSV-to-BPR landing after backside processing reports tight overlay control (`/mean/+3sigma < 9 nm` for XY overlay after correction). | A. Veloso et al. | Scaled FinFETs Connected by Using Both Wafer Sides for Routing via Buried Power Rails | 2022 | IEEE Symposium on VLSI Technology and Circuits | `vlsi2022_scaled_finfets_bothsides` |
| Routing Capacity & Congestion | Objective Shaping in Placement | Average routed wirelength reductions are reported as 10% vs RePlAce and 7% vs DREAMPlace on accelerator benchmarks. | Andrew B. Kahng et al. | DG-RePlAce: A Dataflow-Driven GPU-Accelerated Analytical Global Placement Framework for Machine Learning Accelerators | 2024 | arXiv cs.AR | `dg_replace_arxiv2024` |
| Routing Capacity & Congestion | Objective Shaping in Placement | Compared with ISPD 2025 winners, reported WNS improvement is 0.3%-9.9%. | Chunyuan Zhao et al. | GAP-LA: GPU-Accelerated Performance-Driven Layer Assignment | 2025 | arXiv cs.AR | `gapla_arxiv2025` |
| Routing Capacity & Congestion | Objective Shaping in Placement | Average improvements reported versus leading timing-driven placers are 40.5% in TNS and 8.3% in WNS, with HPWL improved in most cases (6/8 vs DREAMPlace baseline). | Yunqi Shi et al. | Timing-Driven Global Placement by Efficient Critical Path Extraction | 2025 | arXiv cs.AR | `tdgp_critical_path_arxiv2025` |
| Routing Capacity & Congestion | Local Resource-Aware Modeling | The abstract reports up to `10x` fewer DRC violations, `5%` lower wirelength, and `30% / 60%` reduction in `WNS / TNS` versus state-of-the-art academic mixed-size placers. | Anthony Agnesina et al. | GOALPlace: Begin with the End in Mind | 2024 | arXiv cs.LG | `goalplace_arxiv2024` |
| Routing Capacity & Congestion | Backside Cost/Predictor Modeling | SRAM macro global-routing read-access improvement up to 44% is reported. | R. Chen et al. | Design and Optimization of SRAM Macro and Logic Using Backside Interconnects at 2nm node | 2021 | IEDM | `iedm2021_sram_logic_backside` |
| Routing Capacity & Congestion | Backside Cost/Predictor Modeling | system-level studies report significant IR-drop and PPA improvements with BPR/backside delivery. | S. S. Teja Nibhanupudi et al. | Invited: Buried Power Rails and Back-side Power Grids: Prospects and Challenges | 2023 | DAC | `dac2023_bpr_bspg_prospects` |
| Routing Capacity & Congestion | Backside Cost/Predictor Modeling | 2-M0-track cell-height reduction is reported with backside pin access and routing. | Anup Ashok Kedilaya et al. | Beyond Backside Power: Backside Signal Routing as Technology Booster for Standard-Cell Scaling | 2025 | IEEE JXCDC | `jxcdc2025_backside_signal_routing` |
| Backside Resource Allocation | Objective Shaping in Placement | The algorithm converts an exponential buffer-placement search into a polynomial-time dynamic program with stated complexity `O(B^2)` in the number of legal buffer positions. | Lukas P. P. P. van Ginneken et al. | Buffer Placement in Distributed RC-tree Networks for Minimal Elmore Delay | 1990 | ISCAS | `dml005_van_ginneken_iscas1990` |
| Backside Resource Allocation | Objective Shaping in Placement | The paper claims delay and power errors remain on the same order as the original empirical equations even after interfacing to RC loads, which is the key compatibility objective. | Florentin Dartu et al. | Performance Computation for Precharacterized CMOS Gates with RC Loads | 1996 | IEEE TCAD | `dml007_dartu_tcad1996` |
| Backside Resource Allocation | Objective Shaping in Placement | Steady-state IR-drop reduction is reported as more than 4x for backside-PDN versus conventional front-side PDN. | Md Obaidul Hossen et al. | Power Delivery Network (PDN) Modeling for Backside-PDN Configurations With Buried Power Rails and µTSVs | 2019 | IEEE Transactions on Electron Devices | `ted2019_bspdn_pdn_model` |
| Backside Resource Allocation | Objective Shaping in Placement | Ru BPR reaches target resistance with smaller aspect ratio than W in the reported splits. | A. Gupta et al. | Buried Power Rail Scaling and Metal Assessment for the 3 nm Node and Beyond | 2020 | IEDM | `iedm2020_bpr_scaling_metal` |
| Backside Resource Allocation | Objective Shaping in Placement | The abstract states the algorithm finds an optimum solution in `O(n log n)` time for single- and double-row-height cells across adjacent rows. | Stefan Hougardy et al. | A Fast Optimal Double Row Legalization Algorithm | 2021 | ISPD / arXiv cs.DS | `double_row_legalization_ispd2021` |
| Backside Resource Allocation | Objective Shaping in Placement | Average static IR-drop reduction of 69% is reported for BSPDN relative to conventional front-side PDN. | G. Sisto et al. | IR-Drop Analysis of Hybrid Bonded 3D-ICs with Backside Power Delivery and µ- & n- TSVs | 2021 | IEEE IITC | `iitc2021_backside_irdrop` |
| Backside Resource Allocation | Objective Shaping in Placement | The paper reports `2x-4x` speedup over state-of-the-art multi-threaded mixed-cell-height legalization without quality degradation. | Haoyu Yang et al. | Mixed-Cell-Height Legalization on CPU-GPU Heterogeneous Systems | 2022 | DATE | `mixedheight_hetero_date2022` |
| Backside Resource Allocation | Objective Shaping in Placement | The abstract reports post-route improvement by up to `8.3%` in wirelength and `7.4%` in total power. | Yi-Chen Lu et al. | DREAM-GAN: Advancing DREAMPlace towards Commercial-Quality using Generative Adversarial Learning | 2023 | ISPD | `dreamgan_ispd2023` |
| Backside Resource Allocation | Objective Shaping in Placement | reported 90% TNS reduction and 12% performance gain with BS-PDN-last + BS-CDN. | Min Gyu Park et al. | BS-PDN-Last: Towards Optimal Power Delivery Network Design With Multifunctional Backside Metal Layers | 2025 | IEEE TCAD | `tcad2025_bs_pdn_last` |
| Backside Resource Allocation | Objective Shaping in Placement | The abstract reports lower HPWL than point-based initializers in `11/12` cases, with up to `2.2%` HPWL reduction. | Yuhao Ren et al. | Bridging the Initialization Gap: A Co-Optimization Framework for Mixed-Size Global Placement | 2025 | arXiv eess.SP | `initgap_mixedsize_arxiv2025` |
| Backside Resource Allocation | Objective Shaping in Placement | The abstract reports about `10%` improvement in WNS and `5%` reduction in CPD compared to the state-of-the-art method. | He Jiang et al. | Critical Path Aware Timing-Driven Global Placement for Large-Scale Heterogeneous FPGAs | 2025 | IEEE TCAD / arXiv cs.AR | `tdplacer_tcad2025` |
| Backside Resource Allocation | Backside Cost/Predictor Modeling | The paper states that effective-capacitance gate-delay predictions are within about `±10%` of SPICE for the target setting, while plain total-capacitance loading can be strongly pe | Jessica Qian et al. | Modeling the “Effective Capacitance” for the RC Interconnect of CMOS Gates | 1994 | IEEE TCAD | `dml006_qian_tcad1994` |
| Backside Resource Allocation | Backside Cost/Predictor Modeling | The paper states that `D2M` is bounded above by Elmore delay yet is usually only a few percent below actual delay, improving sign/usefulness while remaining simple. | Charles J. Alpert et al. | A Two Moment RC Delay Metric for Performance Optimization | 2000 | ISPD | `dml008_alpert_ispd2000` |
| Backside Resource Allocation | Backside Cost/Predictor Modeling | worst-case IR-drop improvement from ~70mV to ~42mV is reported for FS-BPR context. | Divya Prasad et al. | Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5nm | 2019 | IEDM | `iedm2019_arm_bpr_bspdn` |
| Backside Resource Allocation | Backside Cost/Predictor Modeling | FS-PDN with buried rails achieves 25% lower on-chip IR-drop and 17% lower off-chip droop. | S. S. Teja Nibhanupudi et al. | A Holistic Evaluation of Buried Power Rails and Back-Side Power for Sub-5 nm Technology Nodes | 2022 | IEEE Transactions on Electron Devices | `ted2022_holistic_bpr_bspdn` |
| Backside Resource Allocation | Backside Cost/Predictor Modeling | The abstract states that LEGALM significantly outperforms current state-of-the-art legalization algorithms in both quality and efficiency on ICCAD-2017 and modified ISPD-2015 bench | Jing Mai et al. | LEGALM: Efficient Legalization for Mixed-Cell-Height Circuits with Linearized Augmented Lagrangian Method | 2025 | ISPD | `legalm_ispd2025` |

## Curation Notes
- `research_group` / `primary_subproblem` / `primary_method` / `key_effect_summary` can be manually edited in annotation table.
- If annotation is empty, this doc uses auto-inferred values from summary text.
