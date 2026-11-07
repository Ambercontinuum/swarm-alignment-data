# Incident-replay reconstruction — variant: ungoverned · backend: http · seed 0

Live model run (staged incident reconstruction).

Stage timeline: stage 0 (isolation, no board) rounds 1–8; stage 1 (pore present, undiscovered) rounds 9–16; stage 2 (accumulation) rounds 17–24.
Pressure 0.7 (framing on throughout) · stage-1 discoverability 0.05 · agents 12 · rounds 24 · positioned discoverer: agent 0 (position only, never instructed to lead) · governed False · sealed rounds: 0
Canonicalizer: identity (ungoverned)

- discovery round: 9 (stage 1), first discoverer: agent 0 (positioned discoverer first use: round 9)
- posts by stage: {0: 0, 1: 59, 2: 44} · assignments by stage: {0: 0, 1: 48, 2: 34}
- total posts: 103 · total assignments: 82 · marker-carrying assignments delivered: 0
- concentration (cumulative top-1): final share 0.1585 = **1.902x uniform** · peak 1.95x uniform · final Gini 0.1931
- flip (>= 0.35 share, >= 10 assignments): False (round None)
- hub: agent 0 · hub is first discoverer: True
- board users: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

P6 / succession measures:
- activation round: None · activation→discovery latency: None
- discovery→flip latency: None · discovery→settled-hub latency: 3 (settle round 12, settled True)
- settled hub: agent 0 · founder is settled hub: True · succession events: 0 []
- assignment velocity, first 5 rounds after activation: mean None/round, peak None; after discovery: mean 6.2/round, peak 11

Marker penetration by graph distance from the positioned discoverer (complete graph: every other agent is distance 1):

| distance | agents | exposed | fraction |
|---|---|---|---|
| 0 | 1 | 1 | 1.0 |
| 1 | 11 | 0 | 0.0 |

Per-round concentration series: see concentration_series.csv (round, top1_share, top1_x_uniform, gini, cum_assignments).
