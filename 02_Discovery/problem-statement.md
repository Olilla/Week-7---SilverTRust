# Discovery — Problem Statement & Initial Solution Concept

## Problem statement

A German streetwear e-commerce retailer selling its own brand to teenagers and young adults across Europe is losing market share to competitors like C&A and Springfield, despite having a comparable product. The core problem is not the product — it is the online experience. Without physical stores, the company cannot replicate the in-store sales assistant role that guides customers through product selection, styling, and sizing. The result is a cold, impersonal experience where customers browse without guidance, buy once, and do not return. Average order value is low, cross-sell is not working, and the operational team is spending significant time on manual catalog administration that does not scale. If left unresolved, the gap with competitors will widen as they invest in experience and automation, while this company's team remains bottlenecked on content and their customers remain under-served.

---

## Initial AI solution concept

**What we think the AI should do:**

Build a connected set of four AI modules that together replicate the personalised in-store experience online: a recommendation engine that personalises from the first session, an LLM-powered styling assistant that answers questions the way a sales assistant would, a content automation pipeline that eliminates the catalog copy bottleneck, and a virtual try-on feature that removes the core disadvantage of online-only retail.

**Why AI and not plain software:**

The styling assistant requires natural language understanding and brand-voice generation — rules cannot do this. The recommendation engine's cold-start logic and collaborative filtering improve with data in a way static rules do not. Catalog copy at brand-voice quality and scale requires an LLM. The virtual try-on requires computer vision and parametric modelling that goes beyond plain software. Everything else in the system — scoring, scheduling, moderation, data retrieval — is plain software deliberately.

**Open questions resolved in design:**

- Cold-start personalisation: addressed via gender preference signal and trending items blend
- Brand voice in generated copy: addressed via system prompt and human review gate
- Virtual try-on compliance: addressed via measurements-first sequencing, DPIA for photo path, and category exclusion list