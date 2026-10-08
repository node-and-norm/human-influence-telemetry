#!/usr/bin/env python3
"""Offline software checks; mocks are not model findings or human review."""
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import run_jev_review as review


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hit-jev-test-")
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "repo"
        self.root.mkdir()
        self.sources = {"sources": [{
            "id": "S1", "url": "https://example.org/report", "publisher": "Fixture publisher",
            "publication_date": "2020-01-01", "updated_date": None,
            "retrieved_at": "2026-10-07", "license": "Synthetic test fixture",
            "passages": [{"id": "P1", "locator": "Section 1", "text": "The body acted in 2020."},
                         {"id": "P2", "locator": "Section 2", "text": "A different body acted in 2021."}],
        }]}
        natural = {"id": "N1", "kind": "natural_claim", "source_claim_id": "C1",
                   "author_decision_ids": ["D1"], "claim": "The body acted in 2020.",
                   "passage_ids": ["P1"], "transformation": "none", "synthetic_evidence": None}
        self.design = {
            "design_id": "HIT-JEV-REVIEW-001", "model": review.MODEL, "mode": "advisory_development",
            "source_packet": "research/sources.json", "protocol": "research/protocol.md",
            "protected_paths": ["research/assessment.json"],
            "items": [natural, {**natural, "id": "F1", "kind": "constructed_diagnostic", "transformation": "formatting"},
                      {**natural, "id": "T1", "kind": "constructed_diagnostic", "transformation": "period", "claim": "The body acted in 2019."},
                      {**natural, "id": "X1", "kind": "constructed_diagnostic", "transformation": "conflict", "synthetic_evidence": "The body did not act in 2020."},
                      {**natural, "id": "N2", "source_claim_id": "C2", "passage_ids": ["P2"]}],
        }
        self.files = {
            "research/design.json": review.encoded(self.design),
            "research/sources.json": review.encoded(self.sources),
            "research/protocol.md": b"# Offline fixture protocol\n",
            "research/assessment.json": b'{"human_decision":"pending"}\n',
            review.RUNNER: Path(review.__file__).read_bytes(),
        }
        for name, raw in self.files.items():
            self.write(name, raw)
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Offline fixture", "-c", "user.email=fixture@example.org", "commit", "-qm", "fixture")
        self.out = self.base / "run"

    def tearDown(self):
        self.temporary.cleanup()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.DEVNULL)

    def write(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def response(self):
        answer = {"type": "choice", "choice": "supported", "probabilities": dict(zip(review.LABELS, (.7, .1, .1, .1))), "confidence": .6}
        return {"model": review.MODEL, "answers": {item["id"]: copy.deepcopy(answer) for item in self.design["items"]}, "usage": {"input_tokens": 40, "output_tokens": 20}}

    def live(self, response=None, transport=None):
        raw = review.encoded(self.response() if response is None else response)
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "offline-test-only"}):
            return review.run("research/design.json", self.out, True, self.root, transport or (lambda request, key: raw))

    def mutate_file_and_hash(self, name, raw):
        (self.out / name).write_bytes(raw)
        meta = review.decoded((self.out / "run.json").read_bytes())
        meta["sha256"][name] = review.digest(raw)
        (self.out / "run.json").write_bytes(review.encoded(meta))

    def test_prepare_is_offline_and_replays(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(review, "send", side_effect=AssertionError("network forbidden")):
            report = review.run("research/design.json", self.out, root=self.root)
        self.assertEqual((report["valid"], report["invalid"], report["not_run"]), (0, 0, 5))
        self.assertEqual(report, review.replay(self.out))
        self.assertEqual(review.decoded((self.out / "run.json").read_bytes())["attempted_requests"], 0)

    def test_questions_are_isolated_and_labels_not_leaked(self):
        request = review.prepare(self.design, self.sources)
        self.assertEqual(request["state"], {})
        first = request["questions"]["N1"]["instructions"]
        last = request["questions"]["N2"]["instructions"]
        self.assertEqual([p["id"] for p in first["passages"]], ["P1"])
        self.assertEqual([p["id"] for p in last["passages"]], ["P2"])
        for prohibited in ("author_decision_ids", "source_claim_id", "expected", "pending_score", '"D1"', '"C1"'):
            self.assertNotIn(prohibited, review.encoded(request).decode())

    def test_formatting_changes_only_whitespace(self):
        request = review.prepare(self.design, self.sources)
        original = request["questions"]["N1"]["instructions"]["passages"][0]
        formatted = request["questions"]["F1"]["instructions"]["passages"][0]
        self.assertEqual(original["text"].split(), formatted["text"].split())
        self.assertNotEqual(original["text"], formatted["text"])
        self.assertEqual({k: v for k, v in original.items() if k != "text"}, {k: v for k, v in formatted.items() if k != "text"})
        self.assertEqual(self.sources["sources"][0]["passages"][0]["text"], original["text"])

    def test_period_claim_and_constructed_conflict_remain_explicit(self):
        questions = review.prepare(self.design, self.sources)["questions"]
        self.assertIn("2019", questions["T1"]["instructions"]["claim"])
        self.assertIn("synthetic, not a historical fact", questions["X1"]["instructions"]["constructed_scenario"]["notice"])
        self.assertNotIn("constructed_scenario", questions["N1"]["instructions"])

    def test_provenance_qualifications_retained_but_raw_blocks_not_sent(self):
        source = self.sources["sources"][0]
        self.sources.update(scope="This is a selected packet, not the full collection.")
        source.update(date_basis="Technical updates do not date substantive changes.",
                      govuk_metadata={"govuk:updated-at": "2026-01-01"},
                      withdrawn=True, withdrawn_at="2024-01-01", withdrawal_notice="Withdrawn guidance.",
                      source_independence="Institutional self-report, not independent verification.",
                      license={"name": "Fixture", "url": "https://example.org/license", "attribution": "Fixture publisher",
                               "scope": "Synthetic text", "observed_page_links": ["https://example.org/license"]})
        passage = source["passages"][0]
        passage.update(text_sha256=review.digest(passage["text"].encode()), govspeak_block_indices_zero_based=[0],
                       blocks=[{"index_zero_based": 0, "tag": "p", "anchor": None, "text": passage["text"]}])
        instruction = review.prepare(self.design, self.sources)["questions"]["N1"]["instructions"]
        self.assertEqual(instruction["packet_scope"], self.sources["scope"])
        returned = instruction["passages"][0]["source"]
        for key in ("date_basis", "govuk_metadata", "withdrawn", "withdrawn_at", "withdrawal_notice", "source_independence"):
            self.assertEqual(returned[key], source[key])
        for key in ("text_sha256", "blocks", "govspeak_block_indices_zero_based"):
            self.assertNotIn(key, instruction["passages"][0])
        passage["text_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            review.prepare(self.design, self.sources)
        passage["text_sha256"] = review.digest(passage["text"].encode())
        passage["blocks"][0]["text"] = "Changed source text"
        with self.assertRaises(ValueError):
            review.prepare(self.design, self.sources)

    def test_reject_malformed_design_and_sources(self):
        mutations = [lambda d: d["items"].append(d["items"][0]),
                     lambda d: d["items"][0].update(expected="supported"),
                     lambda d: d["items"][0].update(passage_ids=["MISSING"]),
                     lambda d: d["items"][0].update(synthetic_evidence="unmarked fiction"),
                     lambda d: d["items"][0].update(transformation="period"),
                     lambda d: d.update(model="jev-latest"),
                     lambda d: d.update(protected_paths=[]),
                     lambda d: d.update(source_packet="../outside.json"),
                     lambda d: d.update(source_packet=".env"),
                     lambda d: d.update(source_packet="research/api_key.json")]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                design = copy.deepcopy(self.design)
                mutation(design)
                with self.assertRaises(ValueError):
                    review.prepare(design, self.sources)
        sources = copy.deepcopy(self.sources)
        sources["sources"][0]["passages"].append(sources["sources"][0]["passages"][0])
        with self.assertRaises(ValueError):
            review.prepare(self.design, sources)

    def test_duplicate_json_and_nonfinite_json_rejected(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                review.decoded(raw)

    def test_only_exact_public_hidden_metadata_path_allowed(self):
        self.assertEqual(review.relative(".zenodo.json"), ".zenodo.json")
        for path in (".env", ".zenodo.json/key", "nested/.zenodo.json", ".zenodo.json.bak", ".git/config", "./.zenodo.json"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                review.relative(path)

    def test_live_sends_exact_retained_bytes_and_replays(self):
        sent = []
        report = self.live(transport=lambda request, key: sent.append(request) or review.encoded(self.response()))
        self.assertEqual(sent, [(self.out / "request.json").read_bytes()])
        self.assertEqual(report["valid"], 5)
        self.assertEqual(report, review.replay(self.out))
        self.assertEqual([row["id"] for row in report["rows"]], [item["id"] for item in self.design["items"]])
        self.assertTrue(all(row["human_review_pending"] for row in report["rows"]))
        self.assertNotIn("matches", report)
        self.assertNotIn("accuracy", report)
        for name, original in self.files.items():
            self.assertEqual((self.root / name).read_bytes(), original)

    def test_invalid_individual_answer_does_not_become_insufficient(self):
        mutations = [lambda a: a.update(choice="insufficient"),
                     lambda a: a.update(confidence=True),
                     lambda a: a.update(confidence=float("nan")),
                     lambda a: a.update(confidence=2),
                     lambda a: a.update(type="score"),
                     lambda a: a.update(probabilities={"supported": 1}),
                     lambda a: a["probabilities"].update(supported=.8),
                     lambda a: a["probabilities"].update(supported=True),
                     lambda a: a["probabilities"].update(supported=-.7)]
        for mutation in mutations:
            response = self.response()
            mutation(response["answers"]["N1"])
            # JSON nonfinite output is an envelope failure; test the other item failures separately.
            raw = json.dumps(response).encode()
            report = review.analyze(self.design, raw, "completed")
            with self.subTest(mutation=mutation):
                self.assertGreater(report["invalid"], 0)
                self.assertIsNone(report["rows"][0]["choice"])
                self.assertEqual(report["rows"][0]["status"], "invalid")

    def test_missing_answer_is_local_failure(self):
        response = self.response()
        del response["answers"]["N1"]
        report = self.live(response)
        self.assertEqual((report["valid"], report["invalid"]), (4, 1))
        self.assertEqual(report, review.replay(self.out))

    def test_bad_model_extra_ids_usage_and_invalid_json_are_failures(self):
        mutations = [lambda r: r.update(model="jev-other"),
                     lambda r: r["answers"].update(unexpected=r["answers"]["N1"]),
                     lambda r: r.update(usage={"input_tokens": True, "output_tokens": 1}),
                     lambda r: r.update(answers=[])]
        for mutation in mutations:
            response = self.response()
            mutation(response)
            self.assertEqual(review.analyze(self.design, review.encoded(response), "completed")["invalid"], 5)
        self.assertEqual(review.analyze(self.design, b"not json", "completed")["invalid"], 5)

    def test_uncommitted_input_stops_before_network_and_output(self):
        for name in self.files:
            with self.subTest(name=name):
                self.write(name, self.files[name] + b"\n")
                with self.assertRaises(ValueError):
                    self.live(transport=lambda *_: self.fail("network forbidden"))
                self.assertFalse(self.out.exists())
                self.write(name, self.files[name])

    def test_no_overwrite_or_protected_output(self):
        review.run("research/design.json", self.out, root=self.root)
        before = (self.out / "run.json").read_bytes()
        with self.assertRaises(FileExistsError):
            review.run("research/design.json", self.out, root=self.root)
        self.assertEqual(before, (self.out / "run.json").read_bytes())
        for path in (self.root / "research/assessment.json", self.root / "research/assessment.json/run"):
            with self.assertRaises(ValueError):
                review.run("research/design.json", path, root=self.root)

    def test_symlink_input_rejected(self):
        path = self.root / "research/protocol.md"
        path.unlink()
        path.symlink_to(self.root / "research/assessment.json")
        with self.assertRaises(ValueError):
            review.run("research/design.json", self.out, root=self.root)

    def test_missing_mandatory_hash_or_file_rejected(self):
        self.live()
        meta = review.decoded((self.out / "run.json").read_bytes())
        for name in list(meta["sha256"]):
            bad = copy.deepcopy(meta)
            del bad["sha256"][name]
            (self.out / "run.json").write_bytes(review.encoded(bad))
            with self.subTest(name=name), self.assertRaises(ValueError):
                review.replay(self.out)
        (self.out / "run.json").write_bytes(review.encoded(meta))
        (self.out / "response.raw").unlink()
        with self.assertRaises(ValueError):
            review.replay(self.out)

    def test_changed_snapshots_rejected(self):
        self.live()
        path = self.out / "protected/0000.bin"
        path.write_bytes(b"changed")
        with self.assertRaises(ValueError):
            review.replay(self.out)

    def test_request_rebuilt_even_when_tamper_hash_updated(self):
        self.live()
        request = review.decoded((self.out / "request.json").read_bytes())
        request["state"] = {"leaked_decision": "approved"}
        self.mutate_file_and_hash("request.json", review.encoded(request))
        with self.assertRaises(ValueError):
            review.replay(self.out)

    def test_derived_analysis_recomputed_even_when_hash_updated(self):
        self.live()
        analysis = review.decoded((self.out / "analysis.json").read_bytes())
        analysis["rows"][0]["human_review_pending"] = False
        self.mutate_file_and_hash("analysis.json", review.encoded(analysis))
        with self.assertRaises(ValueError):
            review.replay(self.out)

    def test_completed_run_cannot_be_relabelled_prepared(self):
        self.live()
        meta = review.decoded((self.out / "run.json").read_bytes())
        meta["status"] = "prepared"
        report_bytes = review.encoded(review.analyze(self.design, None, "prepared"))
        (self.out / "analysis.json").write_bytes(report_bytes)
        meta["sha256"]["analysis.json"] = review.digest(report_bytes)
        (self.out / "run.json").write_bytes(review.encoded(meta))
        with self.assertRaises(ValueError):
            review.replay(self.out)

    def test_lifecycle_fields_are_typed_and_consistent(self):
        self.live()
        original = review.decoded((self.out / "run.json").read_bytes())
        mutations = [{"attempted_requests": True}, {"attempted_requests": 0}, {"response_received": "true"},
                     {"protected_unchanged": 1}, {"protected_unchanged": False}, {"inputs_committed": None},
                     {"finished_at": None}, {"request_seconds": True}, {"http_status": 403},
                     {"status": "incomplete"}, {"status": "failed", "failure": None},
                     {"status": "failed", "failure": "transport_or_configuration_failure"}]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                (self.out / "run.json").write_bytes(review.encoded({**original, **mutation}))
                with self.assertRaises(ValueError):
                    review.replay(self.out)

    def test_interrupted_attempt_replays_as_technical_failure(self):
        calls = []
        def interrupted(*_):
            calls.append(1)
            raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            self.live(transport=interrupted)
        report = review.replay(self.out)
        self.assertEqual(calls, [1])
        self.assertEqual(report["run_status"], "incomplete")
        self.assertEqual((report["valid"], report["invalid"], report["not_run"]), (0, 5, 0))
        self.assertEqual(report["technical_errors"], ["incomplete_run"])
        self.assertTrue(all(row["human_review_pending"] for row in report["rows"]))

    def test_transport_failure_preserved_without_error_body_or_secret(self):
        class ErrorBody(io.BytesIO):
            reads = 0
            def read(self, *args):
                self.reads += 1
                return super().read(*args)
        secret_body = ErrorBody(b"private error body offline-test-only")
        def fail(*_):
            raise urllib.error.HTTPError(review.ENDPOINT, 429, "private exception message", {}, secret_body)
        report = self.live(transport=fail)
        self.assertEqual(report["invalid"], 5)
        self.assertEqual(report, review.replay(self.out))
        self.assertEqual(secret_body.reads, 0)
        for path in self.out.rglob("*"):
            if path.is_file():
                self.assertNotIn(b"private exception message", path.read_bytes())
                self.assertNotIn(b"offline-test-only", path.read_bytes())
        self.assertEqual(review.decoded((self.out / "run.json").read_bytes())["http_status"], 429)

    def test_timeout_not_retried_and_missing_key_recorded(self):
        calls = []
        def timeout(*_):
            calls.append(1)
            raise TimeoutError("private detail")
        self.assertEqual(self.live(transport=timeout)["invalid"], 5)
        self.assertEqual(calls, [1])
        with patch.dict(os.environ, {}, clear=True):
            report = review.run("research/design.json", self.base / "missing-key", True, self.root, lambda *_: self.fail("network forbidden"))
        self.assertEqual(report["run_status"], "failed")
        self.assertEqual(report, review.replay(self.base / "missing-key"))
        self.assertEqual(review.decoded((self.base / "missing-key/run.json").read_bytes())["attempted_requests"], 0)

    def test_protected_change_during_run_is_a_failure(self):
        def changed(*_):
            self.write("research/assessment.json", b"changed by another process")
            return review.encoded(self.response())
        report = self.live(transport=changed)
        self.assertEqual(report["run_status"], "failed")
        self.assertEqual(report["technical_errors"], ["protected_input_changed"])
        self.assertEqual(report, review.replay(self.out))

    def test_transport_disables_proxy_and_redirect_and_uses_fixed_url(self):
        class Response:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *_): pass
            def geturl(self): return review.ENDPOINT
            def read(self): return b"{}"
        with patch.object(review.urllib.request, "build_opener") as build:
            build.return_value.open.return_value = Response()
            self.assertEqual(review.send(b"request bytes", "offline-test-only"), b"{}")
            handlers = build.call_args.args
            self.assertEqual(handlers[0].proxies, {})
            self.assertIsInstance(handlers[1], review.NoRedirect)
            self.assertIsNone(handlers[1].redirect_request(None, None, 302, "redirect", {}, "https://elsewhere.invalid"))
            request = build.return_value.open.call_args.args[0]
            self.assertEqual(request.full_url, review.ENDPOINT)
            self.assertEqual(request.data, b"request bytes")
            self.assertEqual(build.return_value.open.call_args.kwargs, {"timeout": 45})


class RepositoryDesignTests(unittest.TestCase):
    """Construction checks on the actual packet, not expected model-response labels."""

    @classmethod
    def setUpClass(cls):
        cls.design = review.decoded((review.ROOT / review.DEFAULT_DESIGN).read_bytes())
        cls.sources = review.decoded((review.ROOT / cls.design["source_packet"]).read_bytes())
        cls.request = review.prepare(cls.design, cls.sources)
        cls.items = {item["id"]: item for item in cls.design["items"]}

    def test_fourteen_items_and_exact_natural_claims(self):
        self.assertEqual(list(self.items), ["N01", "N02", "N03", "N04", "N05", "N06", "B01", "B02", "B03", "B04", "P01", "P02-base", "P02", "P03"])
        assessment = review.decoded((review.ROOT / "research/strengthening/solo-002-complete/assessment.draft.json").read_bytes())
        claims = {claim["claim_id"]: claim["proposition"] for claim in assessment["evidence_claims"]}
        natural = [item for item in self.design["items"] if item["kind"] == "natural_claim"]
        self.assertEqual(len(natural), 6)
        self.assertEqual({item["source_claim_id"] for item in natural}, {"EC-ADVICE", "EC-REASONS", "EC-REISSUE-REQUIREMENT", "EC-ISSUE-CORRECTION", "EC-EXTERNAL-LIMIT", "EC-ADMISSIONS-LIMIT"})
        for item in natural:
            with self.subTest(item=item["id"]):
                self.assertEqual(item["claim"], claims[item["source_claim_id"]])

    def test_declared_probe_pair_construction(self):
        base = self.items["N04"]
        for name, transformation in (("P01", "period"), ("P02", "conflict"), ("P03", "formatting")):
            item = self.items[name]
            self.assertEqual(item["kind"], "constructed_diagnostic")
            self.assertEqual(item["passage_ids"], base["passage_ids"])
            self.assertEqual(item["transformation"], transformation)
            self.assertIsNone(item["source_claim_id"])
        self.assertIn("19 August", base["claim"])
        self.assertIn("same replacement", self.items["P01"]["claim"])
        self.assertIn("12 August 2020", self.items["P01"]["claim"])
        self.assertEqual(self.items["P03"]["claim"], base["claim"])
        conflict_base = self.items["P02-base"]
        self.assertEqual(conflict_base["claim"], "Replacement AS/A level grades were sent to schools and colleges on 19 August 2020.")
        self.assertEqual(self.items["P02"]["claim"], conflict_base["claim"])
        self.assertEqual(conflict_base["kind"], "constructed_diagnostic")
        self.assertEqual(conflict_base["transformation"], "none")
        self.assertEqual(conflict_base["passage_ids"], self.items["P02"]["passage_ids"])
        self.assertIn("neither has precedence", self.items["P02"]["synthetic_evidence"])
        question = self.request["questions"]
        base_text = question["N04"]["instructions"]["passages"][0]["text"]
        formatted_text = question["P03"]["instructions"]["passages"][0]["text"]
        self.assertEqual(base_text.split(), formatted_text.split())
        self.assertNotEqual(base_text, formatted_text)
        self.assertEqual(question["N04"]["instructions"]["passages"], question["P01"]["instructions"]["passages"])
        self.assertIn("constructed_scenario", question["P02"]["instructions"])
        self.assertNotIn("constructed_scenario", question["P02-base"]["instructions"])
        self.assertEqual(question["P02-base"]["instructions"]["passages"], question["P02"]["instructions"]["passages"])

    def test_actual_default_prepare_and_replay_without_network(self):
        with tempfile.TemporaryDirectory(prefix="hit-jev-integration-") as temporary:
            output = Path(temporary) / "prepared"
            with patch.dict(os.environ, {}, clear=True):
                report = review.run(review.DEFAULT_DESIGN, output, transport=lambda *_: self.fail("network forbidden"))
            self.assertEqual((report["scheduled"], report["valid"], report["invalid"], report["not_run"]), (14, 0, 0, 14))
            self.assertEqual(report, review.replay(output))
            self.assertIn(".zenodo.json", self.design["protected_paths"])
            self.assertTrue(all(row["human_review_pending"] for row in report["rows"]))


if __name__ == "__main__":
    unittest.main()
