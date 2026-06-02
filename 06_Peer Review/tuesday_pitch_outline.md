# Tuesday Pitch — Proposal Outline (~10 minutes)

**Presenting team:** [Your team names]
**Reviewing team (review board):** [Paired team names]
**Date:** Tuesday, Week 7

---

## 1. The client and the problem (~2 min)

- Client: streetwear e-commerce retailer, Germany & Europe, online only, comparable to Springfield
- Stakeholders: Carlos (Marketing Director), Javi (Lead Developer)
- Core problem: the online experience is cold and impersonal — no equivalent to an in-store sales assistant. Customers browse without guidance, buy once, and do not return. AOV is low. Content production does not scale. Market share is being lost to C&A and Springfield.
- Why it matters: the gap is the experience, not the product. If left unresolved, competitors pull further ahead.

---

## 2. The solution (~3 min)

Four modules across three phases:

| Module | What it does | Phase |
|--------|--------------|-------|
| 01 — Rec engine | Personalised picks from session 1 | Phase 2 |
| 02 — Styling assistant | LLM-powered in-store advice, online | Phase 2 |
| 03 — Catalog automation | Python + LLM copy pipeline with human sign-off | Phase 1 |
| 04 — Virtual try-on | Measurements (Option A) first; photo (Option B) after DPIA | Phase 3 |

Key point: AI is used only where genuinely needed. Avatar generation, content moderation, and product retrieval are plain software. This keeps cost down and compliance simpler.

---

## 3. Compliance position (~2 min)

- Modules 1–3: EU AI Act limited risk. Obligations: "AI-powered" label, no covert emotion analysis, LangSmith audit trail.
- Module 4 measurements path: standard GDPR Art. 6. Legitimate interest. No DPIA. Can launch first.
- Module 4 photo path: GDPR Art. 9 biometric data. Explicit consent only. DPIA mandatory before build. User-controlled retention up to 24 months.
- Category exclusion: underwear, swimwear, intimate apparel excluded from try-on at catalog level.
- Open risk flagged: EU AI Act conformity assessment for photo path still to be commissioned.

---

## 4. Monitoring (~1 min)

- LangSmith project live: [link or screenshot]
- What is monitored: inputs and outputs per module, latency, hallucination checks, brand voice scores, human review decisions, photo request detection
- What is never in logs: customer photos, raw measurements, identifiable customer IDs
- Client summary: "Every AI decision is recorded. If something goes wrong, you can find it. If an auditor asks, you can prove it."

---

## 5. The ask

"We are asking for approval to proceed to build on Phase 1 and Phase 2. Phase 3 measurements path can also proceed immediately. Phase 3 photo path is gated on DPIA completion."

Do you approve, or what needs to change?

---

## Anticipated questions

| Question | Prepared answer |
|----------|----------------|
| Is the photo path really biometric under EU AI Act, not just GDPR? | The EU AI Act conformity assessment will confirm this. We have flagged it as an open risk rather than asserting a classification we cannot yet defend. |
| What is the lawful basis for the rec engine if the customer has not consented to tracking? | Legitimate interest under Art. 6(1)(f). Consent banner is required before behavioural data is collected. |
| What happens if the DPIA takes longer than 6 weeks — does Phase 3 slip? | Only the photo path slips. Measurements path has no legal prerequisites and launches on schedule. |
| Can LangSmith actually prove to an auditor what the AI said? | Yes. Every trace includes the exact input, output, model version, and timestamp. The trace is the audit record. |