# System Design for Data Engineering — 12-Week Curriculum

**Target:** Senior DE / SDE roles at FAANG and FAANG-adjacent companies (5 YOE)
**Format:** Phased curriculum, tutor-led, drill-heavy
**Outcome:** Interview-ready fluency in system design fundamentals and DE-specific architecture

---

## Phase 1: Foundations (Weeks 1–3)

You cannot design a data system without these. Interviewers test them indirectly in every question — if your fundamentals are shaky, every subsequent answer leaks.

### Week 1: The Vocabulary of Scale

- Latency vs throughput vs bandwidth — precise definitions, why confusing them costs you the interview
- Back-of-the-envelope estimation — powers of 2, powers of 10, time conversions (seconds in a day, etc.)
- QPS / RPS math — how to estimate from DAU, MAU, and user behavior
- Storage estimation — rows × bytes × retention × replication

> Drill-heavy week. Estimation reps on Swiggy order QPS, Hotstar IPL bandwidth, PhonePe transaction storage.

### Week 2: Distributed Systems Fundamentals

- CAP theorem — what it actually says (and the 90% of candidates who get it wrong)
- PACELC — the extension that matters more than CAP in practice
- Consistency models — strong, eventual, causal, read-your-writes, monotonic
- Replication — leader-follower, multi-leader, leaderless
- Partitioning vs sharding — range, hash, consistent hashing
- The fallacies of distributed computing

### Week 3: Storage Fundamentals

- OLTP vs OLAP — why you can't run analytics on your production Postgres
- Row stores vs column stores — and why Parquet/ORC exist
- B-trees vs LSM trees — when each wins (Postgres vs Cassandra intuition)
- Indexing basics — primary, secondary, covering, composite
- File formats: CSV → JSON → Avro → Parquet → ORC — trade-offs and when each fits

---

## Phase 2: Data Engineering Core (Weeks 4–7)

This is where DE system design diverges from generic backend system design. Most candidates from QA/backend backgrounds underweight this phase and fail interviews on data modeling questions.

### Week 4: Batch Processing & Data Warehouses

- Batch processing mental model — when latency in hours is acceptable
- MapReduce → Spark — why Spark won; RDD → DataFrame → Dataset
- Data warehouse architecture — Snowflake, BigQuery, Redshift internals
- Dimensional modeling — star schema, snowflake schema, fact vs dimension tables
- Slowly Changing Dimensions (SCD Type 1, 2, 3) — interviewers love SCD2
- Real example: how Flipkart models order analytics

### Week 5: Stream Processing & Kafka Deep-Dive

- Batch vs stream vs micro-batch — when to pick which
- Kafka architecture — brokers, topics, partitions, consumer groups, ISR
- Partitioning strategies — why your partition key choice can sink the design
- Delivery semantics — at-most-once, at-least-once, exactly-once (and why EOS is hard)
- Retention, compaction, tiered storage
- Kafka alternatives — Pulsar, Kinesis, Redpanda — and when to pick them
- Real example: how Swiggy/Zomato handle order event streams

### Week 6: Stream Processing Engines & Lambda/Kappa

- Flink vs Spark Streaming vs Kafka Streams — real trade-offs
- Windowing — tumbling, sliding, session
- Watermarks and late data handling (where senior candidates are separated from mid-level)
- Lambda architecture vs Kappa architecture
- Exactly-once in practice — checkpointing, idempotent producers

### Week 7: Data Lakes, Lakehouses & Modern Formats

- Data lake vs warehouse vs lakehouse — what actually changed
- Delta Lake vs Apache Iceberg vs Apache Hudi — the table format wars
- ACID on object storage — how it works, why it matters
- Medallion architecture — bronze/silver/gold
- Schema evolution and time travel
- Real example: how Uber built Hudi for their needs

---

## Phase 3: Pipelines, Modeling & Operations (Weeks 8–9)

### Week 8: Orchestration, Data Quality & Modeling

- Airflow deep-dive — DAGs, operators, executors, scheduling pitfalls
- Airflow alternatives — Dagster, Prefect, Temporal — when each wins
- Idempotency, backfills, late-arriving data
- Data modeling for analytics — Kimball vs Inmon vs Data Vault
- dbt and the analytics engineering layer
- Data contracts, data quality (Great Expectations, Soda)

### Week 9: CDC, Real-Time Analytics & Serving

- Change Data Capture — Debezium, log-based vs query-based CDC
- Real-time OLAP — Druid, Pinot, ClickHouse — trade-offs
- Serving layers for ML features — online vs offline feature stores
- Caching strategies for data systems — Redis, materialized views
- Real example: how Zomato/Uber power live dashboards

---

## Phase 4: Interview Mastery (Weeks 10–12)

### Week 10: Full Mock Interviews — Common Questions

- "Design the data platform for Swiggy's order analytics"
- "Design a real-time fraud detection pipeline for PhonePe"
- "Design Hotstar's video viewing analytics for IPL"

> Full 45-min format with ruthless feedback.

### Week 11: Full Mock Interviews — Harder Questions

- "Design a feature store for Flipkart recommendations"
- "Design a data lineage and catalog system"
- "Design a multi-tenant data warehouse for a SaaS company"

> Deep-dive rounds — drill into ONE component for 20 min.

### Week 12: Polish, Weak-Spot Remediation, Behavioral Framing

- Remediation of your lowest-scored topics from the tracker
- How to structure the 45 minutes — minute-by-minute
- How to handle "I don't know" gracefully
- Communicating trade-offs like a senior engineer, not reciting facts
- Final diagnostic mock and readiness signal

---

## Standing Drill Rules (apply across all sessions)

1. **Restate the question** before answering.
2. **Enumerate all actors** who read the data and the action each takes based on the read.
3. **Justify with a named failure mode** and named cost-of-wrong vs. cost-of-strong.
4. **Sanity-check** by verifying the chosen model/strategy mechanically prevents the named failure mode.

## Current Status Snapshot

- **Week 2 ~80% complete.** Covered: CAP, consistency models, PACELC, partitioning (range/hash/consistent), replication (single-leader/multi-leader/leaderless), Fallacies of Distributed Computing.
- **Deferred items:** WhatsApp consistency-model assignment (in progress at last session close), one replication redo on the specific-failure-mode pattern.
- **Next up:** Close Week 2 → begin Week 3 (Storage Fundamentals).
