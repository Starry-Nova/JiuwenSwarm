# EvidenceRail Demonstration Runbook

## Scope

This demo proves three properties without inventing experimental results:

1. traceable literature and experiment artifacts enter a common ledger;
2. an untraceable citation is excluded from the approved writer context;
3. resource-report files are emitted alongside the ledger.

## Setup

Install JiuwenSwarm according to the upstream project guide and ensure its Python environment is active. Do not put model keys in this repository. Configure them through the official environment/configuration mechanism.

## Execute

```powershell
python scripts/run_evidence_rail_demo.py
```

Expected output directory:

```text
outputs/evidence_rail_demo/
  evidence_ledger.json
  resource_report.json
  resource_report.md
```

The provided fixture contains three valid artifacts and one deliberately invalid citation. The ledger must report the invalid citation as rejected. Replace the fixture only with real literature records and real experiment paths before recording a competition run.

## Integrate with a research team

1. Register `swarm.evidence` on planner, literature, method, experiment, writer, and reviewer members.
2. Place each member's `ResearchArtifact` objects in callback `extra["research_artifacts"]`.
3. Make Writer read only `extra["evidence_ledger"]["approved"]`.
4. Call `ResearchAuditTrail.record()` around each model/tool stage and export reports at completion.
5. Archive the input artifact JSON, raw experiment output, generated PDF, and both reports in the submission package.

## Evaluation evidence

Record a screen/video showing the generated ledger, rejected invalid citation, resource report, and resulting PDF. This is stronger evidence of a real Rail contribution than a static architecture diagram alone.
