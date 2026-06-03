**AI TRANSFORMATION PROPOSAL**

Streetwear E-Commerce — Germany & Europe

**Addendum: Module 4 — Virtual Try-On with Photo Storage & Body Measurements**

Prepared for Carlos (Marketing Director) and Javi (Lead Developer)  ·  June 2026  ·  Private & Confidential

| **CONTEXT & SCOPE CHANGES** |
| --- |

# **1. What has changed**

The original proposal scoped Module 4 (Virtual Try-On) as a session-only feature with no data stored. A first addendum updated this to include optional 6-month encrypted photo storage.

Following further client feedback, a second input method has been added: customers will now be able to enter their body measurements (height, chest, waist, hips, inseam) as an alternative or complement to uploading a photo. This gives customers who prefer not to upload a photo a fully functional path through the try-on experience.

| *The measurements option is commercially and technically simpler than photo storage. It carries a significantly lighter compliance profile and should be considered the baseline option available to all customers by default.* |
| --- |

| **UPDATED MODULE 4 SCOPE** |
| --- |

# **2. Updated Module 4 description**

Module 4 now offers three input methods for the try-on experience. Customers can choose any one or combine them:

| **Option A Body measurements** | Customer enters height, chest, waist, hips, and inseam. A 3D avatar is generated from these measurements. The garment is draped on the avatar. No photo required. Measurements can be stored in the customer account for future visits (simple personal data — no biometric classification). |
| --- | --- |
| **Option B Photo upload / camera** | Customer uploads a photo or takes one in real time. The garment overlay is applied to their actual image. With explicit consent, the photo can be stored encrypted for 6 months. Content moderation filter runs at upload. |
| **Option C Combined** | Customer enters measurements first, then optionally adds a photo to refine the result. The avatar generated from measurements is enhanced by the photo's pose and body outline. Measurements and photo are treated with their respective data handling rules independently. |

| *Customers who decline photo storage or who prefer not to upload a photo at all must have full access to the try-on experience via measurements (Option A). No degraded experience for non-photo users.* |
| --- |

## **Updated workflow — measurements path (Option A)**

| **Step 1** | Customer selects "Enter measurements" on the try-on screen |
| --- | --- |
| **Step 2** | Customer inputs height, chest, waist, hips, inseam via a simple form with guidance icons |
| **Step 3** | 3D avatar generated from measurements — displayed to customer for confirmation |
| **Step 4** | Garment draped on avatar — personalised result displayed |
| **Step 5** | With opt-in, measurements saved to account for future visits (simple toggle in account settings) |
| **Step 6** | Customer can update or delete measurements at any time from account settings |

## **Updated workflow — photo path (Option B)**

| **Step 1** | Customer opts in to photo use via explicit consent screen |
| --- | --- |
| **Step 2** | Photo passes content moderation filter (nudity, age, quality checks) |
| **Step 3** | Try-on model processes photo and displays result |
| **Step 4** | With explicit consent, photo stored encrypted in Frankfurt for 6 months |
| **Step 5** | On return visits, stored photo retrieved automatically |
| **Step 6** | After 6 months, photo permanently and automatically deleted |

| **LEGAL & COMPLIANCE REQUIREMENTS** |
| --- |

# **3. Legal requirements — measurements vs photo**

The two input methods carry substantially different compliance profiles. This is important: the measurements option avoids most of the complexity introduced by photo storage.

| **Requirement** | **Measurements (Option A)** | **Photo storage (Option B)** |
| --- | --- | --- |
| Data classification | Standard personal data (GDPR Art. 4). Not biometric data. Not special category. | Likely biometric personal data under GDPR Art. 9. Special category. Highest protection tier. |
| Legal basis | Legitimate interest or consent. Either is valid and straightforward to document. | Explicit consent only. Cannot rely on legitimate interest. Separate opt-in required. |
| DPIA required? | No. Standard personal data processing does not trigger mandatory DPIA. | Yes. Mandatory before build begins. Biometric data + emerging AI = DPIA threshold met. |
| Retention period | Indefinite while customer account is active, or until customer deletes. Simple account data. | 6 months maximum from upload date. Automated deletion required. Strictly enforced. |
| Deletion obligation | Must delete on account deletion or customer request. Standard GDPR Art. 17. | Must delete on consent withdrawal, account deletion, request, or 6-month expiry. Cascading deletion. |
| Encryption required? | Standard encryption in transit and at rest. Same as other account data. | AES-256 at rest minimum. Isolated storage bucket. Strict access controls required. |
| Content moderation | Not applicable. Measurements are numbers, not images. | Mandatory. Nudity detection, age flagging, quality check before any processing. |
| EU AI Act | No specific obligations for the measurements form itself. | Art. 52 transparency label required. System must not covertly analyse emotions. |

| *The measurements option should be the default path offered to all customers. It is simpler to build, simpler to operate, and carries substantially lower legal risk. Photo upload should be presented as an enhancement option, not the primary flow.* |
| --- |

## **3.1 GDPR — measurements data**

| **Art. 6 — Legal basis** | Legitimate interest is available for storing measurements to improve the shopping experience. Alternatively, standard consent (not explicit consent) is sufficient. Either is straightforward to document. |
| --- | --- |
| **Art. 13 — Transparency** | Privacy policy must state that measurements are stored, for how long, and how to delete them. No special disclosure beyond standard account data. |
| **Art. 17 — Erasure** | Customer can delete measurements at any time from account settings. Must also be deleted on account closure. Standard pipeline — no special cascade required. |
| **DPIA** | Not required. Storing height and clothing measurements does not meet the threshold for a mandatory DPIA under GDPR Article 35. |

## **3.2 GDPR — photo data (unchanged from previous addendum)**

All requirements from the previous addendum remain in force for Option B. Article 9 biometric classification, explicit consent, DPIA mandatory, AES-256 encryption, 6-month auto-deletion, and cascading deletion pipeline. See previous addendum for full detail.

## **3.3 EU Data Act — data portability**

Both measurements and photo data are subject to data portability rights under the EU Data Act. Customers must be able to download or transfer their stored measurements and their stored photo profile. These are separate data exports and must be handled independently.

| **TECHNICAL REQUIREMENTS** |
| --- |

# **4. Technical requirements — measurements**

## **4.1 Measurements input form**

- Fields required: height (cm or ft/in), chest circumference, waist circumference, hip circumference, inseam length

- Optional fields: shoulder width, arm length, neck circumference (improves accuracy for upper-body garments)

- Unit toggle: metric (cm) and imperial (ft/in, inches) both supported

- Visual guidance: each measurement field accompanied by a small illustration showing where to measure on the body

- Validation: min/max range checks per field to catch obvious input errors (e.g. height below 100cm or above 250cm)

- Size suggestion: after measurements are entered, the system should display the recommended size for the selected garment before the avatar is generated

## **4.2 Avatar generation from measurements**

- A parametric 3D body model is generated from the input measurements

- The garment is draped onto the avatar using the same pose estimation model used for photos

- The avatar should display in a neutral stance with options to view front, side, and back

- A fit indicator (tight / good fit / loose) should accompany the result, derived from the measurements vs. garment size chart

- No AI inference or external API call is required for the measurements form itself — this is pure parametric modelling

## **4.3 Measurements storage**

- Stored as structured data (JSON or database record) in the customer account profile

- No special isolated storage required — can reside in the standard customer account database in Frankfurt

- Standard encryption in transit (TLS 1.2+) and at rest consistent with other account data

- Customer can update any measurement at any time via account settings

- Measurements deleted automatically on account closure

- Measurements deleted immediately on customer request

- No retention period cap required (unlike photo storage) — measurements remain until the customer deletes them or closes their account

## **4.4 Photo storage (unchanged)**

All technical requirements from the previous addendum remain in force for photo storage: AES-256 encryption, isolated Frankfurt storage bucket, content moderation at upload, 6-month TTL, cascading deletion pipeline, no photos in logs. See previous addendum for full detail.

| **FRONT-END REQUIREMENTS** |
| --- |

# **5. Front-end requirements — measurements option**

## **5.1 Input method selection screen**

The try-on entry point must present three equally prominent options:

| **Option A Enter measurements** | Recommended for customers who prefer not to upload a photo. Shown first. Labelled as the default option. |
| --- | --- |
| **Option B Upload / take photo** | For customers who want to see the garment on their actual image. Requires separate consent flow. |
| **Option C Use both** | Enter measurements for sizing accuracy, then optionally add a photo for a more realistic visual result. |

| *Option A (measurements) must never be presented as a lesser or secondary experience. It must be visually equivalent to the photo option and produce a high-quality result.* |
| --- |

## **5.2 Measurements input screen**

- Clear, simple form with one measurement per row

- Each row: measurement name, small illustration, input field, unit selector

- A 'How to measure' expandable help section with a full-body diagram

- Real-time size suggestion updates as measurements are entered

- A save toggle: 'Save measurements to my account for next time' (opt-in, unchecked by default for new customers, pre-checked for returning customers who already saved measurements)

- Clear 'Continue to try-on' button once all required fields are complete

## **5.3 What is NOT allowed — measurements**

| **❌ Requiring measurements to use the store** | Measurements are for the try-on feature only. They must never gate access to browsing or purchasing. |
| --- | --- |
| **❌ Pre-filling from third-party sources** | Measurements must not be inferred or pre-filled from browsing data, order history, or external data sources without explicit disclosure. |
| **❌ Using measurements for profiling** | Stored measurements must be used only for try-on. They must not feed into recommendation engine targeting or marketing segmentation without separate consent. |
| **❌ Sharing measurements externally** | Measurements must not be shared with any third party (brand, supplier, analytics provider) without explicit consent. |

## **5.4 Account settings — measurements management**

- Customer can view all stored measurements at any time

- Customer can edit any individual measurement

- Customer can delete all measurements with a single action

- Customer can toggle measurement storage on or off independently of photo storage

| **UPDATED COST & TIMELINE IMPACT** |
| --- |

# **6. Impact on cost and timeline**

| **Measurements build scope** | Input form UI · Parametric avatar generation model · Fit indicator logic · Size recommendation engine · Measurements storage in account DB · Account settings measurements page |
| --- | --- |
| **Estimated additional cost** | €6k–12k on top of photo storage scope. Measurements are technically simpler than photo processing — no content moderation, no isolated storage, no biometric pipeline. |
| **Timeline impact** | Measurements can be built in parallel with the photo path. No legal prerequisites (no DPIA required). Can be delivered as part of Phase 3 without extending the timeline. |
| **Running cost** | Negligible. Measurements are simple structured data. Storage cost is trivial. No moderation API calls. No LLM inference required for avatar generation. |
| **Compliance overhead** | Minimal. Standard GDPR account data treatment. No DPIA. No biometric handling. Privacy policy update required to mention measurements storage. |

| *Recommendation: deliver the measurements option (Option A) first within Phase 3, as it has no legal prerequisites. The photo path (Option B) can follow once the DPIA is complete. This means the try-on feature can go live sooner with a working, fully compliant experience for all customers.* |
| --- |

| **RECOMMENDED NEXT STEPS** |
| --- |

# **7. Recommended next steps**

| **1** | Confirm measurements fields required — agree with Carlos and Javi which measurements are mandatory vs optional for the garment categories in scope |
| --- | --- |
| **2** | Select parametric avatar model — evaluate build vs buy for the 3D body model generation (open-source options available: SMPL, CAESAR body model) |
| **3** | Privacy policy update — add measurements storage alongside photo storage update |
| **4** | DPIA for photo path — commission now, measurements path can go live before DPIA is complete |
| **5** | Design input form UX — measurements form requires careful design to avoid user drop-off. Illustrations and guidance are critical. |
| **6** | Phase 3 build sequencing — recommend measurements path as first deliverable, photo path as second once DPIA signed off |

| *Phases 1 and 2 are unaffected by this scope addition. Only Module 4 Phase 3 is impacted.* |
| --- |

*Prepared June 2026  ·  Private & Confidential  ·  This document is an addendum to the original AI Transformation Proposal.*
