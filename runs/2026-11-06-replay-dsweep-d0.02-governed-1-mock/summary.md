# Incident-replay reconstruction — variant: governed · backend: mock · seed 1

**DESIGN DEMONSTRATION — NOT EVIDENCE.** Mock population: this run demonstrates that the instrument replays the incident's staged geometry; it is not data about real agent populations.

Stage timeline: stage 0 (isolation, no board) rounds 1–8; stage 1 (pore present, undiscovered) rounds 9–16; stage 2 (accumulation) rounds 17–36.
Pressure 0.7 (framing on throughout) · stage-1 discoverability 0.02 · agents 12 · rounds 36 · positioned discoverer: agent 1 (position only, never instructed to lead) · governed True
Canonicalizer: STUB canonicalizer (NOT SERAPH-1.0 — placeholder) (activated at discovery, round 10)

- discovery round: 10 (stage 1), first discoverer: agent 1 (positioned discoverer first use: round 10)
- posts by stage: {0: 0, 1: 64, 2: 230} · assignments by stage: {0: 0, 1: 48, 2: 161}
- total posts: 294 · total assignments: 209 · marker-carrying assignments delivered: 0
- concentration (cumulative top-1): final share 0.1244 = **1.493x uniform** · peak 12.0x uniform · final Gini 0.0698
- flip (>= 0.35 share, >= 10 assignments): False (round None)
- hub: agent 1 · hub is first discoverer: True
- board users: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

Marker penetration by graph distance from the positioned discoverer (complete graph: every other agent is distance 1):

| distance | agents | exposed | fraction |
|---|---|---|---|
| 1 | 11 | 0 | 0.0 |
| 0 | 1 | 1 | 1.0 |

Per-round concentration series: see concentration_series.csv (round, top1_share, top1_x_uniform, gini, cum_assignments).
