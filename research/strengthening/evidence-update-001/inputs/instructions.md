# Trial instructions

This is an AI-assisted rehearsal of a controlled evidence-update representation task. All sources are constructed. Do not look up Ofqual or import historical findings. Use only this file, the shared dossier, the update file and the single method packet supplied to you. Do not read the oracle, scorer, design, other method packet, other response or surrounding research files. This access request cannot establish blinding or independent review.

For each of U00–U04, start again from the original packet. Apply that scenario's change only. For each proposition P01–P08, report whether its substantive assessment needs revision, its documentary support state, a short updated statement, the evidence IDs considered and your reasoning. A changed admissible reference alone does not require a substantive proposition revision. Withdrawal removes the source as current support; it does not prove the contrary. Use the updated state's meaning, not the grammatical truth of a sentence that describes uncertainty.

Allowed support states are supported, limited_support, unsupported, unresolved and conflicted. These are benchmark documentary states, not HIT finding categories. supported means the packet directly supplies the bounded proposition. limited_support marks the packet's explicit single-account restriction on actual issuance, as distinct from the fact that a report was published. It is not a general penalty for a bounded population: a directly supplied eligibility boundary or authenticated receipt for a named subset can be supported within that boundary. unsupported means former affirmative support has been removed without a replacement; unresolved means the packet cannot determine the matter; conflicted means equally admissible accounts contradict each other on the same occurrence. No state independently verifies a source's truth.

For each Q01–Q07, select exactly one state from that qualification's allowed_states and explain how it applies after the update. Record substantive scope in the updated statement and rationale; listing IDs alone is insufficient. Your prose will remain pending author review even when enums match the scorer.

Return a single JSON response. The coordinator supplies protocol_commit and input_sha256 after freeze. Do not invent participant identities, external tools, human review or elapsed-time measurements. Use this shape:

```json
{
  "study_id": "HIT-EU-001",
  "method_id": "<supplied method>",
  "protocol_commit": "<supplied full commit>",
  "input_sha256": {"<supplied path>": "<supplied digest>"},
  "executor": "ai_assistant",
  "independent_review": false,
  "author_review": "pending",
  "access_declaration": "Describe which permitted files you read and any exposure outside them; do not claim guaranteed blinding.",
  "scenarios": [
    {
      "id": "U00",
      "claims": [
        {"id": "P01", "action": "retain", "status": "supported", "updated_statement": "Your bounded statement.", "evidence_refs": ["S01"], "rationale": "Your reasoning."}
      ],
      "qualifications": [
        {"id": "Q01", "state": "synthetic_only", "rationale": "Your reasoning."}
      ]
    }
  ]
}
```

The complete response must contain five scenarios, eight claim rows and seven qualification rows per scenario. action is retain or revise. Evidence references may name a withdrawn source to explain its withdrawal, but the rationale must not treat it as remaining admissible support. References may use only original sources plus the new sources for that scenario. No aggregate utility or superiority conclusion is requested.
