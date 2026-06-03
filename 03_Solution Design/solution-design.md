# Solution Design

**Client:** Silver Tour Streetwear E-Commerce (Germany & Europe)
**Prepared for:** Carlos (Marketing Director) & Javi (Lead Developer)
**Version:** 1.0 — Tuesday, Week 7

---

## What the AI does

Four modules delivered across three phases:

| Module | Name | What it does | Phase |
|--------|------|--------------|-------|
| 01 | Recommendation engine | Personalised product picks from session 1, no purchase history required. Session-based and user-to-user collaborative filtering, weighted score merge, in-stock and margin filters. | Phase 2 (Weeks 6–14) |
| 02 | AI styling assistant | LLM-powered chat interface replicating in-store advice. RAG pulls live catalog so only real products are recommended. Brand voice enforced via system prompt. | Phase 2 (Weeks 6–14) |
| 03 | Catalog automation | Python + LLM pipeline generates product descriptions and SEO copy from structured product data. Human review required before publish. | Phase 1 (Weeks 1–8) |
| 04 | Virtual try-on | Three input options: body measurements (Option A), photo upload (Option B), or both combined (Option C). Avatar or overlay generated and displayed. Optional storage with consent. | Phase 3 (from Week 16) |

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

## Workflow — Module 01: Recommendation engine

1. New visitor: gender prefs + trending items weighted blend
2. Browsing session underway: session-based collaborative filter on viewed items
3. Returning buyer: user-to-user collaborative filter on purchase data
4. Score merge: weighted blend, in-stock filter, margin boost, diversity rule
5. Output: top 6–12 personalised products served in under 80ms
6. LangSmith traces every ranking decision

---

## Workflow — Module 02: AI styling assistant

1. Customer types a styling question in natural language
2. RAG retrieves matching live catalog products
3. LLM generates response in brand voice (system prompt set by Carlos)
4. Response displayed with product cards and add-to-cart links
5. LangSmith scores every response for tone and accuracy
6. Cap: 5 turns per session to control token cost

---

## Workflow — Module 03: Catalog automation

1. Product data pulled from DB (name, category, colour, size, price, images)
2. Python cron job sends data to LLM with brand-voice prompt
3. LLM generates product description and SEO copy
4. Draft sent to human review queue — nothing publishes without approval
5. Approved copy written back to product DB
6. LangSmith tracks every generated draft and human decision

---

## Workflow — Module 04: Virtual try-on

### Option A — Body measurements

1. Customer enters height, chest, waist, hips, inseam via form with visual guidance
2. Parametric 3D avatar generated from measurements (no LLM inference)
3. Garment draped on avatar; fit indicator displayed (tight / good fit / loose)
4. Size recommendation shown before avatar generation
5. With opt-in toggle: measurements saved to customer account
6. Customer can update or delete measurements from account settings at any time

### Option B — Photo upload

1. Explicit consent screen shown before any photo interaction (unchecked by default)
2. Age confirmation (18+)
3. Content moderation filter: nudity detection, partial nudity flagging, single-person verification, quality check
4. Try-on model drapes garment on photo
5. With explicit consent: photo stored encrypted in Frankfurt; retention user-controlled (session / 6 / 12 / 24 months), hard maximum 24 months
6. Auto-deletion at chosen TTL or immediately on customer request
7. LangSmith logs request ID, latency, error flags — no photo ever in logs

### Option C — Combined (Recommended)

Both paths run in sequence. Measurements provide sizing accuracy; photo provides visual realism. Each data type handled with its own rules independently.

### Category exclusion

The following categories do not display a try-on button and are excluded from all try-on flows: underwear, swimwear, intimate apparel. Enforced at catalog level.

---

## Data the system touches

| Module | Input data | Output data | Storage | Retention |
|--------|------------|-------------|---------|-----------|
| 01 — Rec engine | Session clicks, browse history, purchase history, gender prefs | Product ranking scores | Behavioural vectors in account DB | Until account deleted |
| 02 — Styling assistant | Customer chat messages, live catalog | Text response + product cards | Session only | Session only |
| 03 — Catalog automation | Product name, category, colour, price, images | Copy drafts | Draft queue + approved copy in product DB | Indefinite (product data) |
| 04A — Measurements | Height, chest, waist, hips, inseam | 3D avatar, fit indicator | Customer account DB, Frankfurt | Until deleted by customer |
| 04B — Photo | Customer photo | Try-on result image | Isolated encrypted bucket, Frankfurt | User-controlled: max 24 months |

---

## Investment summary

| Module | Build cost | Monthly running cost |
|--------|------------|----------------------|
| 01 — Rec engine | €15k–25k | €200–600 |
| 02 — Styling assistant | €10k–18k | €300–1,200 |
| 03 — Catalog automation | €6k–10k | €50–200 |
| Phase 1+2 total | €31k–53k | €550–1,900 |
| Phase 3 measurements add | +€6k–12k | negligible |

---

## Delivery timeline

| Phase | Weeks | Modules | Key milestone |
|-------|-------|---------|---------------|
| 1 | 1–8 | Catalog automation | LangSmith live, brand voice set, -70% content time |
| 2 | 6–14 | Rec engine + styling assistant | A/B test live, +15–25% AOV target |
| 3 | 16+ | Virtual try-on | Measurements path first; photo path after DPIA |