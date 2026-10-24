# Discovery log

This log records how sources were found, what each search method produced, and what was rejected without being scored. Scores and tiers are in `data/sources.csv` and `docs/sources.md`, which `scripts/build_sources.py` generates. Every candidate below was opened at its primary page, except where the entry says otherwise.

## Pass 3: 2026-10-24 (America/Los_Angeles), research v0.4

**Goal:**
- Find tier-A evidence for the seven insufficient subtasks (codebase_qa, small_edit, frontend_visual, code_review, planning, long_context, test_writing).
- Find second independent runners for refactor_migration, structured_output and tool_orchestration (good enough).

**Result:** 22 sources added (4 A, 15 B, 3 C); no existing source changed tier. 87 sources in total (19 A, 44 B, 24 C).

### Yield by method

| # | Method | What was tried | Added | A | B | C | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Web search per subtask, phrased as a practitioner question ("which LLM should review code", "model benchmark test generation 2026") | about 25 queries across the 10 target subtasks | 7 | 1 | 4 | 2 | CodePanel (A), IronBee, MacroscopeBench, Qodo, Factory (B), VisualForge, screenshotbench (C). Best yield for code_review: review-tool vendors that rank only third-party models publish model-level benchmarks |
| 2 | Academic arXiv search (2026 papers by subtask keyword) | test generation, mutation testing, code migration, long-context code | 2 | 1 | 1 | 0 | TestSuiteBench (A), TestEvo-Bench (B, ind = 1). Considered: SWE-Mutation (critique paper), ATLAS, LongCodeBench, StructEval (not opened) |
| 3 | Government evaluators (NIST CAISI, UK AISI) | CAISI model evaluations | 1 | 0 | 1 | 0 | PortBench (B, older models). Considered: CAISI GLM-5.3 (cyber only). UK AISI: nothing coding-model-comparative found |
| 4 | Expert-data and eval vendors running others' benchmarks (Mercor APEX, Scale Labs) | Mercor methodology, APEX index and every "Extended" (held-out) board; Scale SWE Atlas sub-boards | 11 | 2 | 9 | 0 | Mercor TB 2.1 Extended (A, 70), Mercor DeepSWE run (A), 7 Mercor B boards, Scale SWE Atlas TW and Refactoring (B). Highest count, but mostly B: there is no cost data, and many boards are LLM-judged |
| 5 | Harness and agent vendors (OpenHands, Factory, Droid) | OpenHands Index, Factory docs | (Factory is counted under 1) | 0 | 0 | 0 | OpenHands Index seen in search only, not opened |
| 6 | Re-checking previously unreadable sources | Martian repo via the GitHub API | 0 | 0 | 0 | 0 | Martian is now readable, so its D5 is lifted, but it stays C on score (48) |
| 7 | Citation graph (Semantic Scholar "cited by" for SWE-bench, TB, AA-LCR) | API queries | 0 | — | — | — | Failed: HTTP 429 rate limit |
| 8 | GitHub / Hugging Face dataset search | benchmark repos and datasets | 0 new | — | — | — | Confirmed IronBee's public artifacts and TestEvo's HF dataset (both counted above) |
| 9 | X (Twitter) search for benchmark announcements | about 6 queries (max 25 results each) | 0 | — | — | — | Leads only: AA MLCR-AA (medical long context), a 10-bug in-house review eval, a KrabArena rerun of Macroscope. None met the bar or had a primary to score |
| 10 | Mirrors and aggregators (BenchLeader, BenchLM, plushcap) | used to find leads | 0 | — | — | — | Leads only (D2) |
| 11 | Workshop and community boards | ArchBench (SA4S), Design2Code, Context Arena | 1 | 0 | 0 | 1 | ArchBench (C, D5/D1). Design2Code (2024 models, mirrors only) not added. Context Arena returns only a JS shell |

**Most productive this pass:**
- (4) runners that rerun others' benchmarks on held-out sets;
- (1) vendor-neutral review-tool companies;
- (2) arXiv papers that are fresh and execution-graded.

**Least productive:** X and the citation graph.

### Candidates opened but not added

| Candidate | Reason |
|---|---|
| sasid.ai structured-output blog | 12–24 cases (would be D6); URL not recorded |
| Design2Code | 2024-era models; only self-reported mirrors seen |
| CAISI GLM-5.3 assessment | Cyber only; maps to no subtask |
| Mercor non-coding boards (APEX-1, Harvey LAB, GDPval, BrowseComp, ProgramBench, SciCode) | Not a routing subtask, or rows rendered without model names |
| Context Arena | JS shell only, unreadable |
| AA MLCR-AA | Seen on X only; medical domain |

### Still open (try next pass)

- OpenHands Index: open the primary.
- ATLAS / LongCodeBench: non-LLM-judged long context.
- StructEval, PRDBench.
- Retry the Semantic Scholar citation graph once the rate limit clears.
- Ask CodePanel for repeat runs and frontier rows, and ask TestSuiteBench for per-app results and completion counts. Those would let its Opus 5.5 / GPT-6.1 Sol / Astra rows qualify under rubric v2.1 §2.1.
- Look for hackathon and course graders (for example university autograders) as fresh, private, execution-graded tasks.
- Look for enterprise case studies with A/B production data.

## Earlier passes

- **Pass 1 (v0.1):** seed list from known leaderboards (Vals, AA, LMArena, SWE-bench family, Scale, METR, Epoch), giving 60 sources.
- **Pass 2 (v0.2–v0.3):** rubric v2 rescoring, older-source re-check, and new boards (Toolathlon-Verified, AA τ², Multi-SWE-bench, SWE-bench Multilingual, Fiction.LiveBench), giving 65 sources. Methods were not logged per pass at the time.
