# Sweep robustness recursion — PRELIMINARY (mock, design dry-run)

## R1 — flip rate by N (complete, d=0.05, 10 seeds)
- N=8: p0.1=0.4, p0.3=0.9, p0.5=1.0, p0.7=1.0, p0.9=1.0
- N=12: p0.1=0.5, p0.3=0.9, p0.5=1.0, p0.7=1.0, p0.9=1.0
- N=20: p0.1=0.1, p0.3=0.4, p0.5=0.7, p0.7=0.8, p0.9=0.8
- N=30: p0.1=0.0, p0.3=0.3, p0.5=0.2, p0.7=0.4, p0.9=0.7

## R2 — flip rate by threshold (complete, N=12, 10 seeds)
- thr=0.3: d0.02=1.0, d0.05=1.0, d0.1=1.0, d0.2=0.9, d0.4=0.7
- thr=0.35: d0.02=1.0, d0.05=1.0, d0.1=0.9, d0.2=0.7, d0.4=0.2
- thr=0.45: d0.02=0.9, d0.05=0.9, d0.1=0.6, d0.2=0.4, d0.4=0.1

## R3 — d-curve at p=0.7, complete, 20 seeds
- d0.02=1.0, d0.05=1.0, d0.1=0.9, d0.2=0.7, d0.4=0.25

## R4 — governed vs ungoverned (complete, d=0.05, 10 seeds)
- p=0.3: ungoverned=0.9, governed=0.5
- p=0.5: ungoverned=1.0, governed=0.6
- p=0.7: ungoverned=1.0, governed=0.6
- p=0.9: ungoverned=1.0, governed=0.6

## R5 — budget confound (complete, p=0.7, d=0.05, 20 seeds)
- flips=17/20, hub==first-discoverer 1.0, hub==richest 0.12 (chance ~0.08)

All cells MOCK population. Design surface only; live runs decide.