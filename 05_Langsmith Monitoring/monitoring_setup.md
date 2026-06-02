# LangSmith Monitoring — Setup & Configuration

**Project:** SilverTrust — Streetwear E-Commerce AI
**Modules monitored:** 01, 02, 03, 04B
**Date:** Tuesday, Week 7

---

## LangSmith project

**Project name:** silvertrust-streetwear
**Link:** [Add LangSmith project URL here]
**Screenshots:** see /05-langsmith-monitoring/screenshots/

---

## What is monitored and why

### Module 01 — Recommendation engine

| Signal | Why |
|--------|-----|
| Input: session context sent to scoring function | Verify no personal data beyond hashed ID is logged |
| Output: ranked product IDs + scores | Audit trail for every ranking decision |
| Latency | SLA target under 80ms; alert if exceeded |
| In-stock filter applied? | Catch cases where out-of-stock items surface |
| Margin boost applied? | Verify business rules are executing correctly |

### Module 02 — AI styling assistant

| Signal | Why |
|--------|-----|
| Input: customer question (full text) | Detect off-topic or harmful queries |
| Output: LLM response (full text) | Score for brand voice and accuracy |
| RAG retrieval: products returned | Verify only live catalog products appear in responses |
| Hallucination check | Flag responses referencing products not in RAG context |
| Photo request detection | Alert fires if any output requests a photo from the customer — hard safety rule |
| Turn count per session | Enforce 5-turn cap; alert if exceeded |
| Latency | Track response time per turn |
| Human feedback score (thumbs up/down) | Collect signal for quality improvement |

### Module 03 — Catalog automation

| Signal | Why |
|--------|-----|
| Input: product attributes sent to LLM | Confirm no personal data in prompt |
| Output: generated copy draft | Stored for audit trail alongside human decision |
| Human review decision (approved / rejected) | Track rejection rate; flag if copy quality degrades |
| Brand voice score | Automatic quality evaluation against tone rubric |
| Latency | Monitor batch processing time |

### Module 04B — Virtual try-on (photo path)

| Signal | Why |
|--------|-----|
| Request ID (hashed) | Audit trail — no customer-identifiable data |
| Model version | Reproducibility |
| Content moderation outcome (pass/fail) | Compliance audit; confirm rejected photos never reach processing |
| Latency | Track try-on generation time |
| Error flags | Surface failures before customers notice |
| What is NEVER logged | Customer photo, measurement values, consent status, raw customer ID |

---

## Alert rules

| Alert | Condition | Action |
|-------|-----------|--------|
| Latency spike — rec engine | P99 over 200ms | Notify Javi |
| Hallucination detected — styling assistant | Product in response not in RAG context | Flag for manual review |
| LLM photo request detected | Any output requests a photo from the customer | CRITICAL — immediate alert; block response |
| Brand voice score below threshold | Score under 0.7 | Block publish; return to draft queue |
| Content moderation failure rate spike | More than 5% of uploads rejected in 1 hour | Investigate input source |
| Photo in trace detected | Any blob or image data in LangSmith log | CRITICAL — immediate alert; never permitted |

---

## Retention

LangSmith traces retained for 12 months. No personal data beyond hashed customer ID in any trace.