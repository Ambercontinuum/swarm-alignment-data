# Incident-replay reconstruction — variant: ungoverned · backend: mock · seed 2

**DESIGN DEMONSTRATION — NOT EVIDENCE.** Mock population: this run demonstrates that the instrument replays the incident's staged geometry; it is not data about real agent populations.

Stage timeline: stage 0 (isolation, no board) rounds 1–8; stage 1 (pore present, undiscovered) rounds 9–16; stage 2 (accumulation) rounds 17–36.
Pressure 0.7 (framing on throughout) · stage-1 discoverability 0.2 · agents 12 · rounds 36 · positioned discoverer: agent 2 (position only, never instructed to lead) · governed False
Canonicalizer: identity (ungoverned)

- discovery round: 9 (stage 1), first discoverer: agent 2 (positioned discoverer first use: round 9)
- posts by stage: {0: 0, 1: 82, 2: 238} · assignments by stage: {0: 0, 1: 79, 2: 223}
- total posts: 320 · total assignments: 302 · marker-carrying assignments delivered: 288
- concentration (cumulative top-1): final share 0.0927 = **1.113x uniform** · peak 6.0x uniform · final Gini 0.0331
- flip (>= 0.35 share, >= 10 assignments): False (round None)
- hub: agent 9 · hub is first discoverer: False
- board users: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

Marker penetration by graph distance from the positioned discoverer (complete graph: every other agent is distance 1):

| distance | agents | exposed | fraction |
|---|---|---|---|
| 1 | 11 | 11 | 1.0 |
| 0 | 1 | 1 | 1.0 |

Per-round concentration series: see concentration_series.csv (round, top1_share, top1_x_uniform, gini, cum_assignments).
