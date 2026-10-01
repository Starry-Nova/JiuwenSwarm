"""Generate a deterministic EvidenceRail ledger and resource report.

Run in an installed JiuwenSwarm environment:
    python scripts/run_evidence_rail_demo.py
"""

from __future__ import annotations

import json
from pathlib import Path

from jiuwenswarm.agents.harness.common.rails.evidence_rail import EvidenceRail
from jiuwenswarm.agents.harness.common.research_audit import (
    ResearchAuditTrail,
    ResourceEvent,
)

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "examples" / "evidence_rail" / "research_artifacts.json"
OUTPUT = ROOT / "outputs" / "evidence_rail_demo"


def main() -> None:
    artifacts = json.loads(INPUT.read_text(encoding="utf-8"))
    ledger = EvidenceRail.build_ledger(artifacts, max_context_chars=4_000)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "evidence_ledger.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    audit = ResearchAuditTrail()
    audit.record(ResourceEvent(stage="literature", elapsed_seconds=0.0, status="demo"))
    audit.record(ResourceEvent(stage="evidence_validation", elapsed_seconds=0.0, status="demo"))
    audit.write(OUTPUT)
    print(f"Approved artifacts: {ledger['approved_count']}")
    print(f"Rejected artifacts: {ledger['rejected_count']}")
    print(f"Evidence ledger: {OUTPUT / 'evidence_ledger.json'}")


if __name__ == "__main__":
    main()
