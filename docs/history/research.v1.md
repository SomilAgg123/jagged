# Model routing v0.2: research notes

Data checked: 2026-10-24 (America/Los_Angeles). Every number below comes from a public page listed in `sources.csv` / `sources.md`. Blank or "unknown" means I could not find it. No custom evals were run. The first-pass version is kept as `research.v0.md`.

## 1. Method

- **Evidence bar.** Every source is scored against `SOURCE_RUBRIC.md` on nine criteria: independence, contamination, method, reproducibility, statistics, recency, relevance, cost reporting and judging. Hard disqualifiers D1–D7 and B-caps also apply. `build_sources.py` computes the tier. Results: 60 sources reviewed; 9 tier A (7 pick, 1 method, 1 price); 23 tier B; 28 tier C.
- **Tier-A pick sources (two runners only):**
  - Vals AI: TB4, Code Migration v1.1, Vibe Code Bench v1.1, Router Index.
  - Artificial Analysis: TB4, Coding Agent Index v2.0, FrontierCode 1.1, AutomationBench-AA.

  Two AA boards count as one runner, and so do two Vals boards.
- **Conclusion status (rubric §5):**
  - **Supported:** two A runners agree, or one A plus a B from another runner.
  - **Provisional:** one A runner only.
  - **Contested:** A support but an A/B contradiction.
  - **Insufficient evidence:** no A.

  Each pick cites at most 3 data points, tagged by tier.
- **Mirrors** (BenchLeader, BenchLM) are reading aids only (D2). Every number is attributed to its primary. Values read only on a mirror are marked "(mirror)".
- **Prices** come from provider pricing pages (tier A for the `price` role). For Z.ai, Xiaomi, Alibaba, Mistral and MiniMax, Vals list prices are used (secondary).
- **Cost per task over price per token.** See design conclusion X2.

## 2. Benchmark status in Oct 2026

| Benchmark | Runner | Status (2026-10-24) | Use for routing? |
|---|---|---|---|
| Terminal-Bench 4.0 | Vals (mini-swe-agent, avg@3); AA | **Maintained**. Vals updated 10/24. 66 new tasks, median 4h expert time, about 3/4 non-SWE. Not comparable to 2.x | **Yes**, core agentic signal |
| SWE-bench Verified | Vals | **Saturated and retired**. Vals stopped running new models; last update 9/1/2026; top 97.0%. Official swebench.com board's newest entry is Feb 2026 | Floor check only ("can it do easy fixes at all") |
| SWE-Bench Pro V2 | Scale (co-developed with Reflection) | Maintained. Public split is near ceiling (Opus 5 99.40%). Private split shows a large gap | Use the **private** split where available |
| SWE-Bench Pro (original public) | Scale | Stale (top: Muse Spark 1.1 61.5%) | No |
| Code Migration **v1.1** | Vals (Pi harness, revised hidden tests) | Maintained, updated 10/20. **Replaces v1** in Vals Index v2.2; v1 scores are not comparable (v1 was mini-swe-agent) | **Yes** (A). v1 is history only (B) |
| SWE-bench Multimodal | Vals (no network) | Maintained, 10/16. Public 2024 dataset, so memorization is not controlled | Corroboration only (B) |
| Vibe Code Bench v1.1 | Vals (OpenHands) | Maintained, 10/24 | **Yes**, greenfield app proxy |
| LMArena WebDev | LMArena (votes, CC BY 4.0) | Maintained, 10/22 | Yes, but rewards visual polish |
| AutomationBench-AA | AA (Zapier tasks, partial credit) | Maintained, 10/23 | **Yes**, tool/API orchestration proxy |
| τ³-bench | Sierra | Lags. Opus 5.5, GPT-6 and Gemini 4 absent | Secondary |
| BFCL V4 | Berkeley | **Stale** (last update Apr 12, 2026) | No |
| AA-LCR | AA (~100k token docs) | Maintained | Yes, long-context proxy (top is compressed) |
| AA-Omniscience | AA | Maintained | Yes, hallucination proxy for summaries and answers |
| SWE Atlas Codebase QnA | Scale | Maintained (24 configs). Few of the newest models. Judge is Claude Opus 4.5 | Yes, codebase comprehension proxy |
| ReviewBench | GitHub (judge: Claude Sonnet 5) | Maintained, 10/20. Scores whole review **agents**, not bare models | Weak signal |
| IFBench | AA | **Not run on newest models** (none of Opus 5.5 / GPT-6 / Gemini 4) | No |
| Structured Output Benchmark (SOB) | Interfaze (a vendor) | Stale model set (top: GPT-5.4 87.0%) | No |
| Aider Polyglot | Aider | Effectively unmaintained | No |
| LiveCodeBench | — | Stale; Vals archived it | No |
| FrontierCode 1.1 | AA (Stirrup harness, 3 runs; tasks by Cognition) | Maintained, Oct 2026. 100 private maintainer-built tasks graded on mergeability | **Yes** (A), issue-resolution proxy |
| Coding Agent Index v2.0 | AA (Claude Code, Codex × model) | Maintained, Oct 2026. FrontierCode + TB4 + SWE-Atlas-QnA-AA | **Yes** (A) for harness+model pairs |
| SWE-Atlas-QnA-AA | AA | Maintained. LLM-judge only (GPT-6 Luna); public data | B |
| SWE-rebench | Nebius | Best method in the set, but last update **2026-07-01** and no current frontier models | B until it updates |
| LiveBench 2.0 | Abacus AI | Released 10/14, updated 10/23. Coding suite near ceiling | B |
| Arena Agent (code) | LMArena | Maintained, 10/23. Satisfaction signals, not correctness | B |
| Zapier AutomationBench (strict) | Zapier | Pre-release partner report for Gemini 4 Argon | B |
| MCP Atlas | Scale | Maintained, but no Opus 5.5 / GPT-6 / Gemini 4; Meta–Scale conflict | B |
| Terminal-Bench 2.x | tbench.ai, KiloBench | TB2.1 fixed 28 of 89 TB2.0 tasks; superseded by TB4.0 | No (C / B) |
| SWT-bench, TestGenEval, JSONSchemaBench, MCP-Universe, FeatureBench, SWE-CI | academic | **Stale** (newest models Claude 4 / GPT-5 / Opus 4.6 era) | No (C) |

## 3. Subtask taxonomy and benchmark mapping

| # | Subtask id | What the harness is doing | Primary proxy | Secondary | Proxy quality |
|---|---|---|---|---|---|
| 1 | `codebase_qa_search` | Explore an unfamiliar repo, trace behavior, answer "how does X work" | SWE-Atlas-QnA-AA (B) | Scale SWE Atlas (B) | No tier-A proxy (LLM-judge only) |
| 2 | `small_edit` | Well-specified single-file edit or bug fix | none (SWE-V saturated, C) | — | No usable proxy |
| 3 | `issue_resolution` | Real multi-file bug fix from an issue | AA FrontierCode 1.1 (A) | SWE-rebench (B), Scale Pro V2 private (B) | Good, but one A runner |
| 4 | `refactor_migration` | Large multi-file rewrite or port that must keep behavior | Vals Code Migration v1.1 (A) | — | Good, but one runner |
| 5 | `greenfield_app` | Build an app or feature end to end from a spec | Vibe Code Bench v1.1 (A) | LMArena WebDev (B) | Good |
| 6 | `frontend_visual` | UI work from screenshots and visual bugs | SWE-bench Multimodal (Vals, B) | LMArena WebDev (B) | No tier-A proxy |
| 7 | `terminal_agentic_loop` | Long-horizon autonomous shell work (build, debug, ops, ML) | Terminal-Bench 4.0 (Vals A + AA A) | AA Coding Agent TB4 (A), LiveBench agentic (B), Arena Agent (B) | Good, two runners |
| 8 | `tool_orchestration` | Multi-step tool/function calling against APIs and SaaS | AutomationBench-AA (A) | Zapier strict (B), MCP Atlas (B) | Good |
| 9 | `code_review` | Find real issues in a PR diff | none (ReviewBench B) | — | No tier-A proxy |
| 10 | `planning_architecture` | Decompose a task, design, hard reasoning | none (AA index, ECI: B aggregates) | AA-Omniscience (B) | No tier-A proxy |
| 11 | `long_context_summarize` | Summarize or compact long context and logs | AA-LCR (B) | AA-Omniscience (B) | No tier-A proxy |
| 12 | `structured_output` | JSON/schema extraction, classification, commit messages | **None current** | SOB, IFBench (both stale) | Gap |
| — | `test_writing` | Write meaningful tests | **None current** (SWE Atlas Test Writing announced, no results) | — | Gap |

## 4. Conclusions per subtask (v0.2, evidence-gated)

Rules:
- **Best:** in the top tier of a tier-A source (within 3 pts of the leader).
- **Good enough:** within 10 pts of the leader on the same tier-A source, and cheaper per task.
- **Step-down / budget:** a cheaper option outside that bar, listed for the harness to weigh.

Each pick cites ≤3 data points. A data point reads as source (tier): number.

### 4.1 Summary

| Subtask | Best | Good enough | Step-down / budget | Status |
|---|---|---|---|---|
| `terminal_agentic_loop` | Opus 5.5 or Sonnet 5.5 (Opus cheaper per task) | Kimi K3.1 Pro (**contested**) | GPT-6.1 Sol | Best **supported**; good enough contested; step-down supported |
| `tool_orchestration` | Gemini 4 Argon (high) | MiniMax M3.1 Flash | — | Best **supported**; good enough provisional |
| `greenfield_app` | Sonnet 5.5 | Haiku 5.5 (**contested**) | DeepSeek V4.1 Flash 1017 (**contested**) | Best **supported** |
| `refactor_migration` | Sonnet 5.5 | GPT-6.1 Sol | DeepSeek V4.1 Flash 1017 (floor) | **Provisional** (one runner) |
| `issue_resolution` | Opus 5.5 at **medium** effort | GPT-6.1 Sol (max) | DeepSeek V4.1 Flash in Codex (**contested**) | **Provisional** |
| `codebase_qa_search` | — | — | — | **Insufficient evidence** (B-only: Claude models in Claude Code lead) |
| `small_edit` | — | — | — | **Insufficient evidence** (SWE-V saturated, C) |
| `frontend_visual` | — | — | — | **Insufficient evidence** (B-only: Opus 5.5 leads SWE-MM and WebDev) |
| `code_review` | — | — | — | **Insufficient evidence** |
| `planning_architecture` | — | — | — | **Insufficient evidence** (B-only aggregates) |
| `long_context_summarize` | — | — | — | **Insufficient evidence** (AA-LCR is B) |
| `structured_output` | — | — | — | **Insufficient evidence** (no current board) |
| `test_writing` | — | — | — | **Insufficient evidence** (no current board) |

For subtasks marked insufficient, the harness should fall back to the default model of the nearest supported subtask, flagged "no evidence". It should not use the B-only leader as a pick.

### 4.2 Detail

**`terminal_agentic_loop`**
- **Best: Claude Opus 5.5 (max) or Sonnet 5.5. Supported.**
  1. Vals TB4 (A): Opus 65.15% at $13.20/test; Sonnet 64.14% at $16.51/test.
  2. AA Coding Agent Index, TB4 in Claude Code (A): Sonnet 66%, Opus 63%.
  3. LiveBench 2.0 agentic (B): Opus 85.0 is the top score.

  Opus is cheaper per task on both A runners (AA pooled $11.42 vs $13.30). AA's model-level TB4 puts Opus at 59.6, 7.6 below Kimi, so Opus is not top-tier on every A board.
- **Good enough: Kimi K3.1 Pro. Contested.**
  1. Vals TB4 (A): 63.64% at $4.57/test.
  2. AA TB4 (A): 67.2% (#1).
  3. LiveBench 2.0 agentic (B, contradicts): 49.5 vs Opus 85.0. Arena Agent also lists it as preliminary (#9).

  It launched 10/23, so independent data is 1–2 days old. Re-check by 11/24.
- **Step-down: GPT-6.1 Sol (max). Supported as step-down.**
  1. Vals TB4 (A): 55.05% at $1.72.
  2. AA TB4 (A): 56.1%.
  3. Arena Agent (B): #4 net improvement, P50 $1.76/task.

  It sits 10–11 pts below the leader, which is just outside the good-enough bar, at about 1/8 of Opus's cost.
- **Not good enough (supported):**
  - Haiku 5.5: Vals 36.36%, AA 32.8%.
  - DeepSeek V4.1 Flash 1017: Vals 31.82%, AA 33.8%.
  - Grok 4.7: Vals 28.79% at $18.01, AA 25.8%.
- **Changed from v0:** Kimi went from good enough at H confidence to contested. Opus and Sonnet are now co-best. GPT-6.1 Sol is relabeled as the step-down.

**`tool_orchestration`**
- **Best: Gemini 4 Argon (high). Supported.**
  1. AutomationBench-AA (A, private held-out set): 77.5%, #1.
  2. Zapier AutomationBench 1.0.6 strict (B, different runner): Argon High 51.3% at $1.70 (#1), then Sonnet 5.5 Max 44.7%, Opus 5.5 Max 42.5% and GPT-6 Astra Max 41.4%.

  The two sources agree on the order of the top 4.
- **Good enough: MiniMax M3.1 Flash. Provisional.**
  1. AutomationBench-AA (A): 72.5%, at $0.15/$0.60 list.

  Zapier strict does not list MiniMax. Kimi K3.1 Pro scores 73.3% (A) but is not cheaper per token. AA $/task was not captured.
- **Note:** MCP Atlas (B) has no overlap with these models. Its leader is Meta's Muse Spark, and Meta has a large stake in Scale.
- **Changed from v0:** the budget line "DeepSeek V4.1 Flash max 68.9%" is dropped. DeepSeek 1017 scores 66.6%, which is outside the 10-pt bar.

**`greenfield_app`**
- **Best: Claude Sonnet 5.5. Supported.**
  1. Vibe Code Bench v1.1 (A): 92.39% at $31.25/test.
  2. LMArena WebDev (B): top 3 (~1768; Opus 5.5 1807, GPT-6 Astra ~1774).

  The VCB top 6 sit within 2.8 pts. Gemini 4 Argon (91.91% at $8.11) is also top-tier on A, but on WebDev it is 1673, well below the WebDev leaders.
- **Good enough: Claude Haiku 5.5. Contested.**
  1. VCB (A): 90.44% at $6.07/test.
  2. WebDev (B, contradicts): 1585.

  WebDev measures first-draft polish, so check output quality before routing user-visible UI work to Haiku.
- **Budget: DeepSeek V4.1 Flash 1017. Contested.**
  1. VCB (A): 87.73% at $0.58/test.
  2. WebDev (B): 1664, below the leaders.
- **Changed from v0:** confidence was M-H. The top-tier pick is now supported. Haiku and DeepSeek are contested.

**`refactor_migration`**
- **Best: Claude Sonnet 5.5. Provisional.**
  1. Vals Code Migration v1.1 (A): 86.88% at $43.88/test. Opus 5.5 scores 81.01% at $72.40 and GPT-6 Astra 80.58% at $62.07.
- **Good enough: GPT-6.1 Sol. Provisional.**
  1. Vals CM v1.1 (A): 77.32% at $9.51/test, 9.6 pts below Sonnet at about 1/4.6 of the cost.
- **Floor: DeepSeek V4.1 Flash 1017. Provisional.**
  1. Vals CM v1.1 (A): 67.52% at $1.76/test, 19 pts below. Use only for low-stakes ports.
- **Not good enough:** Haiku 5.5, 52.36% at $6.20 (A).
- **Reliability caveat:** in the Vals Router Index (A), Anthropic content-filter refusals counted as failures with no fallback. Opus 5.5 scored 47.5% on Code Migration there. The harness needs a refusal fallback.
- **Changed from v0:** all numbers move from v1 to v1.1, which is not comparable. The Sonnet–Sol gap widens (−4.7 → −9.6 pts). The DeepSeek floor rises from 45.62% to 67.52%. Status M → provisional.

**`issue_resolution`**
- **Best: Claude Opus 5.5 at medium effort. Provisional.**
  1. AA FrontierCode 1.1 (A): Opus 5.5 Medium 57.1%, High 54.0%, XHigh 53.5%, Max 52.2% (mirror). Medium beats Max.
  2. AA Coding Agent Index (A, same runner): Claude Code + Opus 5.5 max scores 56% on FrontierCode.
  3. SWE-rebench (B, older models): the top 5 sit within about 2 pts, e.g. Opus 5 63.4% at $3.47.

  The Cognition FrontierCode board (B) could add a second runner, but its numbers did not render on the primary page.
- **Good enough: GPT-6.1 Sol (max). Provisional.**
  1. AA FrontierCode (A): 49.1% (mirror), −8.0 pts.
  2. AA Coding Agent Index (A): 49% in Codex, pooled $1.50/task vs $11.42 for Claude Code + Opus 5.5.

  FrontierCode-specific $/task was not captured.
- **Budget lead: DeepSeek V4.1 Flash in Codex. Contested.**
  1. AA Coding Agent Index (A): 53% on FrontierCode at pooled $0.39/task.
  2. The same runner's model-level FrontierCode run (A, mirror) scores it 44.0%. The 9-pt gap is unexplained (harness or variance).
- **Changed from v0:** v0 used the Scale SWE-Bench Pro V2 private split, now B because it covers only 5 older models and has a Reflection/Meta conflict. v0 picks were Opus 5 / Gemini 3.8 Flash / GLM 5.3. The primary source is now AA FrontierCode.

**Insufficient-evidence subtasks**
- **`codebase_qa_search`: insufficient.**
  - SWE-Atlas-QnA-AA (B, LLM-judge only, public data): Opus 5.5 and Fable 5.1 in Claude Code 66%, Sonnet 5.5 64%, DeepSeek V4.1 Flash in Codex 61% (pooled $0.39), GPT-6.1 Sol 60%, Haiku 5.5 34%.
  - Scale SWE Atlas (B, older models): Opus 5 63.17%.
  - B-only consensus: Claude models in Claude Code lead. DeepSeek in Codex is a cheap lead worth testing.
  - Changed from v0: v0 picked Opus 5 / Gemini 3.8 Flash at L.
- **`small_edit`: insufficient.**
  - SWE-bench Verified is saturated and flagged "Flawed" (C).
  - The LangChain A/B (B, method) shows cheap tiers handled about a third of production threads without a measurable drop in merged PRs. That is a routing hint, not a pick.
  - Changed from v0: v0 picked GLM 5.3 Flash / GPT-5.6 Luna at M.
- **`frontend_visual`: insufficient.**
  - Vals SWE-MM (B, public 2024 data): Opus 5.5 70.21% at $4.92.
  - WebDev (B): Opus 5.5 1807, #1.
  - B-only consensus: Opus 5.5.
  - Changed from v0: was M.
- **`code_review`: insufficient.**
  - GitHub ReviewBench (B) scores agents, not bare models, and GitHub scores its own Copilot.
  - CodeReviewBench (C: 30 PRs, one run) and Martian (C: unverifiable) add nothing usable.
  - Changed from v0: was L.
- **`planning_architecture`: insufficient.**
  - Aggregates only, all capped at B: AA Intelligence Index (Opus 5.5 max 58 at $5.98/task; GPT-6.1 Sol 52 at $0.72), Epoch ECI (Opus 5.5 / GPT-6 Astra 169, GPT-6.1 Sol 168) and LiveBench overall.
  - B-only consensus: Opus 5.5, GPT-6 Astra and GPT-6.1 Sol lead.
  - Changed from v0: was L.
- **`long_context_summarize`: insufficient.**
  - AA-LCR (B, LLM-judged, read via mirror) has its top 15 within about 6 pts.
  - Changed from v0: v0 picked Kimi K3 / GPT-6 Luna at M.
- **`structured_output`, `test_writing`: insufficient.**
  - Every candidate board is stale (C): JSONSchemaBench, IFBench, SOB, SWT-bench and TestGenEval.

### 4.3 Design conclusions (cross-cutting)

| # | Conclusion | Data points | Status |
|---|---|---|---|
| X1 | A static per-subtask lookup beats shipped routers | (1) Vals Router Index (A): all 5 routers are off the cost/accuracy frontier. One model per benchmark beats them by 11.0 / 9.9 / 13.2 ±1.2 pts at equal cost; DeepSeek 1017 alone scores 61.3% at $0.66 vs Ramp 57.80% at $0.96. (2) Agent-as-a-Router (B): static per-dimension best reaches ~83% of oracle and beats always-Opus. (3) Scrouting (B): no learned router beats the strongest single model; solve sets are nested | **Supported** |
| X2 | Rank on measured $/task, not token price | (1) Vals TB4 (A): Sonnet 5.5 at half Opus's token price costs more per task ($16.51 vs $13.20). (2) AA Coding Agent Index (A): Sonnet $13.30 vs Opus $11.42 pooled per task | **Supported** |
| X3 | Key rows on model + effort; max is not always best | (1) AA FrontierCode (A): Opus 5.5 Medium 57.1% > Max 52.2% (mirror). (2) CursorBench 4.0 (B): Opus 5.5 High 56.0% at $3.97 vs Max 57.8% at $13.43 | **Supported** |
| X4 | Add a refusal/failure fallback per provider | (1) Vals Router Index (A): Anthropic content-filter refusals were scored as failures (Opus 5.5 47.5% on Code Migration vs 81.01% standalone; harnesses differ) | **Provisional** |
| X5 | Harness choice changes results | (1) AA Coding Agent Index vs AA model-level (A, same runner): DeepSeek V4.1 Flash 53% in Codex vs 44.0% (mirror) on FrontierCode | **Provisional** |
| X6 | Do not route on public, static SWE-bench numbers | Scale Pro V2 public 99.4% vs private 81.6% (B). Scrouting: Opus 4.6 falls from 0.720 to 0.480 on fresh tasks (B). Vals retired SWE-V at 97% | **Adopted as a source rule** (rubric D7 and contamination criterion), not a pick |
| X7 | Cheap-tier routing in production keeps quality | LangChain A/B (B): 29.2% vs 27.3% merged PRs (p = 0.49) at −64% median cost. A fast-only arm was stopped for low quality | **Insufficient** (B only). Motivates a custom eval |

## 5. Surprising findings (re-checked against the rubric)

1. **Static routing beats commercial routers** (X1, supported). This is the main justification for a context file instead of a learned router.
2. **Per-token price is a poor cost proxy** (X2, supported). On SWE-MM (B) Sonnet 5.5 used 6.21B input tokens against Opus's 3.18B and GPT-6.1 Sol's 242M.
3. **More reasoning effort can lower scores** (X3, supported). Opus 5.5 on FrontierCode scores best at medium effort.
4. **SWE-bench Verified is solved and leaky** (X6). Public-split numbers are excluded from picks.
5. **Network access inflates scores.** Vals found agents looking up upstream fix PRs; cutting network access cost Muse Spark 21–35 pts on SWE-MM. Vendor numbers rarely state network settings. This is one reason D1 excludes self-reports.
6. **A new open-weight-announced model tops TB4 on two A runners but is contradicted elsewhere.** Kimi K3.1 Pro shows why one fresh benchmark is not enough. Its weights are still unpublished.
7. **Prices have expiry dates.** The Gemini 4 Argon promo ends 2026-11-30; Gemini 3.8 Flash's ends 2026-12-31. Context tiers apply to Haiku 5.5 (>100K is 5×), GPT-6.x (>272K) and Grok 4.7 (≥200K). DeepSeek has peak/off-peak rates.
8. **Some top-ranked models can't be routed to.** Muse Wonder Full is not on Meta's API.
9. **Grok 4.7 is weak on agentic work at its price** (supported). TB4: Vals 28.79% at $18.01, AA 25.8%.
10. **Benchmark versions move under you.** Code Migration v1 → v1.1 moved scores by −1 to +31 pts (GLM 5.3 Flash 20.52% → 51.65%) and reshuffled the cheap tier. Terminal-Bench 2.1 found broken tasks in 28 of 89 TB2.0 tasks. Every evidence row needs a benchmark version.

## 6. Caveats

- **Harness:** Vals and AA use model-agnostic harnesses. Native scaffolds (Claude Code, Codex) often score higher (Scale observed this on SWE Atlas). Reflection's SWE-Bench Pro V2 study found harness choice barely moves strong models' scores but does move cost. Picks here assume a generic harness.
- **Reasoning effort:** scores differ a lot by effort. Example: Claude Opus 5.5 on the AA index scores 58 at max ($5.98/task) and 42 at low ($0.55/task). Rows must key on model + effort.
- **Vendor-adjacent benchmarks:**
  - ReviewBench is published by GitHub and scores its own Copilot.
  - SWE Atlas uses Claude Opus 4.5 as judge; ReviewBench uses Claude Sonnet 5.
  - SWE-Bench Pro V2 was co-developed with Reflection, which ships its own model.
  - SOB is run by Interfaze, which ranks its own model.
- **Partial credit:** AutomationBench-AA gives partial credit. Zapier's strict pass/fail scores are 26–27 pts lower for the same leaders, so a pass/fail workflow needs a higher bar.
- **Preference votes:** LMArena WebDev measures preference for a first draft, not correctness.
- **Judges:** FrontierCode-AA and SWE-Atlas-QnA-AA use an OpenAI judge (GPT-6 Luna) while ranking OpenAI models (disclosed). SWE Atlas (Scale) uses Claude Opus 4.5; MCP Atlas uses Gemini 2.5 Pro.
- **Coverage holes:** newest models are missing from SWE-V (Vals), SWE Atlas, the SWE-Bench Pro V2 private split, IFBench and τ³. Where the best model is "Opus 5", Opus 5.5 is untested, not worse.
- **Price conflict resolved:** an earlier read of anthropic.com/pricing was ambiguous about Haiku 5.5. The docs page is clear: $0.10/$0.50 for prompts ≤100K and $0.50/$2.50 above. This matches Vals.

## 7. Biggest data gaps (what would move a subtask out of "insufficient")

1. **A second tier-A runner** for refactor_migration and issue_resolution. Watch for:
   - SWE-rebench updating with current models (it would become A);
   - a readable Cognition FrontierCode board (B).
2. **Codebase QA with execution or human grading.** All current boards are LLM-judged.
3. **Test writing and structured output.** No current board exists. These are the strongest case for the custom evals planned later.
4. **Model-level code review** with ≥100 PRs and repeated runs.
5. **Small-edit discrimination.** Every current model passes SWE-V. A fresh, private small-edit set would decide whether the cheapest tier is safe.
6. **$/task per component** of the AA Coding Agent Index (only pooled cost is published), and AA $/task for AutomationBench.
7. **Kimi K3.1 Pro:** re-check after 30 days of independent runs.
8. Interactive latency under agent loads is not measured by any A source.
9. **Not verified this pass:**
   - SWE-bench-Live board;
   - the Martian repo contents;
   - Cognition FrontierCode numbers;
   - per-model AA FrontierCode values below the top 3 (mirror only).

## 8. Sources

See `sources.csv` (scores, tiers, disqualifiers) and `sources.md` (one-line justification each). All were accessed 2026-10-24. The tier-A pick sources:

- Vals:
  - https://www.vals.ai/benchmarks/terminal-bench-4
  - https://www.vals.ai/benchmarks/code-migration-v1-1
  - https://www.vals.ai/benchmarks/vibe-code
  - https://www.vals.ai/benchmarks/vals_router_index (method)
- Artificial Analysis:
  - https://artificialanalysis.ai/evaluations/terminalbench-4-0
  - https://artificialanalysis.ai/agents/coding-agents
  - https://artificialanalysis.ai/evaluations/frontiercode
  - https://artificialanalysis.ai/evaluations/automationbench-aa/
- Prices: provider pricing pages, listed in `models.csv`.
