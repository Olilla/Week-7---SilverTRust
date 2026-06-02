# Revised Solution & Final Proposal

**Version:** 2.0 — post peer review
**Date:** Wednesday, Week 7

---

## Summary of what changed

Nine change requests received. All accepted. Changes fall into three categories:

- Product design: persistent Fit Profile, Option C as recommended path, try-on preview event tracking, category exclusion list
- Compliance: user-controlled retention replacing fixed 6-month TTL, explicit purpose limitation disclosure at point of collection, expanded age legislation, explicit prohibition on LLM photo requests
- Safety: content moderation scope extended, category-level exclusion of underwear and swimwear

Modules 1–3 unchanged. All changes affect Module 4 only.

---

## Updated Module 4

### What changed

| Area | Previous design | Revised design |
|------|----------------|----------------|
| Retention | Fixed 6-month auto-expiry | User-controlled: session / 6 / 12 / 24 months. Hard max 24 months. |
| User profile | No persistent profile | "My Fit Profile" — measurements always; photo with separate explicit consent. |
| Input method presentation | Options A, B, C presented equally | Option C labelled "Recommended". A and B clearly available. |
| Category scope | All clothing categories | Excluded: underwear, swimwear, intimate apparel. Enforced at catalog level. |
| Age requirement | 18+ self-declaration | 18+ for photo upload. Gate at account creation + re-confirmation at upload. Legal review of verification tooling recommended. |
| LLM photo requests | Not addressed | Explicitly prohibited. Hard constraint in system prompt. LangSmith alert fires if detected. |
| Content moderation scope | Nudity detection, age flagging, quality check | Extended: explicit nudity, partial nudity flagging, single-person verification, body visibility check. |
| Purpose limitation | In compliance memo only | Also disclosed on consent screen at point of collection. |
| Try-on preview tracking | Not tracked | Logged as distinct session event: product ID, timestamp, input method. No photo or measurements in log. Visible in account settings. |

---

## Updated compliance package

**Retention (Art. 5(1)(e)):** Fixed 6-month TTL replaced with user-controlled retention. GDPR requires data kept no longer than necessary — a customer choosing 24 months has a legitimate expectation this serves the stated purpose. 24-month hard maximum is a conservative internal policy ceiling.

**Purpose limitation (Art. 5(1)(b)):** Now disclosed on consent screen at point of collection. Secondary use requires separate opt-in. Secondary use column added to data map.

**Age (Art. 8):** Germany sets digital consent age at 16. For photo upload (biometric-adjacent), 18+ threshold applied conservatively. Self-declaration at account creation plus re-confirmation at upload.

**Try-on preview tracking:** Legitimate interest (Art. 6(1)(f)). Session behavioural data. Disclosed in privacy policy.

**EU AI Act:** Unchanged. Modules 1–3 limited risk. Photo path conformity assessment required before build.

---

## Updated monitoring

Two additions to LangSmith:

1. LLM photo request detection: alert fires if any output requests a photo from the customer. Critical safety rule.
2. Try-on preview event: product ID, timestamp, input method logged per interaction. No photo or measurements. Visible to customer in account settings.

All other monitoring unchanged.