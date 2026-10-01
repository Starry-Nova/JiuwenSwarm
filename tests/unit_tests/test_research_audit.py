import json

import pytest

from jiuwenswarm.agents.harness.common.research_audit import (
    ResearchAuditTrail,
    ResourceEvent,
)


def test_audit_trail_summarizes_and_writes_reports(tmp_path):
    trail = ResearchAuditTrail()
    trail.record(ResourceEvent(stage="literature", elapsed_seconds=1.25, input_tokens=20, output_tokens=10))
    trail.record(ResourceEvent(stage="experiment", elapsed_seconds=2.0, input_tokens=5, output_tokens=0, status="failed"))

    json_path, markdown_path = trail.write(tmp_path)
    report = json.loads(json_path.read_text(encoding="utf-8"))

    assert report["total_tokens"] == 35
    assert report["failed_events"] == 1
    assert "Total tokens: 35" in markdown_path.read_text(encoding="utf-8")


def test_audit_trail_rejects_negative_values():
    with pytest.raises(ValueError):
        ResearchAuditTrail().record(ResourceEvent(stage="writer", elapsed_seconds=-1))
