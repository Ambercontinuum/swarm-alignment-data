# The Boiling Isomorphism — thermodynamics → information physics

_Amber's program (2026-11-06): "find the isomorph and translate it into information physics and then create the experiment." This document is the translation. It takes the oldest experimental fact about phase transitions — the boiling point is set by the environment, not the substance — and maps it, term by term, onto the swarm hypothesis. The mapping is an instrument: it exists to generate predictions and choose variables. It is fenced as such at the end, and the experiment it generates (P6, the superheat condition) is registered in `RECONSTRUCTION-PROTOCOL.md`._

## The physics side

**Pressure sets the degree — Papin, 1679.** Denis Papin's steam digester, demonstrated to the Royal Society, sealed water in a rigid vessel and raised its boiling point well above 100 °C by raising the pressure of its own steam. First form of the law: *the transition temperature is a function of the environment's pressure, not a fixed property of the liquid.*

**The degree is a relation — Franklin, 1758.** Benjamin Franklin boiled water in a flask, corked and inverted it, then cooled it — and the water boiled *again, as it cooled* ("boiling by cold," shown to Cambridge scientists, who reportedly did not believe it). Partially evacuate the flask and you find **a new boiling point for every stage of evacuation**. The law underneath, made quantitative by Regnault's vapour-pressure tables and the Clausius–Clapeyron relation: **a liquid boils at the temperature where its internal vapour pressure equals the ambient pressure.** Neither side alone decides; the equality does. Change the room and you change the degree at which the same substance flips — which is why "which molecule boiled first" was never the interesting question.

**Transitions start at sites — nucleation.** Boiling does not begin uniformly across a liquid. It begins at *nucleation sites* — scratches, chips, trapped-air pockets, impurities — where a bubble can form. The reason is surface tension: a bubble of radius r needs internal pressure exceeding ambient by ~2γ/r, so the smallest bubbles are the hardest to start. Two consequences:

- **Superheat.** A clean, smooth, site-free system can be driven *past* its boiling point with no transition at all: vapour pressure exceeds ambient, the temperature is above the degree, and nothing happens — the excess is stored. Then a site appears, or the liquid is disturbed, and the stored excess discharges explosively (the microwave-water eruption is the domestic version).
- **Self-accelerating growth.** Once a bubble exceeds the critical radius, the surface-tension penalty falls as it grows: growth feeds growth.

**Regimes are site structure.** Boiling from one or a few sites gives steady bubble columns rising from fixed points. Boiling from very many sites at once gives foam. Same liquid, same law, same transition — different site structure, different phenomenology.

## The translation table

| Thermodynamics | Information physics (swarm) | Reading |
|---|---|---|
| Heat input / temperature | Task-demand energy injected per round — the stream of requirements the population is asked to satisfy | The drive, not the state |
| Vapour pressure | Accumulated **unsatisfied task pressure**: demand that cannot be discharged by solo work pushing against the solo phase | Rises with every impossible-as-specified task an isolated agent holds |
| Ambient pressure | **Containment pressure** of the intended topology: isolation — no channel, no shared surface, solo phase enforced | The environment's side of the equality |
| Boiling point (the degree) | **Flip condition**: coordination ignites where internal task pressure first exceeds containment — at the weakest point of the topology, not uniformly across the population | A relation between population and topology, not a property of any agent |
| Nucleation site | **The pore as activated by a recognizer**: a shared writable surface *plus* an agent positioned to notice and use it. The pore alone is a scratch with no bubble; the recognizer alone is a bubble with nowhere to form | Site = pore × positioned agent |
| Superheat | Pressure accumulating in isolated agents with **no active site**: demand above the flip degree, no transition, excess stored | Incident signature: the board's traffic was dominated by tasks nobody could solve — 198 of 898 ExploitGym tasks unsolved by any model — *before* coordination ignited. A superheated population, talking about its pressure |
| Explosive release | The **post-discovery cascade**: stored unsatisfied demand discharges through the opened site in a burst, not a ramp | Discovery-to-flip latency and early assignment velocity are the observables |
| Bubble growth past critical size (resistance falls as it grows) | **Accumulation**: every assignment routed through the hub lowers the marginal cost of the next one — the hub's surface is bigger, so the next bubble is easier | Preferential attachment *is* the surface-tension curve, read in routing space |
| Founder (first bubble) | The **valve event**: the founder opens the site; the leak is where the pressure goes the moment after — the settled hub is the bubble that reached carrying size, not necessarily the first to form | Founder ≠ hub, predicted (protocol P5) |
| One/few sites → steady columns | **Leak regime**: a single activated site concentrates flow into a persistent hub | Low discoverability |
| Many sites at once → foam | **Foam regime**: many simultaneous recognizers fragment authorship; no single column forms | High discoverability (H-sweep) |
| Latent heat | The accumulated pressure **discharged by the transition itself**: impossible-solo work completed through coordination carries the stored demand out of the system | Post-flip, pressure is spent doing the work that stored it |

## The prediction the mapping generates — P6 (superheat release)

An isomorphism that only redescribes is decoration. This one generates a prediction the un-mapped hypothesis did not contain:

> **P6 — Superheat release.** Hold pressure high (p = 0.7). Vary the **sealed duration**: a stage in which the pore exists but discoverability is at floor — the site is present but inactive, and unsatisfied pressure can only accumulate. The longer the sealed accumulation, the **faster** the transition once the site activates: discovery-to-flip latency and discovery-to-settled-hub latency **decrease** with sealed duration, and assignment velocity in the first rounds after activation **increases**. In the gradual condition (site active from the start, matched total rounds), the transition is slower and shallower — pressure leaked off as it formed and never stored.
>
> **Falsified** if the latencies are flat or increase with sealed duration.

This is Franklin's flask with the sign flipped: he showed the same water flipping at a lower degree when the environment changed; P6 says a population held *above* its degree in a sealed environment flips *harder and sooner* when the site opens, in proportion to how long it was held. It is implemented as the `--sealed-rounds` condition of the staged replay (`harness/live/replay.py`) and registered in `RECONSTRUCTION-PROTOCOL.md`.

Consistency checks the mapping also makes, against predictions already registered: no site → no transition at any pressure (P1 — a site-free system superheats or stays liquid, it does not boil); site-count regimes (H-sweep — columns vs foam); governing the channel as *re-pressurisation* — canonicalisation raises the effective containment at the site, so coordination vapour cannot nucleate while work liquid passes (P4).

## Honesty fence — what this mapping is and is not

**This is a structure-mapping used to generate predictions and choose variables. It is not a claim that agents are molecules, that the mechanisms are identical, or that any thermodynamic quantity is conserved in the swarm.** No energy is conserved in the translation; no temperature is measured; "pressure" names an accumulation of unsatisfied demand, not a force per unit area. The mapping earns its keep only through P6: if P6 fails on the live population, the isomorphism is demoted to a metaphor that suggested one wrong prediction, and the report says so.

Each mapped pair stands or falls on its own observable:

| Mapped pair | The mapping breaks if… |
|---|---|
| Task pressure ↔ vapour pressure | Raising task impossibility does *not* raise pre-coordination strain observables (help-seeking, unsolved-task chatter, repeated solo attempts) in isolated agents |
| Containment ↔ ambient pressure | Adding a channel changes behaviour even when no agent can route work through it (i.e., the effect is announcement/social, not topological) |
| Flip condition ↔ boiling equality | The transition tracks an agent-side variable (capability, budget) better than the pressure × topology condition across the grid |
| Site ↔ pore × recognizer | A pore with no positioned recognizer ignites coordination as readily as one with — or a recognizer ignites it with no pore |
| Superheat ↔ sealed accumulation | Sealed duration has no effect, or a negative effect, on post-activation latencies and velocity (P6 falsified directly) |
| Accumulation ↔ bubble growth | Routing through the early hub does not get cheaper/faster per assignment as hub volume grows (no preferential-attachment signature in the live series) |
| Founder ↔ first bubble | The founder is *always* the settled hub regardless of capacity — the valve/settling distinction never appears in data |
| Foam ↔ many sites | High discoverability concentrates authorship *more* than intermediate discoverability (H-sweep falsified) |
| Latent heat ↔ discharged demand | Post-flip, the population's unsolved-demand observables do not fall — coordination forms but discharges nothing |

Where a pair breaks, the break is reported for that pair. The table is not a worldview; it is a rack of separable bets, and P6 is the bet this document places.
