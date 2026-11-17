import unittest
from unittest.mock import MagicMock, call

from tpch_sf1 import EXPECTED_COUNTS, load_and_verify


Q4_ROWS = [
    ("1-URGENT", 10_594),
    ("2-HIGH", 10_476),
    ("3-MEDIUM", 10_410),
    ("4-NOT SPECIFIED", 10_556),
    ("5-LOW", 10_487),
]


class LoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = MagicMock()
        self.cur = self.conn.cursor.return_value.__enter__.return_value
        self.cur.fetchall.side_effect = [[], Q4_ROWS]
        self.cur.fetchone.side_effect = [
            (count,) for count in EXPECTED_COUNTS.values()
        ]

    def test_generates_and_commits_verified_sf1(self) -> None:
        self.assertEqual(load_and_verify(self.conn), EXPECTED_COUNTS)
        self.cur.execute.assert_any_call(operation="CALL dbgen(sf = 1)")
        self.conn.commit.assert_called_once()

    def test_existing_complete_dataset_is_not_appended(self) -> None:
        self.cur.fetchall.side_effect = [
            [(table,) for table in EXPECTED_COUNTS],
            Q4_ROWS,
        ]
        load_and_verify(self.conn)
        self.assertNotIn(
            call(operation="CALL dbgen(sf = 1)"), self.cur.execute.call_args_list
        )
        self.conn.commit.assert_called_once()

    def test_partial_dataset_fails_before_writes(self) -> None:
        self.cur.fetchall.side_effect = [[("orders",)]]
        with self.assertRaisesRegex(RuntimeError, "Partial TPC-H tables"):
            load_and_verify(self.conn)
        self.assertEqual(self.cur.execute.call_count, 1)
        self.conn.commit.assert_not_called()

    def test_wrong_scale_is_not_committed(self) -> None:
        self.cur.fetchone.side_effect = [(5,), (25,), (1_000,)]
        with self.assertRaisesRegex(RuntimeError, "supplier: expected"):
            load_and_verify(self.conn)
        self.conn.commit.assert_not_called()

    def test_wrong_query_result_is_not_committed(self) -> None:
        self.cur.fetchall.side_effect = [[], []]
        with self.assertRaisesRegex(RuntimeError, "query 4 verification failed"):
            load_and_verify(self.conn)
        self.conn.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
