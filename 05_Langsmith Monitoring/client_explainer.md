# LangSmith — Client Explainer

**For:** Carlos and Javi
**Purpose:** Plain-language explanation of what LangSmith does and why it matters

---

## The one-paragraph version

Every time the AI does something — recommends a product, answers a styling question, writes a product description, or processes a try-on request — LangSmith records it. You can see the exact question that went in, the exact answer that came out, which version of the model produced it, and how long it took. If something goes wrong, you can find it. If an auditor asks what the AI said to a customer last Tuesday, you can show them. The AI is not a black box — it has windows, and you hold the keys.

---

## What Carlos can see

- Every styling assistant conversation, scored for brand voice
- Which product recommendations were shown to which session (no personal data — session IDs only)
- Whether the "AI-powered" label was displayed as required by law
- Quality scores for all generated catalog copy before it goes to human review

## What Javi can see

- Latency per request, per module
- Error rates and failure types
- Which model version produced which output
- Whether content moderation fired on a photo upload and what the outcome was
- Any alert that fires when something is outside expected range

## What neither of you will ever see in LangSmith

- Customer photos (legally prohibited — photo must never appear in any log or trace)
- Raw measurement values tied to a customer identity
- Anything that identifies a customer individually (IDs are hashed before logging)

---

## How to explain this to a sceptical board member

"Our AI consultant has set up a monitoring system that records every decision the AI makes — what it was asked, what it answered, and when. If the AI ever produces something wrong or off-brand, we can find it, fix it, and prove to any auditor exactly what happened. We are not flying blind."

---

## How it helps with compliance

- GDPR Art. 30: LangSmith traces serve as the audit log for AI-driven processing activities
- EU AI Act Art. 52: the trace confirms the "AI-powered" label was shown
- DPIA for photo path: the trace proves photos never enter the log, satisfying the biometric data isolation requirement
- Internal accountability: if a generated product description is wrong, the trace shows which model version produced it and which human approved it