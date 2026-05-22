from __future__ import annotations

from typing import Any

import duckdb
import pyarrow as pa

from stie.config.settings import settings


class DuckDBAnalytics:
    def __init__(self):
        self.path = settings.duckdb_path
        self.conn: duckdb.DuckDBPyConnection | None = None

    def connect(self):
        self.conn = duckdb.connect(self.path)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE SCHEMA IF NOT EXISTS analytics;
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS analytics.threat_summary (
                report_date DATE,
                threat_type VARCHAR,
                severity VARCHAR,
                count INTEGER,
                avg_confidence DOUBLE
            )
        """)

    def query(self, sql: str) -> list[dict[str, Any]]:
        if self.conn is None:
            self.connect()
        result = self.conn.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    def query_arrow(self, sql: str) -> pa.Table:
        if self.conn is None:
            self.connect()
        assert self.conn is not None
        return self.conn.execute(sql).arrow()

    def ingest_report(self, report_data: dict):
        if self.conn is None:
            self.connect()
        assert self.conn is not None
        self.conn.execute("""
            INSERT INTO analytics.threat_summary BY NAME
            VALUES (?)
        """, [report_data])

    def get_threat_trends(self, days: int = 30) -> pa.Table:
        return self.query_arrow(f"""
            SELECT report_date, threat_type, SUM(count) as total
            FROM analytics.threat_summary
            WHERE report_date >= CURRENT_DATE - INTERVAL '{days}' DAY
            GROUP BY report_date, threat_type
            ORDER BY report_date
        """)

    def close(self):
        if self.conn:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()


duckdb_analytics = DuckDBAnalytics()
