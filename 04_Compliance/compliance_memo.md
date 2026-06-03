**Compliance memo — AI solution**   ·   For internal review

**COMPLIANCE MEMO**

**AI solution — EU AI Act, GDPR & data governance**

| Prepared for **Carlos (Marketing) & Javi (Development)** | Date **June 2026** |
| --- | --- |

| This memo explains what EU and German law requires of an AI-powered e-commerce system like the one proposed. It is written for a business audience, not a legal one. Where action is needed, it is marked clearly. You should share the relevant sections with your legal counsel before go-live. |
| --- |

**1. The short version**

Three sets of rules apply to this project. None of them are dealbreakers. All of them are manageable with straightforward implementation choices — most of which are already built into the proposed architecture.

| **EU AI Act** | You are building a limited-risk AI system. Obligations are light: tell customers they are talking to AI, keep basic documentation, and log decisions. No special approval required. |
| --- | --- |
| **GDPR** | Your data is already in Frankfurt. The main things to confirm before launch: consent basis for using browsing data, and a deletion pipeline so customers can exercise their right to erasure. |
| **Data hosting** | All customer data stays in Frankfurt, Germany. No data crosses EU borders. This is your strongest compliance asset — it eliminates a whole category of GDPR risk. |

**2. EU AI Act — what it means for you**

The EU AI Act came into force in 2024 and applies to any AI system used in the EU. It places systems into four risk categories. The good news: the modules in this proposal all fall into the lowest two categories.

**What risk tier are you in?**

| **Unacceptable risk** | Banned outright. Not relevant here. |
| --- | --- |
| **High risk** | Requires formal conformity assessment, human oversight, and registration. Not relevant here — this tier applies to AI in hiring, credit scoring, law enforcement, and similar. |
| **Limited risk** | Your tier. Recommendation engine and styling assistant fall here. Obligation: tell users they are interacting with AI. One line of UI text. That is it. |
| **Minimal risk** | Catalog content automation falls here. No obligations apply. |

**What you need to do**

- **UI disclosure:** Add a visible 'AI-powered' label to the styling assistant chat widget.

- **Documentation:** Keep a record of which AI model versions you are running and when they changed. LangSmith does this automatically.

- **Phase 3 only:** Before shipping virtual try-on (Phase 3), conduct a risk assessment — it processes body images, which the Act treats as biometric data. This is a scoping exercise, not a blocker.

| None of the Phase 1 or Phase 2 modules require formal registration or third-party audit. The EU AI Act compliance cost for this project is low. |
| --- |

**3. GDPR — what it means for you**

GDPR governs how you collect, store, use, and delete personal data about EU customers. You are already broadly compliant — Frankfurt hosting, encryption, and data access controls are in place. The items below are the gaps that need closing before the AI modules go live.

**The four things to confirm before launch**

| **What needs doing** | **Why it matters** |
| --- | --- |
| **Consent banner audit** | Cookie-based browsing data powers the recommendation engine. The legal basis for using it — legitimate interest or explicit consent — must be documented and reflected in the consent banner before the engine goes live. |
| **Deletion pipeline** | Customers have a right to request deletion of their data. That request must flow through the recommendation model, not just the main database. This is a technical task for Javi's team and is included in the project scope. |
| **Data processing records** | GDPR Article 30 requires a record of processing activities. The pipeline logs in LangSmith and the Python scripts serve this purpose — they just need to be pointed to in your ROPA document. |
| **Processor agreements** | If the LLM API (Anthropic or OpenAI) processes any personal data, a Data Processing Agreement must be in place. In practice, the system prompt and product catalog contain no personal data, so this risk is low — but worth confirming with your legal team. |

**What you do not need to worry about**

- Data transfers outside the EU — everything stays in Frankfurt.

- Special category data processing (health, politics, religion) — not relevant to fashion e-commerce.

- DPIA (Data Protection Impact Assessment) for Phases 1 and 2 — the processing is not high-risk under GDPR. Phase 3 (try-on with body images) may require one.

**4. LangSmith — compliance by design**

LangSmith is the monitoring layer for the AI system. From a compliance perspective, it does three useful things automatically:

- **Audit trail:** Every AI decision is logged with a timestamp, model version, and output. This satisfies the EU AI Act documentation requirement and provides an audit trail if a customer ever disputes a recommendation or AI-generated output.

- **Quality monitoring:** Token costs, latency, and error rates are tracked per call. If the styling assistant ever produces something unexpected, it is visible immediately — not discovered weeks later.

- **Change control:** When the AI model changes, LangSmith runs regression tests to confirm behaviour is consistent. No model update ships without validation.

| LangSmith is not just an engineering tool — it is your compliance paper trail. Keep it running from day one, even during the Phase 1 pilot. |
| --- |

**5. Action checklist — before go-live**

The items below should be completed before each phase launches. None require legal expertise to action — they are operational tasks.

**Phase 1 (catalog automation) — weeks 1–8**

- Confirm with legal team that pipeline logs satisfy GDPR Article 30 record-keeping requirements.

- Ensure no personal customer data is included in LLM prompts used for product description generation.

**Phase 2 (recommendation engine + styling assistant) — weeks 6–14**

- Complete consent banner audit — confirm legal basis for using cookie-based browsing data.

- Add 'AI-powered' disclosure label to the styling assistant widget.

- Confirm deletion pipeline is live and tested — a customer deletion request must clear the recommendation model.

- Confirm Data Processing Agreements are in place with any LLM API provider used.

**Phase 3 (virtual try-on) — from week 16**

- Conduct EU AI Act risk assessment before build begins — body image processing may require additional safeguards.

- Assess whether a GDPR Data Protection Impact Assessment is required.

- Confirm explicit consent mechanism for photo upload — this is a clear user action, not a passive cookie.

**6. Data flow inventory**

The table below documents what data each AI module touches — inputs it receives, outputs it produces, where those outputs are stored, and how long they should be kept. This is the information your DPO will need for the ROPA update and any GDPR review.

| Retention periods shown are recommendations. Your legal team should confirm these against your existing data retention policy before go-live. |
| --- |

**Module 1 — Recommendation engine**

| **Inputs** | Cookie ID or customer ID · gender preference signal · browsing events (pages viewed, products clicked, time on page) · purchase history · current session behaviour |
| --- | --- |
| **Outputs** | Ranked list of product IDs returned to the storefront per request · no personal data in the output itself |
| **What is stored** | User embedding vector (a mathematical representation of preferences — not readable as personal data but linked to a customer ID) · click and purchase events used to retrain the model nightly |
| **Storage location** | Frankfurt company cloud infrastructure · encrypted at rest |
| **Retention — events** | Behavioural events (clicks, views): recommend 24 months, then delete or anonymise · purchase events: align with your existing order retention policy |
| **Retention — vectors** | User embedding vectors: delete or re-derive when underlying event data is deleted · must be cleared when a customer exercises right to erasure |
| **Personal data?** | Yes — user embeddings are linked to customer IDs and are therefore personal data under GDPR. The deletion pipeline must cover these. |
| **LangSmith logging** | Each recommendation request is traced: request timestamp, model version, response time, product IDs returned. No personal data in traces if customer ID is hashed before logging. |

**Module 2 — AI styling assistant**

| **Inputs** | Customer's free-text message · current page context (product ID, category) · live product catalog (injected via RAG — no personal data) · optional: session history within same conversation |
| --- | --- |
| **Outputs** | AI-generated text response · product IDs of recommended items · these are displayed to the customer and not stored by default |
| **What is stored** | Conversation logs should NOT be stored unless a specific decision is made to do so. If stored for quality review, they must be treated as personal data. Recommend: store only anonymised LangSmith traces, not full conversation text. |
| **Storage location** | LangSmith traces: Frankfurt (self-hosted) · if conversation logs are kept: Frankfurt company cloud only |
| **Retention — traces** | LangSmith traces (anonymised): 12 months for quality monitoring, then delete |
| **Retention — conversations** | If conversation history is stored: maximum 30 days, then auto-delete. Requires explicit consent basis separate from general T&Cs. |
| **Personal data?** | Potentially yes — free-text messages may contain personal data (name, address, payment details typed by mistake). System prompt should instruct the assistant to never acknowledge or store personal details typed by users. |
| **LangSmith logging** | Input prompt (without personal data), output text, latency, quality score, model version. Customer ID should be hashed or omitted from traces. |

**Module 3 — Catalog content automation**

| **Inputs** | Product attributes from internal database (name, category, colour, size, price) · brand voice template · no customer personal data |
| --- | --- |
| **Outputs** | Draft product descriptions · SEO metadata · product attribute tags · these enter a human review queue before publishing |
| **What is stored** | Draft descriptions in the review queue until approved or rejected · approved descriptions stored in the product database as standard content · rejected drafts can be deleted immediately |
| **Storage location** | Frankfurt company cloud · same location as existing product database |
| **Retention** | Approved descriptions: indefinite (standard product content) · rejected drafts: delete after 30 days · LangSmith batch logs: 6 months |
| **Personal data?** | No — this module processes product data only. No customer personal data is involved at any stage. |
| **LangSmith logging** | Batch job ID, number of products processed, cost per run, quality scores. No personal data in any log. |

**Module 4 — Virtual try-on (Phase 3)**

| Phase 3 has the most complex data profile. Body images are likely classified as biometric data under the EU AI Act and may be sensitive personal data under GDPR. Finalise this section with your legal team before the Phase 3 build begins. |
| --- |

| **Inputs** | Customer-uploaded photo (face and/or body) · selected product ID · image dimensions |
| --- | --- |
| **Outputs** | Composite image showing the product on the customer's photo · this is generated on demand and should not be stored |
| **What is stored** | Recommendation: do not store uploaded photos beyond the duration of the session. Process and discard. If caching is needed for performance, maximum 24 hours with explicit consent. |
| **Storage location** | If temporarily stored: Frankfurt only · must not be sent to external GPU providers outside the EU without a Data Processing Agreement and Standard Contractual Clauses |
| **Retention** | Uploaded photos: session duration only, then permanent deletion · generated try-on images: session duration only · no long-term storage of body images without explicit, specific consent |
| **Personal data?** | Yes — body images are personal data. They may also qualify as biometric data under GDPR Article 9 (special category), which requires explicit consent as the legal basis, not just legitimate interest. |
| **LangSmith logging** | Request ID, model version, latency, error flags only. The photo itself must never appear in any log. |
| **Key action before build** | Legal review required. Confirm: (1) consent mechanism, (2) whether DPIA is required, (3) EU AI Act biometric risk assessment, (4) Data Processing Agreement with any inference provider. |

**Summary — personal data by module**

| **Module** | **Personal data?** | **Sensitive data?** | **Deletion required?** | **Key action** |
| --- | --- | --- | --- | --- |
| **Recommendation engine** | **Yes** | **No** | **Yes** | Deletion pipeline for user vectors |
| **Styling assistant** | **Maybe** | **No** | **Yes** | Hash customer ID in traces |
| **Catalog automation** | **No** | **No** | **N/A** | None — product data only |
| **Virtual try-on (Ph. 3)** | **Yes** | **Likely** | **Yes** | Legal review before build |

**7. What this is not**

This memo is a practical guide to the compliance requirements as we understand them at the time of writing. It is not a legal opinion and does not replace advice from a qualified lawyer or data protection officer.

We recommend sharing the Phase 2 checklist with your legal team or DPO at least four weeks before the recommendation engine goes live. The items are straightforward but require sign-off.

| Bottom line: the compliance picture for this project is manageable. No high-risk AI classifications, no cross-border data flows, and no novel legal questions. The main pre-launch tasks are a consent banner audit and a UI disclosure label. |
| --- |

*This memo is informational only and does not constitute legal advice.*
