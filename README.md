# Baseball Analytics with Claude and Hardcharger

This repository contains a blog post and its supporting data and screenshots.
It follows a baseball analytics project on GizmoData Cloud, using Hardcharger,
a persistent DuckLake catalog, and Claude Desktop connected through MCP.

**[Read the blog post](./baseball-cloud-mcp-blog.md).**

## What the walkthrough covers

1. Creating a small Hardcharger cluster on GizmoData Cloud.
2. Creating and attaching a persistent `baseball` DuckLake catalog.
3. Importing player information and batting statistics into separate tables
   with the Python ADBC driver.
4. Querying the data in the Hardcharger web UI.
5. Connecting Claude Desktop through MCP and asking baseball questions.
6. Demonstrating idle stop and automatic resume when a supported client
   queries the stopped cluster.

The catalog stores the data independently of compute, so the tables survive
cluster stops and starts.

## Project contents

| File or directory | Purpose |
|---|---|
| [baseball-cloud-mcp-blog.md](./baseball-cloud-mcp-blog.md) | Main blog post, setup instructions, import example, and SQL queries |
| [images/](./images/) | Screenshots used in the post |
| [People.csv](./People.csv) | Player information, imported as `baseball.main.people` |
| [Batting.csv](./Batting.csv) | Batting statistics, imported as `baseball.main.batting` |
| [requirements.txt](./requirements.txt) | Python ADBC driver dependency for the import example |

Both tables join on `playerID`. The CSV files used in this project contain
24,270 people and 128,598 batting records.

## Following along

Start with the [blog post](./baseball-cloud-mcp-blog.md) for cluster creation,
catalog setup, data import, Claude Desktop configuration, and example queries.
Use your own GizmoData Cloud account and cluster endpoint. Keep passwords,
API keys, and session tokens out of source files and screenshots.

The data comes from the
[SABR Lahman Baseball Database](https://sabr.org/lahman-database/), created by
Sean Lahman. Review its documentation and applicable usage terms for
attribution and redistribution.
