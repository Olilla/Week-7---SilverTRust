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

Module 4 offers three input methods. Customers can choose any one or combine them.

### Option A — Body measurements

| Step | Action |
|------|--------|
| 1 | Customer selects "Enter measurements" on the try-on screen |
| 2 | Customer inputs height, chest, waist, hips, inseam via a simple form with guidance icons |
| 3 | 3D avatar generated from measurements — displayed to customer for confirmation |
| 4 | Garment draped on avatar — personalised result displayed |
| 5 | With opt-in, measurements saved to account for future visits (simple toggle in account settings) |
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
- Storage: structured data (JSON or database record) in standard customer account database in Frankfurt. Standard encryption in transit (TLS 1.2+) and at rest.

### Option B — Photo upload / camera

| Step | Action |
|------|--------|
| 1 | Customer opts in to photo use via explicit consent screen |
| 2 | Photo passes content moderation filter (nudity, age, quality checks) |
| 3 | Try-on model processes photo and displays result |
| 4 | With explicit consent, photo stored encrypted in Frankfurt for 6 months |
| 5 | On return visits, stored photo retrieved automatically |
| 6 | After 6 months, photo permanently and automatically deleted |

### Option C — Combined (Recommended)

Customer enters measurements first for sizing accuracy, then optionally adds a photo to refine the result. The avatar generated from measurements is enhanced by the photo's pose and body outline. Measurements and photo are treated with their respective data handling rules independently.

### Category exclusion

The following categories do not display a try-on button and are excluded from all try-on flows: underwear, swimwear, intimate apparel. Enforced at catalog level.

### Front-end requirements — measurements input screen

- Clear, simple form with one measurement per row
- Each row: measurement name, small illustration, input field, unit selector
- A "How to measure" expandable help section with a full-body diagram
- Real-time size suggestion updates as measurements are entered
- Save toggle: unchecked by default for new customers; pre-checked for returning customers who already saved
- Clear "Continue to try-on" button once all required fields are complete

### Not permitted — measurements

- Requiring measurements to use the store (must never gate access to browsing or purchasing)
- Pre-filling from third-party sources without explicit disclosure
- Using measurements for recommendation engine targeting or marketing segmentation without separate consent
- Sharing measurements with any third party without explicit consent

### Account settings — measurements management

- Customer can view all stored measurements at any time
- Customer can edit any individual measurement
- Customer can delete all measurements with a single action
- Customer can toggle measurement storage on or off independently of photo storage

---

## Data the system touches

| Module | Input data | Output data | Storage | Retention |
|--------|------------|-------------|---------|-----------|
| 01 — Rec engine | Session clicks, browse history, purchase history, gender prefs | Product ranking scores | Behavioural vectors in account DB | Until account deleted |
| 02 — Styling assistant | Customer chat messages, live catalog | Text response + product cards | Session only | Session only |
| 03 — Catalog automation | Product name, category, colour, price, images | Copy drafts | Draft queue + approved copy in product DB | Indefinite (product data) |
| 04A — Measurements | Height, chest, waist, hips, inseam (required); shoulder width, arm length, neck circumference (optional) | 3D avatar, fit indicator, size recommendation | Customer account DB, Frankfurt, standard encryption | Until deleted by customer or account closed |
| 04B — Photo | Customer photo | Try-on result image | Isolated encrypted bucket, Frankfurt, AES-256 | User-controlled: max 24 months |

---

## Investment summary

| Module | Build cost | Monthly running cost | Notes |
|--------|------------|----------------------|-------|
| 01 — Rec engine | €15k–25k | €200–600 | Zero LLM API cost. Margin boost built in. |
| 02 — Styling assistant | €10k–18k | €300–1,200 | Variable LLM tokens. Cap at 5 turns/session. |
| 03 — Catalog automation | €6k–10k | €50–200 | Replaces manual copywriting. Pays back in 4–6 weeks. |
| n8n (optional) | €1k–3k | €0 (self-hosted) | Add later if visual workflow management needed. |
| Phase 1+2 total | €31k–53k | €550–1,900 | — |
| Phase 3 — measurements add | +€6k–12k | Negligible | No content moderation, no isolated storage, no biometric pipeline. |

---

## Delivery timeline

| Phase | Weeks | Modules | Key milestone |
|-------|-------|---------|---------------|
| 1 | 1–8 | Catalog automation | LangSmith live, brand voice set, -70% content time |
| 2 | 6–14 | Rec engine + styling assistant | A/B test live, +15–25% AOV target |
| 3 | 16+ | Virtual try-on | Measurements path first (no legal prerequisites); photo path after DPIA |

Phases 1 and 2 overlap — catalog automation pays for the next phase.

---

## Recommended next steps — Module 4

| Step | Action |
|------|--------|
| 1 | Confirm measurements fields required — agree with Carlos and Javi which are mandatory vs optional for garment categories in scope |
| 2 | Select parametric avatar model — evaluate build vs buy (open-source options: SMPL, CAESAR body model) |
| 3 | Privacy policy update — add measurements storage alongside photo storage update |
| 4 | DPIA for photo path — commission now; measurements path can go live before DPIA is complete |
| 5 | Design input form UX — measurements form requires careful design to avoid user drop-off. Illustrations and guidance are critical. |
| 6 | Phase 3 build sequencing — measurements path as first deliverable, photo path as second once DPIA signed off |