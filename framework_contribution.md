# Framework Contribution

## EvidenceRail and Artifact Provenance Gate

This submission adds two complementary research-workflow capabilities to JiuwenSwarm:

- the opt-in `swarm.evidence` Rail, which creates an auditable evidence hand-off for multi-agent paper generation; and
- the `ArtifactProvenanceGate` (APG), which checks the integrity of a completed PAPER artifact package before publishing its terminal success.

## Changed source

- `jiuwenswarm/agents/harness/common/rails/evidence_rail.py`
- `jiuwenswarm/agents/swarm/providers/builtin_rails.py`
- `jiuwenswarm/agents/swarm/registry.py`
- `jiuwenswarm/agents/harness/common/research_audit.py`
- `jiuwenswarm/agents/harness/common/rsi/artifact_provenance_gate.py`
- `jiuwenswarm/agents/harness/common/rsi/artifact_adapter.py`
- `jiuwenswarm/agents/harness/common/rsi/task_store.py`
- `jiuwenswarm/agents/harness/common/rsi/worker.py`

## Verification

Unit tests cover evidence provenance acceptance/rejection, context budgeting, callback attachment, resource-report output, APG rules, and terminal integration. A 24-case offline APG fault-injection pilot is available for reproduction with the same frozen fixtures used during development; it is evidence for artifact-integrity detection only, not for scientific correctness or a successful end-to-end research run.

## PR / patch

Branch: `feature/evidence-rail`. Create a PR to `main` and record the PR URL here before competition submission.
