# Discovery — Pain-Point Table

| Persona | Role | Discovered pain point | How it affects the solution |
|---------|------|-----------------------|-----------------------------|
| Carlos | Marketing Director | The online experience is impersonal — customers get no styling guidance, sizing advice, or product selection help. The site treats every visitor the same regardless of who they are or what they are looking at. | The AI must replicate the in-store sales assistant role online. This drives the styling assistant (Module 02) and the recommendation engine's cold-start personalisation (Module 01). |
| Carlos | Marketing Director | AI-generated content risks becoming generic and eroding brand voice — a real concern, not a hypothetical. | Catalog automation (Module 03) must enforce brand voice at prompt level, not just produce copy. Human review is non-negotiable before anything publishes. |
| Carlos | Marketing Director | AOV is low and cross-sell is not working — customers buy one item and leave. | The recommendation engine must surface complementary products before checkout, not just similar products after browsing. |
| Javi | Lead Developer | Manual catalog administration and product copy at scale is a significant operational bottleneck — large product volumes mean constant content debt. | Catalog automation (Module 03) directly addresses this. Python + LLM pipeline with human sign-off reduces content creation time without removing quality control. |
| Javi | Lead Developer | No workflow automation currently connecting marketing, catalog, and AI processes — everything is siloed. | n8n considered as an optional orchestration layer to connect the AI pipeline with existing systems. Not in scope for Phase 1 but flagged for later. |
| Both | — | Losing market share to C&A and Springfield despite comparable product quality — the gap is the online experience, not the product. | The entire four-module solution is oriented around closing this gap. Virtual try-on (Module 04) is the highest-differentiation move if Phase 3 is executed well. |

---

## Tensions between personas

| Tension | Between | Implication for design |
|---------|---------|------------------------|
| Brand voice quality vs. content automation speed | Carlos (quality) vs. Javi (efficiency) | Human review step in catalog automation is the resolution — Javi gets speed, Carlos keeps control |
| Personalisation before purchase history exists | Carlos wants it, technically harder | Cold-start logic in rec engine using gender prefs and trending items addresses this |