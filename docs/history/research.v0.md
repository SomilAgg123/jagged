# Model routing v0: research notes

Data checked: 2026-10-24 (America/Los_Angeles). Every number below comes from a public page listed under Sources. Blank or "unknown" means I could not find it. No custom evals were run.

## 1. Method

- **Primary independent sources:** Vals AI and Artificial Analysis (AA). Both run every model themselves on a fixed harness. Vals uses bash-only mini-swe-agent on most coding boards and OpenHands on Vibe Code Bench. Both publish cost per task, not just token prices.
- **Secondary sources:** Scale Labs (SWE-Bench Pro V2, SWE Atlas), LMArena WebDev (human preference votes), and GitHub ReviewBench. Each has a conflict or method caveat, noted below.
- **Mirrors:** BenchLeader and BenchLM re-publish AA, LMArena and Scale data. I used them only where the primary page was hard to read. Treat them as mirrors, not sources. BenchLM's SWE-Bench Pro V2 page mislabels some model creators.
- **Prices:** taken from provider pricing pages where I could reach them (Anthropic, OpenAI, Google, xAI, Meta, DeepSeek, and Moonshot via AA). For Z.ai, Xiaomi, Alibaba, Mistral and MiniMax I used the list price Vals shows. These are labeled secondary in `models.csv`.
- **Cost per task over price per token.** Token efficiency differs by 10x or more between models (see §5), so the router should key on measured $/task wherever a benchmark publishes it.

## 2. Benchmark status in Oct 2026

| Benchmark | Runner | Status (2026-10-24) | Use for routing? |
|---|---|---|---|
| Terminal-Bench 4.0 | Vals (mini-swe-agent, avg@3); AA | **Maintained**. Vals updated 10/24. 66 new tasks, median 4h expert time, about 3/4 non-SWE. Not comparable to 2.x | **Yes**, core agentic signal |
| SWE-bench Verified | Vals | **Saturated and retired**. Vals stopped running new models; last update 9/1/2026; top 97.0%. Official swebench.com board's newest entry is Feb 2026 | Floor check only ("can it do easy fixes at all") |
| SWE-Bench Pro V2 | Scale (co-developed with Reflection) | Maintained. Public split is near ceiling (Opus 5 99.40%). Private split shows a large gap | Use the **private** split where available |
| SWE-Bench Pro (original public) | Scale | Stale (top: Muse Spark 1.1 61.5%) | No |
| Code Migration v1 / v1.1 | Vals | Maintained. v1 updated 10/18; v1.1 (Pi harness) now replaces it in Vals Index | **Yes**, multi-file refactor proxy |
| SWE-bench Multimodal | Vals (no network) | Maintained, 10/16 | **Yes**, screenshot-to-fix proxy |
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

## 3. Subtask taxonomy and benchmark mapping

| # | Subtask id | What the harness is doing | Primary proxy | Secondary | Proxy quality |
|---|---|---|---|---|---|
| 1 | `codebase_qa_search` | Explore an unfamiliar repo, trace behavior, answer "how does X work" | SWE Atlas Codebase QnA | AA-LCR | Medium; few new models |
| 2 | `small_edit` | Well-specified single-file edit or bug fix | SWE-bench Verified (Vals) | SWE-Bench Pro V2 public | Good but saturated: works as a floor |
| 3 | `issue_resolution` | Real multi-file bug fix from an issue | SWE-Bench Pro V2 **private** | Terminal-Bench 4.0 | Medium; private data only for 5 models |
| 4 | `refactor_migration` | Large multi-file rewrite or port that must keep behavior | Vals Code Migration | — | Good |
| 5 | `greenfield_app` | Build an app or feature end to end from a spec | Vibe Code Bench v1.1 | LMArena WebDev | Good |
| 6 | `frontend_visual` | UI work from screenshots and visual bugs | SWE-bench Multimodal (Vals) | LMArena WebDev | Good |
| 7 | `terminal_agentic_loop` | Long-horizon autonomous shell work (build, debug, ops, ML) | Terminal-Bench 4.0 (Vals + AA) | — | Good |
| 8 | `tool_orchestration` | Multi-step tool/function calling against APIs and SaaS | AutomationBench-AA | τ³-bench | Medium (partial-credit scoring) |
| 9 | `code_review` | Find real issues in a PR diff | ReviewBench | — | Weak (agent-level, vendor-run) |
| 10 | `planning_architecture` | Decompose a task, design, hard reasoning | AA Intelligence Index | AA-Omniscience; SWE Atlas architecture subset | Weak, indirect |
| 11 | `long_context_summarize` | Summarize or compact long context and logs | AA-LCR | AA-Omniscience | Medium |
| 12 | `structured_output` | JSON/schema extraction, classification, commit messages | **None current** | SOB, IFBench (both stale) | Gap |
| — | `test_writing` | Write meaningful tests | **None current** (SWE Atlas Test Writing announced, no results) | — | Gap |

## 4. v0 rankings per subtask

Two picks per subtask:
- **Best:** highest independent score.
- **Good enough:** the cheapest model within about 5–10 points of the best (or above the stated bar), with $/task where the board publishes it.

Confidence: H = several independent boards agree; M = one good board; L = weak or indirect proxy.

| Subtask | Best quality | Good enough (cheapest) | Budget / floor | Conf. |
|---|---|---|---|---|
| `codebase_qa_search` | Claude Opus 5 via Claude Code xHigh 63.17% (Fable 5.1 59.95%, GPT-6 Astra 59.14%). Opus 5.5 / Sonnet 5.5 not yet listed | Gemini 3.8 Flash 47.04% (mini-swe-agent), $0.75/$3.75 promo | GLM 5.2 48.12% (open) | L |
| `small_edit` | Claude Opus 5 97.0% SWE-V | GLM 5.3 Flash 92.0% at ~$0.02/test; GPT-5.6 Luna 93.0% at ~$0.04/test | DeepSeek V4 Flash 0731 88.8% at ~$0.01/test | M (saturated, contaminated) |
| `issue_resolution` | Claude Opus 5: 222/272 private (81.6%) | Gemini 3.8 Flash 211/272 (77.6%); GLM 5.3 211/272 (77.6%, open) | Haiku 5.5 87.23% public (no private result) | M |
| `refactor_migration` | Claude Sonnet 5.5 69.83% ($75.83/test) | **GPT-6.1 Sol 65.12% at $6.51/test** (about 1/12 of Sonnet's cost for -4.7 pts) | DeepSeek V4.1 Flash 45.62% at $0.94/test | M |
| `greenfield_app` | Claude Sonnet 5.5 92.39% ($31.25/test) | **Claude Haiku 5.5 90.44% at $6.07/test** | DeepSeek V4.1 Flash 1017 87.73% at $0.58/test | M-H (WebDev agrees on top tier) |
| `frontend_visual` | Claude Opus 5.5 70.21% at $4.92/test (WebDev #1, 1807) | Claude Sonnet 5.5 58.33% at $4.53. No real saving: **just use Opus 5.5** | DeepSeek V4.1 Flash 46.46% at $0.23; Haiku 5.5 43.96% at $0.70 | M |
| `terminal_agentic_loop` | Claude Opus 5.5 65.15% Vals ($13.20/test); Kimi K3.1 Pro tops AA at 67.2% | **Kimi K3.1 Pro 63.64% at $4.57/test** (Vals); GPT-6.1 Sol 55.05% at $1.72/test | GLM 5.3 Flash 37.37% at $1.22; DeepSeek V4.1 Flash 1017 31.82% at $0.54 | H (Vals and AA agree on the top 5) |
| `tool_orchestration` | Gemini 4 Argon (high) 77.5% | **MiniMax M3.1 Flash 72.5%** at $0.15/$0.60 | DeepSeek V4.1 Flash (max) 68.9% | M |
| `code_review` | Opus 5.5 inside Laude RevEngine Prime, F1 59.6% | DeepSeek Harness Reviewer with deepseek-flash, F1 39.9% / precision 89.5% | — | L (harness dominates) |
| `planning_architecture` | Claude Opus 5.5 max: AA index 58, Omniscience 46.4 | **GPT-6.1 Sol max: AA 52 at $0.72/task** vs Opus 5.5 max $5.98/task | DeepSeek V4.1 Flash 1017 max: AA 45 at $0.26/task | L |
| `long_context_summarize` | Kimi K3 max 88.7% AA-LCR (Kimi K3.1 Pro 86.3%, MiMo V2.6 Pro 86.3%) | **GPT-6 Luna max 83.3%** at $0.10/$0.50; DeepSeek V4.1 Flash 82.7–84.0% | Haiku 5.5 82.7%, but its price is 5x above 100K-token prompts | M (board is compressed: top-15 within ~6 pts) |
| `structured_output` | unknown (no current board) | Default to the cheapest model with native JSON-schema mode (e.g. GPT-6 Luna, DeepSeek flash) | — | Gap |
| `test_writing` | unknown | unknown | — | Gap |

### Cross-cutting picks

- **Most frequent "good enough" across subtasks:** GPT-6.1 Sol ($2/$10) and DeepSeek V4.1 Flash 1017 ($0.30/$1.20 peak, $0.15/$0.60 off-peak).
- **Most frequent "best":** Claude Opus 5.5 and Claude Sonnet 5.5.
- **Anthropic's own cheap tier is uneven.** Haiku 5.5 is near-frontier on Vibe Code Bench (90.44%) but far behind on Terminal-Bench (36.36% vs 65.15%) and Code Migration (44.57% vs 69.83%). That makes it a good example for per-subtask routing.

## 5. Surprising findings

1. **Static routing beats commercial routers (Vals Router Index, 10/20).**
   - All five routers tested were dominated on both cost and accuracy by a single model. Ramp Router scored 57.80% at $0.96; OpenRouter Auto 52.20% at $0.82; DeepSeek V4.1 Flash 1017 alone scored 61.3% at $0.66.
   - Choosing "one model per benchmark" in hindsight beat routers by 10–13 points at equal cost.
   - Routers lowered reasoning effort and did not spend more on hard tasks.
   - This directly supports a static, per-subtask context file.
2. **Per-token price is a poor cost proxy.**
   - On SWE-bench Multimodal, Opus 5.5 ($4/$20) cost $4.92/test and Sonnet 5.5 ($2/$10) cost $4.53/test, because Sonnet used 6.21B input tokens to Opus's 3.18B.
   - On Terminal-Bench 4.0, Sonnet 5.5 costs *more* per test than Opus 5.5 ($16.51 vs $13.20).
   - GPT-6.1 Sol used 242M input tokens on SWE-MM, against 6.21B for Sonnet 5.5.
3. **SWE-bench Verified is solved and leaky.**
   - Vals retired it at 97%.
   - SWE-Bench Pro V2 public is at 99.4%, but Opus 5 resolves only 222/272 (81.6%) on the private split, a ~18-point gap. This suggests training-time exposure.
   - Do not route on public SWE-bench numbers.
4. **Network access inflates scores.** Vals found agents with internet access look up the upstream fix PR on SWE-bench Multimodal. Cutting network access cost Muse Spark models 21–35 points. Vendor-reported numbers rarely state network settings.
5. **Open weights are close to the frontier on agentic work.**
   - Kimi K3.1 Pro is #4 on the AA index (55) and #1 on AA's Terminal-Bench 4.0 (67.2%).
   - Its weights are announced but **not yet published** (AA, 10/23), so mark it API-only until they are.
6. **Prices have expiry dates.**
   - Gemini 4 Argon is $2/$10 only through **2026-11-30**, then $4/$20. Vals already uses $4/$20.
   - Gemini 3.8 Flash is $0.75/$3.75 through **2026-12-31**, then $1.50/$7.50.
   - Context-tiered pricing: Haiku 5.5 is 5x above 100K-token prompts; GPT-6.x costs more above 272K; Grok 4.7 doubles at ≥200K.
   - DeepSeek has peak/off-peak rates.
   - The schema has to model all of this, or picks go stale silently.
7. **Some top-ranked models can't be routed to.** Muse Wonder Full (AA 56; WebDev 1726) is not available on Meta's API. Only Muse Wonder ($4/$20) is.
8. **Grok 4.7 is weak on agentic coding at its price.** It scores 28.79% on Vals Terminal-Bench 4.0 at $18.01/test, against 55.05% at $1.72 for GPT-6.1 Sol. It is mid-pack elsewhere (Vibe Code Bench 86.17%, AutomationBench 65.6%).

## 6. Caveats

- **Harness:** Vals and AA use model-agnostic harnesses. Native scaffolds (Claude Code, Codex) often score higher (Scale observed this on SWE Atlas). Reflection's SWE-Bench Pro V2 study found harness choice barely moves strong models' scores but does move cost. Picks here assume a generic harness.
- **Reasoning effort:** scores differ a lot by effort. Example: Claude Opus 5.5 on the AA index scores 58 at max ($5.98/task) and 42 at low ($0.55/task). Rows must key on model + effort.
- **Vendor-adjacent benchmarks:**
  - ReviewBench is published by GitHub and scores its own Copilot.
  - SWE Atlas uses Claude Opus 4.5 as judge; ReviewBench uses Claude Sonnet 5.
  - SWE-Bench Pro V2 was co-developed with Reflection, which ships its own model.
  - SOB is run by Interfaze, which ranks its own model.
- **Partial credit:** AutomationBench gives partial credit. A pass/fail workflow may need a higher bar.
- **Preference votes:** LMArena WebDev measures preference for a first draft, not correctness.
- **Coverage holes:** newest models are missing from SWE-V (Vals), SWE Atlas, the SWE-Bench Pro V2 private split, IFBench and τ³. Where the best model is "Opus 5", Opus 5.5 is untested, not worse.
- **Price conflict resolved:** an earlier read of anthropic.com/pricing was ambiguous about Haiku 5.5. The docs page is clear: $0.10/$0.50 for prompts ≤100K and $0.50/$2.50 above. This matches Vals.

## 7. Biggest data gaps

1. Test writing: no current public board.
2. Structured output / JSON: no board covers current models.
3. Model-level code review: ReviewBench is agent-level and skewed by harness.
4. Codebase QA and private SWE-Bench Pro V2 have no results for Opus 5.5, Sonnet 5.5, GPT-6.1 Sol or Gemini 4 Argon.
5. Latency and time-to-first-token under agent loads. Vals reports run duration, not interactive latency.
6. Kimi K3.1 Pro has no Code Migration or SWE-MM results yet (launched 10/23).
7. Provider-page prices for Z.ai, Xiaomi, Alibaba, Mistral and MiniMax were not checked (Vals list prices used).
8. MiMo V2.6 Flash AA index value was not captured.

## 8. Sources (all accessed 2026-10-24)

- AA leaderboard: https://artificialanalysis.ai/leaderboards/models
- AA Kimi K3.1 Pro: https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks
- AA mirrors (BenchLeader):
  - https://www.benchleader.com/benchmarks/aa_terminalbench_40
  - https://www.benchleader.com/benchmarks/aa_automationbench
  - https://www.benchleader.com/benchmarks/aa_lcr
  - https://www.benchleader.com/benchmarks/aa_omniscience
  - https://www.benchleader.com/benchmarks/aa_ifbench
- Vals boards:
  - https://www.vals.ai/benchmarks/terminal-bench-4
  - https://www.vals.ai/benchmarks/swebench
  - https://www.vals.ai/benchmarks/code-migration
  - https://www.vals.ai/benchmarks/swebench-multimodal
  - https://www.vals.ai/benchmarks/vibe-code
  - https://www.vals.ai/benchmarks/vals_router_index
- Scale:
  - https://labs.scale.com/blog/swe-bench-pro-v2 (mirror: https://benchlm.ai/benchmarks/scale-swe-bench-pro-public-v2-full)
  - https://labs.scale.com/leaderboard/sweatlas-qna
  - https://labs.scale.com/leaderboard/swe_bench_pro (stale)
- LMArena: https://arena.ai/leaderboard/code/webdev ; https://www.benchleader.com/benchmarks/lmarena_webdev
- ReviewBench: https://benchlm.ai/benchmarks/reviewbench
- Other boards:
  - τ-bench: https://taubench.com/leaderboard
  - BFCL: https://gorilla.cs.berkeley.edu/leaderboard
  - Aider: https://aider.chat/docs/leaderboards/
  - SOB: https://interfaze.ai/leaderboards/structured-output-benchmark
- Pricing:
  - Anthropic: https://docs.anthropic.com/en/docs/about-claude/pricing
  - OpenAI: https://platform.openai.com/docs/pricing
  - Google: https://ai.google.dev/gemini-api/docs/pricing
  - xAI: https://docs.x.ai/docs/models
  - Meta: https://dev.meta.ai/docs/pricing-rate-limits
  - DeepSeek: https://api-docs.deepseek.com/quick_start/pricing
