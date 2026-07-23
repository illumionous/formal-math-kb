import tempfile
import unittest
from pathlib import Path

from pipeline.dedup import deduplicate
from pipeline.generate import generate_records
from pipeline.lean import LeanVerifier
from pipeline.verify import validate_example, verify_records


ROOT = Path(__file__).resolve().parents[1]


class PipelineTest(unittest.TestCase):
    def test_generation_is_seeded_and_structurally_valid(self) -> None:
        first = generate_records(ROOT / "kb", 10, seed=42)
        second = generate_records(ROOT / "kb", 10, seed=42)
        self.assertEqual(first, second)
        self.assertTrue(all(not validate_example(record) for record in first))

    def test_skip_mode_never_claims_formal_verification(self) -> None:
        records = generate_records(ROOT / "kb", 2, seed=1)
        with tempfile.TemporaryDirectory() as directory:
            verifier = LeanVerifier(Path(directory), mode="skip")
            output, accepted = verify_records(records, verifier)
        self.assertEqual(accepted, 0)
        self.assertTrue(all(record["verified"] is False for record in output))

    def test_dedup_filters_unverified_and_exact_duplicates(self) -> None:
        record = generate_records(ROOT / "kb", 1, seed=2)[0]
        record["verified"] = True
        self.assertEqual(len(deduplicate([record, dict(record)])), 1)
        record["verified"] = False
        self.assertEqual(deduplicate([record]), [])


if __name__ == "__main__":
    unittest.main()
