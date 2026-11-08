# IDE certification cell p5a

Assessment: **not_certified**.

Assignments: 46; flip: False; marker delivered: 0; backend errors: 79.
Hub candidate: None; settled: False; strict class: unsettled.

Verified calibration: 10/10 board users at commit f51f88ce. The unchanged tools/replication_driver.py executed this cell.
This is an explicitly requested fresh batch; prior local replicas are retained separately. No outcome was retried into agreement.

## Checks

- same_config: True
- no_backend_errors: False
- flip_matches: True
- candidate_class_matches: False
- marker_presence_matches: True
- concentration_regime_matches: True
- strict_settlement_matches: False

Strict settlement is shown separately because a candidate ID can exist while settled=false; regime means ratio<10 and same side of 4.2. No statistical-equivalence claim.

Inspect CERTIFICATION.json, summary.json, succession.json and transport.jsonl. Raw HTTP bodies are retained, without authorization headers.
Backend errors are failures, not model behavior. A zero driver exit status alone is not certification.
