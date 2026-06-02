# Change Log

**Presenting team:** [Your team names]
**Review board:** [Paired team names]
**Version:** Wednesday post-review

---

## Change log table

| # | Change requested | What we did | Why |
|---|-----------------|-------------|-----|
| 1 | Photo retention period too short — should be longer than 6 months | Revised to user-controlled retention with a maximum of 24 months, replacing the fixed 6-month auto-expiry. Customer chooses at point of consent: session only, 6 months, 12 months, or 24 months. Auto-expiry at 24 months if no active choice is made. | GDPR does not mandate a specific maximum — it requires retention no longer than necessary. A user-controlled model satisfies purpose limitation while giving customers the experience they want. |
| 2 | Persistent user profile for photo and sizing data | Accepted. Added "My Fit Profile" to account settings. Stores measurements (legitimate interest) and most recent photo (separate explicit consent). Editable and deletable at any time. | Commercially and technically viable. No additional legal groundwork for measurements. Photo storage already required explicit consent — consent screen now makes the profile use explicit. |
| 3 | Address purpose limitation — can try-on data be reused for marketing or recommendations? | Rule already existed in compliance memo. Now also disclosed on the consent screen at point of collection: "Your data is used for try-on only." Any future secondary use requires a separate opt-in. | GDPR Art. 5(1)(b) purpose limitation is non-negotiable. Added a secondary use column to the data map. |
| 4 | Classify which categories can and cannot use try-on | Accepted. Categories excluded: underwear, swimwear, intimate apparel. Enforced at catalog level — no try-on button on excluded items. | Eliminates the most sensitive content moderation scenarios at source. No swimsuit or underwear images enter the system. |
| 5 | Age legislation for photo upload by minors | Accepted. 18+ required for photo upload (conservative position for biometric-adjacent data). Age gate at account creation plus re-confirmation at upload. Legal review of age verification tooling recommended before Phase 3 launch. | Biometric data processing of minors is a specific high-risk area under GDPR and the EU AI Act. The 18+ position is defensible and reduces exposure significantly. |
| 6 | Hybrid AI + data input — combine measurements and photo | Accepted — Option C was already designed. Now promoted as the recommended path on the entry screen, labelled "Recommended". Options A and B remain equally accessible. | The review board's point was about presentation, not design. They were right that Option C deserved more prominence. |
| 7 | Address nudity risk, swimsuit uploads, LLM requesting photos | Accepted. Three additions: (1) category exclusion (change 4) removes swimwear at source; (2) content moderation extended to include partial nudity flagging and single-person verification; (3) LLM is explicitly prohibited from requesting photos — enforced at system prompt level and monitored via LangSmith alert. | The LLM must never solicit biometric data. This is both a safety requirement and a GDPR purpose limitation issue. |
| 8 | Track which items were previewed via try-on | Accepted. Try-on preview event added to session log: product ID, timestamp, input method used. No photo or measurements in this log. Visible to customer in account settings under "My try-on history". | Behavioural data with the same legal basis as other rec engine events. Commercially valuable; legally straightforward. |
| 9 | Retention user-controlled not fixed | Addressed together with change 1. Fixed 6-month TTL replaced with user-controlled retention (session / 6 / 12 / 24 months), hard maximum 24 months. | See change 1. |

---

## Summary

All nine change requests accepted. No requests rejected. Most material changes: category exclusion (eliminates swimwear/nudity risk at source), user-controlled retention (improves UX while remaining GDPR-compliant), LLM photo request prohibition (safety constraint that should have been in the original design — the review board caught it).