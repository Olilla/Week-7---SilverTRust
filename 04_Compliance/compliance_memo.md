# Compliance Memo

**AI Solution — Virtual Try-On: Photo Storage & Body Measurements**
**Updated to reflect body measurements input as a third try-on option**

| | |
|---|---|
| **Prepared for** | Carlos (Marketing) & Javi (Development) |
| **Date** | June 2026 |
| **Version** | 3 — supersedes previous compliance memos for Module 4 |
| **Scope** | Module 4 Virtual Try-On only. Modules 1–3 unchanged. |

> This memo is a practical guide to compliance requirements as understood at the time of writing. It is not a legal opinion. Share with your legal team and DPO before build begins on any part of Module 4.

---

## 1. The short version — three input methods, two compliance profiles

Module 4 now offers three ways for a customer to interact with the virtual try-on: enter body measurements, upload or take a photo, or use both together. These two data types are fundamentally different from a compliance perspective.

| | **Measurements (Option A)** | **Photo storage (Option B)** |
|---|---|---|
| Data type | Standard personal data. Height and clothing measurements. Not biometric data. | Likely biometric personal data under GDPR Article 9. Body image linked to identity. |
| GDPR tier | Standard. Articles 5–6 apply. Legitimate interest or consent. | Special category. Article 9 applies. Explicit consent only. Highest protection. |
| DPIA needed? | No. Does not meet the mandatory threshold. | Yes. Mandatory before build begins. |
| Encryption level | Standard account data encryption. | AES-256 minimum. Isolated storage bucket. |
| Retention | Until customer deletes or closes account. | 6 months maximum. Auto-deletion enforced. |
| Content moderation | Not applicable. | Mandatory at upload. Nudity, age, quality. |
| Complexity | Low. Equivalent to storing a shipping address. | High. Full biometric data handling pipeline. |

Measurements are the simpler, lower-risk option. They should be the default path for all customers, with photo upload as an opt-in enhancement. This sequencing also means the try-on feature can launch sooner — the measurements path has no legal prerequisites.

---

## 2. Regulatory framework — what laws apply and to which option

| **Framework** | **Measurements** | **Photo storage** | **Applies to both** | **Key point** |
|---|---|---|---|---|
| GDPR | Art. 5, 6, 13, 17 | Art. 6, 7, 9, 13, 17, 35 | Art. 17 erasure | Measurements = standard data. Photos = special category. |
| EU AI Act | Not applicable to input form | Art. 52 transparency | LangSmith audit trail | AI disclosure label required for photo try-on result. |
| DSA | Anti-dark patterns apply | Anti-dark patterns apply | Symmetric choice | Declining either option must be easy and penalty-free. |
| Consumer Rights | Sizing accuracy obligation | Sizing accuracy obligation | Right of withdrawal | AI sizing must not deceive. Returns remain customer right. |
| EU Data Act | Portability right applies | Portability right applies | Both data types | Customers can export measurements and photo data. |
| ePrivacy | If cached locally | If cached locally | Cookie consent | Applies if data stored in browser cache or local storage. |

---

## 3. Measurements — GDPR in detail

### Is measurement data personal data?

Yes. Height, chest, waist, hips, and inseam are personal data under GDPR Article 4 because they relate to an identified or identifiable person (the customer account holder). However, they are not special category data and do not qualify as biometric data under Article 9 unless they are used to uniquely identify a person through automated processing — which storing measurements for clothing purposes does not constitute.

Practical implication: storing a customer's height and clothing measurements carries the same legal weight as storing their delivery address. Manageable with standard account data practices.

### Article 6 — Legal basis for measurements

| Option | Detail |
|--------|--------|
| **Option 1 — Legitimate interest (recommended)** | The most straightforward basis. The business has a legitimate interest in helping customers find the right size. Customers have a reasonable expectation that measurements they enter will be used to improve their shopping experience. A brief Legitimate Interest Assessment (LIA) documents this. |
| **Option 2 — Consent** | Also valid. A simple opt-in toggle ("Save my measurements") at the point of entry. Less procedural overhead than photo consent because standard consent, not explicit consent, is sufficient for non-special category data. |

### Article 13 — Transparency

- Privacy policy must state that body measurements may be stored in the customer account
- Must state the legal basis (legitimate interest or consent, whichever is chosen)
- Must state how long measurements are kept and how to delete them
- No special disclosure format required — standard privacy policy language is sufficient

### Article 17 — Right to erasure

- Customer can delete all stored measurements at any time from account settings
- Measurements deleted automatically when the customer account is closed
- Deletion is immediate and complete — no backup retention required beyond standard data backup policy
- Deletion of measurements must not affect other account data (orders, preferences, etc.)

### DPIA — not required for measurements

A Data Protection Impact Assessment is not required for storing body measurements. The DPIA threshold under GDPR Article 35 is triggered by large-scale processing of special category data or systematic monitoring. Storing height and clothing measurements for an e-commerce try-on feature does not meet this threshold.

---

## 4. Photo storage — GDPR in detail

All requirements from the previous compliance memo remain in force. Key points summarised below.

| Requirement | Detail |
|-------------|--------|
| **Art. 9 — Biometric data** | Body images stored in a database linked to a customer account are very likely biometric personal data under Article 9. Highest protection tier. Explicit consent required. Cannot rely on legitimate interest. |
| **Art. 6 & 7 — Consent** | Explicit, specific, freely-given consent required. Separate opt-in. Unchecked by default. Withdrawable at any time. Consent records must be kept. |
| **Art. 35 — DPIA** | Mandatory before build begins. Processing biometric data with AI at scale triggers this requirement. Allow 4–6 weeks. |
| **Art. 17 — Erasure** | Immediate, permanent, cascading deletion on request. Auto-expiry at 6 months. Must cover primary storage, backups, CDN cache, derived data. |
| **Art. 13 & 14 — Transparency** | Privacy policy must state what is collected, where stored, how long, and how to delete. Biometric data handling must be explicitly mentioned. |

---

## 5. Front-end compliance rules

### Required — measurements

| Rule | Detail |
|------|--------|
| Input guidance | Each measurement field must include a visual illustration showing where to measure on the body. A "How to measure" help section is required to avoid inaccurate inputs. |
| Save toggle | An opt-in toggle to save measurements. Can be pre-checked for returning customers who previously saved. Must be unchecked for new customers. |
| Independent deletion | Measurements can be deleted independently of photo data. One deletion must not trigger the other. |
| Non-discriminatory access | The measurements path must produce a full-quality try-on result. Customers who decline photo upload must not receive a visually degraded experience. |
| Use limitation disclosure | If measurements are used for anything beyond try-on, this must be disclosed in the privacy policy and at the point of data collection. |

### Required — photo

| Rule | Detail |
|------|--------|
| Explicit consent screen | Shown before any photo interaction. Unchecked opt-in by default. Separate from T&Cs. Equal prominence for accept and decline. |
| Age confirmation | Customer must confirm 18+ before photo upload. Never assume adult. |
| AI disclosure label | Visible "AI-powered" label required. Customer must know the try-on image is synthetically generated. |
| Content moderation | Nudity detection, age flagging, quality check before any processing. Rejected photos discarded immediately, never stored. |
| Post-session confirmation | Tell customer whether photo was stored or deleted. Link to account settings. |

### Not permitted — both options

| Rule | Detail |
|------|--------|
| Gatekeeping access | Neither measurements nor photo upload may gate access to browsing or purchasing. |
| Cross-use without consent | Measurements must not feed recommendation engine targeting. Photos must not be used for any purpose other than try-on without separate explicit consent. |
| Pre-checked photo consent | Photo storage checkbox must always be unchecked by default. Illegal under GDPR Art. 6 & 7. |
| Storing rejected photos | Photos rejected by content moderation must be permanently discarded immediately. |
| Photos outside Frankfurt | No photo transferred to any server or service outside the EU at any point. |
| Covert emotion analysis | No tracking of facial expressions or emotional reactions to try-on results without disclosure. |
| Photos in logs | Photo must never appear in LangSmith, system logs, or any audit record. |

---

## 6. Data flow inventory — Module 4

### Measurements data

| | |
|---|---|
| **Inputs** | Height, chest, waist, hips, inseam (required). Shoulder width, arm length, neck circumference (optional). Entered manually by the customer. |
| **Outputs** | Parametric 3D avatar displayed to customer. Size recommendation for selected garment. Fit indicator (tight / good / loose). |
| **What is stored** | Measurement values as structured data in customer account profile. No image generated or stored. |
| **Storage location** | Frankfurt customer account database. Standard account data. No isolated bucket required. |
| **Retention** | Until customer deletes or closes account. No maximum retention period. Updated by customer at any time. |
| **Personal data?** | Yes — standard personal data under GDPR Art. 4. Not special category. Not biometric. |
| **Legal basis** | Legitimate interest or standard consent. Either is valid. |
| **LangSmith logging** | Not applicable. No LLM inference required for avatar generation from measurements. |

### Photo data

| | |
|---|---|
| **Inputs** | Customer-uploaded or camera photo (full body or portrait). Must pass content moderation before processing. |
| **Outputs** | AI-generated try-on result image. Displayed to customer. Not stored by default. |
| **What is stored** | Original photo encrypted in isolated Frankfurt storage bucket. Linked to customer account ID only. |
| **Storage location** | Frankfurt only. Isolated encrypted storage bucket. Not the general account database. |
| **Retention** | 6 months from upload, then permanent deletion. Deleted immediately on customer request or consent withdrawal. |
| **Personal data?** | Yes — likely biometric personal data under GDPR Art. 9. Special category. |
| **Legal basis** | Explicit consent only. Cannot rely on legitimate interest. |
| **LangSmith logging** | Request ID, model version, latency, error flags. Customer ID hashed. Photo never logged. |

### Summary — personal data by input method

| Data element | Personal data? | Special category? | DPIA needed? | Key action |
|---|---|---|---|---|
| Measurements | Yes | No | No | Legitimate interest basis. Standard account data handling. Delete on request. |
| Photo (stored) | Yes | Likely yes | Yes | Explicit consent. AES-256 storage. 6-month TTL. Full deletion pipeline. |
| Try-on result image | Only if stored | Only if stored | No | Session-only by default. Separate consent if customer wishes to save. |
| Consent record | Yes | No | No | Keep for duration of account relationship. Log timestamp and text version. |
| LangSmith traces | Minimal (hashed ID) | No | No | 12-month retention. No photo or measurement values in traces. |

---

## 7. EU AI Act classification

**Modules 1–3: Limited risk** (Art. 52 transparency obligations apply). No formal audit required.

**Our role:** Deployer. The underlying LLM is provided by a third-party. The client is responsible for how the model is used, not for the model itself.

| Obligation | What it means in practice |
|-----------|--------------------------|
| Art. 52 — Transparency | Visible "AI-powered" label required on the styling assistant and on any try-on output |
| Art. 5 — No prohibited practices | System must not covertly measure customer emotion or reaction |
| Audit trail | LangSmith logs every AI decision with timestamp, model version, and quality score |

**Module 4 — photo path:** The measurements path (Option A) remains limited risk. The photo path (Option B) involves biometric data processing by an AI system, which requires assessment against potential high-risk classification under Art. 6(2) and Annex III point 1(a). Commission a formal EU AI Act conformity assessment alongside the DPIA before Phase 3 photo build begins.

---

## 8. Open risks

| Risk | Severity | Status |
|------|----------|--------|
| Photo path may trigger high-risk EU AI Act designation | High | Conformity assessment required before Phase 3 photo build |
| LLM provider DPA not yet confirmed | Medium | Must be resolved before Phase 2 launch |
| DPIA for photo path not yet started | High | Commission now — measurements path can go live first |
| Privacy policy not yet updated | Medium | Required before Phase 1 launch |

Surfacing these risks now is the right approach. A clear classification with named open risks is more defensible than a memo that claims everything is resolved.

---

## 9. Action checklist

### Phases 1 & 2 — Modules 1–3

- [ ] No personal data in LLM prompts for product descriptions
- [ ] Pipeline logs satisfy GDPR Art. 30 record-keeping
- [ ] LangSmith monitoring live from day one
- [ ] Privacy policy updated
- [ ] Consent banner — legal basis for behavioural data confirmed
- [ ] "AI-powered" label on styling assistant widget
- [ ] Deletion pipeline live and tested for rec engine vectors
- [ ] DPA confirmed with LLM API provider

### Phase 3 — measurements path (can launch first)

- [ ] Privacy policy updated to include measurements storage, legal basis, retention, and deletion rights
- [ ] Legitimate Interest Assessment documented
- [ ] Input form UX designed and built with visual guidance for each field
- [ ] Measurements management page built in account settings: view, edit, delete all measurements
- [ ] Avatar model selected and integrated (build vs buy — SMPL, CAESAR body model)
- [ ] Size recommendation logic built: fit indicator from measurements vs garment size chart

### Phase 3 — photo path (requires DPIA first)

- [ ] DPIA completed and signed off (allow 4–6 weeks)
- [ ] Consent screen UI designed and legal-reviewed before build begins
- [ ] Content moderation API integrated; DPA with provider confirmed
- [ ] AES-256 encrypted storage + 6-month auto-deletion built and tested
- [ ] Cascading deletion pipeline tested end-to-end (primary storage, backups, CDN, derived data)
- [ ] DPA confirmed with LLM inference provider before photos processed
- [ ] Penetration test on photo storage infrastructure before go-live

Recommended sequencing: launch the measurements path first (no DPIA required, faster to build). Launch the photo path once the DPIA is complete.

---

*This memo is informational only and does not constitute legal advice. June 2026. Private & Confidential.*