# EvidenceRail Architecture

## Design goal

EvidenceRail augments JiuwenSwarm's native Rail lifecycle with provenance control for automated scientific-paper workflows. It does not generate citations or measurements itself; it constrains what later agents may treat as evidence.

## Components

```text
Planner / Literature / Method / Experiment / Reviewer
                  │ ResearchArtifact[]
                  ▼
             EvidenceRail
        validate → budget → ledger
                  │ ctx.extra
                  ▼
             Writer / PDF pipeline
```

- `EvidenceRail`: a registered `swarm.evidence` `DeepAgentRail`; executes in `before_invoke` and `before_model_call`.
- `ResearchArtifact`: JSON contract for inter-agent hand-offs.
- `evidence_ledger`: approved and rejected records, retained provenance, budget accounting.
- `ResearchAuditTrail`: exports model/tool elapsed time and token counts for the required resource report.

## Failure policy

Untraceable citation records and result records without an output path are retained as rejected diagnostics, never silently converted to valid evidence. The writer should use only `evidence_ledger.approved`; it must label remaining claims as unverified or remove them.
