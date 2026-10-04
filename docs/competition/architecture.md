# Evidence-Aware Research Pipeline Architecture

## Design goal

This extension adds two deterministic safeguards around a JiuwenSwarm PAPER workflow. They do not assess scientific truth; they make the evidence and completion claim inspectable.

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
                  │ durable Provider completion
                  ▼
       Artifact Provenance Gate (APG)
      audit → publish completion or block
```

- `EvidenceRail`: a registered `swarm.evidence` `DeepAgentRail`; executes in `before_invoke` and `before_model_call`.
- `ResearchArtifact`: JSON contract for inter-agent hand-offs.
- `evidence_ledger`: approved and rejected records, retained provenance, budget accounting.
- `ResearchAuditTrail`: exports model/tool elapsed time and token counts for the required resource report.
- `ArtifactProvenanceGate`: a deterministic PAPER terminal gate. It writes `audit.json` and publishes a completed result only when required output evidence is present.

## APG completion contract

APG runs after the Provider has durably reported `COMPLETED` and before that result is exposed as public completion. Its Edition 1 checks are deliberately narrow:

1. `APG001`: `paper/main.pdf` exists, is a regular file, and is nonempty.
2. `APG002`: the selected Manager state has a successful terminal Reporting record.
3. `APG003`: Reporting artifact paths are relative, confined to the run root, and present.
4. `APG004`: the model-call ledger parses and contains at least one traceable, nonnegative token record.
5. `APG005`: when a reliable LaTeX AUX file is available, compiled citation keys resolve to bibliography keys; missing AUX evidence is recorded as `SKIPPED` rather than silently accepted.

A failed blocker produces `PAPER_PROVENANCE_BLOCKED`, while preserving both the artifact package and its audit for diagnosis.

## Failure policy

Untraceable citation records and result records without an output path are retained as rejected diagnostics, never silently converted to valid evidence. The writer should use only `evidence_ledger.approved`; it must label remaining claims as unverified or remove them. APG applies the corresponding rule at task completion: it prevents a durable terminal status alone from being interpreted as evidence that a usable, auditable paper package exists.
