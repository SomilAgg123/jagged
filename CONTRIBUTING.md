# Contributing to Jagged

Jagged is only as good as its evidence. The most useful contributions are new sources, corrections to existing scores and data points, and fresh dates on old ones.

## Propose a source

Open an issue or pull request with:
- **Name, URL and runner**: who runs and funds it.
- **Which subtask(s)** it measures (see the taxonomy in `docs/research.md` §3), and how directly.
- **Method facts:**
  - task count, repeats or CIs
  - harness, effort and turn caps
  - how it is graded (execution, LLM judge, votes)
  - whether the data is private or post-cutoff
  - whether cost per task is reported
- **Dates**: the newest result, and per-row run dates if shown.
- **Conflicts**: does the runner sell or promote any ranked model, harness, router or engine?

Better still, open a pull request that adds an entry to `SRC` in `scripts/build_sources.py`:
1. Fill in the nine 0–3 scores, disqualifiers and caps.
2. Write a one-paragraph justification.
3. Run `python3 scripts/build_sources.py` and commit the regenerated `data/sources.csv` and `docs/sources.md`.

## How sources are scored

Scoring follows `docs/SOURCE_RUBRIC.md`:
- **Tier rules:** the script computes the tier from the scores. Tier A needs a weighted score ≥70, independence, contamination and judging all ≥2, no disqualifier and no cap.
- **Disqualifiers:** self-reported, mirror/estimated, usage-as-quality, unverifiable, anecdote and saturated sources are tier C.
- **Caps:** commercial stake, preference signals, aggregate indexes, method-only sources and superseded versions are capped at B.
- **Per data point:** each one carries `evidence_date`, age and a freshness flag. Older evidence counts at full tier only for the exact model it tested, and only while that model is still sold at a verified price.
- **Never invent numbers.** If a value or date can't be read from a primary source, leave it blank or `unknown`. Mark mirror-only values "(mirror)".

Changes to the rubric itself need a written rationale, plus a list of the tiers and conclusions the change would move.

## Data points and picks

- Cite at most 3 data points per pick, each with its source, effective tier, value, evidence date, age, freshness and direct/family scope.
- A pick's status (supported / provisional / contested / insufficient) follows rubric §6 mechanically. Disagree by changing evidence, not by editing the status.
- Prices must come from the provider's own pricing page when possible. Note promos and their end dates.

## Neutrality and conflict-of-interest policy

- **No vendor gets special treatment.** Labs, model vendors, tool vendors and routers are scored by the same rubric. A vendor's own benchmark is capped or disqualified by the same rules as everyone else's.
- **Self-reported scores are never evidence for picks.** This covers model cards, launch posts and vendor-quoted numbers.
- **Disclose affiliations.** If you work for, are funded by, or hold equity in a lab, model vendor, inference provider, harness or router company, or a benchmark runner, say so in your PR or issue. Disclosed contributors are welcome. Undisclosed conflicts may lead to contributions being reverted.
- **Review:** changes that move a pick toward a contributor's affiliated product need review by a maintainer with no such affiliation.
- **Corrections are welcome from anyone**, including vendors pointing out errors in their own results. Back them with a public, primary source.

## Licensing

By contributing, you agree that:
- code contributions are licensed under Apache-2.0 (`LICENSE`);
- data and documentation contributions are licensed under CC BY 4.0 (`LICENSE-DATA`).
