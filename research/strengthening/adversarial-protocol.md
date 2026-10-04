# Adversarial evidence-state tests

Design: HIT-ADV-001. Declared before this workbench's first execution, with AI-assisted expected results. These expectations are development judgments, not an independently established gold standard or an external preregistration.

Each fixture supplies a concrete synthetic scenario, encoded facts, an existing rubric rule, and an expected result. Paired mutations remove relevant evidence, add a contradiction, or change applicability. They exercise the preserved rubric functions without altering normative rules or the conformance engine.

The primary endpoint is exact equality of each returned object to its declared object. Every fixture is reported; failures stop validation. The runner records input and implementation digests. A repeated run over identical bytes must reproduce identical output. Counts refer to synthetic tests, not people or institutional cases.

The cases cover affirmative absence versus silence, time applicability, evidence access timing, contrary evidence, vendor control, unresolved contradictions, Reform follow-up, and shared-origin corroboration. The shared-origin pair explicitly encodes independence as false: the code does not discover source genealogy. Likewise, interpreting source text into facts is outside these tests.

The result cannot establish field validity, reliability, useful deployment, or source truth. Natural-language interpretation requires a separate evaluation, such as the advisory Jev pilot, and human empirical application remains governed by the existing protocol.

## Failure handling

Retain the original expectation and actual result when a mismatch occurs. Determine whether the scenario encoding, expected interpretation, or implementation caused the failure. A scoring-rule change requires contract review. Do not alter expectations merely to obtain a pass. Any revised suite must disclose the change and reason in Git history.
