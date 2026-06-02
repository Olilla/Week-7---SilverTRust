# Compliance Memo

**AI Solution — Streetwear E-Commerce: Modules 1–4**
**Prepared for:** Carlos (Marketing Director) & Javi (Lead Developer)
**Date:** June 2026 | Version 3
**Scope:** All four modules. Module 4 updated to reflect body measurements as a third input option and user-controlled retention.

> This memo is a practical guide, not a legal opinion. Share with your legal team and DPO before build begins on any part of Module 4.

---

## 1. The short version

**Modules 1–3** are limited risk under the EU AI Act. No formal audit required. Compliance is straightforward: consent banner, deletion pipeline, LangSmith audit trail, and an "AI-powered" label on the styling assistant.

**Module 4** has two compliance profiles:

| | Measurements (Option A) | Photo storage (Option B) |
|---|---|---|
| Data type | Standard personal data. Not biometric. | Likely biometric under GDPR Art. 9. |
| GDPR tier | Standard (Art. 5–6). Legitimate interest or consent. | Special category (Art. 9). Explicit consent only. |
| DPIA required? | No | Yes — mandatory before build begins |
| Encryption | Standard account data encryption | AES-256 minimum. Isolated storage bucket. |
| Retention | Until customer deletes or closes account | User-controlled: session / 6 / 12 / 24 months. Hard max 24 months. |
| Complexity | Low | High — full biometric data handling pipeline |

Recommended sequencing: launch the measurements path first. Launch the photo path once the DPIA is complete.

---

## 2. EU AI Act classification

### Modules 1–3: Limited risk

**Classification:** Limited risk (Art. 52 transparency obligations apply).

**Justification:** None of modules 1–3 falls into prohibited or high-risk categories under Annex III. They do not make decisions with legal or similarly significant effects on individuals, do not operate in a high-risk sector, and do not use biometric identification.

**Our role:** Deployer. The underlying LLM is provided by a third-party. The client is responsible for how the model is used, not for the model itself.

**Obligations:**

| Obligation | What it means in practice |
|-----------|--------------------------|
| Art. 52 — Transparency | Visible "AI-powered" label required on the styling assistant and on any try-on output |
| Art. 5 — No prohibited practices | System must not covertly measure customer emotion or reaction |
| Audit trail | LangSmith logs every AI decision with timestamp, model version, and quality score |

### Module 4 — Photo path: assessment required

The measurements path (Option A) remains limited risk. The photo path (Option B) involves biometric data processing by an AI system, which triggers a mandatory DPIA and requires assessment against potential high-risk classification under Art. 6(2) and Annex III point 1(a). Commission a formal EU AI Act conformity assessment alongside the DPIA before Phase 3 photo build begins.

---

## 3. GDPR

### Modules 1–3

| Personal data use | Legal basis | Data minimisation | Rights handling |
|-------------------|-------------|-------------------|-----------------|
| Session behaviour (rec engine) | Legitimate interest (Art. 6(1)(f)) | Session data only; no third-party enrichment | Deletion pipeline on account closure or request |
| Purchase history (rec engine) | Contract performance (Art. 6(1)(b)) | Only what is needed for scoring | Same deletion pipeline |
| Chat messages (styling assistant) | Legitimate interest | Session only — not stored | Not applicable |
| Product copy generation (catalog) | No personal data involved | Product attributes only | Not applicable |

### Module 4 — Measurements (Option A)

Measurements are standard personal data under GDPR Art. 4. Not special category. Not biometric.

| Requirement | Detail |
|------------|--------|
| Legal basis | Legitimate interest (Art. 6(1)(f)) — recommended. LIA required. Alternatively, standard consent. |
| Transparency (Art. 13) | Privacy policy must state measurements are stored, legal basis, retention, and how to delete. |
| Erasure (Art. 17) | Customer deletes from account settings at any time. Auto-deletion on account closure. |
| DPIA | Not required. |
| Purpose limitation (Art. 5(1)(b)) | Measurements used for try-on only. Must not feed recommendation engine or marketing without separate consent. Disclosed at point of collection. |
| Portability (EU Data Act) | Customer must be able to export stored measurements. |

### Module 4 — Photo storage (Option B)

Body photos linked to a customer account are very likely biometric personal data under GDPR Art. 9.

| Requirement | Detail |
|------------|--------|
| Legal basis | Explicit consent only (Art. 6 & 7). Separate opt-in, unchecked by default, withdrawable at any time. |
| DPIA (Art. 35) | Mandatory before build begins. Allow 4–6 weeks. |
| Encryption | AES-256 at rest. Isolated Frankfurt storage bucket. Strict access controls. |
| Retention | User-controlled: session / 6 / 12 / 24 months. Hard maximum 24 months. Auto-deletion on expiry, consent withdrawal, account deletion, or customer request. Cascading deletion. |
| Transparency (Art. 13 & 14) | Privacy policy must explicitly mention biometric data: what is stored, where, how long, how to delete. |
| Purpose limitation | Photos used for try-on only. Disclosed on consent screen. Secondary use requires separate opt-in. |
| Portability (EU Data Act) | Customer must be able to export stored photo. Handled independently from measurements. |

### Age

Germany sets digital consent age at 16 (GDPR Art. 8). For photo upload (biometric-adjacent data), the conservative 18+ threshold applies. Age gate at account creation plus re-confirmation at photo upload. Legal review of age verification tooling recommended before Phase 3.

---

## 4. Other applicable law

**Digital Services Act (DSA):** No dark patterns. Declining photo storage must be as easy as accepting it. Applies to both flows.

**Consumer Rights Directive:** Brand remains liable for returns if AI sizing guidance is inaccurate. Right of withdrawal must not be restricted.

**ePrivacy Directive:** Cookie consent required if behavioural data is stored in browser cache or local storage before server-side processing.

---

## 5. Front-end compliance rules

### Required — all modules
- Visible "AI-powered" label on styling assistant and on any try-on output
- Consent banner for behavioural data collection
- No covert emotion or sentiment analysis

### Required — Module 4 measurements
- Visual guidance illustration for each measurement field
- Save toggle: unchecked by default for new customers
- Measurements must never gate access to browsing or purchasing
- Measurements used for try-on only — disclosed at point of collection

### Required — Module 4 photo
- Explicit consent screen before any photo interaction, unchecked by default, separate from T&Cs
- Age confirmation (18+) before upload
- Content moderation: explicit nudity detection, partial nudity flagging, single-person verification, quality check
- Post-session confirmation: tell customer what was stored or deleted
- Rejected photos discarded immediately — never stored
- LLM must never request a photo from the customer — enforced at system prompt level and monitored in LangSmith

### Not permitted — Module 4
- Pre-checked photo consent box
- Blocking try-on access if consent declined
- Storing rejected photos
- Photos in LangSmith traces, system logs, or any audit record
- Photos transferred to any server outside the EU
- Try-on button on excluded categories: underwear, swimwear, intimate apparel

---

## 6. Open risks

| Risk | Severity | Status |
|------|----------|--------|
| Photo path may trigger high-risk EU AI Act designation | High | Conformity assessment required before Phase 3 photo build |
| LLM provider DPA not yet confirmed | Medium | Must be resolved before Phase 2 launch |
| DPIA for photo path not yet started | High | Commission now — allows measurements path to launch first |
| Privacy policy not yet updated | Medium | Required before Phase 1 launch |

---

## 7. Pre-launch checklist

### Phase 1 — Catalog automation
- [ ] No personal data in LLM prompts for product descriptions
- [ ] Pipeline logs satisfy GDPR Art. 30 record-keeping
- [ ] LangSmith monitoring live from day one
- [ ] Privacy policy updated

### Phase 2 — Rec engine + styling assistant
- [ ] Consent banner — legal basis for behavioural data confirmed
- [ ] "AI-powered" label on styling assistant widget
- [ ] Deletion pipeline live and tested for rec engine vectors
- [ ] DPA confirmed with LLM API provider

### Phase 3 — Measurements path (can launch first)
- [ ] Privacy policy updated to include measurements storage
- [ ] Legitimate Interest Assessment documented
- [ ] Measurements form UX with visual guidance built
- [ ] Deletion from account settings built and tested

### Phase 3 — Photo path (requires DPIA first)
- [ ] DPIA completed and signed off
- [ ] Consent screen UI designed and legal-reviewed
- [ ] Content moderation API integrated; DPA with provider confirmed
- [ ] AES-256 encrypted storage + user-controlled TTL built and tested
- [ ] Cascading deletion pipeline tested end-to-end
- [ ] Penetration test on photo storage infrastructure

---

*This memo is informational only and does not constitute legal advice.*