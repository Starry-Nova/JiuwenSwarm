# openJiuwen Module Call Description

| Requirement | JiuwenSwarm integration |
| --- | --- |
| Framework extension | `@harness_element(kind=ElementKind.RAIL, name="swarm.evidence", builder=EvidenceRail)` in `agents/swarm/providers/builtin_rails.py` |
| Framework registration | `agents/swarm/registry.py` imports provider declarations and calls `register_from_catalog()` |
| Lifecycle hooks | `EvidenceRail.before_invoke()` and `EvidenceRail.before_model_call()` receive `AgentCallbackContext` |
| Inter-agent state | callback `ctx.extra["research_artifacts"]` becomes `ctx.extra["evidence_ledger"]` |
| Resource trace | `ResearchAuditTrail` writes JSON and Markdown reports adjacent to output artifacts |

To activate the rail in a research-team member, include the registered type `swarm.evidence` in its `RailSpec` list. This is deliberately an opt-in research capability rather than a behavior change for general JiuwenSwarm users.
