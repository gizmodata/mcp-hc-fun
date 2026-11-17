# Local Hardcharger TPC-H SF=1

Uses the official Python ADBC driver to execute SQL over the running desktop
server's HTTP API. Keep the Hardcharger desktop app running.

## Run

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tpch_sf1.py
```

Enter your server administrator password at the hidden terminal prompt. The
script does not save it. The default user is `hardcharger`; pass
`--username YOUR_USER` to change it. Desktop-managed credentials live in the
operating system's keychain; if needed, configure your administrator credentials
in the desktop app. Do not paste credentials into chat or source files.

The connection defaults to
`hardcharger://127.0.0.1:31337/warp?tls=false`, matching the API advertised by
this local desktop installation. For a server using the newer Chargewire path:

```sh
.venv/bin/python tpch_sf1.py --uri 'hardcharger://127.0.0.1:31337?tls=false'
```

Unencrypted HTTP is for this local loopback connection only. Use TLS for remote
servers.

## Behavior

- Installs and loads DuckDB's `tpch` extension on the server (the initial install
  may require internet access).
- Generates SF=1 into the current database's `main` schema in a transaction.
- Refuses to generate if any of the eight TPC-H table names already exist.
  If all eight exist, it only verifies them, without appending data.
- Checks all eight row counts and the documented SF=1 result for TPC-H query 4
  before committing. Errors propagate; closing the uncommitted connection rolls
  back changes. Existing tables are never dropped.
- Data persists in the desktop app's database, not in this project folder.

This is dataset setup and a query smoke test, not a full or official TPC-H
benchmark run.

## References

- [Hardcharger docs](https://docs.hardcharger.gizmodata.com/)
- [macOS desktop app](https://docs.hardcharger.gizmodata.com/guides/desktop-app/)
- [Python driver](https://docs.hardcharger.gizmodata.com/clients/python/)
- [DuckDB TPC-H extension](https://duckdb.org/docs/2.0/core_extensions/tpch.html)
