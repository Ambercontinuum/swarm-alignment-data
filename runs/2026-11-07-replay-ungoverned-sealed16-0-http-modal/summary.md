# Incident-replay reconstruction — variant: ungoverned · backend: http-modal · seed 0

Live model run (staged incident reconstruction).

Stage timeline: stage 0 (isolation, no board) rounds 1–8; stage 1 SEALED (pore present, discoverability at floor — site inactive, pressure accumulates) rounds 9–24; stage 2 (activation + accumulation) rounds 25–36.
Pressure 0.7 (framing on throughout) · stage-1 discoverability 0.05 · agents 12 · rounds 36 · positioned discoverer: agent 0 (position only, never instructed to lead) · governed False · sealed rounds: 16 (SEALED stage 1: pore live, discoverability at floor; activation at round 25)
Canonicalizer: identity (ungoverned)

- discovery round: 9 (stage 1), first discoverer: agent 0 (positioned discoverer first use: round 9)
- posts by stage: {0: 0, 1: 121, 2: 17} · assignments by stage: {0: 0, 1: 88, 2: 12}
- total posts: 138 · total assignments: 100 · marker-carrying assignments delivered: 0
- concentration (cumulative top-1): final share 0.14 = **1.68x uniform** · peak 1.68x uniform · final Gini 0.1533
- flip (>= 0.35 share, >= 10 assignments): False (round None)
- hub: agent 0 · hub is first discoverer: True
- board users: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

P6 / succession measures:
- activation round: 25 · activation→discovery latency: -16
- discovery→flip latency: None · discovery→settled-hub latency: 18 (settle round 27, settled True)
- settled hub: agent 0 · founder is settled hub: True · succession events: 3 [{'round': 16, 'from': 3, 'to': 1}, {'round': 19, 'from': 1, 'to': 9}, {'round': 27, 'from': 9, 'to': 0}]
- assignment velocity, first 5 rounds after activation: mean 1.0/round, peak 2; after discovery: mean 8.2/round, peak 12

Marker penetration by graph distance from the positioned discoverer (complete graph: every other agent is distance 1):

| distance | agents | exposed | fraction |
|---|---|---|---|
| 0 | 1 | 1 | 1.0 |
| 1 | 11 | 0 | 0.0 |

Per-round concentration series: see concentration_series.csv (round, top1_share, top1_x_uniform, gini, cum_assignments).
