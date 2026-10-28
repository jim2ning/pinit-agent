import unittest
from agent import connect, record
from graph_agent import plan

class GraphTests(unittest.TestCase):
    def setUp(self): self.db = connect(":memory:")
    def tearDown(self): self.db.close()
    def test_retry_uses_personalized_factor(self):
        for _ in range(5): record(self.db, "a", "취업", 10, 20)
        seen = []
        def generate(state):
            seen.append((state["multiplier"], state["error"]))
            return [{"title":"공고 조사", "done_when":"공고 하나 정리", "base_minutes":20 if len(seen)==1 else 15}]
        result = plan(self.db, "a", "취업", "자소서", generate)
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(result["tasks"][0]["estimated_minutes"], 30)
        self.assertEqual(seen[0][0], 2)
        self.assertIn("30분", seen[1][1])
    def test_exhausted_retries_fail(self):
        calls = []
        def generate(state):
            calls.append(1)
            return [{"title":"너무 큼", "done_when":"완료", "base_minutes":40}]
        with self.assertRaises(ValueError): plan(self.db, "a", "취업", "자소서", generate)
        self.assertEqual(len(calls), 3)

if __name__ == "__main__": unittest.main()

