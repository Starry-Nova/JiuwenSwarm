from types import SimpleNamespace

import pytest

from jiuwenswarm.agents.harness.common.rails.evidence_rail import (
    EVIDENCE_LEDGER_CONTEXT_KEY,
    EVIDENCE_POLICY_CONTEXT_KEY,
    EvidenceRail,
)


def test_ledger_approves_traceable_sources_and_rejects_untraceable_claims():
    ledger = EvidenceRail.build_ledger(
        [
            {"id": "paper-1", "kind": "literature", "doi": "10.1/example", "claim": "Prior work."},
            {"id": "result-1", "kind": "result", "path": "outputs/result.json", "summary": "F1 improved."},
            {"id": "paper-2", "kind": "citation", "claim": "No source."},
        ],
        200,
    )

    assert [item["id"] for item in ledger["approved"]] == ["paper-1", "result-1"]
    assert ledger["rejected"] == [{"id": "paper-2", "reason": "citation has no DOI, URL, or source path"}]


def test_ledger_budgets_context_without_dropping_provenance():
    ledger = EvidenceRail.build_ledger(
        [{"id": "paper-1", "kind": "literature", "url": "https://example.org", "claim": "abcdefghij"}],
        4,
    )

    assert ledger["approved"][0]["claim"] == "abcd"
    assert ledger["approved"][0]["truncated"] is True
    assert ledger["approved"][0]["source"] == "https://example.org"


@pytest.mark.asyncio
async def test_rail_attaches_ledger_and_writer_policy():
    extra = {"research_artifacts": [{"id": "p", "kind": "literature", "url": "https://example.org"}]}
    ctx = SimpleNamespace(extra=extra)

    await EvidenceRail().before_invoke(ctx)

    assert extra[EVIDENCE_LEDGER_CONTEXT_KEY]["approved_count"] == 1
    assert extra[EVIDENCE_POLICY_CONTEXT_KEY]["writer_may_cite_only_approved"] is True
