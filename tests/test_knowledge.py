import unittest
from pathlib import Path

from pipeline.knowledge import load_knowledge_base, prerequisite_path


ROOT = Path(__file__).resolve().parents[1]


class KnowledgeBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.points = load_knowledge_base(ROOT / "kb")

    def test_representative_base_has_twelve_items(self) -> None:
        self.assertEqual(len(self.points), 12)

    def test_prerequisites_are_topologically_ordered(self) -> None:
        path = prerequisite_path(self.points, "func.quadratic.vertex")
        self.assertEqual(path, ["func.square.nonnegative", "func.quadratic.vertex"])

    def test_all_six_topics_are_covered(self) -> None:
        topics = {point.id.split(".", 1)[0] for point in self.points.values()}
        self.assertEqual(topics, {"alg", "func", "seq", "trig", "geom", "prob"})


if __name__ == "__main__":
    unittest.main()
