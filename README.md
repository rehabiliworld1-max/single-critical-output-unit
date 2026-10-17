# single-critical-output-unit

Supporting materials for the paper:

> Obaru, K. **A Single Critical Output Unit in a Feedforward Bipedal Locomotion Policy: Cross-Seed Replication and Mechanism Analysis in the Unitree G1 Humanoid.** *Frontiers in Robotics and AI* (under review, Manuscript ID 1957291).

Author: Kenshi Obaru, M.D., Ph.D. — rehabiliworld, Kumamoto City, Japan (research@rehabiliworld.com)

## Contents

| Folder | Contents |
|---|---|
| `notebooks/01_ablation_screen_sweep_dose_response.ipynb` | Setup, verification of the output layer and the single-unit output ablation (§2.3); the 29-joint screen in 3 and then 8 policies at 0.5 m/s (Table 1, Figure 1, Supplementary Table S1); the original cross-seed speed sweep; and the graded attenuation experiment (§3.4, Figure 4). Sections 10–12, 14 and 15 contain the original mechanism analysis, which read joint angles after the automatic reset and has been withdrawn; they are kept unchanged for transparency and marked as superseded. |
| `notebooks/02_remeasure_mechanism_right_knee_1p0_screen.ipynb` | Fall detection before the automatic reset (§2.4), the Stage 2 sweep with the mechanism analysis for the five joints (8 policies × 9 speeds), unablated walking baseline, the 29-joint screen at 1.0 m/s, simulation and training specifications, and Supplementary Videos S1–S4. Section §C of this notebook belongs to a companion study and is not used in this paper. |
| `results/P1_mechanism_summary.csv` | One row per trial of the Stage 2 sweep (joint, seed, speed, fall, fall step, joint deviations at fall onset and over the last 0.5 s). |
| `results/S_screen_1p0.csv` | 29-joint screen at 1.0 m/s (Table 1; Supplementary Table S4). |
| `results/D_baseline_walk.csv` | Unablated walking (8 policies × 9 speeds). |
| `results/graded_attenuation_fall_rates.csv` | Fall rate across the 8 policies at each remaining output level (0.5 m/s; Figure 4), as printed by §16 of notebook 01. |
| `results/A_artifact_check.json` | Check that the fall step is identical with the environment termination and with the analysis-code criterion. |
| `trajectories/P1_prefall_trajectories.zip` | Joint angles, commanded targets, trunk tilt and root height up to fall onset for all 196 falling trials (`.npz`, one file per trial). |
| `analysis/stats.py`, `analysis/figures.py` | Scripts that compute every statistic in §3.1–3.3 and draw Figures 2 and 3 from `results/` and the unzipped trajectories. |
| `figures/` | Figures 2 and 3 of the revised manuscript. |
| `videos/` | Supplementary Videos S1–S4. |

## Data not retained

The per-trial tables of the original 29-joint screen at 0.5 m/s (Table 1, Figure 1) and of the graded-attenuation experiment (Figure 4) were not retained. They can be regenerated with §13 and §16 of notebook 01 and the released checkpoints; because the GPU simulator is not bitwise deterministic, single trials close to a fall threshold may differ.

## Trained policies

The eight trained policies (seeds 1–8) are shared with the companion studies and are available at
https://github.com/rehabiliworld1-max/fall-threshold-unilateral-attenuation.
The notebooks expect them in `logs/` (see §0 of notebook 02).

## Software

mjlab 1.2.0, MuJoCo 3.5.0, MuJoCo Warp 3.6.0, warp-lang 1.12.1, rsl-rl-lib 5.0.1, PyTorch 2.11.0 (CUDA 12.8), NumPy 2.1.3; NVIDIA Tesla T4 (Google Colab).
The GPU simulator is not bitwise deterministic, so individual trials close to a fall threshold can change outcome between runs; the files in `results/` are those of the run reported in the paper.

## Reproducing the statistics

```bash
cd single-critical-output-unit
mkdir -p results/trajectories && unzip trajectories/P1_prefall_trajectories.zip -d results/trajectories
python analysis/stats.py results
python analysis/figures.py results
```

## License

MIT License (see `LICENSE`).
