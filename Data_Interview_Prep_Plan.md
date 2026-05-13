# Data Interview Prep Plan

## Philosophy

This plan is built around one principle: scenarios before theory. You already know definitions. What gets you rejected is freezing when the interviewer says "You've got 2 billion rows of order data with heavy skew on merchant_id — walk me through how you'd design the pipeline." Every week leads with situations you'll actually face in the chair, and backfills theory only where gaps show up.

Your QA background is not a weakness to hide — it's a weapon to deploy. Data quality, edge-case thinking, testing rigor, and validation pipelines are things most DE candidates hand-wave. You won't.

---

## Week 1 — SQL Foundations Under Pressure

**Goal:** Handle any SQL question thrown at a Senior DE screen without hesitating.

### Day 1–2: Window Functions Deep Dive

- ROW_NUMBER, RANK, DENSE_RANK — when each one matters and when interviewers try to trip you up with ties
- LEAD/LAG for session analysis, churn detection, consecutive-day problems
- Running totals, moving averages with ROWS BETWEEN
- **Scenario:** "Swiggy wants to find users whose order value dropped for 3 consecutive months. Write the query."

### Day 3–4: CTEs, Subqueries & Query Structure

- Recursive CTEs (org hierarchy, category trees — Flipkart uses these)
- CTE vs subquery vs temp table — when to pick which, and why it matters for the optimizer
- **Scenario:** "Given a table of employee-manager pairs with NULLs for bad data, build the full reporting chain and find broken links."

### Day 5–6: Aggregation & Grouping Edge Cases

- GROUP BY with NULLs, HAVING vs WHERE, GROUPING SETS / ROLLUP / CUBE
- Conditional aggregation (CASE inside SUM/COUNT)
- **Scenario:** "Razorpay needs a single query showing daily, weekly, and monthly transaction volumes side by side."

### Day 7: First Drill Session

- 5 timed SQL problems (20 min each), scored pass/bubble/fail
- Debrief: identify patterns in mistakes

---

## Week 2 — SQL: Optimization & The "Why" Questions

**Goal:** Answer "why is this query slow?" and "how would you fix it?" — the questions that separate Senior from Mid.

### Day 1–2: Indexing & Execution Plans

- B-tree vs hash vs bitmap indexes — when each is appropriate
- Composite index column ordering and the left-prefix rule
- Reading EXPLAIN output: seq scan, index scan, hash join, nested loop, sort
- **Scenario:** "Your daily Flipkart seller-payout query takes 45 minutes. Here's the EXPLAIN plan. What's wrong and what do you change?"

### Day 3–4: Join Performance & Anti-Patterns

- Join algorithms: nested loop, hash join, merge join — which the optimizer picks and why
- The N+1 query problem in reporting
- Self-joins, cross joins, anti-joins (LEFT JOIN WHERE NULL vs NOT EXISTS vs NOT IN with NULLs)
- **Scenario:** "A Meesho analyst wrote a query joining 5 tables that returns correct results but takes 12 minutes. Diagnose and fix."

### Day 5–6: Advanced Patterns Interviewers Love

- De-duplication strategies (ROW_NUMBER vs DISTINCT ON vs GROUP BY — trade-offs)
- Gap-and-island problems (consecutive sessions, streaks)
- Pivot/unpivot without PIVOT keyword
- **Scenario:** "CRED wants to identify users who made payments in at least 5 consecutive months. Handle gaps, NULLs, and duplicate records."

### Day 7: Timed SQL Mock (20 min)

- 3 scenario-based problems, interviewer-style follow-ups after each

---

## Week 3 — Python for Data Engineering (Not Data Science)

**Goal:** Write Python that a Senior DE would actually ship — not Leetcode, not Jupyter notebook hacks.

### Day 1–2: Data Structures & Complexity That Matter

- dict/set internals (hash tables), defaultdict, Counter, OrderedDict
- When to use list vs deque vs heap — with pipeline examples
- Generator expressions for memory-efficient streaming
- **Scenario:** "You need to deduplicate 500M records from a file that doesn't fit in memory. Walk me through your Python approach."

### Day 3–4: File Handling & ETL Patterns

- Reading CSV/JSON/Parquet: chunked processing, schema validation
- Context managers, pathlib, error handling for production pipelines
- Idempotency patterns: how to make a Python ETL script safe to re-run
- **Scenario:** "Zepto's vendor sends a daily CSV that sometimes has encoding errors, missing columns, and duplicate headers mid-file. Write the ingestion code."

### Day 5–6: OOP for Pipelines & Testing

- When classes help (pipeline stages, config management, retry logic) vs when functions are enough
- Decorators for logging, timing, retry
- Writing testable ETL code — unit tests for transforms, mocking external services
- **Scenario:** "Design a Python class structure for a pipeline that ingests from 3 sources, validates, transforms, and loads to a warehouse. Show me the error-handling strategy."

### Day 7: Python Drill

- 4 problems: 2 coding + 2 design/walkthrough, scored

---

## Week 4 — PySpark Fundamentals & Mental Model

**Goal:** Understand what Spark actually does under the hood — not just the API.

### Day 1–2: Architecture & Execution Model

- Driver, executors, tasks, stages, shuffle boundaries
- Lazy evaluation — why it matters, how the DAG is built
- Narrow vs wide transformations — why this distinction determines performance
- **Scenario:** "You see 200 tasks in Stage 1 and 50,000 tasks in Stage 2. What happened and is this a problem?"

### Day 3–4: DataFrame API Mastery

- select, filter, groupBy, agg, join, withColumn, when/otherwise
- UDFs: why they're slow, pandas UDFs as the alternative
- Column expressions vs Python functions — the performance cliff
- **Scenario:** "Rewrite this PySpark code that uses 4 UDFs. Make it 10x faster without changing the logic."

### Day 5–6: RDD vs DataFrame vs Dataset

- When RDD is still the right answer (custom partitioning, low-level control)
- Catalyst optimizer — what it can and can't optimize
- Schema enforcement: StructType, handling schema evolution
- **Scenario:** "Your team inherited an RDD-based pipeline from 2018. When do you migrate to DataFrames and when do you leave it alone?"

### Day 7: PySpark Drill

- 3 coding problems + 1 architecture walkthrough

---

## Week 5 — PySpark: Performance, Failures & Debugging

**Goal:** Handle the "your Spark job is failing/slow — fix it" questions that are guaranteed at Senior level.

### Day 1–2: Partitioning & Shuffles

- Hash partitioning, range partitioning, repartition vs coalesce
- Shuffle: what triggers it, why it's expensive, how to minimize it
- spark.sql.shuffle.partitions — when 200 is wrong and what to set instead
- **Scenario:** "A daily aggregation job at PhonePe shuffles 800 GB. Walk me through how you'd reduce it."

### Day 3–4: Joins & Skew

- Broadcast join: when it works, size limits, broadcast hint
- Sort-merge join vs shuffle hash join
- Skew handling: salting, key splitting, AQE skew join optimization
- **Scenario:** "A join on user_id is failing OOM because 5% of users generate 60% of events. Fix it."

### Day 5–6: Debugging & Failure Modes

- Reading Spark UI: stages, tasks, shuffle read/write, GC time
- OOM: driver vs executor, where to look first
- Spill to disk, data locality, speculative execution
- **Scenario:** "Your nightly job that ran fine for 6 months suddenly takes 4x longer. Nothing changed in the code. Diagnose."

### Day 7: PySpark Failure-Mode Mock

- 4 debugging scenarios, talk-through format (no code — just diagnosis and plan)

---

## Week 6 — Data Modeling: Think Like an Architect

**Goal:** Design schemas that interviewers at Flipkart, Swiggy, and Razorpay would approve.

### Day 1–2: OLTP vs OLAP & Normalization

- 1NF through 3NF — with real examples, not textbook definitions
- When to denormalize and what breaks when you do
- OLTP schema design for a payments system vs OLAP for analytics
- **Scenario:** "Design the OLTP schema for Razorpay's core payment processing. Now design the OLAP schema the analytics team will query."

### Day 3–4: Dimensional Modeling

- Star schema vs snowflake — trade-offs, not just definitions
- Fact tables: transaction facts, periodic snapshots, accumulating snapshots
- Dimension tables: conformed dimensions, junk dimensions, degenerate dimensions
- Slowly Changing Dimensions: Type 1, 2, 3 — when to use each
- **Scenario:** "Swiggy wants to track order lifecycle from placement to delivery with the ability to analyze historical changes in restaurant ratings. Design the model."

### Day 5–6: Modeling for Scale

- Partitioning strategies for fact tables (date, region, tenant)
- Data vault basics: hubs, links, satellites — when it beats star schema
- Modeling for real-time vs batch — different constraints
- **Scenario:** "Flipkart's product catalog has 500M SKUs with attributes that vary wildly by category. Design a flexible model."

### Day 7: Modeling Drill

- 2 end-to-end schema design problems (whiteboard-style), scored

---

## Week 7 — System Design & Architecture for Data Engineers

**Goal:** Answer "design the data platform for X" without rambling.

### Day 1–2: Batch Pipeline Architecture

- Source → Ingestion → Storage → Transform → Serve pattern
- Choosing storage: S3/HDFS, partitioning strategy, file formats (Parquet vs ORC vs Avro)
- Orchestration: Airflow DAG design, idempotency, backfill strategies
- **Scenario:** "Design the daily batch pipeline for Zomato's restaurant analytics — from raw event logs to a dashboard showing revenue, ratings, and delivery times per city."

### Day 3–4: Streaming & Real-Time

- Kafka basics: topics, partitions, consumer groups, offsets
- Spark Structured Streaming: watermarks, output modes, exactly-once
- Lambda vs Kappa architecture — when each makes sense
- **Scenario:** "Zepto needs real-time inventory tracking across 200 dark stores. Design the streaming pipeline."

### Day 5–6: Data Quality & Governance

- Data quality frameworks: Great Expectations, Deequ, custom checks
- Lineage tracking, data contracts, schema registries
- This is where your QA background becomes your superpower — frame data quality as testing rigor applied to pipelines
- **Scenario:** "You're the first Senior DE at a Series B startup. There's no data quality framework. What do you build in the first 90 days?"

### Day 7: Architecture Mock

- 1 full system design (45 min), scored like a real interview

---

## Week 8 — Behavioral: Turning QA Into Your Edge

**Goal:** Tell stories that make interviewers think "this person owns problems and ships solutions."

### Day 1–2: Building Your Story Bank

- Map your QA experience to DE-relevant stories: 8–10 stories covering ownership, conflict, failure, ambiguity, impact
- Frame QA as strength: "I built automated validation pipelines before I even became a DE — quality is in my DNA"
- Every story gets the STAR treatment: Situation (2 sentences), Task (1 sentence), Action (bulk of the answer — specific, technical, YOUR actions), Result (metrics)

### Day 3–4: Amazon-Style Leadership Principles

- Ownership, Bias for Action, Dive Deep, Earn Trust, Deliver Results, Customer Obsession
- Practice: one polished story per LP
- Drill: "Tell me about a time you found a critical issue that no one else noticed" — your QA background makes this a layup

### Day 5–6: Tricky Behavioral Questions

- "Why are you switching from QA to DE?" — frame as evolution, not escape
- "What's a technical decision you disagreed with?" — show you can disagree and commit
- "Tell me about a time you failed" — show learning, not excuses
- Drill: 3 behavioral questions, critiqued on STAR structure, specificity, and ownership language

### Day 7: Behavioral Mock

- 4 behavioral questions (10 min each), scored

---

## Week 9 — Integration: Cross-Topic Scenarios

**Goal:** Handle interview questions that span multiple topics — because real interviews don't stay in one lane.

### Day 1–2: SQL + Data Modeling Combos

- "Here's a business requirement. Design the schema. Now write the query."
- Optimizing queries against the schema you just designed
- **Scenario:** "PhonePe wants a fraud detection report. Design the data model, write the detection query, and explain how you'd optimize it for 100M daily transactions."

### Day 3–4: PySpark + Architecture Combos

- "Here's a pipeline that's breaking. Diagnose, fix, and redesign."
- Choosing between SQL-based and PySpark-based solutions
- **Scenario:** "Meesho's seller onboarding pipeline processes 50K applications/day. It's slow, has duplicates, and occasionally loses records. Fix the pipeline and add data quality checks."

### Day 5–6: Full-Stack DE Scenarios

- End-to-end: requirements → modeling → pipeline → quality → query → optimization
- **Scenario:** "You're building the analytics platform for a new Swiggy feature: 10-minute grocery delivery. Walk me through everything from raw events to the CEO's dashboard."

### Day 7: Cross-Topic Mock

- 60-min mock covering all areas

---

## Week 10 — Mock Interview Week 1

**Goal:** Simulate real pressure. Get scored. Fix gaps.

### Mock 1 (Day 1–2): Large Product Company Style (Flipkart/Amazon)

- 20 min SQL (hard scenario + optimization follow-up)
- 15 min PySpark (debugging a failing job)
- 15 min Data Modeling (dimensional model design)
- 10 min Behavioral (2 LP questions)
- Full scorecard after

### Mock 2 (Day 3–4): Startup Style (Zepto/Razorpay/CRED)

- Focus: breadth, speed, pragmatism over perfection
- Expect "how would you build this from scratch with a 2-person team?"
- Full scorecard after

### Mock 3 (Day 5–6): System Design Heavy (Swiggy/PhonePe)

- 30 min system design + 15 min deep-dive on one component + 15 min behavioral
- Full scorecard after

### Day 7: Gap Analysis

- Review all 3 scorecards
- Update weak spots in progress tracker
- Build targeted drills for Week 11

---

## Week 11 — Targeted Gap Closure

**Goal:** Attack whatever Week 10 exposed as weak.

This week is intentionally unstructured. Based on mock interview scorecards, we focus entirely on:

- Weakest topic area (extra scenarios + drills)
- Most common mistake patterns (e.g., vague answers, missing trade-offs, incomplete solutions)
- Speed: if you're too slow, timed drills with strict cutoffs
- Depth: if you're too shallow, "why?" chains until you hit bedrock

---

## Week 12 — Final Mocks & Confidence Building

**Goal:** Walk into interviews feeling like you belong.

### Mock 4 (Day 1–2): Hardest Possible — "Rejection Round"

- Intentionally harder than real interviews
- Adversarial follow-ups, ambiguous requirements, curveball questions
- If you survive this, real interviews feel easy

### Mock 5 (Day 3–4): Realistic — "Offer Round"

- Calibrated to actual Senior DE bar
- Clean scorecard = you're ready

### Day 5–6: Story Polish & Quick-Fire Drills

- Behavioral stories: final polish, record yourself (in writing), trim fat
- SQL/PySpark quick-fire: 10 problems in 60 minutes
- Data modeling: 2 rapid schema designs (15 min each)

### Day 7: Final Review

- Review entire progress tracker
- Confidence check: which topics would you be happy to get in an interview? Which ones still scare you?
- Game plan for the first real interview

---

## Ongoing (Every Week)

- 2–3 scenario-based drills on weak areas (refreshed based on progress tracker)
- 1 timed SQL problem daily (15–20 min max)
- 1 behavioral story rehearsal per week (different story each time)
- Read one engineering blog post per week from target companies (Flipkart Tech, Uber Engineering, Swiggy Bytes, etc.) — use these as conversation fuel in interviews
