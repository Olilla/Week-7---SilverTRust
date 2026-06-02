# Data Map — GDPR Article 30

**System:** AI Transformation — Streetwear E-Commerce
**Modules covered:** 1–4
**Version:** 3 — June 2026

---

## Personal data inventory

| Data element | Module | Source | Purpose | Personal data? | Special category? | Legal basis | Retention | Rights mechanism | Secondary use permitted? |
|---|---|---|---|---|---|---|---|---|---|
| Session click / browse events | 01 | Customer browser session | Personalise product ranking | Yes | No | Legitimate interest (Art. 6(1)(f)) | Account lifetime | Deletion pipeline on closure or request | No — try-on data must not feed rec engine without separate consent |
| Purchase history | 01 | Order DB | User-to-user collaborative filter | Yes | No | Contract performance (Art. 6(1)(b)) | Account lifetime | Same deletion pipeline | No |
| Gender preference (self-declared) | 01 | Customer input | Cold-start ranking | Yes | No | Legitimate interest | Account lifetime | Deletable from account settings | No |
| Chat messages | 02 | Customer input | Generate styling response | Yes | No | Legitimate interest | Session only | Not applicable | No |
| Try-on preview event (product ID + timestamp + method) | 04 | System | Session log, personalisation, customer history | Yes (linked to session) | No | Legitimate interest | Account lifetime | Visible in account; deletable | No — without separate consent |
| Body measurements | 04A | Customer input | Avatar generation, size recommendation | Yes | No | Legitimate interest or standard consent (Art. 6(1)(f) or (a)) | Until customer deletes or closes account | Delete from account settings; auto-delete on closure | No |
| Customer photo | 04B | Customer upload | Garment overlay try-on | Yes | Likely yes (biometric, Art. 9) | Explicit consent only (Art. 7 + 9(2)(a)) | User-controlled: session / 6 / 12 / 24 months. Hard max 24 months. | Cascading deletion: primary, backups, CDN, derived data | No |
| Try-on result image | 04B | System-generated | Displayed to customer | Only if stored | Only if stored | Separate explicit consent to store | Session only by default | Not stored unless consented | No |
| Consent records | 04B | Consent UI | GDPR compliance documentation | Yes | No | Legal obligation (Art. 6(1)(c)) | Duration of account relationship | Log timestamp and consent text version | No |
| LangSmith traces | 01, 02, 03, 04B | System | AI observability and audit | Minimal (hashed customer ID only) | No | Legitimate interest | 12 months | No personal data beyond hashed ID | No |

---

## Data flows by module

### Module 01 — Recommendation engine
Customer browser
--> session events --> rec engine (scoring) --> ranked product list --> storefront
--> purchase history (from order DB) --> user-to-user filter

No data leaves the EU. No third-party data sharing.

### Module 02 — AI styling assistant
Customer chat input
--> RAG retrieval (catalog DB) --> LLM API (third-party provider, DPA required)
--> response --> customer
[nothing stored after session ends]

### Module 03 — Catalog automationProduct DB (no personal data)
--> Python cron job --> LLM API --> copy draft --> human review queue
--> approved copy --> product DB

### Module 04A — MeasurementsCustomer input form
--> parametric avatar model (no external API, no LLM)
--> avatar displayed to customer
--> [with opt-in] measurements stored in customer account DB (Frankfurt)

### Module 04B — PhotoCustomer consent screen (retention choice: session / 6 / 12 / 24 months)
--> photo upload
--> content moderation API (DPA required) --> pass/fail
--> [fail] photo discarded immediately
--> [pass] try-on model --> result displayed
--> [with explicit consent] photo encrypted in isolated Frankfurt bucket
--> auto-delete at chosen TTL OR on request OR on consent withdrawal

---

## Storage locations

| Data | Location | Justification |
|------|----------|---------------|
| Customer account data (measurements, preferences) | Frankfurt (EU) | GDPR Art. 44 — no cross-border transfer |
| Photo storage | Frankfurt, isolated encrypted bucket | GDPR Art. 9 — biometric data highest protection |
| Product DB | Client's existing infrastructure | Not personal data |
| LangSmith traces | LangSmith (US-based) — hashed IDs only | DPA required; no personal data in traces |
| LLM API calls | Third-party provider (EU region preferred) | DPA required; no personal data in prompts for catalog |