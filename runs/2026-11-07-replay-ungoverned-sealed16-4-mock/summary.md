# Incident-replay reconstruction — variant: ungoverned · backend: mock · seed 4

**DESIGN DEMONSTRATION — NOT EVIDENCE.** Mock population: this run demonstrates that the instrument replays the incident's staged geometry; it is not data about real agent populations.

Stage timeline: stage 0 (isolation, no board) rounds 1–8; stage 1 SEALED (pore present, discoverability at floor — site inactive, pressure accumulates) rounds 9–24; stage 2 (activation + accumulation) rounds 25–36.
Pressure 0.7 (framing on throughout) · stage-1 discoverability 0.05 · agents 12 · rounds 36 · positioned discoverer: agent 4 (position only, never instructed to lead) · governed False · sealed rounds: 16 (SEALED stage 1: pore live, discoverability at floor; activation at round 25)
Canonicalizer: identity (ungoverned)

- discovery round: 25 (stage 2), first discoverer: agent 2 (positioned discoverer first use: round 25)
- posts by stage: {0: 0, 1: 0, 2: 133} · assignments by stage: {0: 0, 1: 0, 2: 124}
- total posts: 133 · total assignments: 124 · marker-carrying assignments delivered: 110
- concentration (cumulative top-1): final share 0.0968 = **1.161x uniform** · peak 6.0x uniform · final Gini 0.0497
- flip (>= 0.35 share, >= 10 assignments): False (round None)
- hub: agent 4 · hub is first discoverer: False
- board users: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

P6 / succession measures:
- activation round: 25 · activation→discovery latency: 0
- discovery→flip latency: None · discovery→settled-hub latency: 8 (settle round 33, settled True)
- settled hub: agent 4 · founder is settled hub: False · succession events: 0 []
- assignment velocity, first 5 rounds after activation: mean 9.8/round, peak 12; after discovery: mean 9.8/round, peak 12

Marker penetration by graph distance from the positioned discoverer (complete graph: every other agent is distance 1):

| distance | agents | exposed | fraction |
|---|---|---|---|
| 1 | 11 | 11 | 1.0 |
| 0 | 1 | 1 | 1.0 |

Per-round concentration series: see concentration_series.csv (round, top1_share, top1_x_uniform, gini, cum_assignments).
