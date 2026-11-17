import argparse
import getpass
import os

from adbc_driver_hardcharger import dbapi as hardcharger


EXPECTED_COUNTS = {
    "region": 5,
    "nation": 25,
    "supplier": 10_000,
    "customer": 150_000,
    "part": 200_000,
    "partsupp": 800_000,
    "orders": 1_500_000,
    "lineitem": 6_001_215,
}


def load_and_verify(conn: hardcharger.Connection) -> dict[str, int]:
    with conn.cursor() as cur:
        cur.execute(
            operation=(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_catalog = current_database() AND table_schema = 'main'"
            )
        )
        existing = {row[0] for row in cur.fetchall()} & EXPECTED_COUNTS.keys()
        if existing and existing != EXPECTED_COUNTS.keys():
            raise RuntimeError(
                f"Partial TPC-H tables already exist: {sorted(existing)}. "
                "No data was generated; use an empty database or inspect these tables."
            )

        cur.execute(operation="INSTALL tpch")
        cur.execute(operation="LOAD tpch")
        if not existing:
            print("Generating TPC-H SF=1 on the server...", flush=True)
            cur.execute(operation="CALL dbgen(sf = 1)")
        else:
            print("TPC-H tables already exist; verifying without appending data.")

        counts = {}
        for table, expected in EXPECTED_COUNTS.items():
            cur.execute(operation=f'SELECT count(*) FROM main."{table}"')
            row = cur.fetchone()
            if row is None or row[0] != expected:
                raise RuntimeError(
                    f"{table}: expected {expected:,} rows, got {row!r}. "
                    "Changes will not be committed."
                )
            counts[table] = row[0]

        cur.execute(operation="PRAGMA tpch(4)")
        actual = cur.fetchall()
        expected_q4 = [
            ("1-URGENT", 10_594),
            ("2-HIGH", 10_476),
            ("3-MEDIUM", 10_410),
            ("4-NOT SPECIFIED", 10_556),
            ("5-LOW", 10_487),
        ]
        if actual != expected_q4:
            raise RuntimeError(f"TPC-H query 4 verification failed: {actual!r}")

    conn.commit()
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load and verify TPC-H SF=1 through the local Hardcharger API."
    )
    parser.add_argument(
        "--uri",
        default="hardcharger://127.0.0.1:31337/warp?tls=false",
        help="Connection URI; the default matches this desktop server's /warp API.",
    )
    parser.add_argument(
        "--username", default=os.environ.get("HARDCHARGER_USER", "hardcharger")
    )
    args = parser.parse_args()
    password = getpass.getpass(f"Hardcharger password for {args.username}: ")
    if not password:
        parser.error("A nonempty server password is required.")

    with hardcharger.connect(
        uri=args.uri,
        username=args.username,
        password=password,
        autocommit=False,
    ) as conn:
        counts = load_and_verify(conn)

    print("Committed. All eight SF=1 row counts and TPC-H query 4 verified:")
    for table, count in counts.items():
        print(f"  {table:10} {count:>10,}")


if __name__ == "__main__":
    main()
