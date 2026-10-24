# Jagged

**A vendor-neutral, evidence-backed context file that agent harnesses load to route each subtask to the cheapest model that is good enough for it.**

The frontier keeps moving, so for many subtasks several models are now good enough. Routing becomes a cost problem: use the expensive model where it wins, and a cheaper one where it doesn't. Capability is jagged (a model can lead one subtask and trail on the next), which is where the name comes from.

The people best placed to publish this guidance have reasons not to:
- **Labs** recommend their own models.
- **Tool and model vendors** often grade their own homework, even when they say they are model-agnostic.

Jagged builds the routing table from independent public benchmarks instead. Each pick shows the evidence behind it, how strong that evidence is, and how old it is.

> **Disclaimer.** v0 is based solely on public benchmarks and provider price pages as read on **2026-10-24**. No custom evaluations have been run. Scores, prices and model availability change quickly. Treat every pick as a dated, sourced claim, not a guarantee, and re-check before relying on it in production.

## Design principle

**Each conclusion rests on 1–3 high-confidence data points.** To get there:

1. **Collect many diverse sources.** These include independent eval orgs, academic benchmarks, arenas and vendor reports. 65 have been scored so far.
2. **Validate each source against a written reliability bar** ([`docs/SOURCE_RUBRIC.md`](docs/SOURCE_RUBRIC.md)).
   - Nine criteria: independence, contamination resistance, method transparency, reproducibility, statistics, coverage, task relevance, cost reporting and judging method.
   - Hard disqualifiers, such as self-reported scores, mirrors, usage-as-quality, unreadable boards, anecdotes and saturated boards.
   - Caps for commercial stakes and preference votes.
   - Tiers are computed by a script, not hand-assigned.
3. **Gate every conclusion on evidence status.**
   - **Supported:** two independent tier-A runners agree, or tier A plus corroborating tier B from another runner.
   - **Provisional:** a single tier-A runner, or older evidence without an anchor.
   - **Contested:** tier-A support plus a contradiction.
   - **Insufficient:** no tier-A evidence, so no pick.
4. **Date every data point.** Recency is judged per claim: fresh ≤90 days, aging 91–180, stale >180. Older evidence keeps its tier only for the exact model it tested, and only if that model is still sold at a verified price. It carries forward to successors or families only as corroboration. Picks that lean on older evidence are marked ⏳.

## Current status (v0, 2026-10-24)

| Subtask | Best | Good enough / cheaper | Step-down / budget | Status |
|---|---|---|---|---|
| `terminal_agentic_loop` | Claude Opus 5.5 / Sonnet 5.5 | Kimi K3.1 Pro (contested) | GPT-6.1 Sol | Best **supported**; step-down supported |
| `tool_orchestration` | Gemini 4 Argon (high) ⏳ | MiniMax M3.1 Flash | — | Best **supported**; good enough provisional |
| `greenfield_app` | Claude Sonnet 5.5 | Claude Haiku 5.5 (contested) | DeepSeek V4.1 Flash 1017 (contested) | Best **supported** |
| `refactor_migration` | Claude Sonnet 5.5 | GPT-6.1 Sol | DeepSeek V4.1 Flash 1017 (floor) | **Provisional** (one runner) |
| `issue_resolution` | Claude Opus 5.5 (medium) ⏳ | GPT-6.1 Sol (max) ⏳ | DeepSeek V4.1 Flash in Codex (contested); older: GPT-5.6 Sol, GLM-5.2, Grok 4.5 (provisional ⏳) | Best and good enough **supported** |
| `structured_output` | — (current leaders untested) | Grok 4.3 (medium), best among tested ⏳ | — | **Provisional** |
| `codebase_qa_search` | — | — | — | Insufficient |
| `small_edit` | — | — | — | Insufficient |
| `frontend_visual` | — | — | — | Insufficient |
| `code_review` | — | — | — | Insufficient |
| `planning_architecture` | — | — | — | Insufficient |
| `long_context_summarize` | — | — | — | Insufficient |
| `test_writing` | — | — | — | Insufficient |

⏳ = relies on aging, stale, undated or same-family (predecessor) evidence. Full data points, with evidence dates, are in [`docs/research.md`](docs/research.md).

Cross-cutting findings that shape the format:
- A static per-subtask lookup beat every shipped router on the Vals Router Index.
- Measured $/task ranks models differently from $/token.
- Rows must key on model **and** reasoning effort: Opus 5.5 scores higher at medium than at max on FrontierCode.

## Using it in a harness

The machine-readable format is a draft: [`schema/routing.schema-draft.yaml`](schema/routing.schema-draft.yaml). It has two collections:
- `models[]`: one row per (model, reasoning effort), with time- and context-tiered pricing.
- `subtasks[]`: routing signals, proxy benchmarks, dated evidence rows and picks (`best_quality`, `good_enough`, `budget`), each with a status.

A harness would:
1. Classify the current step into a subtask using `routing_signals`, such as multi-step shell work vs. a JSON extraction.
2. Pick `good_enough` when its status is `supported` (or `provisional`, if you accept that risk); otherwise use `best_quality`.
3. Fall back to the nearest supported subtask's default when a subtask is `insufficient`. Never treat a B-only leader as a pick.
4. Respect `pricing[].valid_until`, context-size price tiers and `review_by` dates. Re-route or warn when they pass.
5. Add a per-provider refusal/failure fallback.

A generated `ROUTING.md` (prose for prompt context) and a `models.yaml` are planned; the schema is not stable yet.

## Repository layout

```
docs/SOURCE_RUBRIC.md      reliability bar (v2: per-claim recency)
docs/research.md           current conclusions with every data point
docs/sources.md            per-source scores, justifications, tier moves (generated)
docs/history/              earlier research passes (v0, v1)
data/sources.csv           65 scored sources (generated)
data/models.csv            prices and headline scores for 22 models (generated)
schema/                    draft machine-readable format
scripts/build_sources.py   scores sources -> data/sources.csv, docs/sources.md
scripts/build_csv.py       -> data/models.csv
```

To regenerate the files (Python 3, standard library only), run from the repo root:

```
python3 scripts/build_sources.py
python3 scripts/build_csv.py
```

## Contributing

The biggest need is **tier-A evidence for the seven insufficient subtasks**:
- codebase Q&A with execution or human grading
- small-edit discrimination
- frontend/visual
- model-level code review
- planning
- long-context summarization
- test writing

Next is a **second independent runner** for refactor/migration, plus current-frontier runs on SWE-rebench and IFBench. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to propose a source, how it is scored, and the neutrality policy.

## License

- Code (`scripts/`): [Apache-2.0](LICENSE).
- Data and docs (`data/`, `docs/`, `schema/`, README, CONTRIBUTING): [CC BY 4.0](LICENSE-DATA).
- Cited benchmark results belong to their publishers and are linked to their sources.
