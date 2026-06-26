# Progress Tracker — Agentic AI for Data Engineers (16-Week Track)

> Claude reads this at the **start** of every session and updates it at the **end**. Keep it honest — it drives re-planning if you fall behind. Source of truth for *what to do* is `curriculum.md`.

## Snapshot
| Field | Value |
|---|---|
| Start date | _fill in_ |
| Target end date (16 wks) | _fill in_ |
| Current week | 0 (setup) |
| Weeks completed | 0 / 16 |
| Hours logged | 0 / ~80 |
| Overall progress | 0% |
| Status | Not started |

**Setup checklist (Week 0):**
- [ ] Git repo + Python 3.11+ venv + `.env`
- [ ] AWS Bedrock model access (a Claude-tier + Titan/Cohere embeddings) callable via `boto3` Converse API
- [ ] Local fallback ready (Ollama + local embeddings) to keep costs near zero while learning
- [ ] Corpus chosen for Project 1; database chosen for Project 2
- [ ] Azure equivalents noted (Azure OpenAI, AI Search) — for mapping only

---

## Weekly progress
Status key: ⬜ Not started · 🟨 In progress · ✅ Done

| Wk | Topic | Status | Hrs | Date done | Artifact / link | Interview angle locked? |
|----|-------|:------:|:---:|-----------|-----------------|:----------------------:|
| 1 | LLM mental model + first Bedrock calls | ⬜ | | | | ⬜ |
| 2 | Prompting + tool calling + embeddings | ⬜ | | | | ⬜ |
| 3 | RAG architecture + ingestion & chunking | ⬜ | | | | ⬜ |
| 4 | Vector DBs + baseline RAG end-to-end | ⬜ | | | | ⬜ |
| 5 | Hybrid search + reranking + query transforms | ⬜ | | | | ⬜ |
| 6 | ⭐ Evaluation (recall@k, faithfulness) | ⬜ | | | | ⬜ |
| 7 | Productionize I: FastAPI + guardrails + safety | ⬜ | | | | ⬜ |
| 8 | ⭐ Deploy on AWS + managed (Knowledge Bases) vs self-hosted | ⬜ | | | | ⬜ |
| 9 | Agents: fundamentals + tool use (SQL) | ⬜ | | | | ⬜ |
| 10 | ⭐ LangGraph orchestration + memory & context engineering | ⬜ | | | | ⬜ |
| 11 | Multi-agent + human-in-the-loop | ⬜ | | | | ⬜ |
| 12 | ⭐ MCP server (the differentiator) | ⬜ | | | | ⬜ |
| 13 | ⭐ Agent eval + observability + security hardening | ⬜ | | | | ⬜ |
| 14 | ⭐ Deploy agent on AWS + Bedrock Agents comparison | ⬜ | | | | ⬜ |
| 15 | Polish, package, publish (READMEs, CV bullets) | ⬜ | | | | ⬜ |
| 16 | System design + rapid-fire + mock interviews | ⬜ | | | | ⬜ |

⭐ = highest-signal weeks. If time gets tight, protect these and the flagship deploys; compress elsewhere.

---

## Project 1 — Enterprise RAG (Weeks 3–8)
- [ ] Ingestion + chunking pipeline (with metadata)
- [ ] Vector store (pgvector/Chroma) + baseline retrieval
- [ ] Citations in answers
- [ ] Hybrid search (BM25 + vector + RRF) + reranker
- [ ] Eval harness + golden set
- [ ] FastAPI service + streaming + guardrails
- [ ] Deployed on AWS
- [ ] Bedrock Knowledge Bases comparison done
- [ ] README + architecture diagram + demo + metrics table

**Measured results (fill in — quote these in interviews):**
| Metric | Naive | Advanced | Notes |
|---|---|---|---|
| recall@10 | | | |
| faithfulness | | | |
| p50 latency | | | |
| cost / 1k queries | | | |

## Project 2 — Agentic data assistant + MCP (Weeks 9–15)
- [ ] Baseline agent with tools (NL → SQL → execute)
- [ ] LangGraph stateful graph + short-term memory
- [ ] Persistent vector-backed memory (episodic + semantic) + context compaction
- [ ] Multi-agent / supervisor pattern
- [ ] Human-approval gate + idempotent actions
- [ ] **MCP server** exposing the data source + agent as MCP client
- [ ] Agent eval (task success rate, tool-call accuracy)
- [ ] Tracing + cost/step caps
- [ ] Security hardening: least-privilege tools, sandboxed execution, indirect-injection test
- [ ] Deployed on AWS
- [ ] Bedrock Agents comparison done
- [ ] README + architecture diagram + demo + failure-mode write-up

**Measured results (fill in):**
| Metric | Value | Notes |
|---|---|---|
| task success rate | | |
| tool-call accuracy | | |
| avg cost / task | | |
| avg latency / task | | |

---

## Skills self-rating (1 = new, 5 = could lead it) — update every ~4 weeks
| Skill | Wk 4 | Wk 8 | Wk 12 | Wk 16 |
|---|:--:|:--:|:--:|:--:|
| LLM fundamentals & prompting | | | | |
| Embeddings & vector search | | | | |
| RAG (chunking, hybrid, rerank) | | | | |
| Evaluation (RAG + agents) | | | | |
| Agents & ReAct | | | | |
| LangGraph orchestration | | | | |
| Multi-agent patterns | | | | |
| Agent memory & context engineering | | | | |
| MCP | | | | |
| Guardrails / OWASP LLM | | | | |
| Agent security (indirect injection, least-privilege) | | | | |
| LLMOps (serving, tracing, cost) | | | | |
| AWS Bedrock (KB, Agents, Guardrails) | | | | |
| Azure mapping (Foundry, AI Search) | | | | |

---

## Interview Q-bank (grow weekly; rate confidence 1–5)
Add each week's "Interview angle" here after you've locked it. Revise from this list in Week 16.

| # | Question | From wk | Confidence |
|---|----------|:------:|:----------:|
| | Explain the context window as an engineering tradeoff. | 1 | |
| | Why do LLMs hallucinate, and what are the layers to reduce it? | 1 | |
| | Prompting vs fine-tuning vs RAG — decision criteria. | 2 | |
| | What is function calling and why is it the basis of agents? | 2 | |
| | How does your agent handle a long multi-step task without context degrading? | 10 | |
| | Episodic vs. semantic memory — how did you implement each? | 10 | |
| | What is indirect prompt injection and how do you defend an agent? | 13 | |
| | Explain the lethal trifecta and how you broke it in your design. | 13 | |
| | _add as you go..._ | | |

---

## Blockers / carryover
_Anything unfinished rolls here so the next session picks it up. Note API/cost issues, environment problems, concepts to revisit._

- 

---

## Weekly log
_One short entry per week: what you built, what clicked, what was hard, what to revisit._

**Week 0 (setup):** 

**Week 1:** 
