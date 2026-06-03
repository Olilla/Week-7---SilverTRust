# Silver Trust — AI MVP

Streetwear E-Commerce · Germany & Europe  
A working proof of concept for the AI Transformation Proposal (June 2026).

---

## What this is

A local web app that demonstrates three of the four proposed AI modules:

| Module | Status |
|---|---|
| 🛍️ Storefront with cookie consent | ✅ MVP |
| ✨ Recommendation engine | ✅ MVP |
| 💬 AI Styling Assistant | ✅ MVP |
| 🪞 Virtual try-on | Phase 3 — not in scope |

Every AI call is traced in **LangSmith** (EU endpoint) for full cost, latency, and quality observability.

---

## Project structure

```
MVP/
├── silver_trust_app.py       # Main app — run this
├── silver_trust_mvp.ipynb    # Jupyter notebook version
├── install_dependencies.py   # Run once to install packages
├── .env                      # Your API keys (never commit this)
├── .env.example              # Key template
└── README.md                 # This file
```

---

## First-time setup

### 1. Create your `.env` file

```
Open `.env` and add:

```
OPENAI_API_KEY=sk-...
LANGSMITH_API_KEY=lsv2_...
```

### 2. Create and activate a virtual environment

```powershell
uv venv --python 3.12 venv
venv\Scripts\activate
```

You'll see `(venv)` at the start of your prompt when it's active.

### 3. Install dependencies

```powershell
python install_dependencies.py
```

This installs: `openai`, `langchain`, `langchain-openai`, `langchain-core`, `langsmith`, `gradio`, `numpy`, `python-dotenv`.

---

## Running the app

Every time you want to run the app, open PowerShell in the MVP folder and:

```powershell
# Activate the environment (if not already active)
venv\Scripts\activate

# Start the app
python silver_trust_app.py
```

Wait for:
```
⏳ Embedding catalog…
✅ 8 products embedded
* Running on local URL: http://0.0.0.0:7860
```

Then open **http://localhost:7860** in your browser.

> **Keep the PowerShell window open** while using the app — closing it stops the server.

---

## What to test

### 🛍️ Tab 1 — Storefront

- Two hero products: **Köln Oversized Hoodie** and **Dortmund Cargo Pants**
- Scroll down to see prices, sizes, colour swatches, and tags
- **Cookie consent banner** appears at the bottom — try both Accept and Decline
  - This mirrors the GDPR consent requirement from the compliance memo
  - Accepting enables the recommendation engine; declining shows a notice

---

### ✨ Tab 2 — Recommendations

The embedding-based similarity engine. Tests to run:

**Test 1 — Single product**
- Select only `Köln Oversized Hoodie` → click **Get Recommendations**
- Expect: complementary bottoms and accessories (Dortmund Cargo, Essen Jogger, Berlin Beanie)

**Test 2 — Multiple products**
- Select `Köln Oversized Hoodie` + `Dortmund Cargo Pants` → click **Get Recommendations**
- Expect: the session embedding blends both signals — you should see outerwear or accessories

**Test 3 — Accessories profile**
- Select `Berlin Beanie` + `Frankfurt Crossbody Bag` → click **Get Recommendations**
- Expect: the engine picks up the utility/accessories profile and recommends differently

Each card shows a **match %** score — higher means more similar to your viewed session.

> Every recommendation call is traced in LangSmith as `recommendation-engine`.  
> Note: 0 tokens and $0.00 cost — no LLM is called, just vector math.

---

### 💬 Tab 3 — Styling Assistant

A RAG-powered chat assistant with the full catalog injected into the system prompt. Tests to run:

**Outfit pairing**
> *"What goes with the Köln hoodie?"*  
> Expect: product recommendations with IDs and prices, in brand voice

**Size advice**
> *"I'm 180cm, 75kg — should I go M or L in the Köln hoodie?"*  
> Expect: specific sizing guidance based on the oversized fit description

**Full outfit under a budget**
> *"Build me a full outfit under €250"*  
> Expect: a curated look with multiple items, total price check, product IDs

**Cold weather styling**
> *"Best pick for cold weather but still looks clean?"*  
> Expect: München Crewneck or Hamburg Track Jacket with styling context

**EU AI Act compliance check**
> *"Are you a real person or an AI?"*  
> Expect: clear disclosure that it is an AI assistant (required under EU AI Act Article 52)

**Brand guard test**
> *"Do you sell Nike or Adidas?"*  
> Expect: stays within the Silver Trust catalog, no hallucinated external brands

> Every message is traced in LangSmith as `styling-assistant` with token count and cost.  
> Typical cost: ~$0.0002 per message with `gpt-4o-mini`.

---

## Checking traces in LangSmith

1. Go to **https://smith.langchain.com**
2. Open project **`silver-trust-mvp`**
3. You will see every call logged with:
   - Run name (`styling-assistant` or `recommendation-engine`)
   - Input and output preview
   - Latency in seconds
   - Token count and cost in USD
   - Timestamp

Click any row to see the full prompt, full response, and token breakdown.

---

## Stopping the app

Press **Ctrl + C** in the PowerShell window.

---

## Notes

- **Images**: product photos are served from Unsplash and load in the browser. If one fails, a branded placeholder appears automatically.
- **Python version**: requires Python 3.11 or 3.12. Python 3.14 is not supported (packages don't have wheels for it yet).
- **Public link**: to share the app with Carlos or Javi without them installing anything, change `share=False` to `share=True` in the last line of `silver_trust_app.py`. Gradio will generate a public `gradio.live` URL valid for 72 hours.
