from __future__ import annotations

import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

from stie.models.threat_report import ThreatReport

THREAT_SCHEMA = pa.schema([
    pa.field("id", pa.string()),
    pa.field("title", pa.string()),
    pa.field("description", pa.string()),
    pa.field("threat_type", pa.string()),
    pa.field("severity", pa.string()),
    pa.field("confidence", pa.string()),
    pa.field("tlp_level", pa.string()),
    pa.field("author_id", pa.string()),
    pa.field("organization_id", pa.string()),
    pa.field("created_at", pa.timestamp("us")),
    pa.field("updated_at", pa.timestamp("us")),
    pa.field("tags", pa.list_(pa.string())),
    pa.field("observables", pa.list_(
        pa.struct([
            pa.field("type", pa.string()),
            pa.field("value", pa.string()),
        ])
    )),
    pa.field("affected_satellites", pa.list_(pa.string())),
    pa.field("affected_systems", pa.list_(pa.string())),
])


class ArrowExportClient:
    def __init__(self, data_dir: str = "data/arrow"):
        self.data_dir = data_dir

    def report_to_record_batch(self, report: ThreatReport) -> pa.RecordBatch:
        arrays = [
            pa.array([report.id]),
            pa.array([report.title]),
            pa.array([report.description]),
            pa.array([report.threat_type.value]),
            pa.array([report.severity.value]),
            pa.array([report.confidence.value]),
            pa.array([report.tlp_level.value]),
            pa.array([report.author_id]),
            pa.array([report.organization_id]),
            pa.array([report.created_at]),
            pa.array([report.updated_at]),
            pa.array([report.tags], type=pa.list_(pa.string())),
            pa.array(
                [[{"type": o.type, "value": o.value} for o in report.observables]],
                type=THREAT_SCHEMA.field("observables").type,
            ),
            pa.array([report.affected_satellites], type=pa.list_(pa.string())),
            pa.array([report.affected_systems], type=pa.list_(pa.string())),
        ]
        return pa.RecordBatch.from_arrays(arrays, schema=THREAT_SCHEMA)

    def reports_to_table(self, reports: list[ThreatReport]) -> pa.Table:
        batches = [self.report_to_record_batch(r) for r in reports]
        return pa.Table.from_batches(batches, schema=THREAT_SCHEMA)

    def export_to_parquet(self, reports: list[ThreatReport], path: str):
        table = self.reports_to_table(reports)
        pq.write_table(table, path)

    def query_parquet(self, path: str, columns: list[str] | None = None) -> pa.Table:
        dataset = ds.dataset(path, format="parquet")
        return dataset.to_table(columns=columns)


arrow_client = ArrowExportClient()
