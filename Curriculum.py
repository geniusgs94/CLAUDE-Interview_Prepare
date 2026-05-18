"""
System Design

Phase 1: Foundations (Weeks 1–3)
You cannot design a data system without these. Interviewers test them indirectly in every question — if your fundamentals are shaky, every subsequent answer leaks.
Week 1: The Vocabulary of Scale

Latency vs throughput vs bandwidth — precise definitions, why confusing them costs you the interview
Back-of-the-envelope estimation — powers of 2, powers of 10, time conversions (seconds in a day, etc.)
QPS / RPS math — how to estimate from DAU, MAU, and user behavior
Storage estimation — rows × bytes × retention × replication
Drill-heavy week. I'll make you estimate Swiggy's order QPS, Hotstar's bandwidth during IPL finals, PhonePe's transaction storage per year.

Week 2: Distributed Systems Fundamentals

CAP theorem — what it actually says (and the 90% of candidates who get it wrong)
PACELC — the extension that matters more than CAP in practice
Consistency models — strong, eventual, causal, read-your-writes, monotonic
Replication — leader-follower, multi-leader, leaderless
Partitioning vs sharding — range, hash, consistent hashing
The fallacies of distributed computing

Week 3: Storage Fundamentals

OLTP vs OLAP — why you can't run analytics on your production Postgres
Row stores vs column stores — and why Parquet/ORC exist
B-trees vs LSM trees — when each wins (Postgres vs Cassandra intuition)
Indexing basics — primary, secondary, covering, composite
File formats: CSV → JSON → Avro → Parquet → ORC — trade-offs and when each fits


Phase 2: Data Engineering Core (Weeks 4–7)
This is where DE system design diverges from generic backend system design. Most candidates from QA/backend backgrounds underweight this phase and fail interviews on data modeling questions.
Week 4: Batch Processing & Data Warehouses

Batch processing mental model — when latency in hours is acceptable
MapReduce → Spark — why Spark won, RDD → DataFrame → Dataset
Data warehouse architecture — Snowflake, BigQuery, Redshift internals
Dimensional modeling — star schema, snowflake schema, fact vs dimension tables
Slowly Changing Dimensions (SCD Type 1, 2, 3) — interviewers love SCD2
Real example: how Flipkart models order analytics

Week 5: Stream Processing & Kafka Deep-Dive

Batch vs stream vs micro-batch — when to pick which
Kafka architecture — brokers, topics, partitions, consumer groups, ISR
Partitioning strategies — why your partition key choice can sink the design
Delivery semantics — at-most-once, at-least-once, exactly-once (and why EOS is hard)
Retention, compaction, tiered storage
Kafka alternatives — Pulsar, Kinesis, Redpanda — and when to pick them
Real example: how Swiggy/Zomato handle order event streams

Week 6: Stream Processing Engines & Lambda/Kappa

Flink vs Spark Streaming vs Kafka Streams — real trade-offs
Windowing — tumbling, sliding, session
Watermarks and late data handling (this is where senior candidates are separated from mid-level)
Lambda architecture vs Kappa architecture
Exactly-once in practice — checkpointing, idempotent producers

Week 7: Data Lakes, Lakehouses & Modern Formats

Data lake vs warehouse vs lakehouse — what actually changed
Delta Lake vs Apache Iceberg vs Apache Hudi — the table format wars
ACID on object storage — how it works, why it matters
Medallion architecture — bronze/silver/gold
Schema evolution and time travel
Real example: how Uber built Hudi for their needs


Phase 3: Pipelines, Modeling & Operations (Weeks 8–9)
Week 8: Orchestration, Data Quality & Modeling

Airflow deep-dive — DAGs, operators, executors, scheduling pitfalls
Airflow alternatives — Dagster, Prefect, Temporal — when each wins
Idempotency, backfills, late-arriving data
Data modeling for analytics — Kimball vs Inmon vs Data Vault
dbt and the analytics engineering layer
Data contracts, data quality (Great Expectations, Soda)

Week 9: CDC, Real-Time Analytics & Serving

Change Data Capture — Debezium, log-based vs query-based CDC
Real-time OLAP — Druid, Pinot, ClickHouse — trade-offs
Serving layers for ML features — online vs offline feature stores
Caching strategies for data systems — Redis, materialized views
Real example: how Zomato/Uber power live dashboards


Phase 4: Interview Mastery (Weeks 10–12)
Week 10: Full Mock Interviews — Common Questions

"Design the data platform for Swiggy's order analytics"
"Design a real-time fraud detection pipeline for PhonePe"
"Design Hotstar's video viewing analytics for IPL"
Full 45-min format with ruthless feedback

Week 11: Full Mock Interviews — Harder Questions

"Design a feature store for Flipkart recommendations"
"Design a data lineage and catalog system"
"Design a multi-tenant data warehouse for a SaaS company"
Deep-dive rounds — I'll drill into ONE component for 20 min

Week 12: Polish, Weak-Spot Remediation, Behavioral Framing

Remediation of your lowest-scored topics from the tracker
How to structure the 45 minutes — minute-by-minute
How to handle "I don't know" gracefully
Communicating trade-offs like a senior engineer, not reciting facts
Final diagnostic mock and readiness signal
"""


'''
Philosophy
This plan is built around one principle: scenarios before theory. You already know definitions. What gets you rejected is freezing when the interviewer says "You've got 2 billion rows of order data with heavy skew on merchant_id — walk me through how you'd design the pipeline." Every week leads with situations you'll actually face in the chair, and backfills theory only where gaps show up.
Your QA background is not a weakness to hide — it's a weapon to deploy. Data quality, edge-case thinking, testing rigor, and validation pipelines are things most DE candidates hand-wave. You won't.

Week 1 — SQL Foundations Under Pressure
Goal: Handle any SQL question thrown at a Senior DE screen without hesitating.
Day 1–2: Window Functions Deep Dive

ROW_NUMBER, RANK, DENSE_RANK — when each one matters and when interviewers try to trip you up with ties
LEAD/LAG for session analysis, churn detection, consecutive-day problems
Running totals, moving averages with ROWS BETWEEN
Scenario: "Swiggy wants to find users whose order value dropped for 3 consecutive months. Write the query."

Day 3–4: CTEs, Subqueries & Query Structure

Recursive CTEs (org hierarchy, category trees — Flipkart uses these)
CTE vs subquery vs temp table — when to pick which, and why it matters for the optimizer
Scenario: "Given a table of employee-manager pairs with NULLs for bad data, build the full reporting chain and find broken links."

Day 5–6: Aggregation & Grouping Edge Cases

GROUP BY with NULLs, HAVING vs WHERE, GROUPING SETS / ROLLUP / CUBE
Conditional aggregation (CASE inside SUM/COUNT)
Scenario: "Razorpay needs a single query showing daily, weekly, and monthly transaction volumes side by side."

Day 7: First Drill Session

5 timed SQL problems (20 min each), scored pass/bubble/fail
Debrief: identify patterns in mistakes


Week 2 — SQL: Optimization & The "Why" Questions
Goal: Answer "why is this query slow?" and "how would you fix it?" — the questions that separate Senior from Mid.
Day 1–2: Indexing & Execution Plans

B-tree vs hash vs bitmap indexes — when each is appropriate
Composite index column ordering and the left-prefix rule
Reading EXPLAIN output: seq scan, index scan, hash join, nested loop, sort
Scenario: "Your daily Flipkart seller-payout query takes 45 minutes. Here's the EXPLAIN plan. What's wrong and what do you change?"

Day 3–4: Join Performance & Anti-Patterns

Join algorithms: nested loop, hash join, merge join — which the optimizer picks and why
The N+1 query problem in reporting
Self-joins, cross joins, anti-joins (LEFT JOIN WHERE NULL vs NOT EXISTS vs NOT IN with NULLs)
Scenario: "A Meesho analyst wrote a query joining 5 tables that returns correct results but takes 12 minutes. Diagnose and fix."

Day 5–6: Advanced Patterns Interviewers Love

De-duplication strategies (ROW_NUMBER vs DISTINCT ON vs GROUP BY — trade-offs)
Gap-and-island problems (consecutive sessions, streaks)
Pivot/unpivot without PIVOT keyword
Scenario: "CRED wants to identify users who made payments in at least 5 consecutive months. Handle gaps, NULLs, and duplicate records."

Day 7: Timed SQL Mock (20 min)

3 scenario-based problems, interviewer-style follow-ups after each


Week 3 — Python for Data Engineering (Not Data Science)
Goal: Write Python that a Senior DE would actually ship — not Leetcode, not Jupyter notebook hacks.
Day 1–2: Data Structures & Complexity That Matter

dict/set internals (hash tables), defaultdict, Counter, OrderedDict
When to use list vs deque vs heap — with pipeline examples
Generator expressions for memory-efficient streaming
Scenario: "You need to deduplicate 500M records from a file that doesn't fit in memory. Walk me through your Python approach."

Day 3–4: File Handling & ETL Patterns

Reading CSV/JSON/Parquet: chunked processing, schema validation
Context managers, pathlib, error handling for production pipelines
Idempotency patterns: how to make a Python ETL script safe to re-run
Scenario: "Zepto's vendor sends a daily CSV that sometimes has encoding errors, missing columns, and duplicate headers mid-file. Write the ingestion code."

Day 5–6: OOP for Pipelines & Testing

When classes help (pipeline stages, config management, retry logic) vs when functions are enough
Decorators for logging, timing, retry
Writing testable ETL code — unit tests for transforms, mocking external services
Scenario: "Design a Python class structure for a pipeline that ingests from 3 sources, validates, transforms, and loads to a warehouse. Show me the error-handling strategy."

Day 7: Python Drill

4 problems: 2 coding + 2 design/walkthrough, scored


Week 4 — PySpark Fundamentals & Mental Model
Goal: Understand what Spark actually does under the hood — not just the API.
Day 1–2: Architecture & Execution Model

Driver, executors, tasks, stages, shuffle boundaries
Lazy evaluation — why it matters, how the DAG is built
Narrow vs wide transformations — why this distinction determines performance
Scenario: "You see 200 tasks in Stage 1 and 50,000 tasks in Stage 2. What happened and is this a problem?"

Day 3–4: DataFrame API Mastery

select, filter, groupBy, agg, join, withColumn, when/otherwise
UDFs: why they're slow, pandas UDFs as the alternative
Column expressions vs Python functions — the performance cliff
Scenario: "Rewrite this PySpark code that uses 4 UDFs. Make it 10x faster without changing the logic."

Day 5–6: RDD vs DataFrame vs Dataset

When RDD is still the right answer (custom partitioning, low-level control)
Catalyst optimizer — what it can and can't optimize
Schema enforcement: StructType, handling schema evolution
Scenario: "Your team inherited an RDD-based pipeline from 2018. When do you migrate to DataFrames and when do you leave it alone?"

Day 7: PySpark Drill

3 coding problems + 1 architecture walkthrough


Week 5 — PySpark: Performance, Failures & Debugging
Goal: Handle the "your Spark job is failing/slow — fix it" questions that are guaranteed at Senior level.
Day 1–2: Partitioning & Shuffles

Hash partitioning, range partitioning, repartition vs coalesce
Shuffle: what triggers it, why it's expensive, how to minimize it
spark.sql.shuffle.partitions — when 200 is wrong and what to set instead
Scenario: "A daily aggregation job at PhonePe shuffles 800 GB. Walk me through how you'd reduce it."

Day 3–4: Joins & Skew

Broadcast join: when it works, size limits, broadcast hint
Sort-merge join vs shuffle hash join
Skew handling: salting, key splitting, AQE skew join optimization
Scenario: "A join on user_id is failing OOM because 5% of users generate 60% of events. Fix it."

Day 5–6: Debugging & Failure Modes

Reading Spark UI: stages, tasks, shuffle read/write, GC time
OOM: driver vs executor, where to look first
Spill to disk, data locality, speculative execution
Scenario: "Your nightly job that ran fine for 6 months suddenly takes 4x longer. Nothing changed in the code. Diagnose."

Day 7: PySpark Failure-Mode Mock

4 debugging scenarios, talk-through format (no code — just diagnosis and plan)


Week 6 — Data Modeling: Think Like an Architect
Goal: Design schemas that interviewers at Flipkart, Swiggy, and Razorpay would approve.
Day 1–2: OLTP vs OLAP & Normalization

1NF through 3NF — with real examples, not textbook definitions
When to denormalize and what breaks when you do
OLTP schema design for a payments system vs OLAP for analytics
Scenario: "Design the OLTP schema for Razorpay's core payment processing. Now design the OLAP schema the analytics team will query."

Day 3–4: Dimensional Modeling

Star schema vs snowflake — trade-offs, not just definitions
Fact tables: transaction facts, periodic snapshots, accumulating snapshots
Dimension tables: conformed dimensions, junk dimensions, degenerate dimensions
Slowly Changing Dimensions: Type 1, 2, 3 — when to use each
Scenario: "Swiggy wants to track order lifecycle from placement to delivery with the ability to analyze historical changes in restaurant ratings. Design the model."

Day 5–6: Modeling for Scale

Partitioning strategies for fact tables (date, region, tenant)
Data vault basics: hubs, links, satellites — when it beats star schema
Modeling for real-time vs batch — different constraints
Scenario: "Flipkart's product catalog has 500M SKUs with attributes that vary wildly by category. Design a flexible model."

Day 7: Modeling Drill

2 end-to-end schema design problems (whiteboard-style), scored


Week 7 — System Design & Architecture for Data Engineers
Goal: Answer "design the data platform for X" without rambling.
Day 1–2: Batch Pipeline Architecture

Source → Ingestion → Storage → Transform → Serve pattern
Choosing storage: S3/HDFS, partitioning strategy, file formats (Parquet vs ORC vs Avro)
Orchestration: Airflow DAG design, idempotency, backfill strategies
Scenario: "Design the daily batch pipeline for Zomato's restaurant analytics — from raw event logs to a dashboard showing revenue, ratings, and delivery times per city."

Day 3–4: Streaming & Real-Time

Kafka basics: topics, partitions, consumer groups, offsets
Spark Structured Streaming: watermarks, output modes, exactly-once
Lambda vs Kappa architecture — when each makes sense
Scenario: "Zepto needs real-time inventory tracking across 200 dark stores. Design the streaming pipeline."

Day 5–6: Data Quality & Governance

Data quality frameworks: Great Expectations, Deequ, custom checks
Lineage tracking, data contracts, schema registries
This is where your QA background becomes your superpower — frame data quality as testing rigor applied to pipelines
Scenario: "You're the first Senior DE at a Series B startup. There's no data quality framework. What do you build in the first 90 days?"

Day 7: Architecture Mock

1 full system design (45 min), scored like a real interview


Week 8 — Behavioral: Turning QA Into Your Edge
Goal: Tell stories that make interviewers think "this person owns problems and ships solutions."
Day 1–2: Building Your Story Bank

Map your QA experience to DE-relevant stories: 8–10 stories covering ownership, conflict, failure, ambiguity, impact
Frame QA as strength: "I built automated validation pipelines before I even became a DE — quality is in my DNA"
Every story gets the STAR treatment: Situation (2 sentences), Task (1 sentence), Action (bulk of the answer — specific, technical, YOUR actions), Result (metrics)

Day 3–4: Amazon-Style Leadership Principles

Ownership, Bias for Action, Dive Deep, Earn Trust, Deliver Results, Customer Obsession
Practice: one polished story per LP
Drill: "Tell me about a time you found a critical issue that no one else noticed" — your QA background makes this a layup

Day 5–6: Tricky Behavioral Questions

"Why are you switching from QA to DE?" — frame as evolution, not escape
"What's a technical decision you disagreed with?" — show you can disagree and commit
"Tell me about a time you failed" — show learning, not excuses
Drill: 3 behavioral questions, critiqued on STAR structure, specificity, and ownership language

Day 7: Behavioral Mock

4 behavioral questions (10 min each), scored


Week 9 — Integration: Cross-Topic Scenarios
Goal: Handle interview questions that span multiple topics — because real interviews don't stay in one lane.
Day 1–2: SQL + Data Modeling Combos

"Here's a business requirement. Design the schema. Now write the query."
Optimizing queries against the schema you just designed
Scenario: "PhonePe wants a fraud detection report. Design the data model, write the detection query, and explain how you'd optimize it for 100M daily transactions."

Day 3–4: PySpark + Architecture Combos

"Here's a pipeline that's breaking. Diagnose, fix, and redesign."
Choosing between SQL-based and PySpark-based solutions
Scenario: "Meesho's seller onboarding pipeline processes 50K applications/day. It's slow, has duplicates, and occasionally loses records. Fix the pipeline and add data quality checks."

Day 5–6: Full-Stack DE Scenarios

End-to-end: requirements → modeling → pipeline → quality → query → optimization
Scenario: "You're building the analytics platform for a new Swiggy feature: 10-minute grocery delivery. Walk me through everything from raw events to the CEO's dashboard."

Day 7: Cross-Topic Mock

60-min mock covering all areas


Week 10 — Mock Interview Week 1
Goal: Simulate real pressure. Get scored. Fix gaps.
Mock 1 (Day 1–2): Large Product Company Style (Flipkart/Amazon)

20 min SQL (hard scenario + optimization follow-up)
15 min PySpark (debugging a failing job)
15 min Data Modeling (dimensional model design)
10 min Behavioral (2 LP questions)
Full scorecard after

Mock 2 (Day 3–4): Startup Style (Zepto/Razorpay/CRED)

Focus: breadth, speed, pragmatism over perfection
Expect "how would you build this from scratch with a 2-person team?"
Full scorecard after

Mock 3 (Day 5–6): System Design Heavy (Swiggy/PhonePe)

30 min system design + 15 min deep-dive on one component + 15 min behavioral
Full scorecard after

Day 7: Gap Analysis

Review all 3 scorecards
Update weak spots in progress tracker
Build targeted drills for Week 11


Week 11 — Targeted Gap Closure
Goal: Attack whatever Week 10 exposed as weak.
This week is intentionally unstructured. Based on mock interview scorecards, we focus entirely on:

Weakest topic area (extra scenarios + drills)
Most common mistake patterns (e.g., vague answers, missing trade-offs, incomplete solutions)
Speed: if you're too slow, timed drills with strict cutoffs
Depth: if you're too shallow, "why?" chains until you hit bedrock


Week 12 — Final Mocks & Confidence Building
Goal: Walk into interviews feeling like you belong.
Mock 4 (Day 1–2): Hardest Possible — "Rejection Round"

Intentionally harder than real interviews
Adversarial follow-ups, ambiguous requirements, curveball questions
If you survive this, real interviews feel easy

Mock 5 (Day 3–4): Realistic — "Offer Round"

Calibrated to actual Senior DE bar
Clean scorecard = you're ready

Day 5–6: Story Polish & Quick-Fire Drills

Behavioral stories: final polish, record yourself (in writing), trim fat
SQL/PySpark quick-fire: 10 problems in 60 minutes
Data modeling: 2 rapid schema designs (15 min each)

Day 7: Final Review

Review entire progress tracker
Confidence check: which topics would you be happy to get in an interview? Which ones still scare you?
Game plan for the first real interview


Ongoing (Every Week)

2–3 scenario-based drills on weak areas (refreshed based on progress tracker)
1 timed SQL problem daily (15–20 min max)
1 behavioral story rehearsal per week (different story each time)
Read one engineering blog post per week from target companies (Flipkart Tech, Uber Engineering, Swiggy Bytes, etc.) — use these as conversation fuel in interviews'''


'''
# 14-Week Curriculum: GenAI for Data Engineers

**Time:** 5 hours/week (1 hour × 5 days, or 2.5 hours × 2 days, or whatever works)
**Total:** ~70 hours over 14 weeks
**Stack:** Free APIs (Gemini Flash) + open source tools
**Outcome:** 3 portfolio projects, daily AI workflows, resume-ready

---

## Curriculum Structure

| Weeks | Phase | Outcome |
|-------|-------|---------|
| 1-3 | Foundations | LLM APIs, structured outputs, function calling |
| 4-5 | SQL Agent Project | **Project #1**: Natural-language SQL agent |
| 6-9 | Embeddings + RAG | **Project #2**: Data catalog RAG bot |
| 10-11 | Cost + Production | Make your projects production-ready |
| 12-13 | Data Pipeline Agent | **Project #3**: AI-augmented pipeline assistant |
| 14 | Polish + Deploy | Live demo, resume, LinkedIn |

---

# PHASE 1: FOUNDATIONS (Weeks 1-3)

## Week 1: Your First LLM API Calls

**Total time:** 5 hours
**Goal:** Call Gemini API from Python. Generate text. Understand prompts.

### Hour 1: Setup + First Call
- Get Gemini API key from aistudio.google.com
- Run `pip install google-genai`
- Write a "hello LLM" script: send a prompt, print the response
- Try 5 different prompts. Notice how responses change.

```python
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain Apache Airflow in 2 sentences."
)
print(response.text)
```

### Hour 2: System Prompts Deep Dive
- System prompt = persistent behavior (set role, tone, constraints)
- User prompt = the specific request
- Practice: Make the same user prompt give wildly different outputs with different system prompts.

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=genai.types.GenerateContentConfig(
        system_instruction="You are a senior data engineer. Give terse, technical answers. No fluff."
    ),
    contents="What's the difference between OLTP and OLAP?"
)
```

### Hour 3: Build 3 Useful Utilities
- `summarize_log(text)` — takes raw log text, returns short summary
- `classify_error(error_text)` — returns severity LOW/MEDIUM/HIGH
- `extract_table_names(sql)` — given SQL, returns list of table names referenced

### Hour 4: Error Handling
- API calls fail. Network errors, rate limits, malformed responses.
- Install `tenacity`. Add retry decorators with exponential backoff.
- Test by disconnecting your wifi mid-call.

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def safe_call(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text
```

### Hour 5: Mini-Project — SQL Query Explainer
Build a CLI tool: paste a SQL query, get a plain-English explanation of what it does.

```bash
$ python explain_sql.py "SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON o.user_id = u.id WHERE u.signup_date > '2024-01-01' GROUP BY u.name HAVING COUNT(o.id) > 5"

→ "This query finds the names of users who signed up after January 1, 2024, 
   along with their order counts, but only includes users with more than 5 orders."
```

**Push this to GitHub.** Repo: `sql-query-explainer`. Add a README. This is your first artifact.

### Week 1 Resume Bullet (Draft):
*"Built a CLI tool using Gemini API that translates SQL queries into plain-English explanations, with retry-resilient error handling."*

---

## Week 2: Structured Outputs (THE Most Important Week)

**Total time:** 5 hours
**Goal:** Get reliable, typed data from LLM responses. This is what makes LLMs production-usable.

### Hour 1: Why Structured Outputs Matter
- Raw text outputs break downstream code (different wording each time)
- JSON-in-system-prompt: works but unreliable (hallucinated keys, wrong types)
- **Structured output mode**: AI guaranteed to match a schema you define
- Read: Gemini's "Structured Output" docs (30 mins)

### Hour 2: Pydantic + Gemini Structured Outputs
- Pydantic = Python data validation. You already use it in FastAPI.
- Define a Pydantic model → Gemini guarantees output matches it.

```python
from pydantic import BaseModel
from typing import Literal

class TicketAnalysis(BaseModel):
    summary: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    affected_pipeline: str
    estimated_records_affected: int
    suggested_action: str

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"Analyze this incident: {ticket_text}",
    config=genai.types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=TicketAnalysis,
    )
)

# Direct parsing
result: TicketAnalysis = response.parsed
print(result.severity)  # Guaranteed to be one of LOW/MEDIUM/HIGH/CRITICAL
```

### Hour 3: Practice With Real Data Engineering Schemas

Convert these to structured-output extractors:
1. **Airflow task failure** → extract: task_id, dag_id, exception_type, retry_count, root_cause_hypothesis
2. **Spark job metrics** → extract: job_id, duration_sec, records_processed, shuffle_read_mb, bottleneck_stage
3. **Data quality issue** → extract: column_name, issue_type, severity, affected_row_count, suggested_fix

### Hour 4: Build — ETL Log Analyzer

Build a function that takes raw Airflow/Spark logs and returns structured incident reports.

```python
def analyze_etl_log(log_text: str) -> IncidentReport:
    """Takes raw ETL log, returns structured incident."""
    ...
```

Test it on real-looking log samples (generate some, or grab some from open-source pipelines).

### Hour 5: Polish + GitHub

- Add CLI interface (use `click` or `argparse`)
- Add 5+ test cases
- Write a great README with example inputs/outputs
- Push to GitHub: `etl-log-analyzer`

### Week 2 Resume Bullet:
*"Built an ETL log analyzer using Gemini structured outputs that converts raw Airflow/Spark logs into validated Pydantic-typed incident reports with severity classification and root-cause hypothesis."*

---

## Week 3: Function Calling (How AI Becomes Useful)

**Total time:** 5 hours
**Goal:** AI decides which of YOUR functions to call. This is how AI agents work.

### Hour 1: The Mental Model
- LLM doesn't execute code — it tells you WHICH function to call WITH WHICH arguments.
- You execute. Send the result back. AI continues reasoning.
- This is the magic that makes "AI agents" work.

### Hour 2: Your First Function Call
- Define a Python function with a clear docstring + type hints
- Pass it as a "tool" to Gemini
- Send a user prompt that requires the tool

```python
def get_table_row_count(table_name: str) -> int:
    """Returns the number of rows in the specified database table."""
    # Real implementation hits your DB
    return 42

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="How many rows are in the customers table?",
    config=genai.types.GenerateContentConfig(
        tools=[get_table_row_count]
    )
)
print(response.text)  # "The customers table has 42 rows."
```

### Hour 3: Multiple Tools, Smart Routing
Define 3 tools. AI picks the right one based on user intent.

```python
def get_table_schema(table_name: str) -> dict:
    """Returns column names and types for a table."""
    ...

def get_recent_pipeline_failures(pipeline_name: str, hours: int = 24) -> list:
    """Returns recent failures for a pipeline."""
    ...

def search_data_catalog(query: str) -> list:
    """Searches the data catalog for tables matching a query."""
    ...
```

Test with prompts like:
- "What columns does the orders table have?" → uses `get_table_schema`
- "Has the daily_revenue pipeline failed recently?" → uses `get_recent_pipeline_failures`
- "Find tables related to customer transactions" → uses `search_data_catalog`

### Hour 4: Tool Chaining (Sequential Calls)
- AI calls Tool A, gets result, decides Tool B is needed, calls it.
- Use Gemini's "automatic function calling" mode.

### Hour 5: Mini-Project — Data Dictionary Assistant
Build a CLI tool: AI answers questions about your "data catalog" (use a hardcoded dict for now).

```bash
$ python catalog_assistant.py
> What's in the orders table?
[AI uses get_table_schema] → Returns: id, user_id, amount, status, created_at

> Find tables with customer info
[AI uses search_data_catalog] → Returns: users, customer_profiles, customer_addresses

> Has the customer_etl pipeline failed today?
[AI uses get_recent_pipeline_failures] → Returns: 2 failures in last 24h, both rate-limit errors
```

Push to GitHub: `data-dict-assistant`.

### Week 3 Resume Bullet:
*"Built a function-calling data dictionary assistant using Gemini that routes natural-language questions to appropriate catalog/pipeline/schema query functions."*

---

# PHASE 2: SQL AGENT PROJECT (Weeks 4-5)

## Week 4: SQL Agent Design

**Total time:** 5 hours
**Goal:** Architecture for a production-safe SQL agent.

### Hour 1: SQL Agent Architecture
- Why text-to-SQL is the highest-leverage AI feature for data engineering
- The 4 layers: schema context, SQL generation, validation, execution
- Common pitfalls: SQL injection, expensive queries, hallucinated columns

### Hour 2: Schema Context Patterns
- How to feed your DB schema to the AI without blowing the context window
- Schema summarization techniques
- Including sample rows (helps AI understand the data)
- Filtering schemas: only show tables relevant to the question

### Hour 3: SQL Generation with Validation
- Generate SQL using function calling
- Validate before execution:
  - Is it SELECT only (no DML)?
  - Does it reference real tables/columns?
  - Are there obvious issues (cross joins, missing WHERE)?
- Use `sqlparse` for AST analysis

### Hour 4: Safe Execution
- **Critical**: Use a read-only database role
- Query timeout (kill anything > 30s)
- Result limit (LIMIT 1000)
- Logging: every query, who asked, results size

### Hour 5: Result Explanation
- After execution, summarize results in plain English
- "Your query returned 47 rows. The top 3 customers are X, Y, Z..."
- This is what makes it useful for non-technical users

---

## Week 5: Build the SQL Agent

**Total time:** 5 hours
**Goal:** Working SQL agent on a real sample database.

### Hour 1-2: Setup + Sample Data
- Use the Chinook sample database (music store: customers, invoices, tracks) OR
- Use Pagila sample (DVD rental store) OR
- Use any public dataset you can load into PostgreSQL
- Load into your local PostgreSQL

### Hour 3-4: Build the Agent

```python
# Pseudo-code structure
class SQLAgent:
    def __init__(self, db_url, schema_context):
        self.db = create_engine(db_url)  # Read-only role!
        self.schema = schema_context
    
    def ask(self, question: str) -> dict:
        # 1. Generate SQL via Gemini with schema context
        sql = self._generate_sql(question)
        # 2. Validate (SELECT only, no DML)
        self._validate(sql)
        # 3. Execute with timeout
        rows = self._execute(sql)
        # 4. Explain results
        explanation = self._explain(question, sql, rows)
        # 5. Log everything
        self._log(question, sql, rows, explanation)
        return {"sql": sql, "rows": rows, "explanation": explanation}
```

### Hour 5: Polish + Deploy

- Wrap in FastAPI: `POST /ask` endpoint
- Simple HTML interface (optional, takes 30 mins with vanilla JS + fetch)
- Clean README with:
  - Architecture diagram (Mermaid in markdown)
  - Example queries
  - Safety features documented
  - Deployment instructions
- **Push to GitHub: `nl-sql-agent`**

### Week 5 Resume Bullet (Strong):
*"Architected and built a natural-language SQL agent (Gemini + FastAPI + PostgreSQL) that safely translates business questions into validated, read-only queries with timeout enforcement, query logging, and result explanation. Demonstrated on Chinook dataset with 95%+ correctness on a 30-question eval set."*

🎯 **MILESTONE: Project #1 done. Start updating LinkedIn with this.**

---

# PHASE 3: EMBEDDINGS + RAG (Weeks 6-9)

## Week 6: Embeddings & Vector Search

**Total time:** 5 hours
**Goal:** Understand and use vector similarity search.

### Hour 1: Embeddings Conceptually
- Text → vector of numbers (e.g., 768 dimensions)
- Similar meaning = similar vectors (close in vector space)
- Cosine similarity as the metric
- This is HOW Google search and ChatGPT memory work under the hood

### Hour 2: Generate Embeddings (Free)
- **Option A: Gemini's embedding API** (free)
  - `models.embed_content(model="text-embedding-004", contents="...")`
- **Option B: sentence-transformers** (totally local, free)
  - `pip install sentence-transformers`
  - Model: `all-MiniLM-L6-v2` (small + fast)
- Generate embeddings for 20 sentences. Verify similar sentences have higher cosine similarity.

### Hour 3: ChromaDB (Local Vector Database)
- `pip install chromadb`
- Create a collection, add documents, query
- Practice with 500+ documents (use any text corpus)

```python
import chromadb
client = chromadb.Client()
collection = client.create_collection(name="my_docs")

collection.add(
    documents=["doc1 text", "doc2 text", ...],
    metadatas=[{"source": "x"}, {"source": "y"}, ...],
    ids=["1", "2", ...]
)

results = collection.query(query_texts=["my search"], n_results=5)
```

### Hour 4: pgvector (Production-Quality, Free)
- Since you're a data engineer, you'll likely use pgvector in real jobs
- PostgreSQL extension that adds vector type + similarity search
- We already started your pgvector Docker container in setup
- Practice: Create table with vector column, insert, query

```sql
CREATE EXTENSION vector;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(384)  -- match your embedding model dimensionality
);

-- Find 5 most similar to a query embedding
SELECT * FROM documents ORDER BY embedding <-> '[0.1, 0.2, ...]' LIMIT 5;
```

### Hour 5: Hybrid Search (Vector + Keyword)
- Vector search misses exact matches ("error code E1042")
- Keyword search misses semantic matches ("not found" vs "missing")
- Combine both with Reciprocal Rank Fusion (RRF)
- Apply to a small data engineering corpus (e.g., Airflow docs)

### Week 6 Resume Bullet:
*"Implemented semantic search over a 500+ document corpus using sentence-transformers embeddings and pgvector with hybrid (BM25 + vector) retrieval."*

---

## Week 7: RAG Architecture & First Build

**Total time:** 5 hours
**Goal:** Build a basic RAG system end-to-end.

### Hour 1: RAG Architecture
- Query → embed → retrieve → augment prompt → generate answer
- Why RAG > "just put it in the prompt": context window costs, freshness, attribution
- The 5 failure modes: bad chunking, weak retrieval, no grounding, hallucination, no citations

### Hour 2: Document Chunking
- Fixed size (500 chars) vs sentence-based vs semantic
- Chunk overlap (10-20% prevents context loss at boundaries)
- For data engineering content: chunk by section, not arbitrary chars
- Use `langchain-text-splitters` (`pip install langchain-text-splitters`)

### Hour 3: Retrieval Layer
- Top-K (typically K=5)
- Metadata filtering (filter by source type, date, etc.)
- Multi-query retrieval: rewrite query into 3 variants, retrieve for each, merge

### Hour 4: Generation with Grounding
- The augmented prompt pattern:
```
You are answering questions about [domain].
Use ONLY the following context to answer. If the answer isn't there, say "I don't know."

Context:
{retrieved_chunks}

Question: {user_query}
```
- Citation handling: tell AI to cite which chunk it used

### Hour 5: First RAG End-to-End
Build a minimal working RAG over Airflow documentation (or PostgreSQL docs):
1. Download docs (or scrape a small subset)
2. Chunk + embed + store in ChromaDB
3. Query API
4. Answer with citations

Don't polish yet — just get it working.

---

## Week 8: Build the Data Catalog RAG (Project #2)

**Total time:** 5 hours
**Goal:** A production-quality RAG over a data catalog (your big portfolio piece).

### Hour 1: Project Plan
- Use a real dataset: take a public data warehouse schema (e.g., dbt's jaffle_shop, or generate a fake one with 30+ tables)
- For each table, gather: schema, sample rows, description, common queries, dbt model code
- Plan the chunking: each "document" = one table's full context

### Hour 2: Ingestion Pipeline
- Script that loads catalog metadata → embeds → stores in pgvector
- Idempotent: rerunning doesn't duplicate
- Run it on your sample catalog

### Hour 3: Query API
- FastAPI endpoint: `POST /ask` with `{"question": "..."}`
- Pipeline: embed query → retrieve top 5 → generate answer with citations
- Return: `{"answer": "...", "sources": [{"table": "...", "snippet": "..."}]}`

### Hour 4: Multi-Turn (Conversational)
- Add chat history: prior turns inform retrieval and generation
- Important: rewrite the question using context before retrieval ("the orders table" → resolve from prior turn)

### Hour 5: Polish + GitHub

- Simple HTML chat UI (Gradio or vanilla — Gradio is faster: `pip install gradio`)
- README with:
  - Demo GIF (use Loom or simple screenshots)
  - Architecture diagram (Mermaid)
  - Example questions and answers
  - "I don't know" examples (out-of-corpus queries)
- **Push to GitHub: `data-catalog-rag`**

### Week 8 Resume Bullet (Hero Project):
*"Architected a RAG system (Gemini + pgvector + FastAPI) over a 30-table data catalog enabling natural-language questions about schema, lineage, and usage. Includes multi-turn conversation, citation-backed answers, and 'I don't know' handling for out-of-corpus queries."*

🎯 **MILESTONE: Project #2 done. This is your interview centerpiece.**

---

## Week 9: RAG Quality + Evaluation

**Total time:** 5 hours
**Goal:** Make your RAG bot measurably better. This is what separates real engineers from demo-builders.

### Hour 1: Reranking
- Initial retrieval optimizes for recall (find candidates)
- Reranking optimizes for precision (best candidates first)
- Free reranking: `pip install rank-bm25` for BM25, or `sentence-transformers` cross-encoder
- Cross-encoder model (free, local): `cross-encoder/ms-marco-MiniLM-L-6-v2`

### Hour 2: Query Expansion
- HyDE (Hypothetical Document Embeddings): AI writes a hypothetical answer, embed THAT, retrieve
- Multi-query: ask AI to generate 3 variants of the question
- Test if these improve your retrieval

### Hour 3: Evaluation — Build Your Test Set
- Manually create 30-50 questions + expected answers about your catalog
- Cover: easy (single-table), medium (joins/relationships), hard (lineage/derivations), out-of-corpus
- Save as a JSON file in your repo

### Hour 4: LLM-as-Judge
- Use Gemini to grade your RAG bot's answers
- Rubric: accuracy (0-3), faithfulness to context (0-3), completeness (0-3)
- Script that runs your eval set + grades each answer + prints summary

### Hour 5: Iterate
- Look at low-scoring answers. Why did they fail?
- Common fixes: better chunking, more retrieved chunks, prompt improvements, reranking
- Re-run eval. Show before/after numbers in README.

### Week 9 Resume Bullet (Adds Numbers to Project #2):
*"Improved RAG retrieval precision from 72% to 89% using cross-encoder reranking and query expansion, validated against a hand-labeled 50-question evaluation set with LLM-as-judge scoring."*

🎯 **MILESTONE: You're now job-ready. Start applying for "Data Engineer with AI elements" roles.**

---

# PHASE 4: COST + PRODUCTION (Weeks 10-11)

## Week 10: Cost Optimization (Critical for Interviews)

**Total time:** 5 hours
**Goal:** Make your AI apps cheap enough to actually run at scale.

📖 **Read `COST_OPTIMIZATION.md` for theoretical depth. This week is applying it.**

### Hour 1: Measure What You Spend
- Add cost tracking to your SQL agent + RAG bot
- Log every call: tokens in, tokens out, model used, cost
- Even with free Gemini tier, track theoretical "what if I paid"

### Hour 2: Model Selection
- When does Gemini Flash work? (90% of cases)
- When do you need Pro/Claude? (complex reasoning, code generation)
- Build a "smart router" that picks the right model based on query complexity

### Hour 3: Caching (Big Wins)
- **Exact-match cache**: same query → return cached response (Redis or simple dict)
- **Semantic cache**: similar-meaning queries → cached response (use embeddings)
- Add Redis to your stack: `docker run -d -p 6379:6379 redis`

### Hour 4: Prompt Optimization
- Token math: input vs output costs
- Compress prompts: remove fluff, shorter examples, abbreviate where safe
- Move static instructions to system prompt (cacheable on some providers)

### Hour 5: Apply to Both Projects
- Add caching to SQL agent and RAG bot
- Measure cache hit rate
- Document cost savings in README

### Week 10 Resume Bullet:
*"Implemented multi-layer cost optimization (semantic caching, model routing, prompt compression) reducing per-query LLM cost by 60% with no quality regression."*

---

## Week 11: Production Patterns Lite

**Total time:** 5 hours
**Goal:** Your apps don't fall over under real conditions.

### Hour 1: Async Patterns
- LLM calls take 2-10 seconds. Sync = blocking. Async = better.
- Convert your FastAPI endpoints to async
- Use `asyncio.gather()` to parallelize multiple LLM calls

### Hour 2: Streaming Responses
- Streaming = perceived latency drops dramatically
- Server-Sent Events (SSE) in FastAPI
- Stream Gemini responses to client

### Hour 3: Observability (Free)
- Simple logging: every LLM call → log to file
- Better: Langfuse (self-hosted via Docker, free) — open-source LLM observability
- Track: latency, errors, cost, retries

### Hour 4: Rate Limit & Retry Handling
- Free tier rate limits will bite you in production
- Token bucket pattern for client-side limiting
- Exponential backoff for retries
- Circuit breaker for repeated failures

### Hour 5: Apply to Existing Projects
- Make SQL agent + RAG bot fully async
- Add Langfuse to both
- Load test with `locust`: simulate 10 concurrent users

### Week 11 Resume Bullet:
*"Productionized GenAI services with async FastAPI, SSE streaming, Langfuse observability, and rate-limit-aware retry logic, sustaining 10 concurrent users with sub-3s P95 latency."*

---

# PHASE 5: DATA PIPELINE AGENT (Weeks 12-13)

## Week 12: Agent Design

**Total time:** 5 hours
**Goal:** Design a stateful agent that helps with data pipeline tasks.

### Hour 1: Pick Your Agent's Purpose
Choose ONE (don't try all):
- **Option A:** CSV-to-dbt: Inspect CSVs, generate dbt models + tests + schema.yml
- **Option B:** Airflow DAG generator: User describes a workflow, agent generates DAG skeleton
- **Option C:** Data quality bot: Inspect a table, suggest quality rules, generate Great Expectations code

Pick the one most relevant to your work.

### Hour 2: Tool Definitions
Define 5-7 tools the agent needs:
- `inspect_csv(path)` → returns column names, types, samples
- `query_database(sql)` → safe SELECT only
- `generate_dbt_model(name, sql)` → creates file
- `generate_dbt_test(model, test_type, column)` → adds tests
- `human_approve(action)` → pauses, waits for user

### Hour 3-4: Core Agent Loop
- Don't use LangGraph (overkill for 5 hrs). Use raw Gemini function calling.
- Build the loop: prompt → AI calls tools → execute → feed back → continue until done.
- Add state tracking (what's been done, what's next).

### Hour 5: First Test
Run on a real CSV. Note where it fails. Don't fix yet — just observe.

---

## Week 13: Build & Polish Pipeline Agent

**Total time:** 5 hours
**Goal:** Complete Project #3.

### Hour 1-3: Full Build
- Implement all tools
- Add the human-in-the-loop pattern
- Output final files (dbt models, tests, schema docs)

### Hour 4: Real Test Case
- Find a real-ish dataset (Kaggle, public CSV)
- Run end-to-end
- Capture screenshots of agent in action

### Hour 5: Polish + GitHub
- README with:
  - "Why I built this" (motivation)
  - Architecture diagram
  - Demo video or GIF
  - Example: input CSV → output dbt project
- **Push to GitHub: `ai-pipeline-assistant`**

### Week 13 Resume Bullet:
*"Built an AI pipeline assistant using Gemini function calling that inspects raw CSVs and generates production-ready dbt models, tests, and documentation with human-in-the-loop validation gates."*

🎯 **MILESTONE: Project #3 done. You now have a strong, defensible portfolio.**

---

# PHASE 6: POLISH & DEPLOY (Week 14)

## Week 14: Convert Projects Into Interview-Winning Artifacts

**Total time:** 5 hours

### Hour 1: Pick Your Hero Project
- Probably the Data Catalog RAG (it's the most impressive)
- Audit code: remove TODOs, clean up, add type hints
- Make sure README is excellent

### Hour 2: Deploy Live (Free Hosting)
- **Option A: Hugging Face Spaces** (free, easy, AI-friendly)
  - Wrap your RAG in Gradio
  - Push to HF Spaces
- **Option B: Railway** (500 hours/month free)
- **Option C: Render** (free tier with auto-sleep)

### Hour 3: Demo Materials
- Take 5 great screenshots of your RAG bot
- Record a 60-90 second Loom video walkthrough
- Add to the README

### Hour 4: Resume + LinkedIn

**Resume update — add this section:**

```
GenAI Engineering (Self-Directed Learning, 14 weeks)

Projects:
• Natural-Language SQL Agent: [link]
  - Gemini API, FastAPI, PostgreSQL
  - Safe query generation with validation, timeout, audit logging
  
• Data Catalog RAG: [link, live demo: ...]
  - Gemini + pgvector + FastAPI + Gradio
  - Multi-turn conversation, citation-backed answers, 89% retrieval precision
  - Productionized with caching, async, observability
  
• AI Pipeline Assistant: [link]
  - Function-calling agent for dbt model generation
  - Human-in-the-loop validation gates

Skills: LLM API integration, prompt engineering, structured outputs, function 
calling, embeddings, vector databases (pgvector, ChromaDB), RAG, LLM evaluation, 
cost optimization, agentic patterns
```

**LinkedIn post template:**
```
I spent 14 weeks adding GenAI skills to my data engineering toolkit. Here's what I built:

🔹 [Project 1 in one sentence + link]
🔹 [Project 2 in one sentence + link]
🔹 [Project 3 in one sentence + link]

Key lessons:
- [lesson 1]
- [lesson 2]
- [lesson 3]

What I'd do differently: [honest reflection]

Open to Data Engineer + AI/ML roles. DMs open.
```

### Hour 5: Interview Prep
- Pick top 5 questions you'd expect:
  - "Walk me through your RAG project"
  - "Why pgvector over Pinecone?"
  - "How do you evaluate RAG quality?"
  - "When would you NOT use RAG?"
  - "What did this teach you about LLMs?"
- Write 60-90 second answers for each
- Practice out loud

---

# AFTER WEEK 14

**Apply broadly.** Numbers game. Tailor each application to mention which project is most relevant to that company.

**Keep learning during interview phase:**
- Read Anthropic's prompt engineering guide cover to cover
- Read one Anthropic technical paper per week (Claude papers, deep dives)
- Try LangGraph properly (you skipped it; pick it up now if asked about it)
- Contribute to one open-source GenAI repo (issue triage, docs, small PRs)

**You're now playing the long game.** The first job is the hard one. After that, the next role is much easier.

Good luck.'''