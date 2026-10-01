# EvidenceRail Research Paper Workflow

## Objective

Generate a short English ICLR-format paper while retaining a traceable path from each claim to a literature source, method decision, or experiment output.

## Swarm stages

1. Planner creates a bounded research question and a `ResearchArtifact` of kind `method`.
2. Literature agent creates `literature` or `citation` artifacts with DOI, URL, or local source path.
3. Experiment agent creates `experiment` and `result` artifacts that point to raw configurations, CSV files, figures, and logs.
4. EvidenceRail writes `evidence_ledger` into the shared callback context and rejects traceability failures from the writer-approved set.
5. Writer consumes only `evidence_ledger.approved`; Reviewer records any remaining unsupported claim as a `review` artifact.

## Required runtime payload

```json
{
  "research_artifacts": [
    {
      "id": "lit-001",
      "kind": "literature",
      "producer": "literature-agent",
      "created_at": "2026-10-01T00:00:00Z",
      "doi": "10.0000/example",
      "claim": "Context selection affects long-horizon agent reliability.",
      "confidence": 0.9
    },
    {
      "id": "exp-001",
      "kind": "result",
      "producer": "experiment-agent",
      "created_at": "2026-10-01T00:00:00Z",
      "path": "outputs/experiments/exp-001/results.csv",
      "summary": "EvidenceRail reduced unsupported citations.",
      "parents": ["lit-001"]
    }
  ]
}
```

## Harness registration

Add `swarm.evidence` to the rail list for each research-team member. The rail runs before invocation and before each model call. It stores `evidence_ledger` and `evidence_policy` in callback `extra`; Writer prompts should enforce `writer_may_cite_only_approved`.

## Submission evidence

- Preserve `outputs/resource_report.json` and `outputs/resource_report.md` from `ResearchAuditTrail`.
- Preserve original literature records, experiment configuration, raw results, and generated PDF.
- Include this document and the EvidenceRail diff in `docs/architecture.md` and `framework_contribution.md`.
