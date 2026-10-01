"""Research-evidence guardrail for reproducible multi-agent writing.

The rail converts hand-offs from researcher, experimenter and writer agents into
a compact, auditable ledger.  It intentionally keeps the payload in ``ctx.extra``
so a swarm can use it without coupling to a particular channel or storage layer.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from openjiuwen.core.single_agent.rail.base import AgentCallbackContext
from openjiuwen.harness.rails.base import DeepAgentRail

RESEARCH_ARTIFACTS_CONTEXT_KEY = "research_artifacts"
EVIDENCE_LEDGER_CONTEXT_KEY = "evidence_ledger"
EVIDENCE_POLICY_CONTEXT_KEY = "evidence_policy"


class EvidenceRail(DeepAgentRail):
    """Validate research evidence and attach a budgeted provenance ledger.

    An artifact is a mapping with an ``id`` and a ``kind``.  Literature
    artifacts must provide a DOI, URL, or explicit local source path; result
    artifacts must provide an output path.  Invalid artifacts remain visible in
    the ledger but are excluded from the writer-facing approved set.
    """

    priority = 18

    def __init__(self, max_context_chars: int = 12_000) -> None:
        super().__init__()
        self.max_context_chars = max_context_chars

    async def before_invoke(self, ctx: AgentCallbackContext) -> None:
        self._attach_ledger(ctx)

    async def before_model_call(self, ctx: AgentCallbackContext) -> None:
        self._attach_ledger(ctx)

    def _attach_ledger(self, ctx: AgentCallbackContext) -> None:
        extra = getattr(ctx, "extra", None)
        if not isinstance(extra, dict):
            return
        raw_artifacts = extra.get(RESEARCH_ARTIFACTS_CONTEXT_KEY, [])
        ledger = self.build_ledger(raw_artifacts, self.max_context_chars)
        extra[EVIDENCE_LEDGER_CONTEXT_KEY] = ledger
        extra[EVIDENCE_POLICY_CONTEXT_KEY] = {
            "writer_may_cite_only_approved": True,
            "writer_must_label_unverified_claims": True,
            "max_context_chars": self.max_context_chars,
        }

    @staticmethod
    def build_ledger(raw_artifacts: object, max_context_chars: int) -> dict[str, Any]:
        """Build a serializable ledger from untrusted inter-agent hand-offs."""
        artifacts = raw_artifacts if isinstance(raw_artifacts, list) else []
        approved: list[dict[str, Any]] = []
        rejected: list[dict[str, str]] = []
        used_chars = 0

        for index, item in enumerate(artifacts):
            if not isinstance(item, Mapping):
                rejected.append({"id": str(index), "reason": "artifact is not an object"})
                continue
            artifact_id = str(item.get("id") or "").strip()
            kind = str(item.get("kind") or "").strip().lower()
            if not artifact_id or not kind:
                rejected.append({"id": artifact_id or str(index), "reason": "missing id or kind"})
                continue

            source = str(item.get("doi") or item.get("url") or item.get("path") or "").strip()
            if kind in {"literature", "citation"} and not source:
                rejected.append({"id": artifact_id, "reason": "citation has no DOI, URL, or source path"})
                continue
            if kind in {"result", "experiment"} and not str(item.get("path") or "").strip():
                rejected.append({"id": artifact_id, "reason": "result has no output path"})
                continue

            claim = str(item.get("claim") or item.get("summary") or "").strip()
            remaining = max(0, max_context_chars - used_chars)
            compact_claim = claim[:remaining]
            used_chars += len(compact_claim)
            approved.append(
                {
                    "id": artifact_id,
                    "kind": kind,
                    "source": source or None,
                    "claim": compact_claim,
                    "confidence": item.get("confidence"),
                    "truncated": len(compact_claim) < len(claim),
                }
            )

        return {
            "approved": approved,
            "rejected": rejected,
            "approved_count": len(approved),
            "rejected_count": len(rejected),
            "context_chars": used_chars,
            "context_budget": max_context_chars,
        }
