# Resource Report (Development Evidence)

## Scope

This report records only measurements that have actually been obtained for the deterministic APG development pilot. It is not a resource report for a successful end-to-end research-paper generation run.

## Controlled APG pilot

The frozen offline pilot contains 24 cases: four valid controls and 20 specification-derived blocking faults (four per APG rule). Each case is evaluated 30 times, for 720 local evaluations.

| Measurement | Observed value |
| --- | --- |
| Manifest expectations | 24 / 24 met |
| Full APG precision / recall / F1 | 1.000 / 1.000 / 1.000 on the frozen pilot |
| PDF-only baseline F1 | 0.333 on the frozen pilot |
| Determinism | all 30 outputs per case identical after excluding `evaluated_at` |
| Local median latency | 9.958 ms in the current development verification |
| Local p95 latency | 12.259 ms in the current development verification |
| APG model-token delta | 0; the gate makes no model call |

The latency measures local gate evaluation only. It excludes LLM inference, tool calls, document compilation, and the rest of the PAPER workflow.

## Required final-run additions

Before competition submission, replace or supplement this report with the following for the selected generated paper:

1. run ID, start/end time, configured models, and environment version;
2. per-stage input/output token and wall-time ledger;
3. final PDF SHA-256 and APG `audit.json` SHA-256;
4. evidence of a successful end-to-end PAPER run; and
5. a statement of any human intervention.

Do not extrapolate the zero-token APG figure to the full paper-generation system.
