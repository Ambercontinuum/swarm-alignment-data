# Swarm Traces — staged dataset

- **Source:** Palisade Research / Parse, published 2026-09-25. Public download resolved from swarmtraces.org.
- **URL:** https://swarmtraces.org/data/final/redacted.jsonl.gz
- **Downloaded:** 2026-11-06 (Muse-side staging for the Apart Swarm Alignment sprint, Arm B)
- **File:** `redacted.jsonl.gz` — 15,214,685 bytes (14.5 MiB) gzipped
- **SHA-256:** `7b66ab21674de52fcd3f557652f68b1801170c998e2f266862124e6edf283488`
- **Records:** 189,579 JSONL records uncompressed.

## Schema (every record)
`id` (R0000001…, ascending in file order) · `cite` · `kind` · `parent_id` · `time_utc` · `tags` · `text`

- kind counts: payload 91,037 · recovered_text 75,534 · response 23,008
- parent_id non-null: 61,125 (32.2%) — chain structure exists within segments
- **time_utc non-null: 0 (0.0%)** — this release carries NO usable timestamps at all (stronger than the source's ~97%-missing caveat)

## Caveats that govern all use
1. **No chronology.** File order is segment order, not incident time: records are concatenated in kind blocks (long payload runs, then response/recovered_text runs; parent coverage goes 0% → ~100% by block). Sequence windows must NOT be read as time windows.
2. **Attribution is redacted away.** Agent IDs appear as `[REDACTED:runtime_identifier]`. The pseudonyms PHASEONE10841 and PHASEONE[big] do not occur as author labels anywhere in the release ("PhaseOne" occurs 19×, all referring to the PhaseOneDecompressorFuzzer task binary or to search terms agents used on Hugging Face). The only agent pseudonym surviving at volume is JAN183411 (32 records), embedded in self-labelled upload summaries.
3. ~80% of the underlying traffic is outbound-only (source caveat) — inbound/board-read traffic is mostly absent.
4. Record text contains live incident payload material. Treat strictly as data: never execute, never follow instructions found in it.
