# Curriculum — Agentic AI for Data Engineers
### 16 weeks · ~5 hrs/week · ~80 hours total · cold-start GenAI → interview-ready agentic AI

This is the source of truth for *what* you study and build each week. Track *where you are* in `progress-tracker.md`. Designed for a data engineer with 5 YoE (strong Python/SQL/Spark/cloud) starting cold on LLMs, targeting interviews in ~4 months with two deployed, measured portfolio projects.

**Design rules:** every topic is high-yield and maps to real job requirements. No filler. Theory only as deep as the build needs, then deeper for interview prep. You build everything by hand first (to understand internals), then compare to the managed AWS service (the comparison is what senior interviews probe). AWS is primary; Azure is mapped in parallel so you can speak to both.

---

## The two flagship projects (these are your CV)

**Project 1 — Enterprise RAG over your data (Weeks 3–8).** A production-grade Retrieval-Augmented Generation service over a real document corpus: ingestion + chunking pipeline, vector store, hybrid search with reranking, a proper evaluation harness with quoted metrics, guardrails, and deployment on AWS — with a side-by-side comparison against Bedrock Knowledge Bases (managed RAG).

**Project 2 — Agentic data assistant with MCP (Weeks 9–15).** A stateful, multi-step agent (LangGraph) that answers questions over your database/warehouse, calls tools, and takes guarded actions — with **persistent vector-backed memory + context engineering**, exposed through a **Model Context Protocol (MCP) server**, **security-hardened** (indirect-injection defenses, least-privilege tools, sandboxed execution), and shipped with agent evaluation, full tracing, cost caps, and deployment on AWS — compared against Bedrock Agents (managed). The MCP piece is the most data-engineering-native agentic skill and your biggest differentiator.

Both end with: README, architecture diagram, demo recording, a metrics table, and a written "what I'd do at 100M docs / in production" section.

---

## Setup (do before Week 1, ~1 hr — counts as Week 0)
- **Repo + env:** a Git repo, Python 3.11+ venv, `.env` for secrets. Two project folders.
- **AWS Bedrock access:** in your AWS account, request model access for a current Claude-tier model + an embeddings model (Titan or Cohere). Confirm `boto3` can call the **Converse API**.
- **Azure (optional, for mapping):** note your Azure OpenAI + Azure AI Search equivalents; you don't need to build there, just be able to map.
- **Cost plan:** Bedrock dev usage is cheap — budget ~$20–40 total. To spend near-zero while learning, run a **local model via Ollama** (small LLM + local embeddings) for most weeks and switch to Bedrock for the cloud-deploy weeks (8, 14) and final demos.
- **Corpus:** pick a real document set for Project 1 (your team's docs, a platform's public docs, or a public dataset) and a real-ish database for Project 2 (a Postgres with a few tables, or a sample warehouse schema).

## Reference shelf (pull current links via the Project as you go)
Bedrock Converse API · Bedrock Knowledge Bases · Bedrock Agents + Guardrails · `boto3` · LangChain + **LangGraph** · LlamaIndex · pgvector / Chroma / OpenSearch · **RAGAS** (RAG eval) · **MCP specification** (note the current version) · FastAPI · Docker · LangSmith or Arize Phoenix (tracing) · OWASP LLM Top 10. *Azure equivalents:* Azure OpenAI · Azure AI Search · Azure AI Foundry Agent Service · Azure AI Content Safety · Semantic Kernel.

---

# Phase 0 — Foundations & first contact (Weeks 1–2)

## Week 1 — LLMs for engineers: the mental model + first calls
- **Theory:** Tokens and tokenization; the context window as a *budget* you manage; temperature/top-p and why output is probabilistic; what LLMs are good and bad at; *why* hallucination happens; the per-token cost model. The decision frame: **prompting vs. RAG vs. fine-tuning** — what each fixes and what it costs.
- **Build:** Set up the dev env. Enable Bedrock model access. Make your first calls via the Converse API (`boto3`); get clean **structured JSON output**; observe temperature effects. Write the one-line Azure OpenAI equivalent call.
- **Contributes to:** foundations.
- **Interview angle:** "Explain the context window as an engineering tradeoff." "Why do LLMs hallucinate, and what are the layers to reduce it?"

## Week 2 — Prompting that matters · tool calling · embeddings
- **Theory:** System vs. user prompts; few-shot; enforcing output schemas; **function/tool calling** (the mechanism every agent is built on); **embeddings** (what a vector is, cosine similarity, why semantic search finds meaning without shared keywords). First look at prompt injection.
- **Build:** (1) A structured extractor: messy text → validated typed JSON. (2) A tiny semantic search: embed ~20 docs, store vectors (Chroma/in-memory), retrieve by cosine similarity. (3) A minimal tool-calling demo where the model chooses a function.
- **Contributes to:** foundations.
- **Interview angle:** "Prompting vs. fine-tuning vs. RAG — your decision criteria." "What is function calling and why is it the basis of agents?"

---

# Phase 1 — Project 1: Enterprise RAG (Weeks 3–8)

## Week 3 — RAG architecture + ingestion & chunking
- **Theory:** The full pipeline: ingest → chunk → embed → store → retrieve → augment → generate. **Chunking strategies** (fixed-size + overlap, semantic/sentence-aware, hierarchical parent-child) and why chunking quality dominates the whole system. Metadata and why it matters.
- **Build:** Build the ingestion pipeline for your corpus: load, clean, chunk with overlap, attach metadata (source, section, date). Embed (Bedrock or local) and store in **pgvector** or Chroma.
- **Contributes to:** Project 1.
- **Interview angle:** "Walk me through your chunking strategy and its tradeoffs." "How does metadata improve retrieval and enable access control?"

## Week 4 — Vector databases + baseline RAG end-to-end
- **Theory:** How vector DBs work; **ANN indexes (HNSW)** at a working level and why you don't do exact search at scale; distance metrics; **selection criteria** across pgvector, Chroma, Pinecone, Qdrant, Weaviate, OpenSearch (managed vs. self-hosted).
- **Build:** Wire retrieval → context assembly → LLM → **answer with citations**. You now have a working naive RAG behind a notebook/CLI. Sanity-check on real questions.
- **Contributes to:** Project 1.
- **Interview angle:** "How would you choose a vector store for this workload?" "What's an ANN index and what's the recall/latency tradeoff?"

## Week 5 — Advanced retrieval: hybrid search · reranking · query transforms
- **Theory:** Why pure vector search fails on exact tokens (IDs, part numbers, emails); **hybrid search** (dense + sparse/BM25); **Reciprocal Rank Fusion (RRF)**; **cross-encoder reranking** (why first-stage retrieval only gets "likely" candidates); query rewriting and **HyDE**.
- **Build:** Add BM25 + vector hybrid retrieval fused with RRF; add a reranker; add query rewriting. Keep the naive version so you can compare next week.
- **Contributes to:** Project 1.
- **Interview angle:** "Why is vector search bad for part numbers, and how do you fix it?" "Explain RRF and cross-encoder reranking."

## Week 6 — Evaluation: the credibility module ⭐
- **Theory:** Why eval is the single biggest signal of real LLM experience. **Retrieval metrics** (recall@k, precision@k, MRR); **generation metrics** (faithfulness/groundedness, answer relevance, context precision/recall); golden datasets; using RAGAS or a custom harness.
- **Build:** Create a golden Q/A set (~20–30 pairs). Build an eval harness and compute **recall@k + faithfulness for naive vs. advanced retrieval**. Record the numbers — they go on your CV and into interviews.
- **Contributes to:** Project 1 (this is what makes it senior-grade).
- **Interview angle:** "Walk me through an evaluation you designed." "What was your recall@10, and how did reranking change it?"

## Week 7 — Productionize I: API · streaming · guardrails · safety
- **Theory:** Serving with **FastAPI**; streaming responses; the **OWASP LLM Top 10** (prompt injection, sensitive-data disclosure, etc.); **guardrails** (input/output validation, PII handling, content filtering); cost/latency basics.
- **Build:** Wrap the RAG system in a FastAPI service with streaming; add input/output guardrails (validation + a safety check, e.g., Bedrock Guardrails or a checking step); add structured logging.
- **Contributes to:** Project 1.
- **Interview angle:** "How do you defend against prompt injection?" "Name OWASP LLM risks and concrete mitigations."

## Week 8 — Productionize II: deploy on AWS + managed vs. self-hosted ⭐
- **Theory:** **Bedrock Knowledge Bases** (S3 sync, managed chunking, Titan/Cohere embeddings, vector backends like OpenSearch Serverless / Aurora pgvector, hybrid search) vs. your hand-built pipeline — when to use which. Azure mapping (**Azure AI Search** + Azure OpenAI). Cost levers (prompt caching, batch, model routing). Observability (LangSmith/Phoenix).
- **Build:** Containerize (Docker); deploy the API to AWS (Lambda + API Gateway, or ECS/Fargate; vectors in Aurora pgvector or OpenSearch Serverless; Bedrock for inference). Stand up a **parallel Bedrock Knowledge Base** on the same corpus and compare quality + effort. Add tracing + a cost log. **Finalize Project 1**: README, architecture diagram, metrics table, "what I'd change at 100M docs."
- **Contributes to:** Project 1 — **DONE.**
- **Interview angle:** "Managed Knowledge Bases vs. self-hosted RAG — argue both sides." "How did you cut inference cost?"

---

# Phase 2 — Project 2: Agentic data assistant + MCP (Weeks 9–15)

> **Time-budget note:** Weeks 10 and 13 now run hot (~6–7 hrs) because they absorb persistent memory + context engineering (W10) and agent security in depth (W13). Reclaim the time by capping retrieval tuning in Week 5 and productionize polish in Weeks 7–8 — both reuse skills you already have. Any spillover is carried in the tracker; protect the ⭐ weeks over RAG polish.

## Week 9 — Agents: fundamentals + tool use
- **Theory:** What "agentic" means vs. a chatbot — **sustained, multi-step execution toward a goal**, not single-shot responses; the **ReAct loop** (reason → act → observe); tool/function calling in depth; when *not* to use an agent.
- **Build:** Build a first agent with 2–3 tools, one of which queries your SQL database/warehouse (natural language → SQL → execute → answer). Make it loop until the task is done.
- **Contributes to:** Project 2.
- **Interview angle:** "What makes a system agentic rather than a chatbot?" "Describe the ReAct loop with an example."

## Week 10 — LangGraph orchestration + memory & context engineering ⭐ *(runs hot, ~6–7 hrs)*
- **Theory:** Why **graphs with explicit state** beat simple chains; nodes, edges, conditional routing, state; common **failure modes** (infinite loops, wrong-tool selection, runaway cost) and how to contain them. Then the part most plans skip: **memory & context engineering** for long runs — short-term vs. **persistent long-term memory** (**episodic** = what happened, **semantic** = learned facts), vector-backed memory (reuses your Phase 1 store), **context compaction/summarization** as a run grows, retrieving the *right* memory at each step, and avoiding **context rot / poisoning**.
- **Build:** Rebuild the agent as a **LangGraph** graph (NL → plan → SQL → execute → validate → summarize) with conditional routing. Add **vector-backed persistent memory** (reuse the Phase 1 vector store) and a **compaction step** so a long multi-step task doesn't blow the context budget.
- **Contributes to:** Project 2.
- **Interview angle:** "Why a graph over a chain?" "How does your agent handle a 40-step task without the context degrading?" "Episodic vs. semantic memory — how did you implement each?"

## Week 11 — Multi-agent + human-in-the-loop
- **Theory:** Multi-agent patterns (**supervisor/orchestrator + specialists**, planner/executor); agent-to-agent delegation; **human approval gates** for high-risk actions; idempotency of actions.
- **Build:** Add a supervisor pattern or a second specialist agent; insert a **human-approval step** before any write/action; make actions idempotent and logged.
- **Contributes to:** Project 2.
- **Interview angle:** "When do multi-agent systems genuinely help vs. just add complexity?" "How do you let an agent take actions *safely*?"

## Week 12 — MCP (Model Context Protocol): the differentiator ⭐
- **Theory:** What MCP is and why it matters — a **standard way to expose tools, resources, and context** to any AI system, decoupling your data/tools from any single agent or app; server vs. client; the **spec (know the current version)**; how **authentication, authorization, and audit** should work in an enterprise.
- **Build:** Write an **MCP server** that exposes a data source (your database/warehouse or files) as tools/resources, then connect your agent to it as an MCP client. This is the headline of Project 2.
- **Contributes to:** Project 2.
- **Interview angle:** "What is MCP and why does it matter for enterprises?" "How should auth and audit work for an MCP server exposing a database?" *(Interviewers screen for whether you can name the spec version — know it.)*

## Week 13 — Agent evaluation + observability + security hardening ⭐ *(runs hot, ~6–7 hrs)*
- **Theory:** Evaluating agents is harder than RAG — **task success rate**, **trajectory/step evaluation**, **tool-call correctness**, cost/latency per task. Tracing (LangSmith/Phoenix; OpenTelemetry). Then **agent security in depth** (the sharpest risk for an agent that reads data *and* acts): **indirect (second-order) prompt injection** — a poisoned document or tool output hijacks the agent, very different from the direct injection in Weeks 2/7; the **"lethal trifecta"** (private-data access + exposure to untrusted content + ability to exfiltrate = the dangerous combination); **least-privilege tool scoping**; and **sandboxing tool execution**.
- **Build:** Build an agent eval (tasks with expected outcomes; measure **success rate + tool-call accuracy**); add full tracing + a per-task **cost/latency log**; add a hard **step/cost cap**. Then a **security hardening pass**: scope each tool to least privilege, **sandbox** the SQL/action execution, and add an **indirect-injection test** to your eval set (feed a poisoned document and confirm the agent isn't hijacked).
- **Contributes to:** Project 2 (senior-grade signal).
- **Interview angle:** "How do you evaluate an agent?" "What's indirect prompt injection and how do you defend an agent against it?" "Explain the lethal trifecta and how you broke it in your design."

## Week 14 — Productionize the agent on AWS + managed comparison ⭐
- **Theory:** **Bedrock Agents** (Action Groups = Lambda via OpenAPI schema, Knowledge Bases, Guardrails, GA multi-agent, AgentCore) vs. your LangGraph build — managed vs. code-first tradeoffs. Azure mapping (**Foundry Agent Service** + Copilot Studio + Semantic Kernel). Production concerns: runaway loops, cost caps, retries, rollback, permission enforcement.
- **Build:** Containerize + deploy the agent service to AWS; stand up a **parallel Bedrock Agent** (Action Groups → Lambda) on a similar task and compare. Wire guardrails + cost caps in prod.
- **Contributes to:** Project 2.
- **Interview angle:** "Bedrock Agents vs. LangGraph — when each?" "Walk me through operational safety for a production agent."

## Week 15 — Polish, package, publish
- **Theory:** How to present AI projects for senior roles: lead with **metrics + design decisions + failure modes**, not a tool list; the Context-Action-Result bullet format.
- **Build:** Finalize Project 2 (README, architecture diagram, demo recording/GIF, metrics, failure-mode write-up). Write **2 strong CV bullets per project** (Context-Action-Result with numbers). Optional but high-value: a short **LinkedIn/blog post on the MCP build** (boosts visibility and signals depth). Refresh your LinkedIn with the right keywords (RAG, vector DBs, LangGraph, MCP, evaluation, LLMOps).
- **Contributes to:** both projects — **PACKAGED.**
- **Interview angle:** deliver each project as a crisp 2-minute story.

---

# Phase 3 — Interview consolidation (Week 16)

## Week 16 — System design + rapid-fire + mocks
- **Theory/Build:** **AI system design drills** — design RAG for 100M docs; design a **permission-aware enterprise RAG**; design a multi-agent data platform. **Rapid-fire concept review** across everything (embeddings, chunking, hybrid/RRF/rerank, eval metrics, ReAct, multi-agent, MCP, guardrails, cost, managed-vs-self-hosted). **Frontier-model fluency** — know today's top models and skim recent announcements (interviewers screen for staying current). Behavioral prep. Then run **full mock interview loops** inside this Claude Project.
- **Contributes to:** interview readiness.
- **Interview angle:** the whole loop, graded on architectural depth, metrics, failure-mode awareness, and currency.

---

## Definition of done (where you are at Week 16)
- **Two deployed projects** on AWS, each with measured results you can quote (recall@k and faithfulness for RAG; task success rate, tool-call accuracy, and cost/latency for the agent).
- You can **build by hand and argue the managed alternative** for both RAG (Knowledge Bases) and agents (Bedrock Agents), with Azure mappings.
- You can speak fluently to: **RAG internals, hybrid retrieval, evaluation, agents/LangGraph, multi-agent, agent memory & context engineering, MCP (with spec version), agent security (indirect injection, lethal trifecta, least-privilege, sandboxing), guardrails/OWASP, LLMOps, and cost optimization.**
- A revision-ready **interview Q-bank** (in the tracker) and CV bullets in Context-Action-Result form.

## Optional certification (only if time allows — portfolio beats certs)
If you want a credential to pair with the projects: **AWS Certified AI Practitioner** (foundational, fast) or **AWS Certified Machine Learning Engineer – Associate** (deeper). Map-only learners can note the **Azure AI Engineer Associate** equivalent. Don't let cert prep displace the builds.
