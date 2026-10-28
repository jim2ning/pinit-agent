import unittest
from agent import connect, factor, record, validate

class Tests(unittest.TestCase):
    def test_personalization_and_isolation(self):
        db = connect(":memory:")
        for _ in range(5): record(db, "a", "취업", 10, 20)
        self.assertEqual(factor(db, "a", "취업"), (2, 5))
        self.assertEqual(factor(db, "b", "취업"), (1, 0))
        self.assertEqual(factor(db, "a", "공부"), (1, 0))
        db.close()
    def test_limit_after_calibration(self):
        with self.assertRaises(ValueError):
            validate([{"title":"초안", "done_when":"완료", "base_minutes":20}], 2)
    def test_rounding(self):
        self.assertEqual(validate([{"title":"개요", "done_when":"3개 작성", "base_minutes":12}], 1.2)[0]["estimated_minutes"], 15)

if __name__ == "__main__": unittest.main()

