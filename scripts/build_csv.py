import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

D="2026-10-24"
AA="https://artificialanalysis.ai/leaderboards/models"
TB="https://www.vals.ai/benchmarks/terminal-bench-4"
TBAA="https://www.benchleader.com/benchmarks/aa_terminalbench_40 (mirror of https://artificialanalysis.ai/evaluations/terminalbench-4-0)"
SWV="https://www.vals.ai/benchmarks/swebench"
SWP="https://benchlm.ai/benchmarks/scale-swe-bench-pro-public-v2-full (mirror of https://labs.scale.com/blog/swe-bench-pro-v2)"
CM="https://www.vals.ai/benchmarks/code-migration (v1, superseded) ; https://www.vals.ai/benchmarks/code-migration-v1-1 (v1.1, current)"
MM="https://www.vals.ai/benchmarks/swebench-multimodal"
VCB="https://www.vals.ai/benchmarks/vibe-code"
WD="https://arena.ai/leaderboard/code/webdev ; https://www.benchleader.com/benchmarks/lmarena_webdev"
AB="https://www.benchleader.com/benchmarks/aa_automationbench (mirror of https://artificialanalysis.ai/evaluations/automationbench-aa/)"
LCR="https://www.benchleader.com/benchmarks/aa_lcr (mirror of AA)"
OM="https://www.benchleader.com/benchmarks/aa_omniscience (mirror of AA)"
QA="https://labs.scale.com/leaderboard/sweatlas-qna"
ANT="https://docs.anthropic.com/en/docs/about-claude/pricing"
OAI="https://platform.openai.com/docs/pricing"
GOO="https://ai.google.dev/gemini-api/docs/pricing"
XAI="https://docs.x.ai/docs/models"
META="https://dev.meta.ai/docs/pricing-rate-limits"
KIMI="https://artificialanalysis.ai/articles/kimi-k3-1-pro-launch-benchmarks"
DS="https://api-docs.deepseek.com/quick_start/pricing"
ZAI="https://docs.z.ai/guides/overview/pricing (provider page, checked 2026-10-24)"
VALSP="Vals AI leaderboard price column (secondary; provider page not checked): "+TB
cols=["model","provider","open_weights","api_available","input_usd_per_mtok","output_usd_per_mtok","cached_input_usd_per_mtok","pricing_notes","context_window","aa_intelligence_index","aa_index_config","aa_cost_per_index_task_usd","terminal_bench_4_vals","terminal_bench_4_aa","swe_bench_verified_vals","swe_bench_pro_v2_public","code_migration_v1_vals","code_migration_v1_1_vals","swe_bench_multimodal_vals","vibe_code_bench_v1_1","lmarena_webdev_elo","automationbench_aa","aa_lcr","aa_omniscience","swe_atlas_codebase_qna","pricing_source","score_sources","date_checked"]
S=" ; ".join([AA,TB,TBAA,SWV,SWP,CM,MM,VCB,WD,AB,LCR,OM,QA])
rows=[
# model provider ow api in out cache notes ctx aaii cfg cost tb4v tb4aa swev swep cm mm vcb wd ab lcr om qa psrc
["Claude Opus 5.5","Anthropic","no","yes",4,20,0.20,"Batch 50% off; fast mode $8/$40; US-only 1.1x","1M",58,"max",5.98,65.15,59.6,"",
 "",66.65,70.21,90.29,1807,69.5,84.7,46.4,"",ANT],
["Claude Sonnet 5.5","Anthropic","no","yes",2,10,0.10,"Batch 50% off","1M",56,"max",5.46,64.14,63.6,"",95.79,69.83,58.33,92.39,1768,71.8,82.7,32.3,"",ANT],
["Claude Haiku 5.5","Anthropic","no","yes",0.10,0.50,0.01,"Prompts >100K tokens billed $0.50/$2.50 (5x)","1M",43,"max",0.21,36.36,32.8,"",87.23,44.57,43.96,90.44,1585,"",82.7,"","",ANT],
["Claude Fable 5.1","Anthropic","no","yes",10,50,0.25,"Batch 50% off","1M",53,"max",7.63,58.08,55.0,"",99.10,54.61,61.25,90.26,1743,59.4,85.3,43.5,59.95,ANT],
["GPT-6 Astra","OpenAI","no","yes",10,50,1.00,">272K input: $20/$75","1M (AA); 1.1M (LMArena)",53,"max",3.26,59.60,59.6,"",96.90,67.74,43.33,89.59,1775,68.5,"",43.7,59.14,OAI],
["GPT-6.1 Sol","OpenAI","no","yes",2,10,0.10,">272K input: $4/$15","1M",52,"max",0.72,55.05,56.1,"",96.11,65.12,43.54,88.93,1749,66.6,84.0,41.5,"",OAI],
["GPT-6 Luna","OpenAI","no","yes",0.10,0.50,0.01,">272K input: $0.20/$0.75","1M",38,"max",0.07,13.64,"","","",42.55,37.50,81.65,1578,"",83.3,"","",OAI],
["Gemini 4 Argon","Google","no","yes",2,10,"","PROMO through 2026-11-30; list $4/$20 from 2026-12-01 (Vals uses $4/$20)","1M",53,"high",1.99,57.58,57.1,"",99.22,68.17,56.04,91.91,1673,77.5,"",42.4,"",GOO],
["Gemini 3.8 Flash","Google","no","yes",0.75,3.75,"","PROMO through 2026-12-31; $1.50/$7.50 from 2027-01-01","1M",41,"high",1.24,19.70,"",80.00,94.86,36.55,40.83,78.65,1585,60.9,84.0,29.6,47.04,GOO],
["Gemini 3.5 Flash-Lite","Google","no","yes",0.30,2.50,"","","1M",22,"default",0.19,"","",75.00,"",6.15,"",37.16,"","","","","",GOO],
["Grok 4.7","xAI (SpaceXAI)","no","yes",2,6,0.50,">=200K prompt: $4/$12","500K",46,"xhigh",3.74,28.79,25.8,"","",44.82,42.92,86.17,1637,65.6,"",32.0,"",XAI],
["Muse Wonder","Meta","no","yes",4,20,0.20,"Muse Wonder Full (AA II 56) is NOT API-accessible (Muse Code subscription only)","1.05M",52,"max",4.54,49.49,52.0,"",96.73,62.55,45.63,83.09,1651,68.1,"",25.5,"",META],
["Kimi K3.1 Pro","Moonshot AI","pending (announced, not yet published)","yes",2,10,0.20,"Launched 2026-10-23","1M",55,"default",2.11,63.64,67.2,"","","","",84.89,"1692 (llmbenchmark.ai mirror)",73.3,86.3,29.5,"",KIMI],
["DeepSeek V4.1 Flash 1017","DeepSeek","yes","yes",0.30,1.20,0.006,"Peak price; off-peak $0.15/$0.60; API name deepseek-flash","1M",45,"max",0.26,31.82,33.8,"","",44.21,"46.46 (V4.1 Flash, pre-1017)",87.73,1664,66.6,82.7,"","",DS],
["DeepSeek V4 Pro 0813","DeepSeek","yes","yes",1.32,3.96,0.044,"Peak price; off-peak $0.66/$1.98; no vision","1M",36,"max",0.67,14.14,"",96.40,"",41.54,"",82.30,"1582 ('DeepSeek V4 Pro high'; version not stated)","56.7 (V4 Pro max, published 2026-08-13)","","","",DS],
["GLM 5.3","Z.ai","yes","yes",1.40,4.40,0.26,"same list price as GLM-5.2","1M",45,"max",2.01,38.89,41.9,95.40,95.60,44.22,"",78.13,1623,62.2,"","","",ZAI],
["GLM 5.3 Flash","Z.ai","yes","yes",0.15,0.50,0.03,"list price; the 50% promo ($0.075/$0.25) ended 2026-09-09 (UTC+8). Vals/AA $/task may have been computed at the promo price","1M",42,"default",0.28,37.37,32.8,92.00,"",20.52,"",30.76,1608,60.4,"","","",ZAI],
["MiMo V2.6 Pro","Xiaomi","yes","yes",0.435,0.87,"","","1M",46,"default",0.13,31.31,34.9,"","",43.01,41.25,85.22,1625,58.6,86.3,"","",VALSP],
["MiMo V2.6 Flash","Xiaomi","yes","yes",0.14,0.28,"","","1M","unknown","","",24.24,22.7,"","",40.93,"",78.96,1634,64.0,"","","",VALSP],
["Qwen 3.8 Max (0902)","Alibaba","no","yes",2,6,"","","984K",45,"default",5.41,38.89,38.9,"","","23.96 (Qwen 3.8 Max, not 0902)","42.50 (Qwen 3.8 Max)",77.14,1673,56.2,"","","",VALSP],
["Mistral Large 4","Mistral","yes (per BenchLeader tag)","yes",1.36,4.18,"","AA lists 'Mistral Large 4 Preview'","524K",38,"preview",1.13,27.78,26.8,"","",30.56,33.13,78.40,1543,59.9,81.3,"","",VALSP],
["MiniMax M3.1 Flash","MiniMax","yes","yes",0.15,0.60,"","","1M",43,"default",0.22,25.25,25.8,"","","","",73.94,1590,72.5,"","","",VALSP],
]
# Vals Code Migration v1.1 (Pi harness, revised hidden tests; updated 2026-10-20). Not comparable to v1.
V11={"Claude Opus 5.5":81.01,"Claude Sonnet 5.5":86.88,"Claude Haiku 5.5":52.36,"GPT-6 Astra":80.58,
 "GPT-6.1 Sol":77.32,"GPT-6 Luna":46.67,"Gemini 4 Argon":70.80,"Gemini 3.8 Flash":38.65,"Grok 4.7":53.22,
 "Muse Wonder":72.36,"DeepSeek V4.1 Flash 1017":67.52,"DeepSeek V4 Pro 0813":51.99,"GLM 5.3":55.07,
 "GLM 5.3 Flash":51.65,"MiMo V2.6 Pro":48.79,"MiMo V2.6 Flash":39.55,"Qwen 3.8 Max (0902)":57.19}
CMI=cols.index("code_migration_v1_vals")
with open(DATA/"models.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(cols)
    for r in rows:
        r=r[:CMI+1]+[V11.get(r[0],"")]+r[CMI+1:]
        assert len(r)==len(cols)-2,(r[0],len(r))
        w.writerow(r+[S,D])
print(len(rows),"rows")
