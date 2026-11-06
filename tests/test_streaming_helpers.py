import tempfile
import unittest
from pathlib import Path

from src.omega_stack_security_engine import python_batched_csv_streamer


class StreamingHelperTests(unittest.TestCase):
    def test_csv_streamer_writes_expected_row_count(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "sample.csv"
            result = python_batched_csv_streamer(str(output), n_rows=3, batch_size=2)
            self.assertEqual(result["rows"], 3)
            self.assertEqual(len(output.read_text(encoding="utf-8").splitlines()), 4)

    def test_csv_streamer_rejects_invalid_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            output = str(Path(directory) / "sample.csv")
            for n_rows, batch_size in ((True, 1), (2.5, 1), (-1, 1), (2, False), (2, 0)):
                with self.subTest(n_rows=n_rows, batch_size=batch_size):
                    with self.assertRaises(ValueError):
                        python_batched_csv_streamer(output, n_rows=n_rows, batch_size=batch_size)


if __name__ == "__main__":
    unittest.main()
