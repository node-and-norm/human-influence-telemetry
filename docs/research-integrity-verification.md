# What the research-integrity checks establish

8 October 2026. This clarification supplements the preserved v0.6.5 audit; it does not replace its map, generated figures or historical outputs.

## Declared judgments and checked files

The historical evaluator resolves evidence locators, aggregates recorded integrity and human-support states, applies declared fitness judgments, and propagates claim dependencies. Its eight negative controls exercise specified changes to those declarations. An accepted `git_tracked` or `locked_digest` label is not, by itself, proof that the referenced file was checked against Git or a digest. Likewise, a recorded human-review state does not authenticate the underlying review or establish source truth.

The additive [file-binding checker](../scripts/validate_claim_bindings.py) supplies a separate, narrower verification. Its [frozen bindings](../evidence/research-integrity-bindings.json) identify 13 claims and 19 evidence references from the map at commit `9af12f6cb891288f692990366e54b85bd21d9e24`. It requires the referenced files to be tracked regular files within the repository, rejects symlink inputs, and compares their bytes with that commit. It also checks the locked comparison's SHA-256 against the preservation and execution records. File identity does not establish document authenticity or a sound interpretation.

The checker separately rejects duplicate identifiers, unknown or repeated dependencies, self-dependencies and dependency cycles. These are structural checks, not an assessment of whether a dependency is scientifically adequate. The historical map has no detected cycle; the additive check does not change its reported eligibility.

## Reproduction and maintenance

Use a full Git clone with the retained history available:

```bash
python scripts/validate_claim_bindings.py --check
python -W error scripts/test_claim_bindings.py
python scripts/run_research_integrity_audit.py --check
```

The ten added tests include direct graph checks, untracked and missing files, changed bytes despite a modified manifest, symlinks, unsafe paths, and altered preservation records. Passing these controls supports file and dependency consistency for the tested inputs. It does not validate human review, evidence fitness, source truth or new conclusion eligibility. The historical audit still reports `PASS_WITH_EXCEPTIONS` within its original scope.

The new bindings deliberately pin their inputs to a named historical commit. They are not a general authorization to freeze every future repository version. If an authorized release changes a bound file, preserve this verification record and make an explicit, reviewed amendment or introduce a separately versioned verification record. Do not silently regenerate the freeze to suppress a failed check. The qualitative reanalysis checker also pins release metadata and normative inputs; a future legitimate version change requires the same explicit treatment.
