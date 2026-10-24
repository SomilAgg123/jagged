from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

"""Score every source against SOURCE_RUBRIC.md and write sources.csv + sources.md.
Tiers are computed, never hand-set."""
import csv
D = "2026-10-24"
# rubric v2 (2026-10-24): recency no longer counts toward the source score or gates tier A.
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

# tiers from the previous pass (v1 rule, sources.csv of 2026-10-24 14:27 PT), used only to report moves
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
"AA IFBench": "C",
"SWE-rebench": "B",
"Epoch AI SWE-bench Verified": "C",
"Epoch Capabilities Index (ECI)": "B",
"METR Time Horizons 1.1": "C",
"METR Opus 5.5 pre-deployment report": "C",
"LiveBench 2.0": "B",
"SWE-bench-Live": "C",
"Agent-as-a-Router / CodeRouterBench (arXiv 2606.22902)": "B",
"Scrouting / SuperScout (arXiv 2608.04804)": "B",
"FeatureBench (arXiv 2602.10975)": "C",
"SWE-CI (arXiv 2603.03823)": "C",
"SWT-bench": "C",
"TestGenEval": "C",
"JSONSchemaBench": "C",
"MCP-Universe": "C",
"Scale SWE-Bench Pro V2 (private split)": "B",
"Scale SWE-Bench Pro V2 (public split)": "C",
"Scale SWE-Bench Pro (original public)": "C",
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
"Berkeley BFCL V4": "C",
"Aider Polyglot": "C",
"LiveCodeBench": "C",
"Interfaze Structured Output Benchmark": "C",
"OpenRouter rankings": "C",
"LangChain Open SWE router A/B": "B",
"CodeRouter phase-aware routing blog": "C",
"The New Stack: DeepSeek V4.1 Flash 1017 vs Haiku 5.5": "C",
"Morph 'best model for coding'": "C",
"Developers Digest / AIHubMix subagent posts": "C",
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
 S(1,1,2,2,1,2,3,2,1),["D6 30 PRs, one run per model; own page says ranks are noise"],[],""),
("Martian Code Review Bench","https://github.com/withmartian/code-review-benchmark/","Martian","harness vendor","pick","code_review",
 S(1,2,0,0,1,2,3,0,1),["D5 repo page showed no content on fetch; results seen only in Greptile marketing"],[],
 "Martian sells a router; scores review tools, not models."),
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
 S(2,1,3,3,2,0,2,2,3),[],[],"Last updated 2025-11-20. Newest rows: gpt-5 (high) 88.0% ($29.08) and DeepSeek-V3.2-Exp Reasoner 74.2% ($1.30). 225 public Exercism tasks, one run (cont = 1). v1: C (D3) → v2: B."),
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
md=["# Sources","",f"Checked {D} (America/Los_Angeles). Scored against `docs/SOURCE_RUBRIC.md` (v2) and generated by `scripts/build_sources.py`; tiers are computed from the scores, not set by hand.","",
    f"**{len(rows)} sources: {c['A']} tier A, {c['B']} tier B, {c['C']} tier C.** Previous pass (v1 rule, {sum(c1.values())} sources): {c1['A']} A, {c1['B']} B, {c1['C']} C.","",
    "v2 change: recency no longer counts toward the source score (denominator 34.5, not 39) and no longer gates tier A; D3 is retired. Recency is now applied to each data point (see `docs/SOURCE_RUBRIC.md` §4). `rec` is still recorded as information about current-model coverage.","",
    "Score order: ind / cont / meth / repro / stats / rec* / rel / cost / judge (each 0–3; *rec is not scored).","",
    "## Tier moves vs. the previous pass","","| Source | Was | Now | Why |","|---|---|---|---|"]
for r in moved:
    md.append(f"| {r['source']} | {r['prev_tier']} | {r['tier']} | {WHYMOVE.get(r['source'],'')} |")
md+=["","Same tier, different reason: SWE-bench-Live and LiveCodeBench stay C, now for D5 (leaderboard unreadable on fetch) instead of D3. Vals SWE-bench Verified and Epoch SWE-bench Verified stay C for D7. Interfaze stays C (D1), and the CodeRouter blog stays C (no quality measurement). Vals Code Migration v1 stays B under a new 'superseded version' cap; without it, dropping the recency gate would have promoted it to A even though v1.1 replaced it.",""]
md+=["","## Added this pass","","| Source | Tier | Note |","|---|---|---|"]
for r in added:
    md.append(f"| {r['source']} | {r['tier']} | {r['disqualifiers'] or r['caps'] or 'newest result: '+r['newest_result']} |")
md+=["","Considered and not added: AA SciCode (scientific coding; it maps to none of the 13 subtasks); SWE-PolyBench (Amazon; seen in search only).",""]
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
