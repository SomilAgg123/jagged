from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

"""Score every source against SOURCE_RUBRIC.md and write sources.csv + sources.md.
Tiers are computed, never hand-set."""
import csv
D = "2026-10-24"
# rubric v2.1 (2026-10-24): D6 single-run test (§2.1). v2: recency no longer counts toward the source score or gates tier A.
# `rec` is still recorded per source (coverage of current models, informational) and recency
# is applied per data point (evidence_date, age_days, freshness flag) in research.md / schema.
W = dict(ind=2, cont=2, meth=1, repro=1, stats=1.5, rec=1.5, rel=1.5, cost=1, judge=1.5)
K = list(W)
SCORED = [k for k in K if k != "rec"]          # rec excluded from the score (v2)
DEN = sum(W[k]*3 for k in SCORED)               # max weighted points = 34.5
def tier(s, disq, caps):
    disq = [d for d in disq if not d.startswith("D3")]   # D3 retired in v2
    pct = round(sum(W[k]*s[k] for k in SCORED) / DEN * 100)
    if disq: return pct, "C"
    a_ok = pct >= 70 and s["ind"] >= 2 and s["cont"] >= 2 and s["judge"] >= 2
    if a_ok and not caps: return pct, "A"
    if pct >= 50 or a_ok: return pct, "B"
    return pct, "C"

# tiers from the previous pass (research v0.3, data/sources.csv as committed in c654c1b, 65 sources), used only to report moves
PREV = {
"Vals Terminal-Bench 4.0": "A",
"Vals Code Migration v1.1": "A",
"Vals Code Migration v1 (superseded)": "B",
"Vals Vibe Code Bench v1.1": "A",
"Vals SWE-bench Multimodal": "B",
"Vals SWE-bench Verified": "C",
"Vals Router Index": "A",
"AA Terminal-Bench 4.0 (model-level)": "A",
"AA Coding Agent Index v2.0 (harness × model)": "A",
"AA FrontierCode 1.1": "A",
"AA SWE-Atlas-QnA-AA": "B",
"AA AutomationBench-AA": "A",
"AA-LCR": "B",
"AA-Omniscience": "B",
"AA Intelligence Index": "B",
"AA IFBench": "A",
"SWE-rebench": "A",
"Epoch AI SWE-bench Verified": "C",
"Epoch Capabilities Index (ECI)": "B",
"METR Time Horizons 1.1": "A",
"METR Opus 5.5 pre-deployment report": "C",
"LiveBench 2.0": "B",
"SWE-bench-Live": "C",
"Agent-as-a-Router / CodeRouterBench (arXiv 2606.22902)": "B",
"Scrouting / SuperScout (arXiv 2608.04804)": "B",
"FeatureBench (arXiv 2602.10975)": "A",
"SWE-CI (arXiv 2603.03823)": "A",
"SWT-bench": "B",
"TestGenEval": "B",
"JSONSchemaBench": "B",
"MCP-Universe": "B",
"Scale SWE-Bench Pro V2 (private split)": "B",
"Scale SWE-Bench Pro V2 (public split)": "C",
"Scale SWE-Bench Pro (original public)": "B",
"Scale SWE Atlas Codebase QnA": "B",
"Scale MCP Atlas": "B",
"LMArena WebDev": "B",
"Arena Agent leaderboard (code)": "B",
"CursorBench 4.0": "B",
"KiloBench": "B",
"Cline blog (Nemotron 3.5 on TB 2.1)": "C",
"Terminal-Bench official board (tbench.ai)": "C",
"Cognition FrontierCode leaderboard": "B",
"GitHub ReviewBench": "B",
"CodeReviewBench (Kodus)": "C",
"Martian Code Review Bench": "C",
"Zapier AutomationBench (strict, own board)": "B",
"Sierra τ³-bench": "B",
"Berkeley BFCL V4": "A",
"Aider Polyglot": "B",
"LiveCodeBench": "C",
"Interfaze Structured Output Benchmark": "C",
"OpenRouter rankings": "C",
"LangChain Open SWE router A/B": "B",
"CodeRouter phase-aware routing blog": "C",
"The New Stack: DeepSeek V4.1 Flash 1017 vs Haiku 5.5": "C",
"Morph 'best model for coding'": "C",
"Developers Digest / AIHubMix subagent posts": "C",
"Toolathlon-Verified": "B",
"Fiction.LiveBench (via Epoch)": "C",
"AA τ²-Bench Telecom": "C",
"SWE-bench Multilingual (model-card board)": "C",
"Multi-SWE-bench": "C",
"BenchLeader / BenchLM / LLMBoard / benchgap mirrors": "C",
"Provider pricing docs (Anthropic, OpenAI, Google, xAI, Meta, DeepSeek)": "A"
}

def S(ind,cont,meth,repro,stats,rec,rel,cost,judge):
    return dict(zip(K,(ind,cont,meth,repro,stats,rec,rel,cost,judge)))

# (name, url, owner, type, role, subtasks, scores, disqualifiers, caps, why)
SRC = [
# ---------------- independent eval orgs: Vals ----------------
("Vals Terminal-Bench 4.0","https://www.vals.ai/benchmarks/terminal-bench-4","Vals AI","independent eval org","pick","terminal_agentic_loop",
 S(3,2,3,1,2,3,3,3,3),[],[],
 "Runs every model itself on a bash-only mini-swe-agent harness, avg@3 over 66 tasks, measured $/test, updated 10/24. TB4 tasks are public, so contamination is controlled by recency plus a canary, not privacy (2)."),
("Vals Code Migration v1.1","https://www.vals.ai/benchmarks/code-migration-v1-1","Vals AI","independent eval org","pick","refactor_migration",
 S(3,3,3,1,2,3,3,3,3),[],[],
 "Offline sandbox, hidden behavior-test suites (100–400 tests each), anti-cheat checker, 120 CLI migrations plus 10 COBOL repos, $/test. Pi harness. Replaced v1 on 10/20; not comparable to v1."),
("Vals Code Migration v1 (superseded)","https://www.vals.ai/benchmarks/code-migration","Vals AI","independent eval org","pick","refactor_migration",
 S(3,3,3,1,2,1,3,3,3),[],["superseded version"],
 "Same tasks as v1.1, but superseded by it (mini-SWE-agent, older test suites). Kept only as history. Not a separate runner from v1.1. v2: recency no longer blocks A, so the new 'superseded version' cap keeps it at B (a corrected version from the same runner exists)."),
("Vals Vibe Code Bench v1.1","https://www.vals.ai/benchmarks/vibe-code","Vals AI","independent eval org","pick","greenfield_app",
 S(3,2,2,1,2,3,3,3,2),[],[],
 "Builds full apps from specs on OpenHands, graded by automated functional checks of the running app, $/test, updated 10/24. The functional checks use an agent, so judge = 2."),
("Vals SWE-bench Multimodal","https://www.vals.ai/benchmarks/swebench-multimodal","Vals AI","independent eval org","pick","frontend_visual",
 S(3,1,3,2,2,3,3,3,3),[],[],
 "Execution-graded, with network access removed (Vals showed lookup inflated some scores by 21–35 pts). But the public 2024 dataset predates current training cutoffs, so memorization is not controlled (cont = 1). That blocks tier A."),
("Vals SWE-bench Verified","https://www.vals.ai/benchmarks/swebench","Vals AI","independent eval org","pick","small_edit",
 S(3,0,3,2,3,1,2,3,3),["D7 saturated (top 97%; retired 9/1/2026)","D3 no new models"],[],
 "Retired by Vals at 97%. Epoch labels SWE-bench Verified 'Flawed' (5–10% bad tasks, contamination)."),
("Vals Router Index","https://www.vals.ai/benchmarks/vals_router_index","Vals AI","independent eval org","method","routing design (all)",
 S(3,3,3,1,3,3,2,3,2),[],[],
 "Five shipped routers and every single model run through the same agents on about 1,250 tasks (6 of 8 benchmarks private, ZDR), with ±1.2 margins and hindsight baselines. Mixed domains (finance, law, tax, coding), so relevance = 2."),
# ---------------- Artificial Analysis ----------------
("AA Terminal-Bench 4.0 (model-level)","https://artificialanalysis.ai/evaluations/terminalbench-4-0","Artificial Analysis","independent eval org","pick","terminal_agentic_loop",
 S(3,2,3,2,2,3,3,3,3),[],[],
 "AA's own harness, 3 attempts, reward-hacking judge, $/task. Independent of Vals: a second runner on the same task set. Per-model values were read on the BenchLeader mirror and spot-checked against AA."),
("AA Coding Agent Index v2.0 (harness × model)","https://artificialanalysis.ai/agents/coding-agents","Artificial Analysis","independent eval org","pick","terminal_agentic_loop; issue_resolution; codebase_qa_search",
 S(3,2,3,1,3,3,3,3,2),[],[],
 "Scores agent+model pairs (Claude Code, Codex) on FrontierCode 1.1, TB4 and SWE-Atlas-QnA-AA. 3 attempts, 290 tasks, pooled $/task, time and tokens, reward-hack and refusal accounting. The composite is A, but its SWE-Atlas component is scored separately (B) below."),
("AA FrontierCode 1.1","https://artificialanalysis.ai/evaluations/frontiercode","Artificial Analysis (benchmark by Cognition)","independent eval org","pick","issue_resolution",
 S(2,3,3,1,2,3,3,3,2),[],[],
 "Private 100-task set by maintainers, graded on mergeability, 3 attempts, 250-turn cap, solution-lookup scanner, $/task. AA runs it independently, but the benchmark author (Cognition) ships SWE-2 (ind = 2). Some checks use an LLM judge (GPT-6 Luna, disclosed), so judge = 2. Top 3 read on the AA page; the rest via the BenchLeader mirror."),
("AA SWE-Atlas-QnA-AA","https://artificialanalysis.ai/methodology/coding-agents-benchmarking","Artificial Analysis (tasks by Scale AI)","independent eval org","pick","codebase_qa_search",
 S(3,1,3,3,3,3,3,2,1),[],[],
 "124 repository Q&A tasks graded only by an LLM judge (GPT-6 Luna, 5 votes per criterion; OpenAI models are ranked). The dataset is public on HF. LLM-only judging and a public set block tier A."),
("AA AutomationBench-AA","https://artificialanalysis.ai/evaluations/automationbench-aa/","Artificial Analysis (benchmark by Zapier)","independent eval org","pick","tool_orchestration",
 S(3,3,2,1,3,3,2,3,3),[],[],
 "657 tasks, private held-out set, programmatic end-state grading, guardrail violations zero a task, $/task. Partial credit inside a task; a SaaS/REST workflow is a close proxy (rel = 2) for coding-agent tool use."),
("AA-LCR","https://artificialanalysis.ai/evaluations/artificial-analysis-long-context-reasoning","Artificial Analysis","independent eval org","pick","long_context_summarize",
 S(3,2,2,2,2,3,2,3,1),[],[],
 "About 100 long-document reasoning questions with LLM equality judging. The board is compressed (top 15 within ~6 pts). Read via the BenchLeader mirror. LLM judge = 1 blocks tier A."),
("AA-Omniscience","https://artificialanalysis.ai/evaluations/omniscience","Artificial Analysis","independent eval org","pick","planning_architecture; long_context_summarize",
 S(3,2,2,1,3,3,1,2,1),[],[],
 "Knowledge and hallucination index, not coding-specific. Indirect relevance."),
("AA Intelligence Index","https://artificialanalysis.ai/leaderboards/models","Artificial Analysis","independent eval org","pick","planning_architecture",
 S(3,2,3,1,3,3,1,3,2),[],["aggregate index"],
 "Composite across 10 evals with $/index-task by effort. Useful for effort and cost curves; not task-specific, so capped at B."),
("AA IFBench","https://artificialanalysis.ai/evaluations/ifbench","Artificial Analysis","independent eval org","pick","structured_output",
 S(3,2,2,2,2,1,2,2,3),[],[],
 "58 verifiable out-of-domain output constraints, programmatic checks, run independently by AA. The board is maintained (BenchLeader shows a newest result on 2026-10-23), but no Opus 5.5 / GPT-6.x / Gemini 4 row was found, so it cannot support a 'best' claim. AA's own page confirms only the leader (Grok 4.3 medium, 83.3%); the other values were seen via a mirror, and the mirror disagreed with AA on one row (Grok 4.20: 81.2% mirror vs 82.9% AA), so mirror-only values are not used. Proxy for structured output (format constraints, not JSON-schema adherence), rel = 2. v1: C (D3) → v2: A."),
# ---------------- other independent / academic ----------------
("SWE-rebench","https://swe-rebench.com/","Nebius","independent eval org","pick","issue_resolution",
 S(2,3,3,3,3,1,3,3,3),[],[],
 "Fresh monthly GitHub tasks, a decontamination window, ±SE, pass@5, $/problem, public HF data and Docker images, NeurIPS D&B paper. Best methodology in the set. Correction to v1: the changelog's last entry is 2026-07-01, but the table includes Claude Opus 5 (released 2026-07-24), so the newest rows are at most ~92 days old. No Opus 5.5 / GPT-6.x / Gemini 4 runs. Nebius sells open-model inference (ind = 2). v1: B (rec gate) → v2: A for claims about the models it tested."),
("Epoch AI SWE-bench Verified","https://epoch.ai/benchmarks/swe-bench-verified","Epoch AI","independent eval org","pick","small_edit",
 S(3,0,3,3,2,1,2,1,3),["D7 saturated / Epoch labels it 'Flawed'","D3 newest result 2026-06-16"],[],
 "Constant Inspect scaffold, 484 samples. Epoch itself flags 5–10% bad tasks and contamination."),
("Epoch Capabilities Index (ECI)","https://epoch.ai/models/search","Epoch AI","independent eval org","pick","planning_architecture",
 S(3,2,3,2,2,3,1,0,2),[],["aggregate index"],
 "Aggregate capability score with statistical linking. Not coding-specific; no cost."),
("METR Time Horizons 1.1","https://metr.org/time-horizons/","METR","independent eval org","pick","terminal_agentic_loop",
 S(3,2,3,2,3,0,2,0,3),[],[],
 "Strong method (expert-timed tasks, 6 runs per task, reward-hack review). Frozen: 'no longer actively updated' (2026-09-08); the last addition was 2026-05-08 (Mythos Preview); the newest public models are GPT-5.4 and Gemini 3.1 Pro. Readable and dated, so v2 does not exclude it, but it tests no model in the current routing set. v1: C (D3) → v2: A (no picks use it)."),
("METR Opus 5.5 pre-deployment report","https://metr.org/","METR","independent eval org","pick","terminal_agentic_loop",
 S(1,2,2,0,0,3,2,0,1),["D1 lab-reviewed and lab-edited text; qualitative only"],[],
 "Anthropic reviewed and edited the text. No numbers usable for routing."),
("LiveBench 2.0","https://livebench.ai/","Abacus AI","independent eval org","pick","terminal_agentic_loop; greenfield_app; planning_architecture",
 S(2,2,1,1,1,3,2,3,2),[],[],
 "Release 2026-10-14; 7 suites with cost per successful task. Abacus sells an agent product built on these results (ind = 2). The 2.0 grading details and task counts were not reviewed, and no CIs are shown. Coding suite near ceiling (top 5 within 2.3 pts)."),
("SWE-bench-Live","https://swe-bench-live.github.io/","Microsoft","academic","pick","issue_resolution",
 S(2,3,2,3,2,0,3,0,3),["D5 leaderboard table rendered empty on fetch (2026-10-24); no rows readable"],[],
 "Live multi-language splits. Results are PR submissions; maintainers add a 'Verified' tag after checking trajectories (since Feb 2026). It stays C under v2, now for D5 (unreadable) rather than D3."),
("Agent-as-a-Router / CodeRouterBench (arXiv 2606.22902)","https://arxiv.org/abs/2606.22902","NUS / Alibaba DAMO","academic","method","routing design",
 S(1,1,3,3,3,1,3,2,1),[],["method source"],
 "About 10K tasks, 8 older models. Static per-dimension lookup reaches ~83% of oracle and beats always-Opus. Alibaba's Qwen is in the pool (ind = 1). Three dimensions use LLM-judge proxies."),
("Scrouting / SuperScout (arXiv 2608.04804)","https://arxiv.org/abs/2608.04804","SuperAGI","academic","method","routing design; issue_resolution",
 S(1,3,3,3,3,1,3,3,3),[],["commercial stake","method source"],
 "Replay audit of public per-task results: solve sets are nested (containment 0.77–0.94), no learned router beats the strongest single model (p 0.24–0.90), and rank order fails on fresh tasks. The authors sell SuperScout."),
("FeatureBench (arXiv 2602.10975)","https://arxiv.org/abs/2602.10975","academic","academic","pick","greenfield_app",
 S(3,2,2,2,2,0,3,0,3),[],[],
 "Feature-development benchmark (paper). The newest model reported is Opus 4.5, which is still sold ($5/$25), but none of the current routing set. v1: C (D3) → v2: A for its tested models; no current pick uses it."),
("SWE-CI (arXiv 2603.03823)","https://arxiv.org/abs/2603.03823","academic","academic","pick","refactor_migration; issue_resolution",
 S(3,2,2,2,2,0,3,0,3),[],[],
 "CI-driven maintenance benchmark (paper). The newest models are Opus 4.6 and GPT-5.2, both still sold. v1: C (D3) → v2: A for its tested models; no current pick uses it."),
("SWT-bench","https://swtbench.com/","ETH Zurich / LogicStar","academic","pick","test_writing",
 S(2,1,2,3,2,0,3,0,3),[],["commercial stake"],
 "Execution-based issue-reproduction tests (433 Verified tasks); the maintainers re-execute submitted predictions. Newest entry 2026-07-08 (PatchTwin+Guard GPT-5, 82.9% Verified). It ranks agents, not bare models, and LogicStar co-runs it while ranking its own L*Agent. The public SWE-bench issues give cont = 1. v1: C (D3) → v2: B."),
("TestGenEval","https://testgeneval.github.io/leaderboard.html","Meta FAIR (academic)","academic","pick","test_writing",
 S(2,1,2,3,3,0,3,0,3),[],[],"GPT-4o-era results on public repositories (cont = 1). v1: C (D3) → v2: B. Not re-opened this pass."),
("JSONSchemaBench","https://github.com/guidance-ai/jsonschemabench","guidance-ai (academic)","academic","pick","structured_output",
 S(2,2,3,3,3,0,3,0,3),[],["commercial stake"],"Good harness, but the newest results are GPT-4o / Qwen2.5. Correction: it is hosted by guidance-ai, and Guidance is one of the ranked constrained-decoding engines, so it gets the commercial-stake cap. v1: C (D3) → v2: B. Not re-opened this pass."),
("MCP-Universe","https://mcp-universe.github.io/","Salesforce AI Research","academic","pick","tool_orchestration",
 S(2,2,2,3,2,0,2,0,3),[],[],"The top entry is GPT-5-High. v1: C (D3) → v2: B. Not re-opened this pass."),
# ---------------- Scale / LMArena / Arena ----------------
("Scale SWE-Bench Pro V2 (private split)","https://labs.scale.com/blog/swe-bench-pro-v2","Scale AI (co-developed with Reflection)","independent eval org","pick","issue_resolution",
 S(1,3,2,1,2,1,3,0,3),[],[],
 "The private split exposes an ~18-pt public/private gap. Only 5 models; no Opus 5.5 / GPT-6.1. Co-developed with Reflection (ranks Beam), and Meta holds a large stake in Scale (ind = 1). Read via the BenchLM mirror plus the Scale blog."),
("Scale SWE-Bench Pro V2 (public split)","https://labs.scale.com/blog/swe-bench-pro-v2","Scale AI","independent eval org","pick","small_edit; issue_resolution",
 S(1,0,2,2,3,3,3,0,3),["D7 near ceiling (99.40%) with a large private gap → contaminated"],[],""),
("Scale SWE-Bench Pro (original public)","https://labs.scale.com/leaderboard/swe_bench_pro","Scale AI","independent eval org","pick","issue_resolution",
 S(1,1,2,2,3,0,3,0,3),[],[],"Public split; the top entry is Muse Spark 1.1. ind = 1 (Scale/Meta). v1: C (D3) → v2: B."),
("Scale SWE Atlas Codebase QnA","https://labs.scale.com/leaderboard/sweatlas-qna","Scale AI","independent eval org","pick","codebase_qa_search",
 S(1,2,2,2,2,1,3,0,1),[],[],
 "24 configs, none of Opus 5.5 / Sonnet 5.5 / GPT-6.1. LLM judge (Claude Opus 4.5) while Claude models lead. AA's adjusted rerun is scored separately."),
("Scale MCP Atlas","https://labs.scale.com/leaderboard/mcp_atlas","Scale AI","independent eval org","pick","tool_orchestration",
 S(1,2,3,3,3,1,2,0,1),[],[],
 "1,000 real-MCP tasks (500 private), ±CIs, open harness. Claim-level LLM judge (Gemini 2.5 Pro). The leader is Meta's Muse Spark 1.1 and Meta has a large stake in Scale (ind = 1). No Opus 5.5 / GPT-6 / Gemini 4 rows."),
("LMArena WebDev","https://arena.ai/leaderboard/code/webdev","LMArena","community / preference","pick","greenfield_app; frontend_visual",
 S(2,3,2,1,3,3,2,0,1),[],["preference signal"],
 "About 924K pairwise human votes with CIs; fresh prompts. Measures preference for a first draft, not correctness. Arena has faced criticism for private pre-release testing with large labs (ind = 2)."),
("Arena Agent leaderboard (code)","https://arena.ai/leaderboard/agent/code","LMArena","community / preference","pick","terminal_agentic_loop",
 S(2,3,1,0,3,3,3,3,1),[],["preference signal"],
 "About 846K real agent sessions, 55 models, CIs, P50 cost and time per task. Signals are behavioral (confirmed success, praise vs. complaint, steerability), not verified correctness. Task mix uncontrolled."),
# ---------------- harness / tool vendors ----------------
("CursorBench 4.0","https://cursor.com/cursorbench","Cursor (Anysphere)","harness vendor","pick","issue_resolution; greenfield_app",
 S(1,3,1,0,1,3,3,3,2),[],["commercial stake"],
 "Private tasks from real Cursor sessions; $/task, tokens and steps by effort for 78 configs. Cursor ranks its own Composer (27.7%, low). No CIs, unpublished grader. Best effort-vs-cost data outside AA."),
("KiloBench","https://kilo.ai/kilobench","Kilo Code","harness vendor","pick","terminal_agentic_loop",
 S(1,1,2,1,2,2,3,3,3),[],["commercial stake"],
 "Terminal-Bench 2.0 (89 tasks, superseded and public) on Kilo's harness, $/attempt. Kilo sells the kilo-auto router. Opus 5.5 / Sonnet 5.5 absent."),
("Cline blog (Nemotron 3.5 on TB 2.1)","https://cline.ghost.io/","Cline","harness vendor","pick","terminal_agentic_loop",
 S(1,1,1,0,1,2,3,0,3),["D1 co-marketing launch post; single-model claim"],[],""),
("Terminal-Bench official board (tbench.ai)","https://www.tbench.ai/news/terminal-bench-2-1","Laude Institute / Stanford","community / self-submitted","pick","terminal_agentic_loop",
 S(1,2,3,3,2,2,3,0,3),["D1 entries are submitted by agent/model builders themselves"],[],
 "The benchmark is excellent (it is what Vals and AA run), but the official board aggregates self-submitted agent results."),
("Cognition FrontierCode leaderboard","https://cognition.com/frontiercode","Cognition","harness vendor","pick","issue_resolution",
 S(0,3,3,0,2,3,3,2,2),[],["commercial stake"],
 "Benchmark author's own board, which ranks its own SWE-2 (ind = 0). Numbers did not render on the primary page and were seen only via a mirror, so it is not used as data. Use AA's independent run instead."),
("GitHub ReviewBench","https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/","GitHub (Microsoft)","harness vendor","pick","code_review",
 S(1,2,3,2,2,3,2,0,1),[],["commercial stake"],
 "3 repeated runs, human-validated findings, open methodology. Scores review agents (Copilot included), not bare models. LLM judge (Claude Sonnet 5)."),
("CodeReviewBench (Kodus)","https://www.codereviewbench.com/","Kodus","harness vendor","pick","code_review",
 S(1,1,2,2,1,2,3,2,1),["D6 30 PRs, one run per model; own page says ranks are noise. Re-checked under v2.1 §2.1: the worst-case noise on a gap at n = 30 is ~25 pts, and no per-PR results or completion counts were found, so no row passes"],[],""),
("Martian Code Review Bench","https://github.com/withmartian/code-review-benchmark","Martian","harness vendor","pick","code_review",
 S(1,1,2,3,2,2,2,0,1),[],[],
 "Re-checked 2026-10-24: the repo now lists files via the GitHub API, and IronBee re-ran its offline set (50 public PRs, 158 core goldens) from it, so D5 no longer applies. It is C on score (48): public PRs (cont = 1), LLM judge only, no cost, and the board ranks review tools, not bare models (rel = 2). Martian sells a router (ind = 1). Use IronBee's model-level rerun instead."),
("Zapier AutomationBench (strict, own board)","https://zapier.com/benchmarks/gemini-argon-4-report","Zapier","benchmark owner","pick","tool_orchestration",
 S(1,2,3,2,3,3,2,2,3),[],[],
 "657 tasks with strict end-state pass/fail. Zapier ships no model, but this Gemini 4 Argon 'release report' was a pre-release partner run (ind = 1). Claude costs use a different basis."),
("Sierra τ³-bench","https://taubench.com/leaderboard","Sierra","harness vendor","pick","tool_orchestration",
 S(1,2,3,3,2,1,2,0,3),[],[],
 "τ³-Banking customer-service tool-use simulation (user simulator gpt-5.2). It accepts PR submissions, and Sierra sells agents (ind = 1). Leader Qwen 3.8 Max 55.2%; Opus 5 48.7%. No Opus 5.5 / GPT-6 / Gemini 4. B under both v1 and v2."),
("Berkeley BFCL V4","https://gorilla.cs.berkeley.edu/leaderboard","UC Berkeley","academic","pick","tool_orchestration",
 S(3,2,3,3,3,0,2,1,3),[],[],
 "Readable via the board's own data_overall.csv (2026-10-24). Last updated 2026-04-12 (age 195 days). AST and executable function-call checks; open bfcl-eval package. Top rows: Claude Opus 4.5 (FC) 77.47%, Claude Sonnet 4.5 (FC) 73.24%, Gemini 3 Pro Preview (Prompt) 72.51%, GLM-4.6 (FC thinking) 72.38%. Total $ is estimated by Berkeley (cost = 1). It tests no model in the current routing set. v1: C (D3) → v2: A for its tested models."),
("Aider Polyglot","https://aider.chat/docs/leaderboards/","Aider","community","pick","small_edit",
 S(2,1,3,3,2,0,2,2,3),[],[],"Last updated 2025-11-20. Newest rows: gpt-5 (high) 88.0% ($29.08) and DeepSeek-V3.2-Exp Reasoner 74.2% ($1.30). 225 public Exercism tasks, one run (cont = 1). Under v2.1 §2.1, gaps need > 139/√225 = 9.2 pts unless per-task results are used (not checked). v1: C (D3) → v2: B."),
("LiveCodeBench","https://livecodebench.github.io/","academic","academic","pick","small_edit",
 S(3,3,3,3,3,0,1,0,3),["D5 leaderboard showed 'Loading leaderboard data…' on fetch (2026-10-24); no rows readable"],[],"Competitive programming (rel = 1). Vals archived it. It stays C under v2, now for D5 rather than D3."),
("Interfaze Structured Output Benchmark","https://interfaze.ai/leaderboards/structured-output-benchmark","Interfaze","model vendor","pick","structured_output",
 S(0,1,2,1,2,1,3,0,3),["D1 vendor ranks its own model","D3 top GPT-5.4"],[],""),
# ---------------- usage / practitioner ----------------
("OpenRouter rankings","https://openrouter.ai/rankings","OpenRouter","usage data","pick","(adoption only)",
 S(2,0,2,0,3,3,0,1,0),["D4 token usage, not quality (the page says so)"],[],
 "Revealed preference by price-sensitive traffic. Never used as quality evidence."),
("LangChain Open SWE router A/B","https://www.langchain.com/blog/how-to-build-a-model-router-in-the-harness","LangChain","practitioner","method","routing design",
 S(1,3,2,0,2,3,3,3,2),[],["commercial stake"],
 "Live A/B on 973 threads: merged-PR rate 29.2% vs 27.3% (p = 0.49) and median cost −64% vs always-GPT-6 Astra. The fast-only arm was stopped within a day for low quality. LangChain sells routing middleware."),
("CodeRouter phase-aware routing blog","https://www.coderouter.io/blog/phase-aware-routing-30-day-production-2026","CodeRouter","practitioner","method","routing design",
 S(0,1,1,0,1,0,3,3,0),["D3 April 2026 model set","no quality measurement ('indistinguishable' asserted, not measured)"],[],
 "Router vendor. 78.6% savings with no outcome metric."),
("The New Stack: DeepSeek V4.1 Flash 1017 vs Haiku 5.5","https://thenewstack.io/deepseek-flash-haiku-test/","The New Stack","practitioner","pick","small_edit; structured_output",
 S(3,3,2,0,0,3,2,3,3),["D6 three tests, one run each (the author says it does not generalize)"],[],
 "Useful anecdote: DeepSeek $0.07 vs Haiku $0.30, driven by Haiku's >100K price tier."),
("Morph 'best model for coding'","https://morphllm.com/","Morph","practitioner","pick","(various)",
 S(1,0,0,0,0,2,2,0,0),["D2 re-reports others' numbers","vendor"],[],""),
("Developers Digest / AIHubMix subagent posts","https://www.developersdigest.tech/blog/haiku-5-5-vs-gpt-6-luna-subagent","various","practitioner","pick","(subagents)",
 S(1,0,0,0,0,3,2,1,0),["D5 not opened this pass","AIHubMix resells API access"],[],""),
# ---------------- added in v2 (older / never-scored sources) ----------------
("Toolathlon-Verified","https://toolathlon.xyz/docs/leaderboard","HKUST NLP (academic)","academic","pick","tool_orchestration",
 S(3,1,3,3,3,2,3,0,3),[],[],
 "108 tasks across 32 MCP servers (604 tools) plus 7 local toolkits, execution-based evaluation scripts against seeded app states, Pass@1 ± spread plus Pass@3 / Pass^3, open repo. Every Verified row carries the 'independently evaluated by us' badge. Released 2026-06-30 as a new score series (not comparable with pre-Verified Toolathlon). The tasks, ground truth and evaluators are public on GitHub, and the original task set dates from 2025, before most current models' cutoffs. There is no lookup control beyond execution grading, so cont = 1 under the unchanged contamination criterion, which keeps it at B. No $/task. Newest rows: GLM 5.3 Flash (max) 78.4 ±1.9 (2026-08-30) and DeepSeek V4 Pro 0813 (max) 74.4 ±1.2 (2026-08-13). No Opus 5.5 / GPT-6.x / Gemini 4 / Kimi K3.1 / MiniMax M3.1 rows. New in v2: B (would be A except cont = 1)."),
("Fiction.LiveBench (via Epoch)","https://epoch.ai/benchmarks/fictionlivebench","Fiction.live","community","pick","long_context_summarize",
 S(3,1,1,1,1,0,2,0,1),[],[],
 "Long-context story comprehension: 36 questions over 30 stories. The newest result is 2026-01-27 (Kimi K2.5). The stories are public (cont = 1) and the grading method was not reviewed. New in v2: C on score."),
("AA τ²-Bench Telecom","https://artificialanalysis.ai/evaluations/tau2-bench","Artificial Analysis (benchmark by Sierra)","independent eval org","pick","tool_orchestration",
 S(3,2,3,2,2,3,2,2,3),["D7 saturated (GLM-5.2 99.1%)"],[],"New in v2: C."),
("SWE-bench Multilingual (model-card board)","https://paperswithcode.com/sota/swe-bench-multilingual","various (vendor model cards)","community / self-submitted","pick","issue_resolution",
 S(0,1,2,1,2,3,3,0,3),["D1 entries are vendor model-card self-reports"],[],"New in v2: C."),
("Multi-SWE-bench","https://multi-swe-bench.github.io/","ByteDance Seed","benchmark owner","pick","issue_resolution",
 S(1,1,2,3,3,0,3,0,3),["D5 seen in search only (stale entries, e.g. MopenHands + Gemini-2.5-Pro 21.62%); board not opened"],[],"New in v2: C."),
# ---------------- added in v0.4 discovery pass (2026-10-24) ----------------
("CodePanel AI Code Review Benchmark","https://codepanel.ai/benchmarks","CodePanel","review vendor (ranks third-party models only)","pick","code_review",
 S(2,2,3,1,2,3,3,3,2),[],[],
 "62 fixtures across 13 languages (47 with 56 seeded-in-history defects, 15 clean). Headline counts only fixtures from after 2025-01-01 (42 bug, 15 clean), with ranked models compared on the 37 fixtures they all completed. Fixtures, harness and judge prompt are private, with a canary GUID (cont = 2: private, but no lookup control is described). Judged by a 3-model cross-family panel (Sonnet 5.5, GPT-6.1 Sol, Gemini 3.1 Pro) that excludes the reviewed model's own maker; Cohen's κ 0.94–0.96, no human validation yet (judge = 2). 10,000-sample bootstrap CIs and Holm-corrected paired tests; the stated minimum detectable gap is about 21 pts, so the top 7 share rank 1. $/review from token counts at prices checked 2026-10-16. CodePanel sells a review product but ranks only third-party models (ind = 2, same as the LiveBench precedent). Scores updated 2026-10-17. Single production pipeline, so results are pipeline-specific."),
("IronBee Raw LLM Code Review Benchmark","https://ironbee.ai/blog/the-honest-raw-llm-code-review-benchmark","IronBee","review vendor (ranks third-party models only)","pick","code_review",
 S(2,1,3,3,2,3,3,3,2),[],[],
 "Martian's offline set (50 public PRs, 158 core golden findings). 21 models × up to 3 efforts = 58 configs, 3 passes each, 7,980 reviews. Cross-family 3-judge panel calibrated to within 1 pt of the benchmark's own judge, paired-bootstrap CIs, groups instead of ranks, list-price $/PR. Harness, prompts, every review and verdict are public (github.com/ironbee-ai/code-review-benchmarks, pushed 2026-10-20). One-call raw-model setting, F2 (recall-weighted). Public PRs predate current cutoffs (cont = 1), which keeps it at B. IronBee is about to launch its own review tool, which is not ranked here."),
("MacroscopeBench","https://macroscope.com/benchmark","Macroscope","review vendor (ranks third-party models only)","pick","code_review",
 S(2,2,2,1,3,3,3,3,1),[],[],
 "Proprietary set built from public-repo commits; reported subset 195 commits (144 bug, 51 control), 3 runs averaged, measured $ per run, same prompt and harness for every model. Two LLM judges (recall and precision) with tool access, judge models undisclosed (judge = 1), no CIs. Blog 2026-09-22; board includes GPT-6.1 Sol rows."),
("Qodo 'Which LLM should review your code?'","https://www.qodo.ai/blog/which-llm-should-review-your-code/","Qodo","review vendor (ranks third-party models only)","pick","code_review",
 S(2,2,1,1,2,3,3,3,1),[],[],
 "125 PRs with 703 known bugs, 13 models × 38 configs, F1 and $/PR (2026-10-12). Dataset is Qodo-internal. A single LLM judge (Claude Sonnet 4.6) while Anthropic models lead (disclosed, so judge = 1 rather than 0). Some configs were run once; no CIs. Under v2.1 §2.1, the single-run configs need a gap above 139/√125 = 12.4 pts, so the order among the top models (gaps of a few F1 points) is a tie."),
("Factory Review Benchmark","https://docs.factory.com/benchmarks/review-benchmark","Factory","harness vendor","pick","code_review",
 S(2,1,2,3,2,0,3,3,1),[],[],
 "50 public PRs from 5 repos, 167 validated golden bugs, multiple runs, $/PR, open scoring scripts. Run through Factory's Droid Action, but it ranks models, not Droid. LLM judge with a second-judge spot check (judge = 1). Last updated April 2026; newest models GPT-5.5 / Opus 4.7, so no current pick."),
("TestSuiteBench (arXiv 2610.13065)","https://arxiv.org/abs/2610.13065","ETH Zurich + LogicStar (academic)","academic","pick","test_writing",
 S(2,2,2,3,2,2,3,2,3),[],[],
 "165 Rust/Go/C/C++ CLI apps (12,130 requirement-targeted mutants); agents write a test suite from a spec, scored by mutation score (execution), offline Docker with search disabled, 6 h cap, same mutants and scorer for every row. Paper plus board at testsuitebench.com (8 rows, checked 2026-10-24). Code, harness and data (mutants, reference tests, reference impls) are public as of 2026-10-12, MIT (repro = 3). $/instance is token counts × a 2026-09-22 list-price snapshot, not invoices (cost = 2; Gemini 3.8 Flash at its intro price). Single run per model, no CIs, no per-app results, and the scorer averages only the apps a row finished (missing results are excluded, and the first successful retry is kept); completion counts are not published. Rubric v2.1 §2.1 (noise bound 139/√165 = 10.8 pts): rows that qualify are Claude Opus 5 (high), Gemini 3.8 Flash (medium) and GPT-5.6 Sol (medium). These three are the rows in the paper's whole-set analyses (trajectory counts over the 165 apps, and the overlap of killed mutants across all 12,130), which is evidence that they covered the full set. For Opus 5 the paper says so outright ('33 of 165 instances'). GPT-5.6 Sol carries a flag: it is the model that built the benchmark's specs, tests and mutants. Rows that do not qualify: GPT-6 Astra (no evidence it covered every app), Claude Opus 5.5 and GPT-6.1 Sol (board-only rows, not in the paper, no completion evidence), DeepSeek V4 Flash and GPT-5.6 Luna (validity 78/74 vs 88–97 for the rest, a sign of harness trouble; DeepSeek snapshot not stated in the paper). The top four (55.5–50.1) are a tie. A LogicStar co-author, but LogicStar's agent is not ranked (ind = 2)."),
("TestEvo-Bench (arXiv 2607.02469)","https://arxiv.org/abs/2607.02469","University of Waterloo + Google","academic","pick","test_writing",
 S(1,2,3,3,2,0,3,2,3),[],[],
 "746 test-generation and 509 test-update tasks mined from 152 Java/Maven repos, execution-graded (must pass on new and fail on old revision), coverage and mutation score, timestamped for contamination-aware slicing, CC BY 4.0 data. Only 4 agent configs (Claude Code / SWE-Agent × Opus 4.7, Gemini CLI / SWE-Agent × Gemini 3.1 Pro), single run. Under v2.1 §2.1 (no per-task results found, so the bound is 139/√746 = 5.1 pts on test generation), the harness gaps of 8.9–11.4 pts and the drop under a $1 cap clear the noise, and the tie between the two native-harness configs is a tie. Completion handling was not checked. A Google co-author ranks Gemini (ind = 1), which keeps it at B. Useful finding: success drops sharply under a $1 per-task cap for Opus 4.7, much less for Gemini 3.1 Pro."),
("Scale SWE Atlas Test Writing","https://labs.scale.com/leaderboard/sweatlas-tw","Scale AI","independent eval org","pick","test_writing",
 S(1,2,3,3,2,3,3,0,2),[],[],
 "90 tasks from 11 copyleft repos, 3 trials, ±CIs. Graded by a manifest check, a mutation test (execution), and must-have rubrics judged by Claude Opus 4.5 (judge = 2). Dataset updated 2026-07-28 to block upstream-fix lookup. Harness × model rows (Claude Code, Codex, mini-SWE-agent). ind = 1 (Scale/Meta). No Opus 5.5 / Sonnet 5.5 / GPT-6.1 / Gemini 4 rows."),
("Scale SWE Atlas Refactoring","https://labs.scale.com/leaderboard/sweatlas-refactoring","Scale AI","independent eval org","pick","refactor_migration",
 S(1,2,3,3,2,3,3,0,2),[],[],
 "70 tasks across 10 repos and 6 languages: existing tests must still pass (no P2F/M2F) and must-have rubrics judged by Claude Opus 4.5 must pass. ±CIs. ind = 1 (Scale/Meta). Leader GPT 6 Astra (Codex) xHigh; no Sonnet 5.5 / GPT-6.1 / DeepSeek 1017 rows, so it cannot corroborate the Vals Code Migration picks."),
("NIST CAISI PortBench (DeepSeek V4 Pro evaluation)","https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro","NIST CAISI (US government)","government evaluator","pick","refactor_migration",
 S(3,3,1,0,1,1,3,0,3),[],[],
 "Non-public CLI-tool porting benchmark, Inspect ReAct agent, 1M weighted-token budget, test-based scoring. Government evaluator with no product (ind = 3). Task count and full method unpublished, no cost (PortBench was excluded from CAISI's cost comparison). Published 2026-05-01; newest models GPT-5.5 / Opus 4.6 / DeepSeek V4 Pro, so it is an independent refactor/migration runner but has no current-model rows."),
("Mercor Terminal-Bench 2.1 Extended","https://www.mercor.com/apex/mercor-extended/ots-held-out-terminal-bench-2-1-leaderboard/","Mercor","independent eval org (expert-data vendor)","pick","terminal_agentic_loop",
 S(2,2,2,2,2,3,3,0,3),[],[],
 "99 private Mercor-written tasks added to TB 2.1's 89 public ones; Terminus 2 harness (1,000 steps, 3 h), k = 3, max effort for every model, programmatic tests. No CIs and no cost. Mercor sells expert data to labs but ships no model (ind = 2). A third runner on terminal work, independent of Vals and AA. Public-set scores (80–87%) collapse to 44–48% on the held-out set. Score 70 is right at the A line."),
("Mercor DeepSWE v1.1 run","https://www.mercor.com/apex/","Mercor (benchmark by Datacurve)","independent eval org (expert-data vendor)","pick","issue_resolution",
 S(2,2,2,2,3,3,3,0,3),[],[],
 "113 original tasks across 91 repos and 5 languages, not sourced from public commits; mini-swe-agent (500 steps, 2 h), k = 3 (k = 1 for some open models), unit-test grading. No cost. The k = 1 rows are single-run (v2.1 §2.1 bound 139/√113 = 13.1 pts); the rows cited here are k = 3. Only two rows were readable on the APEX index (Opus 5.5 Max 72.3% #1; Opus 5 Max 71.4%); the other top names did not render."),
("Mercor SWE-bench Verified Extended","https://www.mercor.com/apex/mercor-extended/ots-held-out-swe-bench-verified-leaderboard/","Mercor","independent eval org (expert-data vendor)","pick","small_edit; issue_resolution",
 S(2,2,2,2,2,3,2,0,3),[],[],
 "50 private Mercor tasks in SWE-bench Verified style; mini-swe-agent, Pass@1, k = 3, test-graded, no CIs, no cost. The ordering is unusual (DeepSeek V4.1 Flash 82.7%, Opus 5 82.0%, Opus 5.5 66.0%, GPT-6.1 Sol 45.3%), and 50 tasks give roughly ±13-pt noise, so it is B corroboration only."),
("Mercor SWE Atlas Codebase QnA (public + Extended)","https://www.mercor.com/apex/mercor-extended/ots-held-out-swe-atlas-leaderboard/","Mercor (tasks by Scale AI)","independent eval org (expert-data vendor)","pick","codebase_qa_search",
 S(2,2,2,2,2,3,3,0,1),[],[],
 "Mercor's own run of Scale's 124 public tasks plus 50 held-out Mercor tasks; mini-swe-agent (250 steps, 1 h). LLM judge over rubrics (Claude Opus 4.5) while Claude models lead (judge = 1), no cost. DeepSeek V4.1 Flash drops from 53.5% (public, #1) to 36.7% (held-out); Sonnet 5.5 44.7% and Opus 5.5 43.3% lead the held-out set."),
("Mercor AA-LCR Extended","https://www.mercor.com/apex/","Mercor (benchmark by Artificial Analysis)","independent eval org (expert-data vendor)","pick","long_context_summarize",
 S(2,2,2,2,2,3,2,0,1),[],[],
 "89 private Mercor questions plus AA-LCR's 100 public ones, ~100K tokens each, k = 4, LLM judge (Gemini 3.5 Flash). Same LLM-judge limit as AA-LCR (judge = 1). No cost."),
("Mercor APEX-SWE","https://www.mercor.com/apex/","Mercor (with Cognition)","independent eval org (expert-data vendor)","pick","issue_resolution; greenfield_app",
 S(2,2,2,2,3,3,2,0,2),[],[],
 "200 private observability and integration tasks, k = 3, ±CIs, rubrics plus repository tests (judge = 2). Built with Cognition, whose own model is not in the top rows. Opus 5.5 Max 67.6 ±5.9, Sonnet 5.5 Max 66.4 ±6.1. No cost; close proxy for issue resolution (rel = 2)."),
("Mercor τ³-Banking run","https://www.mercor.com/apex/","Mercor (benchmark by Sierra)","independent eval org (expert-data vendor)","pick","tool_orchestration",
 S(2,1,3,3,2,3,2,0,3),[],[],
 "Sierra's public 97-task set, k = 3, ±CIs, GPT-5.2 low as user simulator, programmatic DB-state checks plus one LLM-judged assertion. An independent rerun of a public set (cont = 1). Gemini 4 Argon High 58.1 ±8.9 #1, Opus 5.5 Max 55.0 ±8.2."),
("Mercor APEX-Agents","https://www.mercor.com/apex/","Mercor","independent eval org (expert-data vendor)","pick","tool_orchestration",
 S(2,2,2,2,3,3,2,0,1),[],[],
 "240 private long-horizon cross-app tasks in Google Suite (banking, law, consulting), k = 3, ±CIs, LLM judge over expert rubrics (judge = 1). Gemini 4 Argon High 82.4 ±4.3 #1, Sonnet 5.5 Max 75.5 ±4.7, Opus 5.5 Max 73.5 ±4.9. Professional-services tool use is a proxy (rel = 2)."),
("Mercor FrontierCode run","https://www.mercor.com/apex/","Mercor (benchmark by Cognition)","independent eval org (expert-data vendor)","pick","issue_resolution",
 S(2,2,1,1,2,3,3,0,2),[],[],
 "150 maintainer-built tasks graded on mergeability; not on Mercor's methodology page (meth = 1). Opus 5.5 Medium 54.6%, Fable 5 xHigh 53.5%, Opus 5 Medium 53.4%, GPT-6 Astra Max 53.3%, Sonnet 5.5 xHigh 52.1%. A second runner of FrontierCode besides AA."),
("VisualForge Bench","https://visualforgebench.com/","independent blogger","community","pick","frontend_visual",
 S(2,2,1,0,0,3,3,3,1),["D6 8 scored pages per model, private prompts, LLM-judged"],[],""),
("screenshotbench","https://screenshotbench.com/","community","community","pick","frontend_visual",
 S(2,1,1,1,0,1,3,0,1),["D6 a handful of target pages; older models"],[],""),
("ArchBench (sabench.com)","https://www.sabench.com/","SA4S workshop (academic)","community / self-submitted","pick","planning_architecture",
 S(1,1,1,1,0,0,2,0,1),["D5 only the landing page (6 categories, 38 submissions) was readable; no model rows read","D1 results are submissions"],[],""),
# ---------------- mirrors ----------------
("BenchLeader / BenchLM / LLMBoard / benchgap mirrors","https://www.benchleader.com/","various aggregators","mirror","pick","(all)",
 S(1,0,1,0,0,3,2,0,0),["D2 mirrors; benchgap publishes estimated scores; BenchLM mislabels creators"],[],
 "Used only as a reading aid for primaries whose charts do not render. Every cited number is attributed to the primary."),
# ---------------- prices ----------------
("Provider pricing docs (Anthropic, OpenAI, Google, xAI, Meta, DeepSeek)","https://docs.anthropic.com/en/docs/about-claude/pricing","model providers","provider docs","price","(pricing)",
 S(3,3,3,3,3,3,3,3,3),[],[],
 "Primary source for list prices, context tiers and promo end dates. Used only for the `price` role. The developer's own price is authoritative; its own benchmark claims are not (D1)."),
]

# newest dated result seen on the source (evidence-date upper bound for its rows) and maintenance state.
# "unknown" = not determined this pass. Used to show staleness; it does NOT change the source tier.
NEWEST = {
 "Vals Terminal-Bench 4.0":("2026-10-24 (board update)","maintained"),
 "Vals Code Migration v1.1":("2026-10-20 (board update)","maintained"),
 "Vals Code Migration v1 (superseded)":("unknown","superseded 2026-10-20"),
 "Vals Vibe Code Bench v1.1":("2026-10-24 (board update)","maintained"),
 "Vals SWE-bench Multimodal":("2026-10-16 (board update)","maintained"),
 "Vals SWE-bench Verified":("2026-09-01 (retired)","retired"),
 "Vals Router Index":("2026-10-20 (board update)","maintained"),
 "AA IFBench":("2026-10-23 (newest result, via mirror)","maintained"),
 "SWE-rebench":("≥2026-07-24 (Opus 5 row; changelog last entry 2026-07-01)","maintained (no changelog entry since 07-01)"),
 "METR Time Horizons 1.1":("2026-05-08 (last addition)","frozen 2026-09-08"),
 "Toolathlon-Verified":("2026-08-30 (GLM 5.3 Flash row)","maintained"),
 "Berkeley BFCL V4":("2026-04-12 (last update)","unknown"),
 "Aider Polyglot":("2025-11-20 (last update)","unmaintained"),
 "SWT-bench":("2026-07-08 (newest entry)","maintained"),
 "Sierra τ³-bench":("≥2026-07-24 (Opus 5 row)","maintained"),
 "Fiction.LiveBench (via Epoch)":("2026-01-27 (newest result)","unknown"),
 "LiveBench 2.0":("2026-10-14 (release)","maintained"),
 "CursorBench 4.0":("2026-09-10 (release)","maintained"),
 "LangChain Open SWE router A/B":("2026-10-01 (post)","one-off"),
 "GitHub ReviewBench":("2026-10-20 (post)","unknown"),
 "Arena Agent leaderboard (code)":("2026-10-23 (board)","maintained"),
 "LMArena WebDev":("2026-10-22 (board)","maintained"),
 "AA AutomationBench-AA":("2026-10-23 (board)","maintained"),
 "Scale SWE-Bench Pro V2 (private split)":("≥2026-07-24 (Opus 5 row)","unknown"),
 "Scale MCP Atlas":("≥2026-07-24 (Opus 5 row)","unknown"),
 "CodePanel AI Code Review Benchmark":("2026-10-17 (scores updated)","maintained"),
 "IronBee Raw LLM Code Review Benchmark":("2026-10-19 (post)","one-off"),
 "MacroscopeBench":("2026-09-22 (blog; board has GPT-6.1 Sol rows)","maintained"),
 "Qodo 'Which LLM should review your code?'":("2026-10-12 (post)","one-off"),
 "Factory Review Benchmark":("2026-04 (last updated)","unknown"),
 "TestSuiteBench (arXiv 2610.13065)":("2026-10 (paper); board checked 2026-10-24; repo 2026-10-12","maintained (board added Opus 5.5 / GPT-6.1 Sol rows)"),
 "TestEvo-Bench (arXiv 2607.02469)":("2026-07 (paper)","live (periodic task mining)"),
 "Scale SWE Atlas Test Writing":("≥2026-07-28 (dataset update note)","maintained"),
 "Scale SWE Atlas Refactoring":("unknown (GPT 6 Astra row)","maintained"),
 "NIST CAISI PortBench (DeepSeek V4 Pro evaluation)":("2026-05-01 (report)","one-off"),
 "Mercor Terminal-Bench 2.1 Extended":("unknown (has GPT-6.1 Sol / Opus 5.5 rows)","maintained"),
 "Mercor DeepSWE v1.1 run":("unknown (has Opus 5.5 row)","maintained"),
 "Mercor SWE-bench Verified Extended":("unknown (has GPT-6.1 Sol / Opus 5.5 rows)","maintained"),
 "Mercor SWE Atlas Codebase QnA (public + Extended)":("unknown (has GPT-6.1 Sol / Opus 5.5 rows)","maintained"),
 "Mercor AA-LCR Extended":("unknown (has Opus 5.5 row)","maintained"),
 "Mercor APEX-SWE":("unknown (has Opus 5.5 row)","maintained"),
 "Mercor τ³-Banking run":("unknown (has Gemini 4 Argon row)","maintained"),
 "Mercor APEX-Agents":("unknown (has Gemini 4 Argon row)","maintained"),
 "Mercor FrontierCode run":("unknown (has Opus 5.5 row)","maintained"),
}
WHYMOVE = {
 "AA IFBench":"D3 was its only disqualifier. AA-run, programmatic checks; the board is maintained. It still cannot back a 'best' claim, because no current frontier row was found.",
 "SWE-rebench":"The rec ≥2 gate was its only blocker (ind 2, cont 3, CIs). Now A for the models it tested (Opus 5, Fable 5, Grok 4.5, GLM-5.2, GPT-5.6 Sol…); successors count only as B.",
 "METR Time Horizons 1.1":"D3 was its only disqualifier. Frozen but readable and dated, so v2 does not exclude it. It tests no current routing model.",
 "FeatureBench (arXiv 2602.10975)":"D3 was its only disqualifier; the score clears 70 without rec. Tested models are older (Opus 4.5).",
 "SWE-CI (arXiv 2603.03823)":"D3 was its only disqualifier. Tested models are older (Opus 4.6 / GPT-5.2).",
 "Berkeley BFCL V4":"D3 was its only disqualifier, and the data is readable via its CSV. Last update 2026-04-12 (stale).",
 "SWT-bench":"D3 removed. cont = 1, plus a commercial-stake cap (LogicStar ranks its own agent), keep it at B.",
 "TestGenEval":"D3 removed. cont = 1 keeps it at B.",
 "JSONSchemaBench":"D3 removed. New commercial-stake cap (hosted by guidance-ai, which ranks Guidance) keeps it at B.",
 "MCP-Universe":"D3 removed. Score 68 (<70) keeps it at B.",
 "Scale SWE-Bench Pro (original public)":"D3 removed. ind = 1 and cont = 1 keep it at B.",
 "Aider Polyglot":"D3 removed. cont = 1 (public Exercism) keeps it at B.",
}
rows=[]
for n,u,o,t,role,sub,sc,disq,caps,why in SRC:
    pct,tr=tier(sc,disq,caps)
    prev = PREV.get(n,"new")
    live_disq=[d for d in disq if not d.startswith("D3")]
    nd,mt=NEWEST.get(n,("unknown","unknown"))
    rows.append(dict(source=n,url=u,owner=o,type=t,role=role,subtasks=sub,**sc,weighted_score=pct,tier=tr,
        prev_tier=prev,tier_change=("" if prev in (tr,"new") else f"{prev}→{tr}"),
        newest_result=nd,maintained=mt,
        disqualifiers="; ".join(live_disq),caps="; ".join(caps),date_checked=D,why=why))
cols=["source","url","owner","type","role","subtasks"]+K+["weighted_score","tier","prev_tier","tier_change","newest_result","maintained","disqualifiers","caps","date_checked"]
with open(DATA/"sources.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader(); w.writerows(rows)

from collections import Counter
c=Counter(r["tier"] for r in rows)
c1=Counter(r["prev_tier"] for r in rows if r["prev_tier"]!="new")
moved=[r for r in rows if r["tier_change"]]
added=[r for r in rows if r["prev_tier"]=="new"]
md=["# Sources","",f"Checked {D} (America/Los_Angeles). Scored against `docs/SOURCE_RUBRIC.md` (v2.1) and generated by `scripts/build_sources.py`; tiers are computed from the scores, not set by hand.","",
    f"**{len(rows)} sources: {c['A']} tier A, {c['B']} tier B, {c['C']} tier C.** Previous pass (research v0.3, {sum(c1.values())} sources): {c1['A']} A, {c1['B']} B, {c1['C']} C.","",
    "Rubric v2 (in force since research v0.3): recency no longer counts toward the source score (denominator 34.5, not 39) and no longer gates tier A; D3 is retired. Recency is now applied to each data point (see `docs/SOURCE_RUBRIC.md` §4). `rec` is still recorded as information about current-model coverage. v2.1 makes D6 precise: a single-run result is used row by row, and only for gaps above its noise (§2.1; worst case 139/√n pts).","",
    "Score order: ind / cont / meth / repro / stats / rec* / rel / cost / judge (each 0–3; *rec is not scored).","",
    "## Tier moves vs. the previous pass",""]
if moved: md+=["| Source | Was | Now | Why |","|---|---|---|---|"]
else: md+=["None: no existing source changed tier this pass."]
for r in moved:
    md.append(f"| {r['source']} | {r['prev_tier']} | {r['tier']} | {WHYMOVE.get(r['source'],'')} |")
md+=["","Same tier, different reason: Martian Code Review Bench stays C, now on score (48) instead of D5; its repo is readable again and IronBee re-ran its PR set.",""]
md+=["","## Added this pass","","| Source | Tier | Note |","|---|---|---|"]
for r in added:
    md.append(f"| {r['source']} | {r['tier']} | {r['disqualifiers'] or r['caps'] or 'newest result: '+r['newest_result']} |")
md+=["","Considered and not added (primary not opened or no subtask fit; see `docs/discovery-log.md`): OpenHands Index (harness vendor; HF dataset seen in search only); ATLAS long-context (arXiv 2605.28079) and LongCodeBench (2025 models); Context Arena (JS shell, unreadable); StructEval; PRDBench; SWE-Mutation (critique of mutation benchmarks; older models); Design2Code (2024 models; mirrors only); sasid.ai structured-output blog (12–24 cases, D6 if added); NIST CAISI GLM-5.3 assessment (cyber only); Mercor non-coding boards (APEX-1, Harvey LAB, GDPval, BrowseComp, etc.); AA MLCR-AA (medical long context; seen on X only); X anecdotes (10-bug in-house eval, KrabArena rerun). Earlier: AA SciCode; SWE-PolyBench.",""]
for T,title in (("A","Tier A: can support a conclusion alone (subject to the per-claim recency rules)"),("B","Tier B: corroboration only"),("C","Tier C: excluded")):
    md+=[f"## {title}",""]
    for r in sorted([r for r in rows if r["tier"]==T],key=lambda r:-r["weighted_score"]):
        scs="/".join(str(r[k]) for k in K)
        line=f"- **{r['source']}** ({r['owner']}; {r['role']}; {r['weighted_score']}; {scs}; newest result {r['newest_result']}). {r['why']}".rstrip()
        if r["caps"]: line+=f" *Cap: {r['caps']}.*"
        if r["disqualifiers"]: line+=f" *Disqualified: {r['disqualifiers']}.*"
        line+=f" <{r['url']}>"
        md.append(line)
    md.append("")
open(DOCS/"sources.md","w").write("\n".join(md))
print("v2",c,"v1",c1,len(rows))
for r in rows: print(r["prev_tier"],"->",r["tier"], r["weighted_score"], r["source"])
