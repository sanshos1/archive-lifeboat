# Archive Lifeboat

Archive Lifeboat is a source-bound preservation primitive. A curator freezes one public origin, two independent mirrors, and a preservation policy. Validators re-fetch all four records, verify their digests, and produce a six-cell fidelity matrix covering content, context, and provenance for each mirror.

The verdict is derived from that matrix: `SAFE` only when every facet is preserved, `DRIFTED` when neither mirror retains the content, otherwise `PARTIAL`. The owner can seal an inspected capsule, making the full record a finalized preservation receipt.

## Lifecycle

`launch` → `inspect` → owner-only `seal`. Duplicate source sets, mutated sources, malformed matrices, inconsistent verdicts, unauthorized seals, and repeated transitions are rejected.

## Why GenLayer

Exact file hashes alone cannot determine whether a migration retained authorship, dates, labels, ordering, and origin context. Independent validators interpret the frozen public policy while the contract deterministically checks the matrix and derives the verdict.

## Verify

Run `python -m pytest -q`. Live deployment evidence is written to `deployment.json` and `evidence/live-run.json`.
