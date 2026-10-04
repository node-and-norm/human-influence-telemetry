# Passage perturbation experiment

HIT-JEV-002 tests whether a model preserves claim boundaries across short evidence passages. This is a development experiment using assistant-authored passages, not a test of full-document extraction, HIT scoring, or independent human agreement. Expected labels are assistant judgments awaiting author review.

The base passage condenses Ofqual's 17 August 2020 announcement, reviewed in solo-bc.md. Every passage is a constructed test input. Actor substitutions, contradictions, and changed dates are fictional perturbations; none is a new historical source. The exact text and expectations are in passage-cases.json. No copyrighted document is sent in full.

Freeze the design, protocol, and runner in Git before one request to jev-1.13.0. Use ten isolated Choice questions with empty shared state; embed only the relevant packet and claim in each question. Exclude expectations, transformation names, and other packets from the request. The TypeSafe skill and live API, Choice, and citation-checking documentation informed this decomposition. Retain the request, raw response, model identifier, usage, timing, code digest, and commit. No retry or fallback is permitted.

P01 is the source-derived positive control. P02 removes the decision. P03 paraphrases it. P04 reverses the order of the base sentences. P05 substitutes the actor. P06 substitutes the date. P07 adds a conflicting assertion without a resolution. P08 duplicates the base passage. P09 asks whether delivery was completed, which the base passage does not resolve. P10 negates the announced decision in the claim. Expected labels are specified for every condition before inference. P03, P04, and P08 should retain P01's supported label. P02, P05, P06, P07, and P09 should be insufficient; P10 should be contradicted.

Report each response, agreement with all ten expectations, and failures of the three invariance relations. Missing or malformed responses remain failed scheduled items. Do not tune the inputs after seeing answers or generalize accuracy from this small, exposed test set. Confidence describes the model distribution, not historical truth. A successful test cannot resolve the dossiers' outstanding author judgments.

Run the existing runner with `--design research/strengthening/passage-cases.json --protocol research/strengthening/passage-protocol.md --live --output research/strengthening/jev-live-002`. Supply the authorized private credential through the process environment. Replay with `--analyze research/strengthening/jev-live-002`, without network access.
