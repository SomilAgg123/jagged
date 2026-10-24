# Model routing v0.3: research notes (per-claim recency)

Data checked: 2026-10-24 (America/Los_Angeles). Every number below comes from a public page listed in `data/sources.csv` / `docs/sources.md`. Blank or "unknown" means I could not find it. No custom evals were run. Earlier versions are kept as `docs/history/research.v0.md` (first pass) and `docs/history/research.v1.md` (v0.2, rubric v1).

## 1. Method

- **Evidence bar.** Every source is scored against `docs/SOURCE_RUBRIC.md` **v2**, and `scripts/build_sources.py` computes the tier.
  - v2 removes recency from the source score and from the tier-A gate, and retires D3 (stale).
  - Age is applied per data point instead (rubric §4, R1–R7).
  - Result: **65 sources; 15 tier A, 29 tier B, 21 tier C.** The previous pass had 60 sources: 9 A, 23 B, 28 C.
- **Tier-A sources:**
  - Vals AI: TB4, Code Migration v1.1, Vibe Code Bench v1.1, Router Index (method).
  - Artificial Analysis: TB4, Coding Agent Index v2.0, FrontierCode 1.1, AutomationBench-AA, IFBench.
  - Nebius: SWE-rebench.
  - Older academic boards: METR Time Horizons 1.1, Berkeley BFCL V4, FeatureBench, SWE-CI.
  - Provider pricing pages (price role).
  - Two AA boards count as one runner, and so do two Vals boards.
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

## 3. Subtask taxonomy and benchmark mapping

| # | Subtask id | Primary proxy | Secondary | Proxy quality |
|---|---|---|---|---|
| 1 | `codebase_qa_search` | SWE-Atlas-QnA-AA (B) | Scale SWE Atlas (B) | No tier-A proxy (LLM-judge only) |
| 2 | `small_edit` | none (SWE-V saturated, C) | Aider Polyglot (B, stale) | No usable A proxy |
| 3 | `issue_resolution` | AA FrontierCode 1.1 (A) | **SWE-rebench (A, now)**, Scale Pro V2 private (B) | Good; two A runners |
| 4 | `refactor_migration` | Vals Code Migration v1.1 (A) | SWE-CI (A, stale, no overlap) | Good, but one current runner |
| 5 | `greenfield_app` | Vibe Code Bench v1.1 (A) | LMArena WebDev (B), FeatureBench (A, older models) | Good |
| 6 | `frontend_visual` | Vals SWE-MM (B) | LMArena WebDev (B) | No tier-A proxy |
| 7 | `terminal_agentic_loop` | Terminal-Bench 4.0 (Vals A + AA A) | LiveBench agentic (B), Arena Agent (B), METR (A, no current models) | Good, two runners |
| 8 | `tool_orchestration` | AutomationBench-AA (A) | Zapier strict (B), **Toolathlon-Verified (B)**, BFCL V4 (A, stale), MCP Atlas (B), τ³ (B) | Good; A and B disagree on cheap models |
| 9 | `code_review` | none (ReviewBench B) | — | No tier-A proxy |
| 10 | `planning_architecture` | none (B aggregates) | AA-Omniscience (B) | No tier-A proxy |
| 11 | `long_context_summarize` | AA-LCR (B) | AA-Omniscience (B) | No tier-A proxy |
| 12 | `structured_output` | **AA IFBench (A, proxy, no frontier rows)** | JSONSchemaBench (B) | Weak: format-constraint proxy |
| 13 | `test_writing` | none | SWT-bench (B), TestGenEval (B) | Gap |

## 4. Conclusions per subtask (v0.3)

Rules:
- **Best:** top tier of a tier-A source (within 3 pts of the leader), and the source tested the current frontier (R4).
- **Good enough:** within 10 pts of the leader on the same tier-A source, and cheaper per task.
- **Step-down / budget:** a cheaper option outside that bar, listed for the harness to weigh.

### 4.1 Summary

| Subtask | Best | Good enough / cheaper | Step-down / budget | Status | ⏳ |
|---|---|---|---|---|---|
| `terminal_agentic_loop` | Opus 5.5 or Sonnet 5.5 | Kimi K3.1 Pro (contested) | GPT-6.1 Sol | Best **supported**; good enough **contested**; step-down **supported** | no |
| `tool_orchestration` | Gemini 4 Argon (high) | MiniMax M3.1 Flash | — | Best **supported**; good enough **provisional** | Argon: one point has an unknown date |
| `greenfield_app` | Sonnet 5.5 | Haiku 5.5 (contested) | DeepSeek V4.1 Flash 1017 (contested) | Best **supported** | no |
| `refactor_migration` | Sonnet 5.5 | GPT-6.1 Sol | DeepSeek V4.1 Flash 1017 (floor) | **Provisional** (one runner) | no |
| `issue_resolution` | Opus 5.5 (medium) | GPT-6.1 Sol (max) | DeepSeek V4.1 Flash in Codex (contested); older direct options: GPT-5.6 Sol (medium), GLM-5.2 (high), Grok 4.5 (high) (provisional, unanchored) | Best **supported**; good enough **supported**; older options **provisional** | **yes** |
| `structured_output` | — (no frontier-tested source) | Grok 4.3 (medium), best among IFBench-tested | — | **Provisional** (unanchored) | **yes** |
| `codebase_qa_search` | — | — | — | **Insufficient** (B-only: Claude models in Claude Code lead) | — |
| `small_edit` | — | — | — | **Insufficient** | — |
| `frontend_visual` | — | — | — | **Insufficient** (B-only: Opus 5.5) | — |
| `code_review` | — | — | — | **Insufficient** | — |
| `planning_architecture` | — | — | — | **Insufficient** (B-only aggregates) | — |
| `long_context_summarize` | — | — | — | **Insufficient** | — |
| `test_writing` | — | — | — | **Insufficient** (B-only, older agents) | — |

For insufficient subtasks, the harness should fall back to the default model of the nearest supported subtask, flagged "no evidence". It should not use a B-only leader as a pick.

### 4.2 Detail

Age is counted to 2026-10-24. "≤N d" means the evidence date is a lower bound.

**`terminal_agentic_loop`** (unchanged; all evidence fresh)
- **Best: Claude Opus 5.5 (max) or Sonnet 5.5. Supported.**
  1. Vals TB4 (A) · Opus 65.15% at $13.20/test; Sonnet 64.14% at $16.51 · 2026-10-24 (board update) · 0 d · fresh · direct
  2. AA Coding Agent Index, TB4 in Claude Code (A) · Sonnet 66%, Opus 63% · 2026-10 (board current) · ≤23 d · fresh · direct
  3. LiveBench 2.0 agentic (B) · Opus 85.0, top · 2026-10-14 (release) · 10 d · fresh · direct

  Opus is cheaper per task on both A runners (AA pooled $11.42 vs $13.30). AA's model-level TB4 has Opus at 59.6, 7.6 below Kimi.
- **Good enough: Kimi K3.1 Pro. Contested.**
  1. Vals TB4 (A) · 63.64% at $4.57 · 2026-10-24 · 0 d · fresh · direct
  2. AA TB4 (A) · 67.2% (#1) · 2026-10 · ≤23 d · fresh · direct
  3. LiveBench 2.0 agentic (B, contradicts) · 49.5 vs Opus 85.0 · 2026-10-14 · 10 d · fresh · direct

  It launched 10/23. Re-check by 11/24.
- **Step-down: GPT-6.1 Sol (max). Supported.**
  1. Vals TB4 (A) · 55.05% at $1.72 · 2026-10-24 · 0 d · fresh · direct
  2. AA TB4 (A) · 56.1% · 2026-10 · ≤23 d · fresh · direct
  3. Arena Agent (B) · #4 net improvement, P50 $1.76/task · 2026-10-23 · 1 d · fresh · direct
- **Not good enough (supported):**
  - Haiku 5.5: Vals 36.36%, AA 32.8%.
  - DeepSeek V4.1 Flash 1017: Vals 31.82%, AA 33.8%.
  - Grok 4.7: Vals 28.79% at $18.01, AA 25.8%.
- **Older sources:** METR Time Horizons (A, 169 d, aging) tests no model in the routing set. No change.

**`tool_orchestration`**
- **Best: Gemini 4 Argon (high). Supported. ⏳ (the B point has an unknown date).**
  1. AutomationBench-AA (A) · 77.5%, #1 · 2026-10-23 · 1 d · fresh · direct
  2. Zapier AutomationBench 1.0.6 strict (B) · Argon High 51.3% at $1.70 (#1); Sonnet 5.5 Max 44.7%; Opus 5.5 Max 42.5%; GPT-6 Astra Max 41.4% · unknown (pre-release partner report) · unknown · treated as stale · direct

  Both sources give the same order for the top 4.
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

**`issue_resolution`** (changed: SWE-rebench is now a second tier-A runner)
- **Best: Claude Opus 5.5 at medium effort. Supported ⏳ (corroboration comes from a predecessor).**
  1. AA FrontierCode 1.1 (A) · Medium 57.1%, High 54.0%, XHigh 53.5%, Max 52.2% (mirror) · 2026-10 (board current) · ≤23 d · fresh · direct
  2. AA Coding Agent Index (A, same runner) · Claude Code + Opus 5.5 max 56% on FrontierCode · 2026-10 · ≤23 d · fresh · direct
  3. SWE-rebench (A source → **B, family**: Opus 5 → Opus 5.5) · Opus 5 63.4% at $3.47, 1.1 below leader Fable 5 64.5% · ≥2026-07-24 (Opus 5 release) · ≤92 d · aging · family

  Point 3 comes from a different runner and agrees in direction: an Opus model is in the top tier of a contamination-controlled board. Opus 5 is still sold, but at $5/$25, more than Opus 5.5 at $4/$20, so it is not a cheaper pick.
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
- **`codebase_qa_search`: insufficient.** No change.
  - SWE-Atlas-QnA-AA (B, 2026-10, fresh): Opus 5.5 and Fable 5.1 in Claude Code 66%; Sonnet 5.5 64%; DeepSeek V4.1 Flash in Codex 61% (pooled $0.39); GPT-6.1 Sol 60%; Haiku 5.5 34%.
  - Scale SWE Atlas (B): Opus 5 63.17%.
- **`small_edit`: insufficient.**
  - SWE-V saturated (C).
  - Aider Polyglot is now B but stale (2025-11-20, 338 d): gpt-5 (high) 88.0% at $29.08; DeepSeek-V3.2-Exp Reasoner 74.2% at $1.30. B-only and old.
  - LangChain A/B (B, method, 2026-10-01).
- **`frontend_visual`: insufficient.** No change.
  - Vals SWE-MM (B, 2026-10-16): Opus 5.5 70.21% at $4.92.
  - WebDev (B): Opus 5.5 1807.
- **`code_review`: insufficient.** No change. ReviewBench (B, 2026-10-20) scores agents.
- **`planning_architecture`: insufficient.** No change.
  - B aggregates: AA Intelligence Index (Opus 5.5 max 58 at $5.98/task; GPT-6.1 Sol 52 at $0.72) and Epoch ECI.
  - METR (A) tests no current routing model.
- **`long_context_summarize`: insufficient.** No change.
  - AA-LCR (B, mirror).
  - Fiction.LiveBench was scored this pass and is C (score 46; newest result 2026-01-27).
- **`test_writing`: insufficient.**
  - SWT-bench is now B (newest 2026-07-08, 108 d, aging; agents, not bare models; LogicStar stake).
  - TestGenEval is now B (GPT-4o era).
  - B-only.

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
- **Cost at evidence date:** SWE-rebench $/task was computed at the prices in force when each row ran. Prices were verified unchanged for Grok 4.5 and GLM-5.2. For GPT-5.6 Sol, the page carries a promo note, so its $0.85 may reflect a promo.

## 7. Biggest data gaps

1. **A SWE-rebench run on Opus 5.5 / GPT-6.1 Sol / Gemini 4 Argon.** It would turn issue_resolution's family-B points into direct A points, and anchor the older cheap options.
2. **A second current runner for refactor_migration.**
3. **A current IFBench or JSON-schema run on frontier models**, to anchor structured_output.
4. **Codebase QA with execution or human grading.**
5. **Test writing:** no tier-A board.
6. **Model-level code review** with ≥100 PRs and repeated runs.
7. **Small-edit discrimination:** a fresh, private small-edit set.
8. **AA $/task** for AutomationBench and per component of the Coding Agent Index.
9. **Resolving the Toolathlon vs AutomationBench disagreement** on GLM 5.3 Flash and DeepSeek V4 Pro.
10. **Not verified this pass:**
    - per-row run dates on SWE-rebench and AA IFBench;
    - SWE-bench-Live and Multi-SWE-bench boards;
    - Cognition FrontierCode numbers;
    - Zapier strict report date;
    - per-model AA FrontierCode values below the top 3 (mirror only);
    - FeatureBench / SWE-CI publication-run dates;
    - TestGenEval, JSONSchemaBench and MCP-Universe (not re-opened).

## 8. Sources

See `data/sources.csv` (scores, tiers, previous tier, newest result, maintenance) and `docs/sources.md` (justification and tier moves). All were accessed 2026-10-24.

Tier-A pick sources:
- Vals TB4, CM v1.1, VCB, Router Index
- AA TB4, Coding Agent Index, FrontierCode, AutomationBench-AA, IFBench
- SWE-rebench (https://swe-rebench.com)
- METR, BFCL V4, FeatureBench, SWE-CI

Prices are in `data/models.csv` and come from provider pages.
