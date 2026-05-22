from __future__ import annotations

from typing import Any

from datafusion import SessionContext


class DataFusionAnalytics:
    def __init__(self):
        self.ctx: SessionContext | None = None

    def connect(self):
        self.ctx = SessionContext()

    def register_parquet(self, name: str, path: str):
        if self.ctx is None:
            self.connect()
        self.ctx.register_parquet(name, path)

    def register_csv(self, name: str, path: str):
        if self.ctx is None:
            self.connect()
        self.ctx.register_csv(name, path)

    def sql(self, query: str) -> list[dict[str, Any]]:
        if self.ctx is None:
            self.connect()
        df = self.ctx.sql(query)
        return df.to_pydict()

    def analyze_threats(self, parquet_path: str) -> dict[str, Any]:
        self.register_parquet("threats", parquet_path)
        result = self.sql("""
            SELECT
                threat_type,
                severity,
                COUNT(*) as report_count,
                AVG(CASE confidence
                    WHEN 'high' THEN 90 WHEN 'medium' THEN 50
                    WHEN 'low' THEN 25 ELSE 0
                END) as avg_confidence
            FROM threats
            GROUP BY threat_type, severity
            ORDER BY report_count DESC
        """)
        return {"threat_analysis": result}


datafusion_analytics = DataFusionAnalytics()
