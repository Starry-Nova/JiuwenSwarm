"""Portable audit records for automated research workflows."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class ResourceEvent:
    """One attributable model or tool invocation in a research workflow."""

    stage: str
    elapsed_seconds: float
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = "unknown"
    status: str = "success"
    artifact_id: str | None = None
    timestamp: str = ""

    def with_timestamp(self) -> ResourceEvent:
        return ResourceEvent(
            **{**asdict(self), "timestamp": self.timestamp or datetime.now(UTC).isoformat()}
        )


class ResearchAuditTrail:
    """Accumulate resource use and emit the competition resource report."""

    def __init__(self) -> None:
        self._events: list[ResourceEvent] = []

    def record(self, event: ResourceEvent) -> None:
        if event.elapsed_seconds < 0 or event.input_tokens < 0 or event.output_tokens < 0:
            raise ValueError("resource values cannot be negative")
        self._events.append(event.with_timestamp())

    def summary(self) -> dict[str, object]:
        return {
            "event_count": len(self._events),
            "elapsed_seconds": round(sum(event.elapsed_seconds for event in self._events), 3),
            "input_tokens": sum(event.input_tokens for event in self._events),
            "output_tokens": sum(event.output_tokens for event in self._events),
            "total_tokens": sum(event.input_tokens + event.output_tokens for event in self._events),
            "failed_events": sum(event.status != "success" for event in self._events),
            "events": [asdict(event) for event in self._events],
        }

    def write(self, output_dir: str | Path) -> tuple[Path, Path]:
        """Write machine-readable JSON and a reviewer-friendly Markdown report."""
        destination = Path(output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        summary = self.summary()
        json_path = destination / "resource_report.json"
        markdown_path = destination / "resource_report.md"
        json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        markdown_path.write_text(
            "# Resource Report\n\n"
            f"- Events: {summary['event_count']}\n"
            f"- Elapsed seconds: {summary['elapsed_seconds']}\n"
            f"- Input tokens: {summary['input_tokens']}\n"
            f"- Output tokens: {summary['output_tokens']}\n"
            f"- Total tokens: {summary['total_tokens']}\n"
            f"- Failed events: {summary['failed_events']}\n",
            encoding="utf-8",
        )
        return json_path, markdown_path
