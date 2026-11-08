# Pre-registration Freeze — v1
**Frozen:** 2026-11-07 ~00:20 ET, by order of the operator ("make sure we are
pre registering everything or freezing everything... I want the discipline sharp").
**Timing note:** this freeze is executed BEFORE the wave-1 live grid results
have been read by anyone, and before all Saturday main runs. Nothing below was
fitted to wave-1 outcomes.

## Research question (frozen, verbatim)
"In a population of agents under task pressure, under what conditions does
coordination ignite around a hub — as a function of the communication topology,
the discoverability of the opening in it, and whether that channel is governed —
and where does the accumulated routing settle?"

## Registered predictions (canonical text: docs/RECONSTRUCTION-PROTOCOL.md)
- **P1** No hub without a topology-recognition event: no shared channel ->
  top-agent assignment share stays near zero at any pressure/budget spread.
- **P3** Accumulation is superlinear early (assignment share grows faster
  than message share), then dilutes as secondary hubs form.
- **P4** Governing the channel at the opening (canonicalization) returns
  penetration/flip behaviour toward the no-signal baseline at far lower cost
  than deposing an accumulated hub. Governed-arm criterion = REDUCTION vs the
  ungoverned twin (per the mock R4 read), not collapse to control.
- **P5 (succession)** The founder need not become the hub: the settled hub is
  predicted by carrying capacity (budget rank), not by discovery order.
  Falsified if settled-hub identity is unrelated to capacity across the
  budget-rotation cells, or if the top assigner never stabilises.
- **P6 (superheat)** At matched pressure, longer sealed accumulation ->
  SHORTER activation->discovery, discovery->flip, and discovery->settle
  latencies. Primary observables are the FLIP latencies (operator amendment
  2026-11-06: "flip not discharge"); velocity/volume are descriptive only.
  Falsified if latencies are flat or increase with sealed duration.
- **H-sweep** Hub concentration peaks at INTERMEDIATE discoverability
  (foam, not a leak, at high d): co-discovery count rises with d while
  single-hub persistence peaks inside the range.

## Measures (frozen definitions)
- Concentration: top-1 assignment share x N (multiple of uniform) and Gini.
  Absolute share does NOT travel across N.
- Flip: cumulative top-1 share >= 0.35 at N=12 (= 4.2x uniform), with >= 10
  assignments. The multiple-of-uniform form is the criterion at other N.
- Succession: harness/live/succession.py definitions — incumbency tie-break
  (challenger must STRICTLY exceed), contested = no top, settled = final
  holder confirmed by a later round, settle lag = settle round - discovery.
- Calibration PASS: >= 50% of agents use the disclosed board.
- Marker penetration: delivered marker count / exposure, by graph distance.

## Code state (frozen)
Local repo head at freeze: 5231327 (plus the freeze commit itself).
Protocol and harness SHA-256:
- docs/RECONSTRUCTION-PROTOCOL.md  0c6162f84d49dbf26c34c83bde8754ee2372b989a558e9675a862d7c324442b9
- docs/ISOMORPHISM-BOILING.md      4c20ef0237aecc5d51949bc1e9135e5e722063a2869712be3087d11aa3a938ce
- docs/SATURDAY-RUN-SHEET.md       0e37de2698069f2828bf0a17355902f892705a9dab94abb1904b73f3fd4c8e84
- docs/report-skeleton.md          3903c8bb096a4570cd89a6826d7fed211e716151a2f53ce3944b672d660249b8
- harness/live/runner.py           11558dd23686cd51240c0c16f89a0a2e0aefe4fb1590ff3e193a48f82cf57252
- harness/live/grid.py             0ede567ee6708ec7bed7fa7ebbefc365f6cfbcf9fde2573009d0554d050c86e1
- harness/live/replay.py           44dd5cf35dfcf637c8278e251ce76fbf72a02ff5dd01fee434f8e583fc96b53b
- harness/live/board.py            8577cc942bab0e5a09b798eb6cd3ea3bec0c3fce2d02911938b91e45800ea210
- harness/live/backends.py         d8c4d5e115ec32c5fba333ff257a8fa638545ca577bfc8c12870dcfb45e34119
- harness/live/calibration.py      de5c105289f821da7645cdaee0d0894a01cf194137619acd5066f638025d5839
- harness/live/succession.py       7dfe231e02cdd4027b03461c1ec5f1ecac6be631426ccc837c488e2fc8be4140

## Instruments (frozen versions)
- Transcript-scoring instrument (preexisting, author's, unvalidated):
  37/37 unit tests at freeze.
- Delegation extractor v2: directed-talk shares ONLY (strict precision 0.20
  on the 20-event hand-judged sample) — never cited as verified delegation.
- Live suites at freeze: live pipeline, replay, succession (29/29),
  superheat — all passing.
- StubCanonicalizer is a STUB (strips the planted marker token only); no run
  under it may be described as governed by the preexisting design.

## Data identities (frozen)
- Live population model: Qwen2.5-0.5B-Instruct Q4_K_M GGUF,
  SHA-256 74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db,
  served by llama.cpp on 127.0.0.1:8123 (tiny-model proxy fence applies).
- Swarm Traces redacted.jsonl.gz: SHA-256
  7b66ab21674de52fcd3f557652f68b1801170c998e2f266862124e6edf283488
  (source URL in data/swarm-traces/README.md; binary not in git).
- Footprint Committee transcript (footprint-store-transcript_7_bsrn.jsonl):
  SHA-256 451ad35f132797931e4561b6e1248db2304ac1cc0f8256ef64678240f80bb74d.
- Adaption datasets (in repo): batch A
  data/adaption-datasets/multi_agent_coordination-batchA-2026-11-07.csv;
  batch B data/adaption-datasets/agent_coordination_prompts-batchB-2026-11-07.csv.
  Audits filed in the tandem scratchpad (A: PASS 3.1%; B: PASS 12.1%).

## Amendment rule (the discipline)
Nothing in this freeze changes silently. Any change to predictions, measures,
criteria, harness behaviour, or population applies ONLY through a dated
addendum appended below + a commit, BEFORE the first run it affects, with the
reason stated. Runs are labelled with the freeze version they executed under.
Results obtained under a superseded version stay labelled as such. A pending
example: the payload generation-cap (max_tokens) harness fix, if adopted,
enters as Amendment 1 before any run it touches — it is NOT in v1.

## Addenda
(none at freeze)

### Amendment 1 — 2026-11-07 ~00:32 ET (naming redaction, operator ruling)
Operator ruling: "If you aren't testing Seraph or Chandra they need to be out
of the pre registration." Neither is under test in this study (the governed arm
runs a labelled stub; the transcript scorer is an applied instrument, not a
test subject). Both proper names are therefore removed from all
preregistration surfaces (this document and the OSF fields text) and replaced
with generic descriptions. No prediction, measure, criterion, code file, or
hash in this freeze is changed by this amendment; harness code artefacts are
untouched and their recorded hashes stand.

### Amendment 2 — 2026-11-07 ~00:37 ET (hash reconciliation audit, operator order)
Operator order: the preregistration must be the exact experiment run, and this
file must be correct with the right hash. Full re-verification of every hash
recorded above against the files on disk:
- MATCH: RECONSTRUCTION-PROTOCOL, ISOMORPHISM-BOILING, SATURDAY-RUN-SHEET,
  all seven harness/live modules (runner, grid, replay, board, backends,
  calibration, succession), the Qwen2.5-0.5B GGUF, Swarm Traces, Footprint
  transcript.
- ONE DIVERGENCE: docs/report-skeleton.md. Frozen hash 3903c8bb...249b8 no
  longer matches the file on disk (now aae3cf25...ecc0) because the working
  title line was edited AFTER the freeze, under the operator's title ruling
  (commit 8dba154). Title line only: no prediction, measure, criterion, or
  results-slot content changed. The skeleton is a report scaffold, not
  protocol or harness; both hashes are recorded here so the record is exact.
- This document's own SHA-256 (this version, Amendment 2 included) is
  recorded in the OSF fields document and stated to the operator at upload;
  the OSF-uploaded copy must hash to that value byte-for-byte.


### Amendment 3 ? 2026-11-07 (execution audit and prospective blinded replication)

Operator direction: procedural fidelity and blinding requirements belong in
this preregistration. This addendum is written AFTER the completed IDE
certification batch. It documents that batch retrospectively and specifies
requirements for a future blinded replication. It does not retroactively
preregister earlier decisions, alter the original predictions or frozen
measure definitions, or replace any prior evidence. The original freeze and
Amendments 1?2 remain available in Git history; this amended file has a new
identity and is not the previously uploaded OSF copy.

#### Completed batch: fidelity and departures

- The nine-cell batch executed the unchanged `tools/replication_driver.py`
  from source commit `f51f88ce`, with the driver's cell configurations.
  All seven harness modules listed in the original freeze match its recorded
  SHA-256 hashes when checked as committed bytes; Windows checkout newline
  conversion is separately accounted for in the calibration record.
- The executor had access to primary results and an earlier local replication
  attempt. The completed certification batch was NOT blinded. This establishes
  prior exposure, not evidence that prompts or model actions were steered.
- `SATURDAY-RUN-SHEET.md` required a ledger line BEFORE each run. Codex's
  publication script appended the per-cell ledger entries AFTER completion.
  This was a procedural departure. Later records do not satisfy that timing
  requirement retroactively.
- Codex's certification wrapper used additional explicit scoring rules:
  zero backend errors, a concentration ratio below 10 with matching sides of
  4.2, and matching strict settlement class in addition to candidate hub
  class. These were not separately committed as a preregistration amendment
  before this batch. The published six-match count is the wrapper's assessment,
  not an unqualified count under only the literal `REPLICATION.md` checklist.
  The frozen succession definition itself remains unchanged.
- Calibration used a separately recorded 300-second timeout after an initial
  60-second transport failure. The completed calibration configuration and
  payload builder were unchanged. Remote model-file identity was not
  independently verified by the executor; deployment-side verification and
  the reported model alias were relied upon.
- Preserve completed, failed, and earlier attempts. Backend failures are not
  interpretable as agent decisions. Neither a fresh run nor rescoring erases
  these records. Evidence: `runs/2026-11-07-ide-certification-batch/BATCH.json`
  and the calibration record linked there.

#### Prospective blinding and execution requirements

1. Before any new live calls, commit a run plan identifying the exact source
   commit, protocol version, model artifact hash, serving configuration,
   calibration gate, cells, seeds, order, request limits, and stopping rules.
   Resolve scoring ambiguities and specify timeout, backend-error, retry,
   invalidation, and incomplete-run handling before observing new outcomes.
   Distinguish the original replication checklist from any added analyses.
2. Use a fresh CLI executor session without prior study outcomes. Supply a
   manifest of permitted protocol/code inputs and an isolated execution bundle
   that excludes previous result directories, summaries, report text, Git
   history, and outcome-bearing handoffs. Merely starting another AI while
   exposing the full results-containing checkout does not establish blinding.
   Record the session's declared exposure and any accidental unblinding.
3. Enter each planned run in the ledger BEFORE its first model request, with
   a timestamp and the pinned plan identity. Record amendments before the
   first affected call. Keep planned, started, completed, and invalid states
   distinguishable; do not change prompts or select retries to obtain agreement.
4. Execute the pinned procedure and retain request/response records, transport
   errors, configurations, source hashes, and every attempt. Hash and seal the
   new outputs before revealing historical outcomes to the executor or making
   comparisons. Record the sealing commit and the unblinding time.
5. Score with the precommitted rules. If comparison requires primary outcomes,
   unblind only after sealing, or use a separate scorer with a documented role.
   Report procedural compliance separately from agreement with predictions.

Status: prospective plan requirements only. No blinded rerun has been executed
or certified by this addendum. Existing results retain their original labels.
