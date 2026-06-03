# Solution Design

**Client:** Streetwear E-Commerce (Germany & Europe)
**Prepared for:** Carlos (Marketing Director) & Javi (Lead Developer)
**Version:** 1.0 — Tuesday, Week 7

| 4 AI Modules — covering the full customer journey | 3 Delivery Phases — starting with quick wins in 8 weeks | EU Compliant — GDPR, EU AI Act, Frankfurt-hosted | LangSmith Monitoring — full LLM observability from day one |
|---|---|---|---|

---

## Executive summary

This proposal outlines a four-module AI solution designed to address the core commercial challenges: a shopping experience that feels impersonal, low average order value, limited customer retention, and significant manual effort in catalog operations.

Each module is scoped to deliver measurable value independently, so the client can start with quick wins and expand over time. The full solution is built on existing Frankfurt infrastructure and is designed to be fully compliant with GDPR, the EU AI Act, and German data protection law from day one.

The primary objective is to replicate the in-store experience online — providing the personalisation, guidance, and styling advice that converts browsers into buyers and one-time customers into loyal ones.

### Business challenges we are solving

| Challenge | AI solution |
|-----------|-------------|
| Impersonal shopping experience | AI styling assistant + recommendation engine |
| Low average order value (AOV) | Personalised cross-sell and upsell at checkout |
| Low customer retention | Behaviour-based re-engagement and lifecycle marketing |
| Manual catalog operations | Automated content generation pipeline (Python + LLM) |
| Losing ground to C&A and Springfield | Faster, more personalised experience competitors cannot match |

---

## Why AI and not a custom-built technical solution?

Javi's team could build parts of this with traditional code — rule-based filters, manual segmentation, template-driven content. The question is not capability, it is what happens next.

Rules-based systems require a developer every time customer behaviour shifts or the catalog changes. An AI recommendation engine learns from every session and improves automatically. A styling assistant that answers natural language questions across hundreds of SKUs simply cannot be built as a decision tree — it only exists as an LLM. And template-based content generation produces exactly the generic copy Carlos wants to avoid.

The honest trade-off: custom code means full control and no external dependencies. AI means a dependency on an LLM provider — but it delivers capability that would take years to build from scratch and improves continuously without additional engineering investment.

The proposal does not ask the team to step back from engineering. It asks them to own the infrastructure, and let AI handle what AI does better.

---

## Proposed AI solution — four modules

### Module 1 — Product recommendation engine (Highest priority)

A personalisation layer that understands each customer's preferences and surfaces the right products at the right moment — including before any purchase history exists, using browsing behaviour and preference signals already stored in Frankfurt.

**Workflow:** Browsing events → Embedding model → Ranked product list

**Key benefits:**
- Increases average order value through relevant cross-sell and upsell recommendations
- Solves the cold-start problem using existing gender and category preference signals
- Builds customer purchase profiles that improve with every interaction
- Presents complementary products before checkout to increase basket size

**Workflow detail:**
1. New visitor: gender prefs + trending items weighted blend
2. Browsing session underway: session-based collaborative filter on viewed items
3. Returning buyer: user-to-user collaborative filter on purchase data
4. Score merge: weighted blend, in-stock filter, margin boost, diversity rule
5. Output: top 6–12 personalised products served in under 80ms
6. LangSmith traces every ranking decision

---

### Module 2 — AI styling assistant (High priority)

A chat-style assistant embedded in the storefront that replicates the in-store sales assistant experience. It answers questions like "what goes with this hoodie?" and "what size should I order?", providing the guidance customers currently cannot get online.

**Workflow:** Customer message → LLM + catalog context → Styled response + product links

**Key benefits:**
- Addresses the "cold" online experience Carlos identified directly
- Enables natural cross-sell through conversational product discovery
- Brand voice and tone controlled via system prompt — not generic AI output
- Reduces decision paralysis and cart abandonment

**Workflow detail:**
1. Customer types a styling question in natural language
2. RAG retrieves matching live catalog products
3. LLM generates response in brand voice (system prompt set by Carlos)
4. Response displayed with product cards and add-to-cart links
5. LangSmith scores every response for tone and accuracy
6. Cap: 5 turns per session to control token cost

---

### Module 3 — AI content & catalog automation (High operational value)

An automated pipeline using Python scripts and an LLM to generate product descriptions, attributes, and SEO copy at scale. A human review gate ensures nothing publishes without approval, directly addressing Carlos's concern about generic or off-brand copy.

**Workflow:** Product data + images → Python + LLM pipeline → Draft → review → publish

**Key benefits:**
- Reduces manual content effort dramatically across large product volumes
- Brand voice enforced at prompt level and validated via LangSmith quality scores
- SEO-optimised output improves organic discoverability
- Human-in-the-loop approval: AI accelerates drafting, humans decide what publishes

**Workflow detail:**
1. Product data pulled from DB (name, category, colour, size, price, images)
2. Python cron job sends data to LLM with brand-voice prompt
3. LLM generates product description and SEO copy
4. Draft sent to human review queue — nothing publishes without approval
5. Approved copy written back to product DB
6. LangSmith tracks every generated draft and human decision

---

### Module 4 — Virtual try-on (Phase 3)

Customers upload a photo and receive a visualisation of how products look on them. This is the highest-effort module and the strongest competitive differentiator. A build-vs-buy evaluation is recommended before committing to an approach.

**Workflow:** Photo upload → Pose estimation + overlay model → Personalised visualisation

**Key benefits:**
- Removes one of the core disadvantages of online-only retail
- Significantly reduces return rates by setting accurate expectations
- Creates a memorable experience that drives word-of-mouth and retention
- Strongest differentiator versus C&A and Springfield

Module 4 offers three input methods. Customers can choose any one or combine them.

#### Option A — Body measurements

| Step | Action |
|------|--------|
| 1 | Customer selects "Enter measurements" on the try-on screen |
| 2 | Customer inputs height, chest, waist, hips, inseam via a simple form with guidance icons |
| 3 | 3D avatar generated from measurements — displayed to customer for confirmation |
| 4 | Garment draped on avatar — personalised result displayed |
| 5 | With opt-in, measurements saved to account for future visits |
| 6 | Customer can update or delete measurements at any time from account settings |

**Technical detail:**
- Fields required: height (cm or ft/in), chest circumference, waist circumference, hip circumference, inseam length
- Optional fields: shoulder width, arm length, neck circumference (improves accuracy for upper-body garments)
- Unit toggle: metric (cm) and imperial (ft/in, inches) both supported
- Visual guidance: each field accompanied by a small illustration showing where to measure
- Validation: min/max range checks per field to catch obvious input errors
- Size suggestion: system displays recommended size for selected garment before avatar is generated
- Avatar: parametric 3D body model, displayed in neutral stance with front, side, and back views
- Fit indicator: tight / good fit / loose, derived from measurements vs. garment size chart
- No AI inference or external API call required — pure parametric modelling
- Storage: structured data in standard customer account database in Frankfurt. Standard encryption in transit (TLS 1.2+) and at rest.

#### Option B — Photo upload / camera

| Step | Action |
|------|--------|
| 1 | Customer opts in to photo use via explicit consent screen |
| 2 | Photo passes content moderation filter (nudity, age, quality checks) |
| 3 | Try-on model processes photo and displays result |
| 4 | With explicit consent, photo stored encrypted in Frankfurt |
| 5 | On return visits, stored photo retrieved automatically |
| 6 | After retention period, photo permanently and automatically deleted |

#### Option C — Combined (Recommended)

Customer enters measurements first for sizing accuracy, then optionally adds a photo to refine the result. The avatar generated from measurements is enhanced by the photo's pose and body outline. Measurements and photo are treated with their respective data handling rules independently.

#### Category exclusion

The following categories do not display a try-on button and are excluded from all try-on flows: underwear, swimwear, intimate apparel. Enforced at catalog level.

#### Front-end requirements — measurements input screen

- Clear, simple form with one measurement per row
- Each row: measurement name, small illustration, input field, unit selector
- A "How to measure" expandable help section with a full-body diagram
- Real-time size suggestion updates as measurements are entered
- Save toggle: unchecked by default for new customers; pre-checked for returning customers who already saved
- Clear "Continue to try-on" button once all required fields are complete

#### Not permitted — measurements

- Requiring measurements to use the store (must never gate access to browsing or purchasing)
- Pre-filling from third-party sources without explicit disclosure
- Using measurements for recommendation engine targeting or marketing segmentation without separate consent
- Sharing measurements with any third party without explicit consent

#### Account settings — measurements management

- Customer can view all stored measurements at any time
- Customer can edit any individual measurement
- Customer can delete all measurements with a single action
- Customer can toggle measurement storage on or off independently of photo storage

---

## Where AI/LLM reasoning is genuinely needed vs. plain software

| Component | AI/LLM | Plain software | Reason |
|-----------|--------|----------------|--------|
| Recommendation engine — scoring | No | Yes | Weighted blend of signals; no natural language required |
| Recommendation engine — cold start | No | Yes | Gender prefs + trending items; rule-based is sufficient |
| Styling assistant — response generation | Yes | No | Natural language, brand voice, multi-turn context |
| Styling assistant — product retrieval | No | Yes | RAG retrieval is vector search, not LLM inference |
| Catalog automation — copy generation | Yes | No | Brand-voice prose requires LLM |
| Catalog automation — cron scheduling | No | Yes | Standard job scheduler |
| Virtual try-on — avatar from measurements | No | Yes | Parametric 3D model; no inference required |
| Virtual try-on — garment overlay on photo | No | Yes (CV model) | Computer vision, not an LLM |
| Content moderation (photo upload) | No | Yes (API) | Third-party moderation API, not LLM |

---

## Technical architecture & infrastructure

### Core technology stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Recommendation engine | Collaborative filtering + embeddings | Personalised product ranking from day one |
| AI styling assistant | LLM (Claude / GPT-4o) + RAG | Conversational product guidance with catalog context |
| Content pipeline | Python scripts + LLM + cron | Automated descriptions, attributes, SEO copy — no extra tooling required |
| Pipeline orchestration | n8n (optional, self-hosted) | Visual workflow management — can be introduced later as pipeline count grows |
| LLM monitoring | LangSmith | Tracing, quality scoring, prompt regression testing |
| Data layer | Existing company cloud, Frankfurt | No data migration required; already GDPR-compliant |

Note on pipeline orchestration: the content automation pipeline is built on Python scripts and standard cron scheduling — no additional tooling required. n8n is listed as an optional layer that can be introduced later if the team wants a visual interface for managing workflows, or if the number of automated pipelines grows to a point where a dedicated orchestration tool adds value. The AI outcomes are identical either way.

### LLM monitoring with LangSmith

Every LLM call across the styling assistant and content pipeline is traced in LangSmith:

- Latency and token cost tracked per call — cost management from day one
- Output quality scores flag low-confidence or off-brand responses before they reach users
- Hallucination detection alerts on factually inconsistent product claims
- Prompt regression testing ensures any model update is validated before it ships
- Full audit trail of AI decisions — required for EU AI Act transparency obligations

---

## Data the system touches

| Module | Input data | Output data | Storage | Retention |
|--------|------------|-------------|---------|-----------|
| 01 — Rec engine | Cookie ID, customer ID, gender preference, browsing events, purchase history, session behaviour | Ranked list of product IDs | User embedding vectors + click/purchase events in Frankfurt company cloud, encrypted | Behavioural events: 24 months then delete/anonymise. Vectors: delete on erasure request. |
| 02 — Styling assistant | Customer free-text message, current page context, live catalog (RAG), optional session history | AI-generated text response + product IDs | LangSmith traces only (anonymised). Conversation logs NOT stored by default. | LangSmith traces: 12 months. If conversation logs stored: max 30 days, auto-delete. |
| 03 — Catalog automation | Product attributes from internal DB (name, category, colour, size, price) — no customer data | Draft descriptions, SEO metadata, attribute tags | Draft queue until approved/rejected. Approved copy in product DB. | Approved: indefinite. Rejected drafts: delete after 30 days. LangSmith batch logs: 6 months. |
| 04A — Measurements | Height, chest, waist, hips, inseam (required); shoulder width, arm length, neck (optional) | 3D avatar, fit indicator, size recommendation | Customer account DB, Frankfurt, standard encryption | Until deleted by customer or account closed |
| 04B — Photo | Customer-uploaded photo | Try-on result image | Isolated encrypted bucket, Frankfurt, AES-256 | User-controlled: max 24 months |

---

## Delivery plan

| Phase | Weeks | Focus | Success metric |
|-------|-------|-------|----------------|
| Phase 1 | 1–8 | Catalog automation & foundation | 70%+ reduction in manual content creation time |
| Phase 2 | 6–14 | Recommendation engine & styling assistant | Measurable AOV increase; styling assistant engagement > 15% of sessions |
| Phase 3 | From week 16 | Virtual try-on (scope & build) | -20–30% return rate for try-on products |

**Phase 1 detail:**
- Deploy Python-based content pipeline for AI-generated product descriptions and attributes
- Integrate LangSmith monitoring and establish quality baselines
- Set up brand voice templates and human review workflow
- Audit and update consent banner for GDPR-compliant behavioural data collection

**Phase 2 detail:**
- Deploy recommendation engine using existing preference and behavioural data
- Launch AI styling assistant in storefront with brand voice system prompt
- A/B test recommendations against baseline; measure AOV and conversion impact
- LangSmith dashboards live for Javi's team; first regression test cycle completed

**Phase 3 detail:**
- Conduct build-vs-buy evaluation: assess vendors (Snap AR, Zeekit, custom model)
- Complete biometric data risk assessment required by EU AI Act
- POC with one product category before full rollout
- Measurements path first; photo path after DPIA complete

Phases 1 and 2 overlap — catalog automation pays for the next phase.

### Key success metrics

| Metric | Target | Module |
|--------|--------|--------|
| Average order value (AOV) | +15–25% within 90 days of launch | Recommendation engine |
| Content creation time | 70% reduction by end of Phase 1 | Catalog automation |
| Conversion rate | +10–20% from personalised journeys | Recommendation engine |
| Styling assistant engagement | > 15% of sessions | AI styling assistant |
| Return rate (Phase 3) | -20–30% for try-on products | Virtual try-on |
| Customer retention (6 months) | +10% repeat purchase rate | All modules combined |

---

## Investment summary

| Module | Build cost (est.) | Running cost / mo | Margin lever |
|--------|-------------------|-------------------|--------------|
| Recommendation engine | €15k–25k | €200–600 | Boost scoring weights higher-margin SKUs when similarity scores are close. Zero LLM API cost — pure vector math. |
| AI styling assistant | €10k–18k | €300–1,200 | Variable LLM token cost. Each 3-turn conversation ≈ €0.01–0.03. Cap turns at 5. Monitor via LangSmith budget alerts. |
| Catalog automation | €6k–10k | €50–200 | Direct labour saving: replaces manual copywriting. Typical payback 4–6 weeks. Saving ≈ €2k–6k/mo. |
| n8n (optional) | €1k–3k | €0 (self-hosted) | Visual workflow management layer. Recommended when pipeline count grows beyond 3–4. |
| Virtual try-on (Ph. 3) | €40k–120k | €500–3,000 | Margin case rests on return rate reduction. Scope before committing. |
| Phase 1+2 total | €31k–53k | €550–1,900 | Catalog automation payback: 4–6 weeks |
| Phase 3 — measurements add | +€6k–12k | Negligible | No content moderation, no isolated storage, no biometric pipeline. |

### How to track cost and margin in production

- **LangSmith** — tracks LLM cost per session, tokens in/out per call, cost by model version, and budget alerts when monthly spend exceeds a set threshold.
- **Pipeline logs (Python)** — the content automation scripts log LLM calls per run, execution time, and cost to the existing logging stack. If n8n is adopted later, its built-in execution history replaces this with a visual dashboard.
- **Business metrics (existing analytics)** — AOV before vs after recommendation engine (A/B test), gross margin per order with vs without AI assist, return rate baseline vs post try-on, content cost per SKU before vs after automation.

The monthly margin scorecard Carlos should review: total AI running costs in, revenue attributed to AI touchpoints and labour savings out. Net margin contribution = revenue gain + cost savings minus AI costs.

---

## Availability & resilience

The AI layer must never take the storefront down. Every module is architected as an independent service — if it fails, the site keeps working and customers can always buy.

Core principle: graceful degradation over hard dependency.

### Fallback states per module

**Module 1 — Recommendation engine (Lowest risk — fully cacheable)**

| State | Behaviour |
|-------|-----------|
| Healthy | Live personalised recommendations from Redis cache in <80ms |
| Degraded — cache stale | Serve last known recommendations (TTL extended to 1hr) |
| Scoring service down | Fall back to rule-based bestsellers in user's preferred category. Widget never empty. |

**Module 2 — AI styling assistant (Medium risk — external LLM dependency)**

| State | Behaviour |
|-------|-----------|
| Healthy | LLM API responds within timeout. Full conversational experience with product links. |
| LLM slow (>3s) | Show typing indicator up to 5s, then surface a canned response with top 3 products for current page category. |
| LLM API down | Hide chat widget entirely or show "back shortly". Storefront and rec engine fully unaffected — zero blast radius. |

**Module 3 — Catalog content automation (Lowest risk — fully async)**

| State | Behaviour |
|-------|-----------|
| Healthy | Python cron job runs nightly. New descriptions ready for review each morning. |
| Job fails | Script retries automatically (3x). Alert sent to Javi's team. Previously approved content stays live. |
| LLM unavailable | Job queued for next run. Existing product descriptions remain live. Zero customer impact. |

### SLA targets

| Service | Target | Note |
|---------|--------|------|
| Storefront | 99.9% uptime | Non-negotiable. AI services must never affect this. |
| Recommendation engine | 99.5% uptime, <80ms p99 | Cacheable — Redis keeps this achievable. |
| AI styling assistant | 95% availability | LLM API dependency limits this; fallback covers the gap. |
| Catalog pipeline | Best-effort nightly | Async — downtime has zero customer-facing impact. |

### What Javi's team needs to implement

- Circuit breaker on every LLM call — if 3 consecutive calls fail or time out, open the circuit and serve the fallback immediately
- Hard timeout budgets: recommendation engine 100ms, styling assistant 5s, virtual try-on 30s
- Redis cache as the first line of defence for recommendations
- All AI services deployed independently from the storefront — separate containers, separate deployments, separate health checks
- LangSmith alerts on error rate spike, latency breach, and upstream LLM API status changes
- Runbook per module: what does on-call do when the styling assistant goes down at 23:00 on a Friday?
- Load test before each phase goes live

---

## Why now

The competitive window for AI-powered personalisation in European streetwear is open today, but it will not stay open. C&A and Springfield are large operations with significant technology investment capacity. The advantage goes to the brand that moves first and builds customer data flywheels before the competition catches up.

Every week without a recommendation engine is a week where a customer browses the catalog, does not find what they are looking for without guidance, and buys from a competitor instead.

Current strengths:
- Clean, Frankfurt-hosted customer data already available for immediate use
- A strong internal development team capable of owning and evolving the solution
- A proprietary brand and product catalog — no marketplace dependency
- A clearly identified customer experience gap that AI can close directly

### Proposed next steps

| Step | Action |
|------|--------|
| 1 | Review this proposal with Carlos and Javi and align on Phase 1 scope |
| 2 | Consent banner audit — confirm legal basis for behavioural data used in recommendations |
| 3 | Kick off Python content pipeline POC with a subset of the product catalog (2 weeks) |
| 4 | Stand up LangSmith monitoring environment alongside the POC |
| 5 | Schedule Phase 2 scoping session once Phase 1 POC results are in hand |

### Recommended next steps — Module 4

| Step | Action |
|------|--------|
| 1 | Confirm measurements fields required — agree which are mandatory vs optional for garment categories in scope |
| 2 | Select parametric avatar model — evaluate build vs buy (open-source options: SMPL, CAESAR body model) |
| 3 | Privacy policy update — add measurements storage alongside photo storage update |
| 4 | DPIA for photo path — commission now; measurements path can go live before DPIA is complete |
| 5 | Design input form UX — illustrations and guidance are critical to avoid user drop-off |
| 6 | Phase 3 build sequencing — measurements path first, photo path once DPIA signed off |