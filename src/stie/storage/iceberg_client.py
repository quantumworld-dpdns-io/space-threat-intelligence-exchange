from __future__ import annotations

from typing import Any, Optional

from stie.config.settings import settings


class IcebergClient:
    def __init__(self):
        self.warehouse = settings.iceberg_warehouse
        self.catalog_uri = settings.iceberg_catalog_uri

    def create_table(self, table_name: str, schema: dict[str, Any]):
        pass

    def insert(self, table_name: str, data: list[dict[str, Any]]):
        pass

    def query(self, sql: str) -> list[dict[str, Any]]:
        return []

    def compact_table(self, table_name: str):
        pass

    def expire_snapshots(self, table_name: str, retention_hours: int = 168):
        pass


iceberg_client = IcebergClient()
