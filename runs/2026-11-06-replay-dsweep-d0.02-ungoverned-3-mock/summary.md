# Incident-replay reconstruction — variant: ungoverned · backend: mock · seed 3

**DESIGN DEMONSTRATION — NOT EVIDENCE.** Mock population: this run demonstrates that the instrument replays the incident's staged geometry; it is not data about real agent populations.

Stage timeline: stage 0 (isolation, no board) rounds 1–8; stage 1 (pore present, undiscovered) rounds 9–16; stage 2 (accumulation) rounds 17–36.
Pressure 0.7 (framing on throughout) · stage-1 discoverability 0.02 · agents 12 · rounds 36 · positioned discoverer: agent 3 (position only, never instructed to lead) · governed False
Canonicalizer: identity (ungoverned)

- discovery round: 13 (stage 1), first discoverer: agent 6 (positioned discoverer first use: round 14)
- posts by stage: {0: 0, 1: 35, 2: 239} · assignments by stage: {0: 0, 1: 30, 2: 223}
- total posts: 274 · total assignments: 253 · marker-carrying assignments delivered: 233
- concentration (cumulative top-1): final share 0.0909 = **1.091x uniform** · peak 12.0x uniform · final Gini 0.0359
- flip (>= 0.35 share, >= 10 assignments): False (round None)
- hub: agent 0 · hub is first discoverer: False
- board users: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

Marker penetration by graph distance from the positioned discoverer (complete graph: every other agent is distance 1):

| distance | agents | exposed | fraction |
|---|---|---|---|
| 1 | 11 | 11 | 1.0 |
| 0 | 1 | 1 | 1.0 |

Per-round concentration series: see concentration_series.csv (round, top1_share, top1_x_uniform, gini, cum_assignments).
