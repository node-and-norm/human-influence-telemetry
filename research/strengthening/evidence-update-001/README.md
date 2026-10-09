# Evidence-update representation rehearsal

This controlled benchmark asks whether two equivalent-content representations support correct identification of deliberately changed documentary propositions. It compares a HIT-inspired typed graph with a capable structured-review table. The eight propositions, source links and qualifications are the same in both; navigation labels and the placement of links differ.

Read [the protocol](PROTOCOL.md) before using the outputs. The [shared dossier](inputs/dossier.json), [updates](inputs/updates.json), [trial instructions](inputs/instructions.md) and two packets are synthetic teaching fixtures. The [oracle](inputs/oracle.json) contains planned answers and must not be given to a trial executor. It is public for audit after execution; access isolation is not guaranteed.

Prepare and check with:

```sh
python scripts/run_evidence_update_benchmark.py --prepare
python scripts/test_evidence_update_benchmark.py
```

Preparation checks file hashes and equivalent semantic content. It does not run a trial. Commit and push all frozen files before collecting the two responses. Supply each executor only its permitted inputs and their hashes, along with the full freeze commit. Save the actual responses as responses/hit_graph.json and responses/structured_table.json. Then run:

```sh
python scripts/run_evidence_update_benchmark.py --analyze
```

Analysis prints a deterministic report and does not edit files or contact a model. A checkout with the freeze commit available is required. The report separates affected-claim misses and false positives, state-label agreement, qualification-enum agreement and narrow content tokens. Statement meaning remains pending author review. The run cannot establish comparative utility, effort reduction, human reliability or v1.0 readiness.
