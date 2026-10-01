# Framework Contribution

## EvidenceRail

This submission adds the opt-in `swarm.evidence` Rail to JiuwenSwarm. It provides an auditable research-evidence hand-off mechanism for multi-agent paper generation.

## Changed source

- `jiuwenswarm/agents/harness/common/rails/evidence_rail.py`
- `jiuwenswarm/agents/swarm/providers/builtin_rails.py`
- `jiuwenswarm/agents/swarm/registry.py`
- `jiuwenswarm/agents/harness/common/research_audit.py`

## Verification

Unit tests cover provenance acceptance/rejection, context budgeting, callback attachment, and resource-report output. The demonstration script generates an evidence ledger with a deliberately rejected citation.

## PR / patch

Create a PR from `feature/evidence-rail` to `main` after pushing the branch. Record that PR URL here before competition submission.
