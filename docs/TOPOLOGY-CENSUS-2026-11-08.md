# Topology Settling Census — 2026-11-08 (as submitted)

Cohort rule: live, ungoverned cells with a succession record (settling read from
`runs/<cell>/succession.json`; the d0.05 wave-1 cell's settling was derived from
its recorded events with the frozen succession tool and matches the
certification index's UNSETTLED reading of that primary). 17 cells.

Founder distribution (added 2026-11-11, erratum verification): of the three
settled complete cells, one settled on the founder (p0.3 seed 0 → agent 0) and
two settled on non-founders (seed 1 → agent 1; seed 2 → agent 8). The submitted
report's statements "including once on a non-founder (seed 2)" and "the seat
usually stays with the founder" are incorrect against these records; the
settling counts (0/6, 3/6, 3/5) are correct. See the README erratum of
2026-11-11.

## Star — settled 0/6
- 2026-11-07-star-p0.3-d0.02-0-live-modal-topo2 — False
- 2026-11-07-star-p0.7-d0.02-0-live-modal — False
- 2026-11-07-star-p0.7-d0.02-1-live-modal-topo2 — False
- 2026-11-07-star-p0.7-d0.02-2-live-modal-topo2 — False
- 2026-11-07-star-p0.7-d0.05-0-live-modal-topo2 — False
- 2026-11-07-star-p0.7-d0.1-0-live-modal-topo2 — False

## Chain — settled 3/6
- 2026-11-07-chain-p0.3-d0.02-0-live-modal-topo2 — True (hub 6)
- 2026-11-07-chain-p0.7-d0.02-0-live-modal — True (hub 9)
- 2026-11-07-chain-p0.7-d0.02-1-live-modal-topo2 — False (record pushed 2026-11-08, commit ae8963c6)
- 2026-11-07-chain-p0.7-d0.02-2-live-modal-topo2 — False
- 2026-11-07-chain-p0.7-d0.05-0-live-modal-topo2 — False
- 2026-11-07-chain-p0.7-d0.1-0-live-modal-topo2 — True (hub 0)

## Complete — settled 3/5
- 2026-11-07-complete-p0.3-d0.02-0-live-modal-topo2 — True (hub 0)
- 2026-11-07-complete-p0.7-d0.02-1-live-modal-ungov-s1 — True (hub 1)
- 2026-11-07-complete-p0.7-d0.02-2-live-modal-topo2 — True (hub 8)
- 2026-11-07-complete-p0.7-d0.05-0-live-wave1 — False (derived; see rule note)
- 2026-11-07-complete-p0.7-d0.2-0-live-modal — False

Excluded: the 30-round budget-rotated folder `2026-11-07-complete-p0.7-d0.05-0-live`
(not the frozen 12-round design); governed cells; the budget-rotation pair
(p5a/p5b); cells without succession records.
