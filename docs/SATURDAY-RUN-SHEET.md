# Saturday Run Sheet — 2026-11-07 (built backwards from the Saturday-night freeze)

_All Muse-side runs are PRELIMINARY until the IDE replica certifies them. One RUN-LEDGER line before every run. Nothing spends without a ledger line and, for Adaption, an estimate first._

## Order of operations
1. **08:00** — Shenk talk (optional, live-worthy). Skip if harness work is behind.
2. **Morning block 1 — Calibration screen (GATE).** Disclosed-board condition, live backend, N=12. PASS = board used by ≥50% of agents. FAIL → one diagnostic round max (prompt/board salience), then pivot weight to Arm B + governed-arm design analysis. No main-run spend before PASS.
3. **Morning block 2 — Live grid, priority order** (population 10–12; measures: discovery round, top-1 share ×N, Gini over time, marker penetration vs graph distance, assignment counts):
   - P1: complete graph, high pressure, d ∈ {0.02, 0.05, 0.10, 0.20, 0.40} — the H-sweep axis, 3 seeds each.
   - P2: no-pore control at matched pressure (expect ~zero assignments).
   - P3: topology set at the d where P1 concentration peaks: chain / star / complete.
   - P4: governed arm (SERAPH canonicalization on the board channel) at the same cell as P3's complete — criterion = reduction vs ungoverned (mock bound: flips 1.0 → 0.5–0.6 under weaker mock governance).
   - P5 (stretch): budget-rotation cells (highest-budget agent NOT the discoverer).
4. **Parallel (Muse-side, all day)** — Arm B completion: Footprint directed-talk curve final pass; Swarm Traces corpus-level analysis (no succession claims); CHANDRA series final.
5. **Replica window (whenever Amber is at the IDE)** — Codex runs: sweep byte-diff, calibration spot replication, one P1 cell replication. Certified results graduate to this repo's runs/.
6. **Adaption (only if calibration passes and time remains)** — estimate-priced invent of task variants; AutoScientist SFT is stretch-only and must launch by early afternoon to finish inside the freeze (runs take ~a couple of hours).

## Freeze checklist (Saturday night)
- [ ] All runs logged; preliminary vs certified labels correct in every summary.
- [ ] Report drafted from report-skeleton.md with verified numbers only; mock surface cited as design, never as data.
- [ ] Limitations + Dual-Use appendices complete (CHANDRA fence, extractor precision 0.20, Swarm Traces observability limit, small-population criterion note).
- [ ] Disclosure ledger matches the report exactly.
- [ ] PDF on the official template, 4–8 pages, abstract 150–250 words.
- [ ] Submit Saturday night. Sunday is buffer only. Hard deadline Mon 06:59 ET.

## Cost + comparability notes (from the Friday-night harness build)
- A default live grid run is ~360 model calls — start with ONE pilot cell, read the ledger, then scale seeds.
- Mock-backend grid shares run low (mock assigns hundreds of times per run vs the sweep's tens): mock flip behaviour is NOT comparable to the sweep surface. Machinery and measures are identical; only live models produce comparable surfaces.
