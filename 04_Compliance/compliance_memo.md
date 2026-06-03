# Compliance Memo

**AI Solution — EU AI Act, GDPR & Data Governance**
**Updated to reflect body measurements input as a third try-on option**

| | |
|---|---|
| **Prepared for** | Carlos (Marketing) & Javi (Development) |
| **Date** | June 2026 |
| **Version** | 3 — supersedes all previous compliance memos |
| **Scope** | All modules. Module 4 updated to reflect body measurements as a third input option. |

> This memo explains what EU and German law requires of an AI-powered e-commerce system like the one proposed. It is written for a business audience, not a legal one. Where action is needed, it is marked clearly. Share the relevant sections with your legal counsel before go-live.

---

## 1. The short version

Three sets of rules apply to this project. None of them are dealbreakers. All of them are manageable with straightforward implementation choices — most of which are already built into the proposed architecture.

| Framework | Summary |
|-----------|---------|
| EU AI Act | You are building a limited-risk AI system. Obligations are light: tell customers they are talking to AI, keep basic documentation, and log decisions. No special approval required. |
| GDPR | Your data is already in Frankfurt. The main things to confirm before launch: consent basis for using browsing data, and a deletion pipeline so customers can exercise their right to erasure. |
| Data hosting | All customer data stays in Frankfurt, Germany. No data crosses EU borders. This is your strongest compliance asset — it eliminates a whole category of GDPR risk. |

Module 4 has two compliance profiles:

| | Measurements (Option A) | Photo storage (Option B) |
|---|---|---|
| Data type | Standard personal data. Height and clothing measurements. Not biometric data. | Likely biometric personal data under GDPR Article 9. Body image linked to identity. |
| GDPR tier | Standard. Articles 5–6 apply. Legitimate interest or consent. | Special category. Article 9 applies. Explicit consent only. Highest protection. |
| DPIA needed? | No. Does not meet the mandatory threshold. | Yes. Mandatory before build begins. |
| Encryption level | Standard account data encryption. | AES-256 minimum. Isolated storage bucket. |
| Retention | Until customer deletes or closes account. | 6 months maximum. Auto-deletion enforced. |
| Content moderation | Not applicable. | Mandatory at upload. Nudity, age, quality. |
| Complexity | Low. Equivalent to storing a shipping address. | High. Full biometric data handling pipeline. |

Recommended sequencing: launch the measurements path first (no legal prerequisites). Launch the photo path once the DPIA is complete.

---

## 2. EU AI Act — what it means for you

The EU AI Act came into force in 2024 and applies to any AI system used in the EU.

### Risk tier classification

| Tier | Description | Applies here? |
|------|-------------|---------------|
| Unacceptable risk | Banned outright. | No |
| High risk | Requires formal conformity assessment, human oversight, and registration. Applies to AI in hiring, credit scoring, law enforcement. | No |
| Limited risk | Your tier. Recommendation engine and styling assistant fall here. Obligation: tell users they are interacting with AI. | Yes — Modules 1 & 2 |
| Minimal risk | Catalog content automation falls here. No obligations apply. | Yes — Module 3 |

**Our role:** Deployer. The underlying LLM is provided by a third-party. The client is responsible for how the model is used, not for the model itself.

### What you need to do

- **UI disclosure:** Add a visible "AI-powered" label to the styling assistant chat widget.
- **Documentation:** Keep a record of which AI model versions you are running and when they changed. LangSmith does this automatically.
- **Phase 3 only:** Before shipping the virtual try-on photo path, conduct a risk assessment — it processes body images, which the Act treats as biometric data.

None of the Phase 1 or Phase 2 modules require formal registration or third-party audit.

### Module 4 — photo path: assessment required

The measurements path (Option A) remains limited risk. The photo path (Option B) involves biometric data processing by an AI system, which requires assessment against potential high-risk classification under Art. 6(2) and Annex III point 1(a). Commission a formal EU AI Act conformity assessment alongside the DPIA before Phase 3 photo build begins.

---

## 3. Regulatory framework — what laws apply and to which option

| Framework | Measurements | Photo storage | Applies to both | Key point |
|-----------|-------------|---------------|-----------------|-----------|
| GDPR | Art. 5, 6, 13, 17 | Art. 6, 7, 9, 13, 17, 35 | Art. 17 erasure | Measurements = standard data. Photos = special category. |
| EU AI Act | Not applicable to input form | Art. 52 transparency | LangSmith audit trail | AI disclosure label required for photo try-on result. |
| DSA | Anti-dark patterns apply | Anti-dark patterns apply | Symmetric choice | Declining either option must be easy and penalty-free. |
| Consumer Rights | Sizing accuracy obligation | Sizing accuracy obligation | Right of withdrawal | AI sizing must not deceive. Returns remain customer right. |
| EU Data Act | Portability right applies | Portability right applies | Both data types | Customers can export measurements and photo data. |
| ePrivacy | If cached locally | If cached locally | Cookie consent | Applies if data stored in browser cache or local storage. |

---

## 4. GDPR — what it means for you

GDPR governs how you collect, store, use, and delete personal data about EU customers. You are already broadly compliant — Frankfurt hosting, encryption, and data access controls are in place.

### The four things to confirm before launch

| What needs doing | Why it matters |
|-----------------|----------------|
| Consent banner audit | Cookie-based browsing data powers the recommendation engine. The legal basis — legitimate interest or explicit consent — must be documented and reflected in the consent banner before the engine goes live. |
| Deletion pipeline | Customers have a right to request deletion of their data. That request must flow through the recommendation model, not just the main database. |
| Data processing records | GDPR Article 30 requires a record of processing activities. The pipeline logs in LangSmith and the Python scripts serve this purpose — they just need to be pointed to in your ROPA document. |
| Processor agreements | If the LLM API (Anthropic or OpenAI) processes any personal data, a Data Processing Agreement must be in place. In practice, the system prompt and product catalog contain no personal data, so this risk is low — but worth confirming with your legal team. |

### What you do not need to worry about

- Data transfers outside the EU — everything stays in Frankfurt.
- Special category data processing (health, politics, religion) — not relevant to fashion e-commerce.
- DPIA for Phases 1 and 2 — the processing is not high-risk under GDPR. Phase 3 photo path may require one.

### Measurements — GDPR in detail

**Is measurement data personal data?**

Yes. Height, chest, waist, hips, and inseam are personal data under GDPR Article 4 because they relate to an identified or identifiable person. However, they are not special category data and do not qualify as biometric data under Article 9 unless they are used to uniquely identify a person through automated processing — which storing measurements for clothing purposes does not constitute.

Practical implication: storing a customer's height and clothing measurements carries the same legal weight as storing their delivery address.

**Article 6 — Legal basis for measurements**

| Option | Detail |
|--------|--------|
| Legitimate interest (recommended) | The business has a legitimate interest in helping customers find the right size. Customers have a reasonable expectation that measurements they enter will be used to improve their shopping experience. A brief Legitimate Interest Assessment (LIA) documents this. |
| Consent | Also valid. A simple opt-in toggle ("Save my measurements") at the point of entry. Standard consent, not explicit consent, is sufficient for non-special category data. |

**Article 13 — Transparency**
- Privacy policy must state that body measurements may be stored in the customer account
- Must state the legal basis, how long measurements are kept, and how to delete them
- No special disclosure format required — standard privacy policy language is sufficient

**Article 17 — Right to erasure**
- Customer can delete all stored measurements at any time from account settings
- Measurements deleted automatically when the customer account is closed
- Deletion is immediate and complete
- Deletion of measurements must not affect other account data

**DPIA — not required for measurements**

The DPIA threshold under GDPR Article 35 is triggered by large-scale processing of special category data or systematic monitoring. Storing height and clothing measurements for an e-commerce try-on feature does not meet this threshold.

### Photo storage — GDPR in detail

| Requirement | Detail |
|-------------|--------|
| Art. 9 — Biometric data | Body images stored in a database linked to a customer account are very likely biometric personal data under Article 9. Highest protection tier. Explicit consent required. Cannot rely on legitimate interest. |
| Art. 6 & 7 — Consent | Explicit, specific, freely-given consent required. Separate opt-in. Unchecked by default. Withdrawable at any time. Consent records must be kept. |
| Art. 35 — DPIA | Mandatory before build begins. Processing biometric data with AI at scale triggers this requirement. Allow 4–6 weeks. |
| Art. 17 — Erasure | Immediate, permanent, cascading deletion on request. Auto-expiry at retention limit. Must cover primary storage, backups, CDN cache, derived data. |
| Art. 13 & 14 — Transparency | Privacy policy must state what is collected, where stored, how long, and how to delete. Biometric data handling must be explicitly mentioned. |

---

## 5. LangSmith — compliance by design

LangSmith is the monitoring layer for the AI system. From a compliance perspective, it does three useful things automatically:

- **Audit trail:** Every AI decision is logged with a timestamp, model version, and output. This satisfies the EU AI Act documentation requirement and provides an audit trail if a customer ever disputes a recommendation or AI-generated output.
- **Quality monitoring:** Token costs, latency, and error rates are tracked per call. If the styling assistant ever produces something unexpected, it is visible immediately.
- **Change control:** When the AI model changes, LangSmith runs regression tests to confirm behaviour is consistent. No model update ships without validation.

LangSmith is not just an engineering tool — it is your compliance paper trail. Keep it running from day one, even during the Phase 1 pilot.

---

## 6. Front-end compliance rules

### Required — measurements

| Rule | Detail |
|------|--------|
| Input guidance | Each measurement field must include a visual illustration showing where to measure. A "How to measure" help section is required. |
| Save toggle | Opt-in toggle to save measurements. Pre-checked for returning customers who previously saved. Unchecked for new customers. |
| Independent deletion | Measurements can be deleted independently of photo data. |
| Non-discriminatory access | The measurements path must produce a full-quality try-on result. Customers who decline photo upload must not receive a degraded experience. |
| Use limitation disclosure | If measurements are used for anything beyond try-on, this must be disclosed in the privacy policy and at the point of data collection. |

### Required — photo

| Rule | Detail |
|------|--------|
| Explicit consent screen | Shown before any photo interaction. Unchecked opt-in by default. Separate from T&Cs. Equal prominence for accept and decline. |
| Age confirmation | Customer must confirm 18+ before photo upload. Never assume adult. |
| AI disclosure label | Visible "AI-powered" label required. Customer must know the try-on image is synthetically generated. |
| Content moderation | Nudity detection, partial nudity flagging, single-person verification, quality check before any processing. Rejected photos discarded immediately, never stored. |
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
| LLM photo requests | The LLM must never request a photo from the customer — enforced at system prompt level and monitored via LangSmith alert. |

---

## 7. Data flow inventory — all modules

### Module 1 — Recommendation engine

| | |
|---|---|
| **Inputs** | Cookie ID or customer ID · gender preference signal · browsing events (pages viewed, products clicked, time on page) · purchase history · current session behaviour |
| **Outputs** | Ranked list of product IDs returned to the storefront per request — no personal data in the output itself |
| **What is stored** | User embedding vector (a mathematical representation of preferences — not readable as personal data but linked to a customer ID) · click and purchase events used to retrain the model nightly |
| **Storage location** | Frankfurt company cloud infrastructure · encrypted at rest |
| **Retention — events** | Behavioural events (clicks, views): 24 months, then delete or anonymise · purchase events: align with existing order retention policy |
| **Retention — vectors** | Delete or re-derive when underlying event data is deleted · must be cleared when a customer exercises right to erasure |
| **Personal data?** | Yes — user embeddings are linked to customer IDs. The deletion pipeline must cover these. |
| **LangSmith logging** | Request timestamp, model version, response time, product IDs returned. No personal data in traces if customer ID is hashed before logging. |

### Module 2 — AI styling assistant

| | |
|---|---|
| **Inputs** | Customer's free-text message · current page context (product ID, category) · live product catalog (injected via RAG — no personal data) · optional: session history within same conversation |
| **Outputs** | AI-generated text response · product IDs of recommended items · displayed to the customer and not stored by default |
| **What is stored** | Conversation logs should NOT be stored unless a specific decision is made to do so. If stored for quality review, they must be treated as personal data. Recommend: store only anonymised LangSmith traces, not full conversation text. |
| **Storage location** | LangSmith traces: Frankfurt (self-hosted) · if conversation logs are kept: Frankfurt company cloud only |
| **Retention — traces** | LangSmith traces (anonymised): 12 months for quality monitoring, then delete |
| **Retention — conversations** | If conversation history is stored: maximum 30 days, then auto-delete. Requires explicit consent basis separate from general T&Cs. |
| **Personal data?** | Potentially yes — free-text messages may contain personal data typed by mistake. System prompt should instruct the assistant to never acknowledge or store personal details typed by users. |
| **LangSmith logging** | Input prompt (without personal data), output text, latency, quality score, model version. Customer ID should be hashed or omitted from traces. |

### Module 3 — Catalog content automation

| | |
|---|---|
| **Inputs** | Product attributes from internal database (name, category, colour, size, price) · brand voice template · no customer personal data |
| **Outputs** | Draft product descriptions · SEO metadata · product attribute tags · these enter a human review queue before publishing |
| **What is stored** | Draft descriptions in the review queue until approved or rejected · approved descriptions stored in the product database · rejected drafts can be deleted immediately |
| **Storage location** | Frankfurt company cloud · same location as existing product database |
| **Retention** | Approved descriptions: indefinite · rejected drafts: delete after 30 days · LangSmith batch logs: 6 months |
| **Personal data?** | No — this module processes product data only. No customer personal data is involved at any stage. |
| **LangSmith logging** | Batch job ID, number of products processed, cost per run, quality scores. No personal data in any log. |

### Module 4 — Virtual try-on

#### Measurements data (Option A)

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

#### Photo data (Option B)

| | |
|---|---|
| **Inputs** | Customer-uploaded or camera photo (full body or portrait). Must pass content moderation before processing. |
| **Outputs** | AI-generated try-on result image. Displayed to customer. Not stored by default. |
| **What is stored** | Original photo encrypted in isolated Frankfurt storage bucket. Linked to customer account ID only. |
| **Storage location** | Frankfurt only. Isolated encrypted storage bucket. Not the general account database. |
| **Retention** | User-controlled: session / 6 / 12 / 24 months. Hard maximum 24 months. Deleted immediately on customer request or consent withdrawal. |
| **Personal data?** | Yes — likely biometric personal data under GDPR Art. 9. Special category. |
| **Legal basis** | Explicit consent only. Cannot rely on legitimate interest. |
| **LangSmith logging** | Request ID, model version, latency, error flags. Customer ID hashed. Photo never logged. |
| **Key action before build** | Legal review required. Confirm: (1) consent mechanism, (2) whether DPIA is required, (3) EU AI Act biometric risk assessment, (4) Data Processing Agreement with any inference provider. |

### Summary — personal data by module

| Module | Personal data? | Sensitive data? | Deletion required? | Key action |
|--------|---------------|-----------------|-------------------|------------|
| Recommendation engine | Yes | No | Yes | Deletion pipeline for user vectors |
| Styling assistant | Maybe | No | Yes | Hash customer ID in traces |
| Catalog automation | No | No | N/A | None — product data only |
| Measurements (Option A) | Yes | No | Yes | Legitimate interest basis. Standard account data handling. Delete on request. |
| Photo (Option B) | Yes | Likely yes | Yes | Explicit consent. AES-256 storage. User-controlled TTL. Full deletion pipeline. |
| Try-on result image | Only if stored | Only if stored | Yes if stored | Session-only by default. Separate consent if customer wishes to save. |
| Consent record | Yes | No | No | Keep for duration of account relationship. |
| LangSmith traces | Minimal (hashed ID) | No | No | 12-month retention. No photo or measurement values in traces. |

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

## 9. Action checklist — before go-live

### Phase 1 — Catalog automation (Weeks 1–8)

- [ ] Confirm with legal team that pipeline logs satisfy GDPR Article 30 record-keeping requirements
- [ ] Ensure no personal customer data is included in LLM prompts used for product description generation
- [ ] LangSmith monitoring live from day one
- [ ] Privacy policy updated

### Phase 2 — Recommendation engine + styling assistant (Weeks 6–14)

- [ ] Complete consent banner audit — confirm legal basis for using cookie-based browsing data
- [ ] Add "AI-powered" disclosure label to the styling assistant widget
- [ ] Confirm deletion pipeline is live and tested — a customer deletion request must clear the recommendation model
- [ ] Confirm Data Processing Agreements are in place with any LLM API provider used

### Phase 3 — Measurements path (can launch first)

- [ ] Privacy policy updated to include measurements storage, legal basis, retention, and deletion rights
- [ ] Legitimate Interest Assessment documented
- [ ] Input form UX designed and built with visual guidance for each field
- [ ] Measurements management page built in account settings: view, edit, delete all measurements
- [ ] Avatar model selected and integrated (build vs buy — SMPL, CAESAR body model)
- [ ] Size recommendation logic built: fit indicator from measurements vs garment size chart

### Phase 3 — Photo path (requires DPIA first)

- [ ] Conduct EU AI Act risk assessment before build begins
- [ ] DPIA completed and signed off (allow 4–6 weeks)
- [ ] Consent screen UI designed and legal-reviewed before build begins
- [ ] Content moderation API integrated; DPA with provider confirmed
- [ ] AES-256 encrypted storage + user-controlled TTL built and tested
- [ ] Cascading deletion pipeline tested end-to-end (primary storage, backups, CDN, derived data)
- [ ] DPA confirmed with LLM inference provider before photos processed
- [ ] Penetration test on photo storage infrastructure before go-live

---

## 10. What this is not

This memo is a practical guide to the compliance requirements as understood at the time of writing. It is not a legal opinion and does not replace advice from a qualified lawyer or data protection officer.

Share the Phase 2 checklist with your legal team or DPO at least four weeks before the recommendation engine goes live.

Bottom line: the compliance picture for this project is manageable. No high-risk AI classifications, no cross-border data flows, and no novel legal questions. The main pre-launch tasks are a consent banner audit and a UI disclosure label.

---

*This memo is informational only and does not constitute legal advice. June 2026. Private & Confidential.*