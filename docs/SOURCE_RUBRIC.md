# Source rubric (v2.1, 2026-10-24)

This rubric sets the bar a data source must clear before it can support a routing conclusion. Every source in `data/sources.csv` is scored against it. `scripts/build_sources.py` computes the tier from the scores and flags, so tiers are never hand-assigned.

Design principle: each conclusion rests on 1–3 high-quality data points. The rubric exists so that "high quality" is checkable rather than a judgment call.

**v2.1 change (2026-10-24):** D6 is made precise. "Single run" no longer disqualifies a whole source. A single-run result is used row by row and only for gaps larger than its noise (§2.1).

**v2 change (2026-10-24):** recency moved from the source to the claim.
- A methodologically strong older source can now be tier A, but only for claims about the models it actually tested.
- D3 (stale) is retired as a disqualifier.
- `rec` no longer counts toward the score or gates tier A.
- Every data point now carries its evidence date, age and freshness flag (§4).

All other criteria and disqualifiers are unchanged. v2 adds one cap, "superseded version" (§3): without the recency gate, a superseded board would otherwise have reached A.

## 1. Criteria (score each 0–3)

| Key | Criterion | Weight | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|
| `ind` | **Independence**: who runs and funds it; stake in any ranked model, harness, or router | 2 | Third party with no product in the ranking | Third party with a minor or indirect stake (e.g. sells inference, benchmark author ships a model but someone else runs it) | Runner sells a product that is ranked or is promoted by the result; or co-marketing with a lab | The model's own developer reports its own score |
| `cont` | **Contamination resistance**: private or held-out split, post-cutoff tasks, internet controls | 2 | Private or fresh post-cutoff tasks **and** controls for solution lookup | One of the two | Public, static dataset released before current models' cutoffs, with no lookup control | Known leaked or saturated |
| `meth` | **Method transparency**: harness, prompts, effort, turn caps, versions documented | 1 | Fully documented, with a changelog | Mostly documented | Partly documented | Undocumented |
| `repro` | **Reproducibility**: can an outsider re-run or re-score it | 1 | Code + data + harness public | Code or harness public; data partly private | Results only | Nothing |
| `stats` | **Statistical rigor**: task count, repeats, CIs or SEs | 1.5 | ≥100 tasks with repeats or CIs | ≥50 tasks, or CIs on fewer | 30–50 tasks, single run, no CIs | <30 tasks or anecdote |
| `rec` | **Coverage of current models** (informational only in v2; **not scored, not a gate**) | 0 | Updated in the last 30 days, covers current frontier and cheap tiers | Updated in the last 90 days, covers most current models | Older, or missing most current frontier models | Unmaintained, or newest model >6 months old |
| `rel` | **Task relevance** to a routing subtask | 1.5 | Directly measures the subtask | Close proxy | Indirect | Unrelated |
| `cost` | **Cost reporting** | 1 | Measured cost per task (and tokens) | Cost per task estimated from list prices | Token price only | None |
| `judge` | **Judging method** | 1.5 | Execution-based (tests, end-state checks) | Execution plus LLM-judged parts, or LLM judge with disclosed conflicts and multiple votes | LLM judge only, or human preference votes / satisfaction signals | Undisclosed, or the judge's vendor ranks top with no disclosure |

**Weighted score** = Σ(weight × score over the 8 scored criteria) ÷ 34.5 × 100. The maximum is 100. (v1 included `rec` with weight 1.5 and divided by 39.)

## 2. Hard disqualifiers (automatic tier C)

| Code | Disqualifier |
|---|---|
| D1 | **Self-reported** by the model's developer: model cards, launch posts, vendor-quoted scores. |
| D2 | **Not a measurement**: estimated, imputed or calibrated scores, or a mirror/aggregator with no primary data. Use the primary instead. |
| ~~D3~~ | **Retired in v2.** Age is handled per data point (§4). Abandoned or unreadable boards are still excluded, through D5 and D7. |
| D4 | **Wrong construct**: usage or popularity data offered as quality. |
| D5 | **Unverifiable**: no method or results could be read on the check date. This includes an abandoned board whose rows cannot be tied to a model version and an evaluation date. A board that is frozen but readable and dated is **not** D5. |
| D6 | **Anecdote**: fewer than 30 tasks; or a single run per model in which no row passes the single-run test (§2.1). (Before v2.1: "fewer than 30 tasks, or a single run per model with no repeat".) |
| D7 | **Saturated**: the top cluster sits within noise of the ceiling, so the board cannot separate the models it tests. |

## 2.1 Single-run results (new in v2.1)

A result is **single-run** when each model was run once on the task set: no repeats, no seeds, and no CI from repeated runs. Such a result is used row by row and claim by claim. Everything below has to hold.

1. **Size.** At least 30 tasks. Below that, the source is D6.
2. **The row qualifies.** A row can be the subject of a claim (the model said to be best, good enough, or better than another) only if all of these hold:
   - **Setup per row:** the harness, the reasoning effort and the model snapshot are documented for that row. A config file in the source's public repo counts.
   - **Every task counted:** one of these holds:
     - failed or timed-out tasks score 0;
     - the source reports how many tasks the row completed;
     - all rows are compared on the common subset that every row completed;
     - the source analyses this row over the full task set, which shows it covered every task.

     A score that silently averages only the tasks a row finished does not count. Dropped tasks are usually the hard ones, so the omission flatters the row.
   - **No row-level red flag:** for example, validity far below the other rows (a sign of harness trouble), or an ambiguous snapshot.
3. **Noise test.** A claim that one row beats another needs a gap larger than the 95% noise interval for that gap. Use the first of these that is available:
   1. **Paired bootstrap over tasks**, when per-task results are public. Jagged computes it: 10,000 resamples of tasks, 2.5–97.5 percentile of the gap.
   2. **The source's own CI over tasks.**
   3. **Worst-case bound:** **139/√n points**, for a 0–100 score that is the mean of per-task scores in [0, 1] over n independent tasks. Each per-task score has variance ≤ 0.25, so the gap between two independent rows has SD ≤ √(0.5/n) and 1.96 × √(0.5/n) × 100 ≈ 139/√n. Examples: n = 100 → 13.9; n = 165 → 10.8; n = 500 → 6.2.

   The bound covers both task sampling and run-to-run luck, so it needs no repeat run. It is conservative. A published per-task file almost always gives a tighter interval.
4. **How the claims read.**
   - Rows whose gap is inside the interval are a **tie**. Their order is not evidence.
   - **Best:** the model is in the leader's tie cluster. This replaces the 3-pt rule in §6 for single-run sources.
   - **Good enough:** the usual 10-pt bar applies to a qualifying row.
   - **Step-down and "clearly worse":** the gap must pass the noise test.
   - A row that does not qualify can still be the **lower** side of a "clearly better" claim. Its likely bias is upward, so the claim is conservative. It cannot be the subject of a claim.
5. **Scoring is unchanged.** A single-run source still gets at most `stats` = 2. This section only decides which of its rows and gaps a conclusion may cite. Note in the source's entry which rows qualify.

## 3. Caps (at most tier B)

- **Commercial stake.** The runner sells a model, harness, router or engine that appears in or benefits from the ranking. Examples: Cursor/Composer, Kilo/kilo-auto, GitHub/Copilot, Cognition/SWE-2, SuperAGI/SuperScout, LangChain/routing middleware, LogicStar/L*Agent on SWT-bench, guidance-ai/Guidance on JSONSchemaBench.
- **Preference or satisfaction signal** rather than correctness, such as Arena votes and session sentiment.
- **Aggregate index** that is not task-specific, such as the AA Intelligence Index or Epoch ECI.
- **Method source**: evidence about how to route, not which model to pick, measured on older models. It can support a design decision, never a model pick.
- **Superseded version** (new in v2): the same runner has published a corrected version of the same benchmark, as Vals did when Code Migration v1.1 replaced v1. Use the current version.

## 4. Per-claim recency (new in v2)

The source tier says how far a source's measurements can be trusted. These rules say which claims a given measurement may support, and at what tier.

**R1. Every data point is dated.**
- `evidence_date`: the date the result was published or run on the source. If only a bound is known, record the bound and its basis.
  - Use `≥ YYYY-MM-DD (model release)` when a row can be no older than the model's release.
  - Use `YYYY-MM-DD (board update)` when only the board's last-update date is shown.
- `age_days` = date_checked − evidence_date. When the date is a lower bound, age_days is an upper bound.
- `freshness`:
  - **fresh**: ≤ 90 days
  - **aging**: 91–180 days
  - **stale**: > 180 days
- If neither a date nor a bound can be found, `freshness` = **unknown**, which is treated as stale.
- The flag is shown on every data point. A pick that cites any aging or stale point is marked **⏳ older evidence**.

**R2. Direct claims keep the source tier at any age.** A data point about model X supports claims about X, the same model ID, snapshot and effort setting, at its source's tier. It does so only if X is still offered by its provider at a list price verified on the provider's pricing page on date_checked.
- If X is retired or unavailable, or the current price cannot be verified, the point drops to **B**.
- The source's $/task is always labeled "cost at evidence date". If the list price has changed since then, that $/task is not used for cost ranking. Recompute it, or leave it blank.

**R3. No inheritance by name.** A data point about X supports claims about a different model Y at **B at most**, whether Y is a successor, a sibling, another snapshot or another effort setting. Examples: Opus 5 → Opus 5.5; GPT-5.6 Sol → GPT-6.1 Sol; GLM-5.2 → GLM-5.3. The same applies to family or relative claims, such as "the Opus line leads issue resolution" or "X beats Y, so X′ beats Y′". A source therefore never supports, on its own, a pick of a newer model it did not test.

**R4. "Best" needs frontier coverage.** A data point supports "X is best for subtask S" as A only if the source tested the current top tier for S. The current top tier is the leaders on a fresh tier-A source for S. Otherwise the point says only "best among models tested as of evidence_date". For a "best" claim that counts as **B**.

**R5. Older good-enough claims need an anchor.** Aging and stale points can support "X is good enough for S" only if they are anchored. Anchored means the older source shares at least one tested model with a fresh tier-A source for S, so the gap between the older source's leader and today's frontier can be estimated.
- Unanchored good-enough claims are labeled **unanchored**, and the pick is capped at **provisional**.
- Without an anchor, "within 10 points of the leader" only means "within 10 points of the best model it tested".

**R6. Disagreement on a shared model is a contradiction.** Two tier-A sources may test the same model on the same subtask and place it on opposite sides of the bar, for example one within 3 points of the leader and the other more than 10 points behind. That is a contradiction under §6, whatever the ages of the two points.

**R7. Frozen ≠ excluded.** "No longer actively updated" is not a disqualifier on its own. A frozen board stays at its tier for the models it tested, with every point flagged by age. Only D5 (unreadable, or rows not attributable) or D7 (saturated) remove it.

## 5. Tier rules (applied in this order)

1. Any disqualifier → **C**.
2. **A** requires all of:
   - weighted score ≥ 70;
   - `ind` ≥ 2, `cont` ≥ 2, `judge` ≥ 2 (v1 also required `rec` ≥ 2; removed in v2);
   - no cap.
3. **B**: weighted score ≥ 50, or a source that would be A except for a cap.
4. Otherwise **C**.

A source's tier applies to the role it plays:
- `pick`: which model is good at a subtask.
- `method`: how routing should work.
- `price`: list prices.

Provider pricing pages are primary sources for `price` only. The per-claim rules in §4 can lower a data point below its source tier, but never raise it.

## 6. Rules for supporting a conclusion

Each conclusion cites at most 3 data points. Each point is tagged with its effective tier after §4, its evidence_date, age_days and freshness.

| Status | Requirement |
|---|---|
| **Supported** | Either ≥2 tier-A data points from **different runners** that agree, or 1 tier-A point plus ≥1 tier-B point from a different runner that agrees in direction. No tier-A contradiction. |
| **Provisional** | Exactly 1 tier-A runner, no corroboration, no contradiction; or any pick capped by R5 (unanchored). Ship it, but flag it for re-check. |
| **Contested** | Tier-A support exists, but another A or B source contradicts it (including R6). Ship with a caveat, or fall back to the next pick. |
| **Insufficient evidence** | No tier-A data point. Tier-B points may be listed as "B-only consensus", but they do not make a pick. |

Definitions:
- **Agree:** for a "best" pick, the model is in the source's top tier (within the source's CI, or within 3 points of the leader if no CI is given; for a single-run source, in the leader's tie cluster under §2.1). For a "good enough" pick, the model is within 10 points of the leader and cheaper per task.
- **Different runners:** two Artificial Analysis boards count as one runner. So do two Vals boards.
- **⏳ older evidence:** the pick cites at least one aging or stale point, or relies on an R3 (family) B point. Re-check these first.

## 7. Re-check triggers

Re-score a source, or re-date its points, when any of these happens:
- it publishes a new version, such as Code Migration v1 → v1.1, TB 2.x → 4.0, or Toolathlon → Toolathlon-Verified;
- 90 days pass, so that fresh points become aging;
- a disqualifier condition changes (a board becomes unreadable or saturated, or a runner launches its own model);
- a tested model is retired or re-priced on its provider's page (R2);
- a fresh tier-A source tests the current frontier on a subtask, which can anchor older good-enough claims (R5).
