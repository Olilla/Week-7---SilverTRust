# Discovery — Interview Notes

**Client scenario:** Streetwear E-Commerce (designed by paired team)
**Interviewers:** [Your team names]
**Date:** Monday 01.06.2026

---

## Persona 1 — Carlos, Marketing Director

**Indirect questions used:**

1. Walk us through how you currently handle customer segmentation and campaign targeting.
2. What does a typical week look like for you in terms of content and campaign workload?
3. Where do you feel the online experience falls short compared to what a customer would get in a physical store?
4. When a customer visits the site for the first time, what happens — how does the site respond to them?
5. What would a really strong month look like for you in terms of customer behaviour?

**Raw notes:**

- Company sells its own streetwear brand online only — no physical stores. Target: teenagers and young adults, men and women. Comparable to Springfield.
- Operates mainly in Germany, ships across Europe. All infrastructure in Frankfurt.
- Losing market share to C&A and Springfield. Revenue growth slower than expected.
- Carlos's core complaint: the online experience feels cold and impersonal. No equivalent to a sales assistant who can say "that goes well with this."
- Customers lack styling guidance, sizing advice, product selection help.
- AOV is low. Many customers buy once and don't return. Cross-sell and upsell not working.
- Carlos is worried about AI-generated descriptions becoming generic — brand voice must be preserved.
- He wants personalisation before the first purchase, not just after a purchase history is built.
- Strategic goals: 5–10% revenue growth in coming years, double sales in 10 years, improve margins.

**Signals picked up:**

- The word "cold" came up more than once — this is the core UX problem Carlos is trying to name.
- He pushed back on generic AI copy unprompted — this is a fear, not just a preference.
- He mentioned "before the first purchase" specifically — cold-start personalisation is a real gap.

---

## Persona 2 — Javi, Lead Developer

**Indirect questions used:**

1. What does your team spend the most time on that isn't directly building new features?
2. How does your current content pipeline work — who writes the product descriptions and how long does it take?
3. Where do things slow down when you need to launch a new product or update the catalog?
4. What does your infrastructure look like — where is everything hosted and what are the constraints?
5. You mentioned n8n — what made you start looking at workflow tools?

**Raw notes:**

- Javi is responsible for platform performance, infrastructure, and tech implementation. Interested in scalable AI and workflow automation.
- Significant manual effort for catalog admin, inventory management, and product copy. Large product volumes make this painful at scale.
- Interested in n8n for connecting systems and automating workflows — product data, marketing automation, AI content pipelines, customer segmentation.
- All data encrypted, stored in Frankfurt, managed to German data protection standards.
- Strong internal team: experienced devs, testers, engineers. Existing expertise in e-commerce infrastructure, billing, platform reliability.
- Any AI solution must be scalable, reliable, and integrable with existing systems.
- Javi suggested AI for product descriptions, attribute generation, catalog enrichment, SEO optimisation.

**Signals picked up:**

- Javi brought up content automation unprompted — this is a genuine operational pain, not just a nice-to-have.
- He knows what n8n is and is already thinking about it — the team is technically ready.
- The Frankfurt / German data protection emphasis came up naturally — compliance is already on their radar.

---

## Cross-persona patterns

- Both Carlos and Javi independently identified personalisation as the highest priority.
- Carlos comes at it from the customer experience angle; Javi from the operational efficiency angle.
- The content bottleneck (manual catalog copy) was mentioned by Javi but validated by Carlos's concern about brand voice — they both care about it for different reasons.
- Virtual try-on came up as a strong idea from Carlos (reduce the disadvantage of online-only retail) — Javi did not push back on it technically.
- Neither persona mentioned compliance proactively — it surfaced only when infrastructure and data storage came up.