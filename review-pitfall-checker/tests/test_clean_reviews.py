import csv
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.clean_reviews import clean_reviews_from_csv


def write_reviews_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["review_id", "text", "rating", "useful_count"]
        )
        writer.writeheader()
        writer.writerows(rows)


class CleanReviewsTest(unittest.TestCase):
    def test_filters_short_incentivized_and_duplicate_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            source = Path(tmp_dir) / "reviews.csv"
            write_reviews_csv(
                source,
                [
                    {
                        "review_id": "r1",
                        "text": "包装破损，客服处理很慢，老人用起来不方便",
                        "rating": "2",
                        "useful_count": "8",
                    },
                    {
                        "review_id": "r2",
                        "text": "太差",
                        "rating": "1",
                        "useful_count": "1",
                    },
                    {
                        "review_id": "r3",
                        "text": "商家发的红包，好评返现，大家快来买",
                        "rating": "5",
                        "useful_count": "0",
                    },
                    {
                        "review_id": "r1",
                        "text": "重复评论应该被去掉",
                        "rating": "1",
                        "useful_count": "9",
                    },
                ],
            )

            cleaned = clean_reviews_from_csv(source)

        self.assertEqual(
            cleaned,
            [
                {
                    "review_id": "r1",
                    "text": "包装破损，客服处理很慢，老人用起来不方便",
                    "rating": 2,
                    "useful_count": 8,
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
