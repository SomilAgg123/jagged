# Model routing v0.4: research notes (discovery pass 3)

Data checked: 2026-10-24 (America/Los_Angeles). Every number below comes from a public page listed in `data/sources.csv` / `docs/sources.md`. Blank or "unknown" means I could not find it. No custom evals were run. Earlier versions are kept as `docs/history/research.v0.md` (first pass), `docs/history/research.v1.md` (v0.2, rubric v1) and `docs/history/research.v2.md` (v0.3, per-claim recency). How the new sources were found is logged in `docs/discovery-log.md`.

## 1. Method

- **Evidence bar.** Every source is scored against `docs/SOURCE_RUBRIC.md` **v2.1**, and `scripts/build_sources.py` computes the tier.
  - v2 removes recency from the source score and from the tier-A gate, and retires D3 (stale).
  - Age is applied per data point instead (rubric §4, R1–R7).
  - Result: **87 sources; 19 tier A, 44 tier B, 24 tier C.** v0.3 had 65 sources (15 A, 29 B, 21 C); v0.2 had 60 (9 A, 23 B, 28 C).
  - This pass added 22 sources (4 A, 15 B, 3 C) and moved no existing tier. See §2.1.
- **Tier-A sources:**
  - Vals AI: TB4, Code Migration v1.1, Vibe Code Bench v1.1, Router Index (method).
  - Artificial Analysis: TB4, Coding Agent Index v2.0, FrontierCode 1.1, AutomationBench-AA, IFBench.
  - Nebius: SWE-rebench.
  - Older academic boards: METR Time Horizons 1.1, Berkeley BFCL V4, FeatureBench, SWE-CI.
  - **New in v0.4:** CodePanel AI Code Review Benchmark (code_review); TestSuiteBench (test_writing); Mercor Terminal-Bench 2.1 Extended (terminal; score 70, right at the line); Mercor's DeepSWE v1.1 run (issue_resolution).
  - Provider pricing pages (price role).
  - Two AA boards count as one runner, and so do two Vals boards, and so do Mercor's boards (one runner, many boards).
- **D6, made precise (rubric v2.1 §2.1, decided 2026-10-24).** "Single run" no longer disqualifies a whole source. A single-run result counts only for rows that meet three conditions: the harness, effort and snapshot are documented for that row; every task is counted (failures score 0, or completion is reported, or there is evidence the row covered the full set); and the row has no red flag. Even then, a qualifying row supports only gaps larger than its noise. That noise is a paired bootstrap CI over tasks if per-task results are public, or else the worst case of **139/√n points** (10.8 at n = 165). Rows inside that interval are a tie. D6 still applies below 30 tasks.
  - Effect this pass: on TestSuiteBench, 3 of 8 rows qualify (Opus 5, Gemini 3.8 Flash, GPT-5.6 Sol). The `test_writing` good-enough pick (GPT-6 Astra) is dropped (§4.2).
  - Kodus, VisualForge, screenshotbench and The New Stack stay D6.
  - TestEvo, Qodo, Aider and Mercor's k = 1 rows keep their tiers, and their within-noise orderings are now read as ties.
- **Every data point is written as:** source (effective tier) · value · evidence_date · age_days · freshness · direct | family.
  - Freshness: fresh ≤90 d; aging 91–180 d; stale >180 d; unknown = treated as stale.
  - **direct** means the source tested this exact model and effort, and the model is still sold at a verified list price (R2).
  - **family** means a predecessor, sibling or other effort setting. It counts as B at most (R3).
- **⏳ older evidence** marks a pick that cites an aging, stale or unknown-date point, or a family point.
- **Unanchored** marks a good-enough pick whose older source shares no model with a fresh tier-A source for the subtask. It is capped at provisional (R5).
- **Status (rubric §6):**
  - **Supported:** 2 A runners, or A plus B from another runner.
  - **Provisional:** 1 A runner, or unanchored.
  - **Contested:** A support plus an A/B contradiction.
  - **Insufficient:** no A.
- **Mirrors** (BenchLeader, BenchLM) are reading aids only (D2). Values read only on a mirror are marked "(mirror)". Where a mirror disagreed with the primary (AA IFBench, Grok 4.20), mirror-only values are not used.
- **Prices** come from provider pricing pages where checked. GLM 5.3 / GLM 5.3 Flash now use Z.ai's own page (see §5.11). For Xiaomi, Alibaba, Mistral and MiniMax, Vals list prices are used (secondary).

## 2. Older-source re-check (this pass)

| Source | v1 tier | v2 tier | Evidence age | What it can support now |
|---|---|---|---|---|
| SWE-rebench (Nebius) | B (rec gate) | **A** | Newest row ≥2026-07-24 (Opus 5), age ≤92 d. Rows for other models are undated (unknown) | Direct claims about the models it tested (Fable 5, Grok 4.5, Opus 5, GLM-5.2, GPT-5.6 Sol…). Family-B corroboration for Opus 5.5 / GPT-6.1 Sol |
| AA IFBench | C (D3) | **A** | Leader row Grok 4.3 medium ≥2026-04-30 (model release), age ≤177 d | Direct claim for Grok 4.3 medium, "best among tested" only (no frontier rows) |
| Berkeley BFCL V4 | C (D3) | **A** | 2026-04-12, 195 d, stale | Claims about Opus 4.5 / Sonnet 4.5 / Gemini 3 Pro Preview / GLM-4.6. Not anchored to any current tool-use board; no pick |
| METR Time Horizons 1.1 | C (D3) | **A** | Last addition 2026-05-08, 169 d, aging; frozen 2026-09-08 | Tests no model in the routing set; no pick |
| FeatureBench | C (D3) | **A** | Newest model Opus 4.5 (paper; date not captured) | Opus 4.5 is still sold ($5/$25) but costs more per token than Opus 5.5 ($4/$20); no pick |
| SWE-CI | C (D3) | **A** | Newest models Opus 4.6 / GPT-5.2 (paper; date not captured) | No overlap with Vals CM v1.1 (no anchor); no pick |
| Scale SWE-Bench Pro V2 private | B | B | ≥2026-07-24 (Opus 5 row) | Unchanged: ind = 1 (Reflection / Meta) |
| Scale SWE-Bench Pro original public | C (D3) | B | Not dated this pass | ind = 1, cont = 1 |
| Sierra τ³-bench | B | B | ≥2026-07-24 (Opus 5 row) | Unchanged: ind = 1 |
| AA τ²-Bench Telecom (new) | — | C | — | D7 saturated (GLM-5.2 99.1%) |
| Toolathlon-Verified (new) | — | **B** | Per-row dates; newest 2026-08-30 | cont = 1 (public tasks and evaluators). Contradicts AA AutomationBench on two cheap models (§4.2) |
| Aider Polyglot | C (D3) | B | 2025-11-20, 338 d, stale | cont = 1; B-only for small_edit |
| SWT-bench / TestGenEval | C (D3) | B / B | SWT newest 2026-07-08; TestGenEval GPT-4o era | B-only for test_writing |
| JSONSchemaBench | C (D3) | B | GPT-4o / Qwen2.5 era | Commercial-stake cap (guidance-ai ranks Guidance) |
| MCP-Universe | C (D3) | B | GPT-5-High era | Score 68 |
| SWE-bench-Live / LiveCodeBench | C (D3) | C (D5) | — | Leaderboards unreadable on fetch |
| Multi-SWE-bench (new) | — | C (D5) | — | Board not opened |
| SWE-bench Multilingual board (new) | — | C (D1) | — | Vendor model-card self-reports |
| Fiction.LiveBench via Epoch (new) | — | C (score 46) | 2026-01-27, 270 d | — |
| Vals Code Migration v1 | B | B | superseded | New "superseded version" cap keeps it below A |

Considered and not added: AA SciCode (scientific coding, which maps to no subtask) and SWE-PolyBench (seen in search only).

**Older models used below: list prices verified on provider pages on 2026-10-24** (needed for R2)
- Claude Opus 5: $5 / $25
- Claude Fable 5: $10 / $50
- Grok 4.5: $2 / $6
- GLM-5.2: $1.40 / $4.40
- GPT-5.6 Sol: $4 / $20 (the page carries a promo note)
- Grok 4.3: $1.25 / $2.50

Availability was **not verified** for DeepSeek-V4 Pro (non-0813), MiniMax M3 or MiMo older snapshots, so their SWE-rebench points count as B under R2.

### 2.1 New sources this pass (v0.4)

| Source | Tier | Subtask | Why it matters |
|---|---|---|---|
| CodePanel AI Code Review Benchmark | **A** (74) | code_review | First tier-A review board: private post-2025 fixtures, 3-judge cross-family panel that excludes the reviewed model's maker, bootstrap CIs, $/review. Low power (minimum detectable gap ~21 pts) |
| TestSuiteBench (arXiv 2610.13065) | **A** (78) | test_writing | 165 apps, mutation-score grading (execution), estimated $/instance, code and data public since 2026-10-12. Single run with no per-app results. Under v2.1 §2.1 only 3 of 8 rows qualify (Opus 5, Gemini 3.8 Flash, GPT-5.6 Sol). The board's Opus 5.5 / GPT-6.1 Sol rows do not qualify |
| Mercor Terminal-Bench 2.1 Extended | **A** (70) | terminal | Third independent terminal runner (99 private tasks, k = 3). No cost, no CIs |
| Mercor DeepSWE v1.1 run | **A** (74) | issue_resolution | 113 original tasks, k = 3. Only two rows readable |
| IronBee Raw LLM Code Review | B (74, cont = 1) | code_review | 58 configs × 3 passes on Martian's public PRs, CIs, every artifact public |
| MacroscopeBench | B (71, judge = 1) | code_review | 195 commits × 3 runs, measured $ |
| Qodo LLM review comparison | B (64) | code_review | 125 PRs, single Sonnet 4.6 judge |
| Factory Review Benchmark | B (67) | code_review | Older models only (April 2026) |
| TestEvo-Bench (arXiv 2607.02469) | B (75, ind = 1) | test_writing | 1,255 Java tasks; only Opus 4.7 / Gemini 3.1 Pro |
| Scale SWE Atlas Test Writing | B (ind = 1) | test_writing | 90 tasks, 3 trials, CIs; mutation + LLM rubric |
| Scale SWE Atlas Refactoring | B (ind = 1) | refactor_migration | 70 tasks; no Sonnet 5.5 / GPT-6.1 rows |
| NIST CAISI PortBench | B (68) | refactor_migration | Government runner, private porting tasks; older models only |
| Mercor: SWE-V Extended, SWE Atlas QnA, AA-LCR Extended, APEX-SWE, τ³-Banking, APEX-Agents, FrontierCode | B (57–65) | small_edit, codebase_qa, long_context, issue_resolution, tool_orchestration | Held-out reruns of public benchmarks; no cost on any board |
| VisualForge, screenshotbench, ArchBench | C | frontend_visual, planning | D6 / D5 |

Martian Code Review Bench stays C, but now on score (48) rather than D5: its repo became readable and IronBee re-ran it.

## 3. Subtask taxonomy and benchmark mapping

| # | Subtask id | Primary proxy | Secondary | Proxy quality |
|---|---|---|---|---|
| 1 | `codebase_qa_search` | SWE-Atlas-QnA-AA (B) | Scale SWE Atlas (B), Mercor SWE Atlas QnA + Extended (B) | No tier-A proxy (LLM-judge only, on every runner) |
| 2 | `small_edit` | none (SWE-V saturated, C) | Mercor SWE-V Extended (B, 50 tasks), Aider Polyglot (B, stale) | No usable A proxy |
| 3 | `issue_resolution` | AA FrontierCode 1.1 (A) | SWE-rebench (A), **Mercor DeepSWE v1.1 (A)**, Mercor APEX-SWE / FrontierCode (B), Scale Pro V2 private (B) | Good; three A runners |
| 4 | `refactor_migration` | Vals Code Migration v1.1 (A) | Scale SWE Atlas Refactoring (B), NIST CAISI PortBench (B, older models), SWE-CI (A, no overlap) | Good, but one current A runner |
| 5 | `greenfield_app` | Vibe Code Bench v1.1 (A) | LMArena WebDev (B), FeatureBench (A, older models) | Good |
| 6 | `frontend_visual` | Vals SWE-MM (B) | LMArena WebDev (B); VisualForge, screenshotbench (C) | No tier-A proxy |
| 7 | `terminal_agentic_loop` | Terminal-Bench 4.0 (Vals A + AA A) | **Mercor TB 2.1 Extended (A)**, LiveBench agentic (B), Arena Agent (B), METR (A, no current models) | Good, three runners |
| 8 | `tool_orchestration` | AutomationBench-AA (A) | Zapier strict (B), Toolathlon-Verified (B), Mercor τ³-Banking / APEX-Agents (B), BFCL V4 (A, stale), MCP Atlas (B), τ³ (B) | Good; A and B disagree on cheap models |
| 9 | `code_review` | **CodePanel (A)** | IronBee (B), MacroscopeBench (B), Qodo (B), Factory (B), ReviewBench (B) | One A runner, low power; four B runners |
| 10 | `planning_architecture` | none (B aggregates) | AA-Omniscience (B); ArchBench (C) | No tier-A proxy |
| 11 | `long_context_summarize` | AA-LCR (B) | Mercor AA-LCR Extended (B), AA-Omniscience (B) | No tier-A proxy (LLM-judged) |
| 12 | `structured_output` | **AA IFBench (A, proxy, no frontier rows)** | JSONSchemaBench (B) | Weak: format-constraint proxy |
| 13 | `test_writing` | **TestSuiteBench (A)** | Scale SWE Atlas TW (B), TestEvo-Bench (B), SWT-bench (B), TestGenEval (B) | One A runner, and only 3 of its rows qualify (v2.1 §2.1). Its frontier rows (Opus 5.5, GPT-6.1 Sol) do not |

## 4. Conclusions per subtask (v0.4)

Rules:
- **Best:** top tier of a tier-A source (within 3 pts of the leader), and the source tested the current frontier (R4).
- **Good enough:** within 10 pts of the leader on the same tier-A source, and cheaper per task.
- **Step-down / budget:** a cheaper option outside that bar, listed for the harness to weigh.

### 4.1 Summary

| Subtask | Best | Good enough / cheaper | Step-down / budget | Status | ⏳ |
|---|---|---|---|---|---|
| `terminal_agentic_loop` | Opus 5.5 or Sonnet 5.5 | Kimi K3.1 Pro (contested); Gemini 3.8 Flash (contested) | GPT-6.1 Sol | Best **supported** (3 runners); good enough **contested**; step-down **contested** (was supported) | Mercor points: unknown date |
| `tool_orchestration` | Gemini 4 Argon (high) | MiniMax M3.1 Flash | — | Best **supported**; good enough **provisional** | Argon: one point has an unknown date |
| `greenfield_app` | Sonnet 5.5 | Haiku 5.5 (contested) | DeepSeek V4.1 Flash 1017 (contested) | Best **supported** | no |
| `refactor_migration` | Sonnet 5.5 | GPT-6.1 Sol | DeepSeek V4.1 Flash 1017 (floor) | **Provisional** (one runner) | no |
| `issue_resolution` | Opus 5.5 (medium) | GPT-6.1 Sol (max) | DeepSeek V4.1 Flash in Codex (contested); older direct options: GPT-5.6 Sol (medium), GLM-5.2 (high), Grok 4.5 (high) (provisional, unanchored) | Best **supported** (now with a direct second-runner point); good enough **supported**; older options **provisional** | **yes** |
| `structured_output` | — (no frontier-tested source) | Grok 4.3 (medium), best among IFBench-tested | — | **Provisional** (unanchored) | **yes** |
| `codebase_qa_search` | — | — | — | **Insufficient** (B-only: Claude models in Claude Code lead) | — |
| `small_edit` | — | — | — | **Insufficient** | — |
| `frontend_visual` | — | — | — | **Insufficient** (B-only: Opus 5.5) | — |
| `code_review` | Opus 5.5 | GPT-6.1 Sol (co-leader on the A board, ~¼ the $/review; contested) | GPT-6 Luna; Haiku 5.5 (provisional) | Best **supported**; good enough **contested**; step-down **provisional** (was insufficient) | no |
| `planning_architecture` | — | — | — | **Insufficient** (B-only aggregates) | — |
| `long_context_summarize` | — | — | — | **Insufficient** | — |
| `test_writing` | — (no qualifying frontier row); top among tested: Opus 5 (supported) | — (insufficient; leads only: GPT-6.1 Sol, Opus 5.5) | GPT-5.6 Sol (provisional) | Best-among-tested **supported**; good enough **insufficient** (was GPT-6 Astra, provisional; dropped under rubric v2.1 D6); step-down **provisional** | no |

For insufficient subtasks, the harness should fall back to the default model of the nearest supported subtask, flagged "no evidence". It should not use a B-only leader as a pick.

### 4.2 Detail

Age is counted to 2026-10-24. "≤N d" means the evidence date is a lower bound.

**`terminal_agentic_loop`** (changed: Mercor adds a third tier-A runner; step-down becomes contested)
- **Best: Claude Opus 5.5 (max) or Sonnet 5.5. Supported.**
  1. Vals TB4 (A) · Opus 65.15% at $13.20/test; Sonnet 64.14% at $16.51 · 2026-10-24 (board update) · 0 d · fresh · direct
  2. AA Coding Agent Index, TB4 in Claude Code (A) · Sonnet 66%, Opus 63% · 2026-10 (board current) · ≤23 d · fresh · direct
  3. Mercor TB 2.1 Extended (A, score 70) · Opus 5.5 47.5% #1; Sonnet 5.5 45.5% (−2.0) · ≥ the GPT-6.1 Sol / Opus 5.5 releases (board date not shown) · unknown → treated as stale ⏳ · direct
  4. LiveBench 2.0 agentic (B) · Opus 85.0, top · 2026-10-14 (release) · 10 d · fresh · direct

  Opus is cheaper per task on both A runners (AA pooled $11.42 vs $13.30). AA's model-level TB4 has Opus at 59.6, 7.6 below Kimi.
- **Good enough: Kimi K3.1 Pro. Contested.**
  1. Vals TB4 (A) · 63.64% at $4.57 · 2026-10-24 · 0 d · fresh · direct
  2. AA TB4 (A) · 67.2% (#1) · 2026-10 · ≤23 d · fresh · direct
  3. LiveBench 2.0 agentic (B, contradicts) · 49.5 vs Opus 85.0 · 2026-10-14 · 10 d · fresh · direct

  It launched 10/23. Re-check by 11/24. Mercor has no Kimi K3.1 Pro row.
- **New candidate: Gemini 3.8 Flash. Contested (A vs A).**
  1. Mercor TB 2.1 Extended (A) · 44.4%, −3.1 pts, at $0.75/$3.75 list (promo to 2026-12-31) vs Opus $4/$20 · unknown → stale ⏳ · direct. Mercor shows no $/task, so "cheaper" rests on token price only
  2. Vals TB4 (A, contradicts) · 19.7%, −45.5 pts · 2026-10-24 · fresh · direct

  Two tier-A runners disagree by 25 pts on the same model. Not a pick until the cause (harness, TB version, timeouts) is known.
- **Step-down: GPT-6.1 Sol (max). Contested (was supported).**
  1. Vals TB4 (A) · 55.05% at $1.72, −10.1 pts · 2026-10-24 · 0 d · fresh · direct
  2. AA TB4 (A) · 56.1% · 2026-10 · ≤23 d · fresh · direct
  3. Arena Agent (B) · #4 net improvement, P50 $1.76/task · 2026-10-23 · 1 d · fresh · direct
  4. Mercor TB 2.1 Extended (A, contradicts the "outside the bar" label) · 45.8%, −1.7 pts behind Opus 5.5, i.e. top tier · unknown → stale ⏳ · direct

  Everyone agrees GPT-6.1 Sol is much cheaper per task. They disagree on whether it is top tier or a step down. Treat it as the cheap default with an escalation path.
- **Not good enough (supported):**
  - Haiku 5.5: Vals 36.36%, AA 32.8%.
  - DeepSeek V4.1 Flash 1017: Vals 31.82%, AA 33.8%.
  - Grok 4.7: Vals 28.79% at $18.01, AA 25.8%, Mercor 11.8%.
  - Haiku 5.5 and DeepSeek V4.1 Flash 1017 on Mercor: 37.7% and 38.4% (−9.8 / −9.1, just inside the bar). On Mercor they are good-enough candidates, but Vals and AA (both A, fresh) put them far outside the bar. The "not good enough" label is now contested, and neither is a pick.
- **Older sources:** METR Time Horizons (A, 169 d, aging) tests no model in the routing set. No change.

**`tool_orchestration`**
- **Best: Gemini 4 Argon (high). Supported. ⏳ (the B point has an unknown date).**
  1. AutomationBench-AA (A) · 77.5%, #1 · 2026-10-23 · 1 d · fresh · direct
  2. Zapier AutomationBench 1.0.6 strict (B) · Argon High 51.3% at $1.70 (#1); Sonnet 5.5 Max 44.7%; Opus 5.5 Max 42.5%; GPT-6 Astra Max 41.4% · unknown (pre-release partner report) · unknown · treated as stale · direct

  3. Mercor τ³-Banking (B) · Argon High 58.1 ±8.9 #1; Opus 5.5 Max 55.0 ±8.2 · date unknown · direct
  4. Mercor APEX-Agents (B, rel = 2) · Argon High 82.4 ±4.3 #1; Sonnet 5.5 75.5 · date unknown · direct

  The Zapier source gives the same order for the top 4. Mercor's two boards also have Argon first.
- **Good enough: MiniMax M3.1 Flash. Provisional.**
  1. AutomationBench-AA (A) · 72.5% at $0.15/$0.60 list · 2026-10-23 · 1 d · fresh · direct

  Zapier strict and Toolathlon have no MiniMax M3.1 row. AA $/task was not captured.
- **Not picked: GLM 5.3 Flash and DeepSeek V4 Pro 0813. A and B sources disagree.**
  - GLM 5.3 Flash:
    - AutomationBench-AA (A) · 60.4%, 17.1 below the leader · 2026-10-23 · fresh
    - Toolathlon-Verified (B) · 78.4 ±1.9 (max), top of its tested set · 2026-08-30 · 55 d · fresh
  - DeepSeek V4 Pro 0813:
    - AutomationBench-AA (A) · 56.7%
    - Toolathlon-Verified (B) · 74.4 ±1.2 · 2026-08-13 · 72 d · fresh

  The tier-A source puts both outside the 10-point bar, so neither is a pick. Toolathlon tested no Argon, Opus 5.5 or GPT-6.x model, so it cannot show where they would rank against the frontier.
- **Older sources:** BFCL V4 (A, 2026-04-12, 195 d, stale) tops out at Claude Opus 4.5 77.47%, then GLM-4.6 72.38%. It shares no model with AutomationBench-AA, so it is unanchored. Opus 4.5 ($5/$25) is also dearer per token than Opus 5.5. No pick.
- MCP Atlas (B) and τ³ (B) have no current frontier rows.

**`greenfield_app`** (unchanged; all evidence fresh)
- **Best: Claude Sonnet 5.5. Supported.**
  1. Vibe Code Bench v1.1 (A) · 92.39% at $31.25 · 2026-10-24 · 0 d · fresh · direct
  2. LMArena WebDev (B) · ~1768, top 3 (Opus 5.5 1807) · 2026-10-22 · 2 d · fresh · direct

  Gemini 4 Argon (VCB 91.91% at $8.11) is also top-tier on A, but on WebDev it is at 1673.
- **Good enough: Claude Haiku 5.5. Contested.**
  1. VCB (A) · 90.44% at $6.07 · 2026-10-24 · fresh · direct
  2. WebDev (B, contradicts) · 1585 · 2026-10-22 · fresh · direct
- **Budget: DeepSeek V4.1 Flash 1017. Contested.**
  1. VCB (A) · 87.73% at $0.58 · 2026-10-24 · fresh · direct
  2. WebDev (B, contradicts) · 1664 · 2026-10-22 · fresh · direct
- **Older sources:** FeatureBench (A) reports Opus 4.5 as its newest model, with no overlap with VCB. No pick.

**`refactor_migration`** (unchanged; all evidence fresh)
- **Best: Claude Sonnet 5.5. Provisional.**
  1. Vals Code Migration v1.1 (A) · 86.88% at $43.88; Opus 5.5 81.01% at $72.40; GPT-6 Astra 80.58% at $62.07 · 2026-10-20 · 4 d · fresh · direct
- **Good enough: GPT-6.1 Sol. Provisional.**
  1. Vals CM v1.1 (A) · 77.32% at $9.51, −9.6 pts · 2026-10-20 · 4 d · fresh · direct
- **Floor: DeepSeek V4.1 Flash 1017. Provisional.**
  1. Vals CM v1.1 (A) · 67.52% at $1.76 · 2026-10-20 · fresh · direct
- **Not good enough:** Haiku 5.5, 52.36% at $6.20.
- **Reliability caveat:** in the Vals Router Index (A, 2026-10-20), Anthropic refusals counted as failures (Opus 5.5 47.5% on Code Migration).
- **Older sources:** SWE-CI (A) tests Opus 4.6 / GPT-5.2 and shares no model with CM v1.1, so it is unanchored and cannot be a second runner. Vals CM v1 is the same runner and is superseded.
- **New this pass, still no second A runner:**
  - Scale SWE Atlas Refactoring (B, ind = 1): GPT 6 Astra 59.05 ±6.43 #1; Fable 5.1 56.67. It has no Sonnet 5.5, GPT-6.1 Sol or DeepSeek 1017 row, so it can neither support nor contradict the picks.
  - NIST CAISI PortBench (B, 2026-05-01, 176 d, aging): GPT-5.5 78%, Opus 4.6 60%, DeepSeek V4 Pro 44%, GPT-5.4 mini 41%. Government runner with private tasks, but older models only and no task count.

**`issue_resolution`** (changed: SWE-rebench is now a second tier-A runner)
- **Best: Claude Opus 5.5 at medium effort. Supported ⏳ (corroboration comes from a predecessor).**
  1. AA FrontierCode 1.1 (A) · Medium 57.1%, High 54.0%, XHigh 53.5%, Max 52.2% (mirror) · 2026-10 (board current) · ≤23 d · fresh · direct
  2. AA Coding Agent Index (A, same runner) · Claude Code + Opus 5.5 max 56% on FrontierCode · 2026-10 · ≤23 d · fresh · direct
  3. SWE-rebench (A source → **B, family**: Opus 5 → Opus 5.5) · Opus 5 63.4% at $3.47, 1.1 below leader Fable 5 64.5% · ≥2026-07-24 (Opus 5 release) · ≤92 d · aging · family

  4. Mercor DeepSWE v1.1 run (A) · Opus 5.5 Max 72.3% #1; Opus 5 Max 71.4% · ≥ Opus 5.5 release · unknown → stale ⏳ · direct. The names on ranks 2–4 (72.3 / 72.0 / 71.7) did not render, so it is unknown whether GPT-6.1 Sol or Argon were run.
  5. Mercor FrontierCode run (B) and APEX-SWE (B) · Opus 5.5 is #1 on both (FrontierCode Medium 54.6%; APEX-SWE Max 67.6 ±5.9) · direct

  Point 4 adds a direct point from a second runner, alongside the family point. Its date is unknown, so ⏳ stays. Point 3 comes from a different runner and agrees in direction: an Opus model is in the top tier of a contamination-controlled board. Opus 5 is still sold, but at $5/$25, more than Opus 5.5 at $4/$20, so it is not a cheaper pick.
- **Good enough: GPT-6.1 Sol (max). Supported ⏳ (corroboration from a predecessor).**
  1. AA FrontierCode (A) · 49.1% (mirror), −8.0 pts · 2026-10 · fresh · direct
  2. AA Coding Agent Index (A, same runner) · 49% in Codex, pooled $1.50/task vs $11.42 for Claude Code + Opus 5.5 · 2026-10 · fresh · direct
  3. SWE-rebench (B, family: GPT-5.6 Sol → GPT-6.1 Sol) · GPT-5.6 Sol medium 62.3% at $0.85, 2.2 below the leader at about 1/5 of its $/task · row date unknown (board ≥2026-07-24) · unknown → stale · family
- **Budget lead: DeepSeek V4.1 Flash in Codex. Contested.** (unchanged)
  1. AA Coding Agent Index (A) · 53% on FrontierCode at pooled $0.39 · 2026-10 · fresh · direct
  2. AA FrontierCode model-level (A, mirror, contradicts) · 44.0% · 2026-10 · fresh · direct
- **New: older models with direct, cheaper evidence. Provisional, unanchored ⏳.** All three points come from one source: SWE-rebench (A, direct), with leader Fable 5 at 64.5% and $4.40 ($10/$50 list). Row dates are unknown (the board has rows up to ≥2026-07-24), so all three are treated as stale.

  | Model | SWE-rebench score | $/task | Current list price (verified) |
  |---|---|---|---|
  | Grok 4.5 [high] | 63.8% ±0.60 | $1.47 | $2/$6 |
  | GLM-5.2 [high] | 62.9% ±1.19 | $1.40 | $1.40/$4.40 |
  | GPT-5.6 Sol [medium] | 62.3% | $0.85 | $4/$20, promo note; whether $/task used a promo price is unknown |

  - Each is within 3 pts of the leader at about 1/3 to 1/5 of its $/task. Prices are unchanged where verified.
  - SWE-rebench has no Opus 5.5 / GPT-6.x / Gemini 4 rows, and none of these three models has a FrontierCode row captured, so the gap to today's frontier is unknown (R5). That caps them at **provisional**.
  - Use them only where a harness already depends on that provider.
- **Not usable as A:** SWE-rebench rows for DeepSeek-V4 Pro, MiniMax M3 and MiMo. Their current availability was not verified, so they count as B (R2).
- **Changed from v1:** best and good enough move from provisional to **supported**. Three older direct options are added as provisional.

**`structured_output`** (changed: insufficient → provisional)
- **Pick: Grok 4.3 (medium), "best among models AA IFBench tested". Provisional, unanchored ⏳.**
  1. AA IFBench (A, confirmed on AA's own page) · 83.3%, #1 · ≥2026-04-30 (model release); the eval date was not shown · ≤177 d · aging · direct · $1.25/$2.50 list verified · $/task unknown
- Caveats:
  - IFBench measures output-format constraints, not JSON-schema adherence (rel = 2).
  - It has no Opus 5.5 / GPT-6.x / Gemini 4 rows, so by R4 this is not a "best" claim for the current frontier.
  - Only the leader's value is AA-confirmed. Mirror values for other rows are not used, because the mirror disagreed with AA on Grok 4.20 (81.2% vs 82.9%).
- B-only: JSONSchemaBench (commercial-stake cap; GPT-4o era).

**Insufficient-evidence subtasks**
- **`codebase_qa_search`: insufficient.** No change. Mercor added two more LLM-judged boards.
  - SWE-Atlas-QnA-AA (B, 2026-10, fresh): Opus 5.5 and Fable 5.1 in Claude Code 66%; Sonnet 5.5 64%; DeepSeek V4.1 Flash in Codex 61% (pooled $0.39); GPT-6.1 Sol 60%; Haiku 5.5 34%.
  - Scale SWE Atlas (B): Opus 5 63.17%.
  - Mercor SWE Atlas QnA (B, judge Opus 4.5). On the public set, DeepSeek V4.1 Flash leads with 53.5. On the 50 held-out tasks it falls to 36.7, while Sonnet 5.5 (44.7) and Opus 5.5 (43.3) lead and GPT-6.1 Sol is at 31.3. This is the same Claude-led order as AA, but every runner uses an LLM judge.
- **`small_edit`: insufficient.**
  - SWE-V saturated (C).
  - Aider Polyglot is now B but stale (2025-11-20, 338 d): gpt-5 (high) 88.0% at $29.08; DeepSeek-V3.2-Exp Reasoner 74.2% at $1.30. B-only and old.
  - LangChain A/B (B, method, 2026-10-01).
  - Mercor SWE-V Extended (B, 50 held-out tasks): DeepSeek V4.1 Flash 82.7%, Opus 5 82.0%, Opus 5.5 66.0%, Haiku 5.5 53.3%, GPT-6.1 Sol 45.3%. The ordering is unlike every other board, and 50 tasks are noisy, so it is not used.
- **`frontend_visual`: insufficient.** No change.
  - Vals SWE-MM (B, 2026-10-16): Opus 5.5 70.21% at $4.92.
  - WebDev (B): Opus 5.5 1807.
  - New this pass: VisualForge (C, 8 pages per model) and screenshotbench (C) are both D6. No tier-A visual or front-end board was found.
- **`code_review`**: moved to its own section below.
- **`planning_architecture`: insufficient.** No change.
  - B aggregates: AA Intelligence Index (Opus 5.5 max 58 at $5.98/task; GPT-6.1 Sol 52 at $0.72) and Epoch ECI.
  - METR (A) tests no current routing model.
  - ArchBench (C): a submission-based architecture workshop board; no model rows read.
- **`long_context_summarize`: insufficient.** No change.
  - AA-LCR (B, mirror).
  - Mercor AA-LCR Extended (B, LLM judge): GLM-5.3 76.8, GPT-5.6 Terra 74.4, Opus 5.5 74.2, Opus 5 73.9. These are compressed like AA's board and still LLM-judged.
  - Fiction.LiveBench was scored this pass and is C (score 46; newest result 2026-01-27).
- **`test_writing`**: moved to its own section below.

**`code_review`** (changed: insufficient → best supported, good enough contested)
- **Best: Claude Opus 5.5. Supported.**
  1. CodePanel (A) · 87% of bugs caught, −3 vs leader GPT-6.1 Sol 90%, at $0.159/review · 2026-10-17 · 7 d · fresh · direct. The top 7 share rank 1 (minimum detectable gap ~21 pts).
  2. IronBee (B) · Opus 5.5 low F2 62.1, in the top group with Sonnet 5.5 low 64.4 · 2026-10-19 · 5 d · fresh · direct
  3. MacroscopeBench (B) · Opus 5.5 max 83.9, #1, at $11.58 · ≥2026-09-22 · ≤32 d · fresh · direct
  4. Qodo (B) · Opus 5.5 high F1 56.8, #1, $1.00/PR · 2026-10-12 · 12 d · fresh · direct
- **Good enough / cheaper: GPT-6.1 Sol. Contested.**
  1. CodePanel (A) · 90%, the board leader, at $0.041/review (about ¼ of Opus) · fresh · direct
  2. MacroscopeBench (B) · max 78.5 (−5.4) at $1.05 vs Opus $11.58; high 76.7 at $0.56 · fresh · direct
  3. IronBee (B, contradicts) · xhigh F2 47.5 (−16.9 vs leader), default 44.2 · fresh · direct. IronBee attributes this to low recall on its one-call setup.
  4. Qodo (B) · only GPT-6 Sol medium (48.7, −8.1) was found, not 6.1; family evidence only.

  The disagreement looks like a harness effect: GPT-6.1 Sol leads CodePanel's multi-step pipeline but trails in a single raw call. Use it behind a pipeline, not as a one-shot reviewer.
- **Step-down / budget: GPT-6 Luna or Claude Haiku 5.5. Provisional.**
  1. CodePanel (A) · Luna 63% at $0.0029/review; Haiku 5.5 60% at $0.004 · fresh · direct
  2. IronBee (B) · Haiku 5.5 50.7 at $0.023; Luna xhigh 44.2 at $0.009 · fresh · direct (agrees: both are well below the top)
- **Not picked:**
  - Sonnet 5.5 leads IronBee (64.4) and is #2 on Qodo (54.9), but CodePanel (A) has it at 77%, 13 below the leader. B-only support with an A contradiction.
  - DeepSeek V4.1 Flash: IronBee 56.5 at $0.025/PR; Macroscope max 72.0 at $0.75. No A row (CodePanel tested V4 Flash, not 4.1).
  - Gemini 4 Argon: CodePanel 82% (−8) at $0.054, which is more than GPT-6.1 Sol, so it is not cheaper than the leader.
- **Caveat:** CodePanel's power is low (37 common fixtures). Treat it as one A runner. A second A runner with ≥100 private items would make the picks solid.

**`test_writing`** (v0.4, revised under rubric v2.1 D6: the good-enough pick is dropped; best-among-tested is unchanged)

TestSuiteBench row review (n = 165 apps, single run, noise bound 10.8 pts on a gap; board checked 2026-10-24):

| Row (effort) | M | $/app (est.) | Qualifies? | Why |
|---|---|---|---|---|
| Claude Opus 5 (high) | 55.5 | 10.56 | **Yes** | In the paper. The paper says outright that it analysed all 165 runs ("33 of 165 instances"). Validity 96.1. It ran at high effort, while most rows ran at medium. |
| Claude Opus 5.5 (medium) | 53.9 | 2.33 | No | Board-only row, not in the paper. No completion evidence. |
| GPT-6.1 Sol (medium) | 51.6 | 0.44 | No | Board-only row, not in the paper. No completion evidence. |
| GPT-6 Astra (medium) | 50.1 | 2.18 | No | In the paper, and validity is fine (94.3). But no analysis shows it covered every app, and the scorer drops missing apps. |
| Gemini 3.8 Flash (medium) | 37.9 | 1.63 | **Yes** | In the paper's whole-set analyses (trajectories, overlap across all 12,130 mutants). Its cost uses an introductory price. |
| GPT-5.6 Sol (medium) | 37.7 | 0.89 | **Yes, flagged** | Same whole-set analyses. The effort sweep is consistent (low 31.3, xhigh 46.5). Flag: it is the model that built the benchmark's specs, tests and mutants. |
| DeepSeek V4 Flash (high) | 28.6 | 0.14 | No | Validity 78.1 and R 66.8 are well below the rest, which suggests harness trouble. The paper does not say which snapshot it used. |
| GPT-5.6 Luna (medium) | 19.3 | 0.03 | No | Validity 74.1 and R 65.4, the same red flag. |

What the board can show:
- The top four (55.5 to 50.1, a spread of 5.4) are a **tie**.
- That tie cluster is clearly ahead of Gemini 3.8 Flash and GPT-5.6 Sol (gaps ≥ 12.2).
- Gemini 3.8 Flash and GPT-5.6 Sol are tied with each other (gap 0.2).
- The gaps from GPT-5.6 Sol to DeepSeek (9.1) and from DeepSeek to Luna (9.3) are inside the noise.

- **Top among tested models: Claude Opus 5 (high). Supported, but not a frontier claim (R4).**
  1. TestSuiteBench (A; qualifying row) · mutation score 55.5 at $10.56 (token estimate), #1 · 2026-10 (paper) · ≤24 d · fresh · direct ($5/$25, still sold)
  2. Scale SWE Atlas TW (B, different runner) · 62.22 ±5.58, within the CI of leader Fable 5.1 67.04 ±5.33 · ≥2026-07-28 · ≤88 d · fresh · direct

  Opus 5.5, GPT-6.1 Sol and GPT-6 Astra sit in Opus 5's tie cluster on TestSuiteBench. They are not ranked below it, but they are not qualifying rows either. Opus 5 also costs more per token than Opus 5.5. A harness would likely pick Opus 5.5 here, but that is a family inference (B at most), not evidence.
- **Good enough: none. Insufficient.** It was GPT-6 Astra (provisional) before rubric v2.1. Astra's row fails "every task counted", so it is dropped.
  - Leads to verify (not evidence):
    - GPT-6.1 Sol (medium): 51.6 at about $0.44/app. That is 3.9 below Opus 5 at about 1/24 of its $/app. List price $2/$10 verified.
    - Claude Opus 5.5 (medium): 53.9 at $2.33. List price $4/$20 verified.
  - Either would become a pick if the authors published per-app results or completion counts, or if a second runner tested it.
- **Step-down: GPT-5.6 Sol (medium). Provisional.**
  1. TestSuiteBench (A; qualifying row, construction-model flag) · 37.7 at $0.89. It trails Opus 5 by 17.8, which is more than the 10.8 noise bound, so it is clearly behind. · fresh · direct
- **Gemini 3.8 Flash:** TestSuiteBench 37.9 (−17.6, clearly behind); Scale TW 53.70 ±5.86 (−13.3). Not good enough on either.
- **Other B evidence:**
  - TestEvo-Bench (B, ind = 1): Claude Code + Opus 4.7 and Gemini CLI + Gemini 3.1 Pro both score 77.5% on test generation, a tie. Under a $1 per-task cap, Opus falls to 44.2% and Gemini holds at 69.8%. Both changes clear TestEvo's 5.1-pt bound.
  - SWT-bench (B) and TestGenEval (B) are unchanged.

### 4.3 Design conclusions (cross-cutting)

| # | Conclusion | Data points (evidence date) | Status |
|---|---|---|---|
| X1 | A static per-subtask lookup beats shipped routers | (1) Vals Router Index (A, 2026-10-20, fresh): all 5 routers are off the frontier; single model per benchmark beats them by 11.0 / 9.9 / 13.2 ±1.2 pts at equal cost. (2) Agent-as-a-Router (B). (3) Scrouting (B) | **Supported** |
| X2 | Rank on measured $/task, not token price | (1) Vals TB4 (A, 10-24): Sonnet $16.51 vs Opus $13.20. (2) AA CAI (A, 2026-10): Sonnet $13.30 vs Opus $11.42 | **Supported** |
| X3 | Key rows on model + effort | (1) AA FrontierCode (A, 2026-10): Opus 5.5 Medium 57.1% > Max 52.2% (mirror). (2) CursorBench 4.0 (B, 2026-09-10, 44 d): High 56.0% at $3.97 vs Max 57.8% at $13.43 | **Supported** |
| X4 | Add a refusal fallback per provider | (1) Vals Router Index (A, 2026-10-20) | **Provisional** |
| X5 | Harness choice changes results | (1) AA CAI vs AA model-level (A): DeepSeek V4.1 Flash 53% vs 44.0% (mirror) | **Provisional** |
| X6 | Do not route on public, static SWE-bench numbers | Scale Pro V2 public 99.4% vs private 81.6% (B); Scrouting (B); Vals retired SWE-V | **Adopted as a source rule** |
| X7 | Cheap-tier routing in production keeps quality | LangChain A/B (B, 2026-10-01) | **Insufficient** |
| X8 (new) | Store evidence_date and freshness per row, and re-check older rows first | Rubric v2 R1–R7. SWE-rebench's changelog said 07-01, but its table had a 07-24 model, so board-level dates mislead | **Adopted as a schema rule** |
| X9 (new) | Check for a same-family successor before routing to an older model | Opus 5 $5/$25 vs Opus 5.5 $4/$20; Opus 4.5 $5/$25 (provider pages, 2026-10-24) | **Adopted as a design rule** (price fact, not a quality claim) |

## 5. Surprising findings

1. **Static routing beats commercial routers** (X1, supported).
2. **Per-token price is a poor cost proxy** (X2, supported).
3. **More reasoning effort can lower scores** (X3).
4. **SWE-bench Verified is solved and leaky** (X6).
5. **Network access inflates scores** (Vals SWE-MM: −21 to −35 pts for Muse Spark without network).
6. **A single fresh benchmark is not enough** (Kimi K3.1 Pro, contested).
7. **Prices have expiry dates.**
   - Gemini 4 Argon's promo ends 2026-11-30, and Gemini 3.8 Flash's ends 2026-12-31.
   - The GLM 5.3 Flash 50% promo ended on 2026-09-09. The previous pass used the expired promo price ($0.075/$0.25) from a secondary source. It is now $0.15/$0.50 from Z.ai's page, and Vals/AA $/task for it may still reflect the promo.
8. **Some top-ranked models can't be routed to** (Muse Wonder Full).
9. **Grok 4.7 is weak on agentic work at its price** (TB4: Vals 28.79% at $18.01, AA 25.8%).
10. **Benchmark versions move under you** (Code Migration v1 → v1.1; TB2.1 fixed 28 of 89 tasks; Toolathlon → Toolathlon-Verified is a new score series).
11. **Older models are often more expensive than their successors.** Opus 5 and Opus 4.5 list at $5/$25, Opus 5.5 at $4/$20. Strong older evidence about Opus 5 therefore yields no cheaper pick.
12. **Two tool-use benchmarks disagree on cheap open-weight models.** GLM 5.3 Flash scores 78.4 on Toolathlon-Verified and 60.4 on AutomationBench-AA. DeepSeek V4 Pro 0813 scores 74.4 and 56.7. Cause unknown: task mix, partial credit, harness or contamination.
13. **Held-out sets cut scores hard.** On Mercor, the same runner's public-set score vs its private held-out set: Opus 5 drops from 93.5 to 82.0 on SWE-V, Fable 5 from 95.9 to 78.7, Opus 5.5 from 83.5 to 47.5 on TB 2.1, and DeepSeek V4.1 Flash from 53.5 to 36.7 on SWE Atlas QnA, where it goes from #1 to mid-table. This strengthens X6: rank on private or fresh sets.
14. **Review quality depends on the pipeline.** GPT-6.1 Sol leads CodePanel's review pipeline (90%), but in IronBee's one-call raw review it is 16.9 F2 below the leader. Sonnet 5.5 shows the reverse pattern.
15. **Two tier-A terminal runners disagree by 25 pts on Gemini 3.8 Flash** (Vals TB4 19.7% vs Mercor TB 2.1 Extended 44.4%).
16. **Budget caps change the ranking.** On TestEvo-Bench, Opus 4.7 in Claude Code falls from 77.5% to 44.2% on test generation under a $1 per-task cap, while Gemini CLI holds at 69.8%. Routing rows should carry a budget assumption.
17. **Government evals exist, but lag.** NIST CAISI's PortBench is the most independent source in the set (ind = 3, private tasks), but it only covers models from the spring of 2026.

## 6. Caveats

- **Harness:** Vals and AA use model-agnostic harnesses. Native scaffolds often score higher. Picks assume a generic harness.
- **Reasoning effort:** rows must key on model + effort (Opus 5.5 AA index: 58 at max, $5.98; 42 at low, $0.55).
- **Vendor-adjacent benchmarks:**
  - ReviewBench (GitHub / Copilot)
  - SWE Atlas (Claude Opus 4.5 judge)
  - SWE-Bench Pro V2 (Reflection)
  - SOB (Interfaze)
  - SWT-bench (LogicStar)
  - JSONSchemaBench (guidance-ai)
- **Partial credit:** AutomationBench-AA gives partial credit; Zapier strict scores are 26–27 pts lower.
- **Judges:** FrontierCode-AA and SWE-Atlas-QnA-AA use GPT-6 Luna (disclosed).
- **Dates are often bounds.** Many boards show no per-row run date. A model-release lower bound makes the age an upper bound. Undated rows are treated as stale.
- **Low statistical power on the new code-review A source.** CodePanel states a minimum detectable gap of about 21 pts. Its top 7 models are statistically tied, and "best" there means "within 3 pts", not "proven better".
- **Single-run sources (rubric v2.1 D6).** TestSuiteBench publishes no per-app results, no completion counts and no variance. Its scorer averages only the apps each row finished. So the review relies on the worst-case 139/√n bound and on indirect evidence of full coverage.
  - A GPT-5.6 Sol flag stays: it built the benchmark.
  - Another flag: Opus 5 ran at high effort while most rows ran at medium.
  - Repeat counts were not recorded for several tier-A sources: Vals Code Migration v1.1 / Vibe Code Bench v1.1, AA IFBench / AutomationBench-AA, BFCL, FeatureBench, SWE-CI and CodePanel. Any of them that turns out to be single-run must pass §2.1 too.
    - CodePanel passes either way: it publishes its own bootstrap CIs over fixtures and compares rows on the fixtures every row completed.
    - The others were not re-audited this pass (§7).
- **Mercor caveats:**
  - None of the Mercor boards report cost, and none show a run date.
  - Some rows did not render with model names (DeepSWE ranks 2–4, and parts of ProgramBench and SciCode). Only named rows are used.
  - SWE-V Extended has a 50-task held-out set and an unusual ordering.
  - Mercor sells expert data to labs (ind = 2).
- **Scale value gaps.** The GPT 6 Astra value (rank 5) on SWE Atlas TW and the Gemini 3.8 Flash value on SWE Atlas Refactoring did not render and are not used.
- **Cost at evidence date:** SWE-rebench $/task was computed at the prices in force when each row ran. Prices were verified unchanged for Grok 4.5 and GLM-5.2. For GPT-5.6 Sol, the page carries a promo note, so its $0.85 may reflect a promo.

## 7. Biggest data gaps

1. **A second current tier-A runner for refactor_migration.** Scale Refactoring (B) has no rows for the picked models, and CAISI PortBench (B) covers older models only.
2. **A second tier-A runner for structured_output, and any frontier rows.** None was found this pass.
3. **codebase_qa:** a board with execution or human grading. Every runner found (AA, Scale, Mercor) uses an LLM judge.
4. **long_context:** a board without an LLM judge. Mercor AA-LCR Extended is still LLM-judged; ATLAS / LongCodeBench were not opened.
5. **small_edit:** a fresh, private small-edit set with ≥100 tasks. Mercor's 50-task held-out SWE-V is too small and anomalous.
6. **frontend_visual:** every visual board found has <30 items (D6), or is preference-based (WebDev, B).
7. **planning_architecture:** no task-specific board beyond aggregates. ArchBench was unreadable.
8. **test_writing:** TestSuiteBench per-app results or completion counts would let Opus 5.5 / GPT-6.1 Sol / GPT-6 Astra qualify. It would also allow a paired bootstrap CI, which is likely much tighter than 10.8 pts. Also needed: frontier rows (Gemini 4 Argon; Opus 5.5 / GPT-6.1 Sol) on Scale TW or TestEvo.
   - **Single-run audit:** record run counts for the tier-A sources listed in §6 and apply §2.1 where they are single-run.
9. **code_review:** a second A runner with ≥100 private items, to resolve the GPT-6.1 Sol contest.
10. **Cost on Mercor boards**, and the cause of the Gemini 3.8 Flash terminal disagreement.
11. Carried over: SWE-rebench rows for current frontier models; AA $/task for AutomationBench; Toolathlon vs AutomationBench disagreement; per-row dates on SWE-rebench and IFBench.
12. **Not opened this pass:** OpenHands Index, ATLAS, LongCodeBench, StructEval, PRDBench, Design2Code leaderboard, sasid.ai structured-output blog, Context Arena (JS-only). The citation-graph search failed (Semantic Scholar 429).

## 8. Sources

See `data/sources.csv` (scores, tiers, previous tier, newest result, maintenance) and `docs/sources.md` (justification and tier moves). All were accessed 2026-10-24.

Tier-A pick sources:
- Vals TB4, CM v1.1, VCB, Router Index
- AA TB4, Coding Agent Index, FrontierCode, AutomationBench-AA, IFBench
- SWE-rebench (https://swe-rebench.com)
- METR, BFCL V4, FeatureBench, SWE-CI
- New in v0.4: CodePanel (https://codepanel.ai/benchmarks), TestSuiteBench (https://arxiv.org/abs/2610.13065), Mercor TB 2.1 Extended and Mercor DeepSWE v1.1 run (https://www.mercor.com/apex/)

Prices are in `data/models.csv` and come from provider pages.
