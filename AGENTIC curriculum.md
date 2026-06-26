# Curriculum — Agentic AI for Data Engineers
### 16 weeks · ~5 hrs/week · ~80 hours total · cold-start GenAI → interview-ready agentic AI

Source of truth for *what you do each hour*. Track *where you are* in `progress-tracker.md`. For a data engineer with 5 YoE (strong Python/SQL/Spark/cloud) starting cold on LLMs, targeting interviews in ~4 months with two deployed, measured portfolio projects.

**How this is structured.** Each week is broken into ~5 one-hour blocks. Every block has a specific action and a **→ Done when:** line — a concrete, checkable target. If the "done when" isn't true, the hour isn't finished; carry it in the tracker. Hours within a week are ordered but you can merge two into one sitting. "Concept" hours always produce a **notes file in your own words** — that's how theory becomes deterministic and how you build your interview answers.

**Design rules:** every block is high-yield and maps to real job requirements — no filler. You build by hand first (to understand internals), then compare to the managed AWS service (that comparison is what senior interviews probe). AWS is primary; Azure is mapped in parallel.

---

## The two flagship projects (these are your CV)

**Project 1 — Enterprise RAG over your data (Weeks 3–8).** Production-grade RAG over a real corpus: ingestion + chunking pipeline, vector store, hybrid search with reranking, an evaluation harness with quoted metrics, guardrails, AWS deployment — plus a side-by-side comparison against Bedrock Knowledge Bases (managed RAG).

**Project 2 — Agentic data assistant with MCP (Weeks 9–15).** A stateful, multi-step agent (LangGraph) over your database/warehouse that calls tools and takes guarded actions — with **persistent vector-backed memory + context engineering**, exposed through an **MCP server**, **security-hardened** (indirect-injection defenses, least-privilege tools, sandboxed execution), shipped with agent evaluation, tracing, cost caps, and AWS deployment — compared against Bedrock Agents (managed). The MCP piece is your biggest differentiator.

---

## Setup — Week 0 (~1 hr)
- **H1 — Environment + access.** Create the Git repo, Python 3.11+ venv, `.env`, and two project folders. Request AWS Bedrock model access (a current Claude-tier model + Titan/Cohere embeddings). Install Ollama and pull a small LLM + an embedding model for free local dev. **→ Done when:** a `hello_bedrock.py` returns a completion via the `boto3` Converse API **and** `ollama run <model>` responds locally.

**Cost plan:** use Ollama for most learning hours; switch to Bedrock for cloud-deploy weeks (8, 14) and final demos. Budget ~$20–40 total.
**Corpus/DB:** pick a real document set for Project 1 and a real-ish Postgres/warehouse for Project 2 now, so Weeks 3 and 9 start immediately.

## Reference shelf (pull current links via the Project as you go)
Bedrock Converse API · Bedrock Knowledge Bases · Bedrock Agents + Guardrails · `boto3` · LangChain + **LangGraph** · LlamaIndex · pgvector / Chroma / OpenSearch · **RAGAS** · **MCP specification** (note the current version) · FastAPI · Docker · LangSmith / Arize Phoenix · OWASP LLM Top 10. *Azure equivalents:* Azure OpenAI · Azure AI Search · Azure AI Foundry Agent Service · Azure AI Content Safety · Semantic Kernel.

---

# Phase 0 — Foundations & first contact (Weeks 1–2)

## Week 1 — LLMs for engineers: mental model + first calls · ~5 hrs
**Friday outcome:** a provider-agnostic `call_llm()` wrapper that returns validated structured output, plus a fundamentals notes file. *(Feeds: foundations)*
- **H1 — Concept.** Tokens, context window as a budget, temperature/top-p, why hallucination happens, the per-token cost model, and prompting vs. RAG vs. fine-tuning. **→ Done when:** `notes/w1-fundamentals.md` explains, in your words, the context window as a tradeoff and the 3 layers that reduce hallucination.
- **H2 — First calls.** Call the Bedrock Converse API; parameterize temperature; log input/output token counts and compute cost. **→ Done when:** one script prints a completion + token counts at temp 0.0 and temp 1.0.
- **H3 — Structured output.** Make the model return strict JSON for a small extraction task; validate with pydantic. **→ Done when:** the script returns a pydantic-validated object and invalid JSON is caught and retried.
- **H4 — Provider abstraction.** Wrap calls in `call_llm(prompt, ...)` and make it run against both Bedrock and local Ollama; note the one-line Azure OpenAI equivalent. **→ Done when:** the same script runs unchanged against Bedrock and Ollama by swapping one argument.
- **H5 — Lock + log.** Write your answers to the two W1 interview angles; add to the Q-bank; update the tracker. **→ Done when:** Q-bank W1 rows filled with drafted answers; tracker W1 = Done.
- **Interview angle:** context window as an engineering tradeoff; why LLMs hallucinate and the layers to reduce it.

## Week 2 — Prompting · tool calling · embeddings · ~5 hrs
**Friday outcome:** a robust structured extractor, a tiny semantic search, and a working tool-calling demo. *(Feeds: foundations)*
- **H1 — Prompt patterns.** Build `prompts.py` with a system prompt + few-shot template; test zero-shot vs. few-shot on 5 examples. **→ Done when:** you've documented the measured quality difference on those 5 examples.
- **H2 — Extractor (project-grade).** Messy text → validated typed JSON with retries on invalid output. **→ Done when:** the extractor returns valid output for 5 messy inputs (after at most one retry each).
- **H3 — Embeddings.** Embed ~20 short docs; compute cosine similarity; return top-3 for a query. **→ Done when:** a query prints its 3 nearest docs by cosine similarity.
- **H4 — Tool calling.** Define 2 tools; let the model choose and call one; parse the tool-use response and feed the result back. **→ Done when:** the model routes 3 different prompts to the correct tool and returns a final answer using the tool result.
- **H5 — Lock + log.** **→ Done when:** Q-bank W2 filled; tracker updated; work committed.
- **Interview angle:** prompting vs. fine-tuning vs. RAG decision criteria; what function calling is and why it's the basis of agents.

---

# Phase 1 — Project 1: Enterprise RAG (Weeks 3–8)

## Week 3 — RAG ingestion & chunking · ~5 hrs
**Friday outcome:** your corpus is chunked, embedded, and queryable in a vector store. *(Feeds: Project 1)*
- **H1 — Concept + decision.** Chunking strategies (fixed+overlap, semantic, hierarchical) and why chunking dominates quality; pick your size/overlap. **→ Done when:** `notes/w3-chunking.md` records your chunking choice and why.
- **H2 — Loader.** Build `ingest/load.py` to read your docs (pdf/md/html) into `{text, source, section}`. **→ Done when:** all corpus docs load into a clean list with metadata.
- **H3 — Chunker.** Implement fixed-size + overlap chunking with metadata propagation; try a sentence-aware variant. **→ Done when:** corpus → chunks; chunk count and average size printed.
- **H4 — Embed + store.** Embed chunks and store in pgvector (or Chroma) with metadata. **→ Done when:** the store holds N chunks queryable by similarity.
- **H5 — Smoke test + log.** Run 3 similarity queries; eyeball relevance; check off the ingestion pipeline. **→ Done when:** 3 queries return plausibly relevant chunks; tracker updated.
- **Interview angle:** chunking strategy and tradeoffs; how metadata improves retrieval and enables access control.

## Week 4 — Vector DBs + baseline RAG end-to-end · ~5 hrs
**Friday outcome:** a working naive RAG that answers real questions with citations, saved as your baseline. *(Feeds: Project 1)*
- **H1 — Concept.** HNSW/ANN, distance metrics, vector-DB selection criteria. **→ Done when:** `notes/w4-vectordb.md` explains the ANN recall/latency tradeoff and your store choice.
- **H2 — Retriever.** `retrieve(query, k)` → top-k chunks with scores + metadata. **→ Done when:** the function returns top-k with scores.
- **H3 — Generation with citations.** Assemble context into a prompt; call the LLM; return answer + cited sources. **→ Done when:** answers include source citations.
- **H4 — End-to-end.** Wrap as `ask(question)` behind a CLI or notebook. **→ Done when:** naive RAG answers a real question end-to-end.
- **H5 — Baseline capture + log.** Run 5 real questions; save outputs as the naive baseline. **→ Done when:** `baseline_answers.md` saved; tracker updated.
- **Interview angle:** how to choose a vector store for a workload; what an ANN index is and the recall/latency tradeoff.

## Week 5 — Advanced retrieval: hybrid · reranking · query transforms · ~5 hrs
**Friday outcome:** an upgraded retriever (hybrid + rerank + query rewrite) you can compare to the baseline. *(Feeds: Project 1 · time-reclaim week — cap tuning)*
- **H1 — Concept.** Hybrid search, BM25, RRF, cross-encoder reranking, HyDE/query rewriting. **→ Done when:** `notes/w5-retrieval.md` explains why vector search fails on exact tokens and how RRF + rerank fix it.
- **H2 — Hybrid.** Add BM25 retrieval; fuse with vector results via RRF. **→ Done when:** the hybrid retriever returns fused ranked results.
- **H3 — Reranker.** Add a cross-encoder reranker over the top-N candidates. **→ Done when:** reranked order differs from first-stage on 3 queries and looks better.
- **H4 — Query rewriting.** Add an LLM query-rewrite/HyDE step before retrieval. **→ Done when:** a vague query is rewritten and retrieves better chunks.
- **H5 — Compare + log.** Re-run the 5 baseline questions; save a side-by-side. **→ Done when:** `naive_vs_advanced.md` saved; tracker updated. *(Stop tuning here — banked time goes to Weeks 10/13.)*
- **Interview angle:** why vector search is bad for part numbers and the fix; RRF and cross-encoder reranking explained.

## Week 6 — Evaluation: the credibility module ⭐ · ~5 hrs
**Friday outcome:** quoted metrics (recall@k, faithfulness) for naive vs. advanced, in the tracker. *(Feeds: Project 1)*
- **H1 — Concept + golden-set design.** recall@k, MRR, faithfulness, answer relevance; design the golden-set format. **→ Done when:** `notes/w6-eval.md` defines your golden-set schema.
- **H2 — Golden set.** Write 20–30 Q/A pairs with expected source chunks. **→ Done when:** `golden.jsonl` has ≥20 pairs.
- **H3 — Retrieval eval.** Compute recall@k + MRR for naive vs. advanced. **→ Done when:** a metrics table prints recall@5/@10 for both.
- **H4 — Generation eval.** Use RAGAS (or a custom LLM-judge) for faithfulness + answer relevance. **→ Done when:** faithfulness is computed for both pipelines.
- **H5 — Record + log.** Fill the Project 1 metrics table with real numbers; draft the eval answer. **→ Done when:** tracker metrics table populated; Q-bank W6 filled.
- **Interview angle:** "walk me through an eval you designed"; "what was your recall@10 and how did reranking change it?"

## Week 7 — Productionize I: API · streaming · guardrails · ~5 hrs
**Friday outcome:** a FastAPI service with streaming and guardrails. *(Feeds: Project 1 · time-reclaim week — cap polish)*
- **H1 — Concept.** Serving patterns + OWASP LLM Top 10 + guardrails. **→ Done when:** `notes/w7-safety.md` lists 5 OWASP LLM risks with mitigations.
- **H2 — FastAPI.** Wrap `ask()` in a `/query` endpoint. **→ Done when:** an HTTP call returns an answer JSON.
- **H3 — Streaming.** Add token/SSE streaming. **→ Done when:** tokens stream to the client.
- **H4 — Guardrails.** Add input validation + an output safety check (Bedrock Guardrails or a checking prompt) + PII redaction. **→ Done when:** a malicious/PII input is blocked or redacted.
- **H5 — Logging + log.** Structured request/response/latency logging. **→ Done when:** logs capture query/answer/latency; tracker updated. *(Stop polishing — banked time goes to Weeks 10/13.)*
- **Interview angle:** defending against prompt injection; OWASP LLM risks and concrete mitigations.

## Week 8 — Productionize II: AWS deploy + managed comparison ⭐ · ~5 hrs (may spill)
**Friday outcome:** Project 1 deployed on AWS, compared to a Bedrock Knowledge Base, and packaged. *(Feeds: Project 1 — DONE)*
- **H1 — Concept + Dockerize.** Managed vs. self-hosted RAG; cost levers; write the `Dockerfile`. **→ Done when:** the image builds and runs locally.
- **H2 — Deploy to AWS.** Container on Lambda+API Gateway or ECS/Fargate; vectors in Aurora pgvector or OpenSearch Serverless; Bedrock for inference. **→ Done when:** an AWS endpoint answers a query.
- **H3 — Bedrock Knowledge Base.** Stand up a KB on the same corpus (S3 sync). **→ Done when:** the KB answers the same question via console/API.
- **H4 — Compare + cost.** Run your 5 questions through both; log cost + latency; note quality/effort tradeoffs. **→ Done when:** a `yours_vs_KB.md` comparison is saved.
- **H5 — Package.** README + architecture diagram + metrics table + "at 100M docs" section; tag the repo. **→ Done when:** Project 1 README is complete and the repo is tagged `v1`.
- **Interview angle:** managed Knowledge Bases vs. self-hosted RAG (argue both sides); how you cut inference cost.

---

# Phase 2 — Project 2: Agentic data assistant + MCP (Weeks 9–15)

> **Time-budget note:** Weeks 10 and 13 run hot (~6–7 hrs) because they absorb persistent memory + context engineering (W10) and agent security in depth (W13). The banked hours from capping retrieval tuning (W5) and productionize polish (W7–8) cover them. Protect the ⭐ weeks over RAG polish; carry any spillover in the tracker.

## Week 9 — Agents: fundamentals + tool use · ~5 hrs
**Friday outcome:** a ReAct-style agent that answers DB questions via NL→SQL using ≥2 tool calls. *(Feeds: Project 2)*
- **H1 — Concept.** Agentic vs. chatbot; the ReAct loop; when not to use an agent. **→ Done when:** `notes/w9-agents.md` explains ReAct with an example.
- **H2 — SQL tool.** Build a read-only `run_sql(query)` tool against your DB. **→ Done when:** the tool executes a SELECT and returns rows.
- **H3 — NL→SQL.** Prompt the model to generate SQL from a question; execute it. **→ Done when:** 3 questions return correct rows.
- **H4 — Agent loop.** Wrap in a ReAct loop with 2–3 tools that iterates until answered. **→ Done when:** the agent answers a question needing ≥2 tool calls.
- **H5 — Lock + log.** **→ Done when:** Q-bank W9 filled; tracker updated.
- **Interview angle:** what makes a system agentic vs. a chatbot; describe the ReAct loop.

## Week 10 — LangGraph orchestration + memory & context engineering ⭐ · ~6–7 hrs
**Friday outcome:** the agent as a stateful LangGraph graph with persistent memory and context compaction. *(Feeds: Project 2)*
- **H1 — Concept.** Graphs vs. chains, state, failure modes, episodic vs. semantic memory, context compaction, context rot/poisoning. **→ Done when:** `notes/w10-memory.md` explains episodic vs. semantic memory and compaction.
- **H2 — LangGraph graph.** Rebuild the agent as a graph: plan → SQL → execute → validate → summarize, with state. **→ Done when:** the graph runs the full multi-step flow.
- **H3 — Routing + short-term memory.** Add conversation state + a conditional edge (e.g., retry on bad SQL). **→ Done when:** the agent recovers from a failed step via routing.
- **H4 — Persistent memory.** Add vector-backed long-term memory (reuse the Phase 1 store) that writes/reads episodic + semantic memories. **→ Done when:** the agent recalls a fact from a prior run.
- **H5 — Context compaction.** Add a summarization step when state exceeds a token threshold. **→ Done when:** a long run stays under the token budget via compaction.
- **H6 — Failure-mode test + log.** Force a loop/runaway and confirm a step cap contains it. **→ Done when:** the cap stops a runaway; tracker + checklist updated.
- **Interview angle:** why a graph over a chain; how the agent handles a 40-step task without context degrading; episodic vs. semantic memory implementation.

## Week 11 — Multi-agent + human-in-the-loop · ~5 hrs
**Friday outcome:** a supervisor delegating to specialists, with an approval gate before any action. *(Feeds: Project 2)*
- **H1 — Concept.** Supervisor/specialist, planner/executor, HITL, idempotency. **→ Done when:** `notes/w11-multiagent.md` explains the supervisor pattern and when multi-agent helps.
- **H2 — Supervisor.** Add a supervisor node routing to ≥2 specialist agents. **→ Done when:** the supervisor delegates correctly on 2 task types.
- **H3 — Approval gate.** Insert a human-approval interrupt before any write/action. **→ Done when:** a write pauses for approval, then proceeds or cancels.
- **H4 — Idempotency.** Make actions idempotent + logged with an action id. **→ Done when:** re-running an action doesn't double-apply.
- **H5 — Lock + log.** **→ Done when:** Q-bank W11 filled; tracker updated.
- **Interview angle:** when multi-agent genuinely helps vs. adds complexity; how to let an agent take actions safely.

## Week 12 — MCP (Model Context Protocol): the differentiator ⭐ · ~5 hrs
**Friday outcome:** an MCP server exposing your data source, consumed by your agent, with auth + audit. *(Feeds: Project 2)*
- **H1 — Concept + spec.** Server/client, tools/resources, auth/authorization/audit; read the spec. **→ Done when:** `notes/w12-mcp.md` states the spec version and the server/client roles.
- **H2 — Server skeleton.** Scaffold an MCP server exposing one tool (e.g., `query_warehouse`). **→ Done when:** the server starts and lists its tool.
- **H3 — Expose data source.** Add tools/resources for your DB/warehouse (a read + a guarded action). **→ Done when:** an MCP client can call the tool and get data back.
- **H4 — Connect agent.** Wire your LangGraph agent to consume the MCP server as a client. **→ Done when:** the agent answers a question by calling the MCP tool.
- **H5 — Auth/audit + log.** Add basic auth + an audit log of tool calls; draft the MCP answers. **→ Done when:** tool calls are authed + logged; Q-bank W12 filled.
- **Interview angle:** what MCP is and why it matters; how auth and audit should work for an MCP server exposing a database (know the spec version).

## Week 13 — Agent evaluation + observability + security hardening ⭐ · ~6–7 hrs
**Friday outcome:** agent metrics quoted, full tracing, and a security-hardened agent that survives an injection test. *(Feeds: Project 2)*
- **H1 — Concept.** Agent eval (success rate, trajectory, tool-call accuracy), tracing; agent security — indirect injection, the lethal trifecta, least-privilege, sandboxing. **→ Done when:** `notes/w13-eval-security.md` explains indirect injection and the lethal trifecta.
- **H2 — Eval set.** Define 10–15 tasks with expected outcomes/tool calls. **→ Done when:** `agent_tasks.jsonl` exists.
- **H3 — Run eval.** Compute task success rate + tool-call accuracy. **→ Done when:** metrics are printed for the agent.
- **H4 — Tracing + caps.** Add LangSmith/Phoenix tracing + a per-task cost/latency log + a hard step/cost cap. **→ Done when:** a trace + cost log appear for a run and the cap halts overruns.
- **H5 — Security hardening.** Least-privilege tool scoping + sandbox the SQL/action execution. **→ Done when:** tools run with minimal permissions inside a sandbox.
- **H6 — Injection test + log.** Add a poisoned document to the eval set; confirm the agent isn't hijacked; fill the Project 2 metrics table. **→ Done when:** the injection test passes; tracker metrics populated.
- **Interview angle:** how you evaluate an agent; what indirect prompt injection is and how you defend against it; the lethal trifecta and how you broke it.

## Week 14 — Productionize the agent on AWS + managed comparison ⭐ · ~5 hrs (may spill)
**Friday outcome:** the agent deployed on AWS and compared to a Bedrock Agent, with prod caps. *(Feeds: Project 2)*
- **H1 — Concept + Dockerize.** Bedrock Agents (Action Groups/Lambda) vs. LangGraph; prod concerns; write the Dockerfile. **→ Done when:** the agent image builds and runs locally.
- **H2 — Deploy to AWS.** Deploy the agent service (ECS/Fargate or Lambda) with Bedrock inference. **→ Done when:** the deployed endpoint runs a task.
- **H3 — Bedrock Agent.** Build a parallel Bedrock Agent (Action Group → Lambda) on a similar task. **→ Done when:** the Bedrock Agent completes the task in the console.
- **H4 — Compare + prod guardrails.** Compare effort/behavior; wire guardrails + cost caps into the deployed service. **→ Done when:** comparison notes saved and caps are active in prod.
- **H5 — Lock + log.** **→ Done when:** Q-bank W14 filled; tracker updated.
- **Interview angle:** Bedrock Agents vs. LangGraph (when each); operational safety for a production agent.

## Week 15 — Polish, package, publish · ~5 hrs
**Friday outcome:** both projects packaged and your CV/LinkedIn updated. *(Feeds: both — PACKAGED)*
- **H1 — README + diagram.** Project 2 README + architecture diagram. **→ Done when:** both exist and are clear.
- **H2 — Demo + failure modes.** Record a demo GIF/video; write the failure-mode section. **→ Done when:** a demo artifact + failure-mode write-up exist.
- **H3 — CV bullets.** 2 Context-Action-Result bullets per project, with numbers. **→ Done when:** 4 metric-bearing bullets are drafted.
- **H4 — LinkedIn + (optional) blog.** Update your profile with the right keywords; optionally draft a post on the MCP build. **→ Done when:** profile updated; post drafted or consciously skipped.
- **H5 — Repo hygiene + log.** Clean repos, pin deps, tag releases. **→ Done when:** both repos are public and tagged.
- **Interview angle:** deliver each project as a crisp 2-minute story.

---

# Phase 3 — Interview consolidation (Week 16)

## Week 16 — System design + rapid-fire + mocks · ~5 hrs
**Friday outcome:** two written system designs, a rated Q-bank, and one completed mock. *(Feeds: interview readiness)*
- **H1 — System design I.** Design RAG for 100M docs. **→ Done when:** a 1-page design with components + tradeoffs exists.
- **H2 — System design II.** Permission-aware enterprise RAG + a multi-agent data-platform sketch. **→ Done when:** two design sketches exist.
- **H3 — Rapid-fire.** Self-quiz the full Q-bank; rate confidence; restudy weak ones. **→ Done when:** every Q-bank row has a confidence rating.
- **H4 — Currency + behavioral.** Skim current top-model announcements; prep 3 STAR stories. **→ Done when:** a "current models" note + 3 behavioral stories exist.
- **H5 — Full mock.** Run a mock interview inside this Claude Project; capture feedback. **→ Done when:** one full mock is completed and gaps are noted.
- **Interview angle:** the whole loop, graded on architectural depth, metrics, failure-mode awareness, and currency.

---

## Definition of done (where you are at Week 16)
- **Two deployed projects** on AWS with measured results you can quote (recall@k + faithfulness for RAG; task success rate, tool-call accuracy, cost/latency for the agent).
- You can **build by hand and argue the managed alternative** for both RAG (Knowledge Bases) and agents (Bedrock Agents), with Azure mappings.
- You can speak fluently to: **RAG internals, hybrid retrieval, evaluation, agents/LangGraph, multi-agent, agent memory & context engineering, MCP (with spec version), agent security (indirect injection, lethal trifecta, least-privilege, sandboxing), guardrails/OWASP, LLMOps, and cost optimization.**
- A revision-ready **interview Q-bank** (in the tracker) and CV bullets in Context-Action-Result form.

## Optional certification (only if time allows — portfolio beats certs)
**AWS Certified AI Practitioner** (foundational, fast) or **AWS Certified Machine Learning Engineer – Associate** (deeper). Map-only learners can note the **Azure AI Engineer Associate** equivalent. Don't let cert prep displace the builds.
