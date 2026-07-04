import json
import tempfile
import unittest
from pathlib import Path

from xquik_export import load_xquik_rows


class XquikExportTest(unittest.TestCase):
    def test_load_wrapped_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            export_path = Path(tmp_dir) / "tweets.json"
            export_path.write_text(
                json.dumps(
                    {
                        "data": [
                            {
                                "username": "alice",
                                "full_text": "first row",
                                "like_count": "4",
                                "retweets": "2",
                                "created_at": "2026-01-01T00:00:00Z",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            rows = load_xquik_rows(export_path)
            self.assertEqual(rows[0]["username"], "alice")
            self.assertEqual(rows[0]["text"], "first row")
            self.assertEqual(rows[0]["like_count"], 4)
            self.assertEqual(rows[0]["retweet_count"], 2)

    def test_load_csv(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            export_path = Path(tmp_dir) / "tweets.csv"
            export_path.write_text("user,text,likes,replies\nbob,second row,3,1\n", encoding="utf-8")
            rows = load_xquik_rows(export_path)
            self.assertEqual(rows[0]["username"], "bob")
            self.assertEqual(rows[0]["text"], "second row")
            self.assertEqual(rows[0]["like_count"], 3)
            self.assertEqual(rows[0]["reply_count"], 1)

    def test_reject_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            export_path = Path(tmp_dir) / "tweets.json"
            export_path.write_text("{bad", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                load_xquik_rows(export_path)


if __name__ == "__main__":
    unittest.main()
