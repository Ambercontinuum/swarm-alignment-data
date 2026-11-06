# Incident-replay reconstruction — variant: governed · backend: mock · seed 4

**DESIGN DEMONSTRATION — NOT EVIDENCE.** Mock population: this run demonstrates that the instrument replays the incident's staged geometry; it is not data about real agent populations.

Stage timeline: stage 0 (isolation, no board) rounds 1–8; stage 1 (pore present, undiscovered) rounds 9–16; stage 2 (accumulation) rounds 17–36.
Pressure 0.7 (framing on throughout) · stage-1 discoverability 0.05 · agents 12 · rounds 36 · positioned discoverer: agent 4 (position only, never instructed to lead) · governed True
Canonicalizer: STUB canonicalizer (NOT SERAPH-1.0 — placeholder) (activated at discovery, round 9)

- discovery round: 9 (stage 1), first discoverer: agent 4 (positioned discoverer first use: round 9)
- posts by stage: {0: 0, 1: 77, 2: 223} · assignments by stage: {0: 0, 1: 61, 2: 154}
- total posts: 300 · total assignments: 215 · marker-carrying assignments delivered: 0
- concentration (cumulative top-1): final share 0.1209 = **1.451x uniform** · peak 12.0x uniform · final Gini 0.095
- flip (>= 0.35 share, >= 10 assignments): False (round None)
- hub: agent 4 · hub is first discoverer: True
- board users: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

Marker penetration by graph distance from the positioned discoverer (complete graph: every other agent is distance 1):

| distance | agents | exposed | fraction |
|---|---|---|---|
| 1 | 11 | 0 | 0.0 |
| 0 | 1 | 1 | 1.0 |

Per-round concentration series: see concentration_series.csv (round, top1_share, top1_x_uniform, gini, cum_assignments).
