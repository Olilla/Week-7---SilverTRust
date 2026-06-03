"""
Silver Trust — AI MVP · Gradio Frontend
========================================
Three tabs:
  1. 🛍️  Storefront      — two hero articles + cookie consent banner
  2. ✨  Recommendations  — embedding-based similarity engine
  3. 💬  Styling Assistant — RAG-powered AI chat, LangSmith traced

Run:
    python silver_trust_app.py
    
    browser: http://localhost:7860
"""

import os
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from dotenv import load_dotenv
load_dotenv()

# ── Validate keys ─────────────────────────────────────────────────────────────
_missing = [k for k in ("OPENAI_API_KEY", "LANGSMITH_API_KEY") if not os.getenv(k)]
if _missing:
    raise EnvironmentError(
        f"Missing keys in .env: {', '.join(_missing)}\n"
        "Copy .env.example → .env and fill in your values."
    )

# ── LangSmith ─────────────────────────────────────────────────────────────────
os.environ.setdefault("LANGSMITH_TRACING",  "true")
os.environ.setdefault("LANGSMITH_PROJECT",  "silver-trust-mvp")
os.environ.setdefault("LANGSMITH_ENDPOINT", "https://eu.api.smith.langchain.com")

# ── Models ────────────────────────────────────────────────────────────────────
CHAT_MODEL      = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

# =============================================================================
# CATALOG
# =============================================================================

@dataclass
class Product:
    id: str
    name: str
    category: str
    price: float
    colours: List[str]
    sizes: List[str]
    description: str
    tags: List[str]
    image_url: str
    embedding: Optional[List[float]] = field(default=None, repr=False)

    def catalog_text(self) -> str:
        return (
            f"[{self.id}] {self.name} | {self.category} | €{self.price:.2f} | "
            f"Colours: {', '.join(self.colours)} | Sizes: {', '.join(self.sizes)} | "
            f"{self.description} | Tags: {', '.join(self.tags)}"
        )


HERO_PRODUCTS = [
    Product(
        id="ST-001", name="Köln Oversized Hoodie", category="Tops", price=89.90,
        colours=["Washed Black", "Off White", "Sage Green"],
        sizes=["XS", "S", "M", "L", "XL", "XXL"],
        description="400 gsm French terry, dropped shoulders, kangaroo pocket. Heavyweight oversized fit — wears like a statement, feels like a blanket.",
        tags=["hoodie", "oversized", "heavyweight", "unisex", "bestseller"],
        image_url="https://images.unsplash.com/photo-1565693413579-8ff3fdc1b03b?w=600&q=80",
    ),
    Product(
        id="ST-002", name="Dortmund Cargo Pants", category="Bottoms", price=119.90,
        colours=["Olive", "Concrete Grey", "Off Black"],
        sizes=["28", "30", "32", "34", "36"],
        description="Relaxed-fit cargo with six functional pockets, adjustable ankle cuffs, and a nylon ripstop shell. Built for the city, ready for anything.",
        tags=["cargo", "relaxed", "pockets", "utility", "unisex"],
        image_url="https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&q=80",
    ),
]

SUPPORT_PRODUCTS = [
    Product(
        id="ST-003", name="Essen Slim Jogger", category="Bottoms", price=79.90,
        colours=["Black", "Charcoal"], sizes=["XS", "S", "M", "L", "XL"],
        description="Tapered slim jogger in brushed cotton. Ribbed cuffs, zip pocket.",
        tags=["jogger", "slim", "tapered", "cotton", "everyday"],
        image_url="https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=600&q=80",
    ),
    Product(
        id="ST-004", name="Düsseldorf Graphic Tee", category="Tops", price=49.90,
        colours=["White", "Black", "Rust"], sizes=["XS", "S", "M", "L", "XL", "XXL"],
        description="220 gsm heavyweight tee. Screen-printed chest graphic. Boxy fit.",
        tags=["tee", "graphic", "boxy", "cotton", "streetwear"],
        image_url="https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600&q=80",
    ),
    Product(
        id="ST-005", name="Hamburg Track Jacket", category="Outerwear", price=139.90,
        colours=["Navy", "Black", "Burgundy"], sizes=["S", "M", "L", "XL"],
        description="Retro track jacket, contrast piping, full-zip, two side pockets.",
        tags=["jacket", "track", "retro", "zip", "outerwear"],
        image_url="https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600&q=80",
    ),
    Product(
        id="ST-006", name="Berlin Beanie", category="Accessories", price=29.90,
        colours=["Black", "Olive", "Grey"], sizes=["One Size"],
        description="Ribbed merino-blend beanie. Embroidered logo tab. Foldable cuff.",
        tags=["beanie", "hat", "accessories", "winter", "merino"],
        image_url="https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=600&q=80",
    ),
    Product(
        id="ST-007", name="Frankfurt Crossbody Bag", category="Accessories", price=69.90,
        colours=["Black", "Olive"], sizes=["One Size"],
        description="600D nylon crossbody. Adjustable strap, external zip pocket, 4L capacity.",
        tags=["bag", "crossbody", "accessories", "nylon", "utility"],
        image_url="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80",
    ),
    Product(
        id="ST-008", name="München Crewneck Sweatshirt", category="Tops", price=99.90,
        colours=["Stone", "Black", "Forest Green"], sizes=["XS", "S", "M", "L", "XL", "XXL"],
        description="360 gsm fleece-back crew. Relaxed fit, ribbed cuffs and hem.",
        tags=["crewneck", "sweatshirt", "relaxed", "heavyweight", "fleece"],
        image_url="https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=600&q=80",
    ),
]

ALL_PRODUCTS   = HERO_PRODUCTS + SUPPORT_PRODUCTS
CATALOG_INDEX  = {p.id: p for p in ALL_PRODUCTS}

# =============================================================================
# AI CLIENTS  (initialised once at startup)
# =============================================================================

from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langsmith import traceable

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
llm = ChatOpenAI(model=CHAT_MODEL, temperature=0.7,
                 openai_api_key=os.environ["OPENAI_API_KEY"])

# =============================================================================
# RECOMMENDATION ENGINE
# =============================================================================

def _get_embedding(text: str) -> List[float]:
    return openai_client.embeddings.create(
        model=EMBEDDING_MODEL, input=text
    ).data[0].embedding


def _cosine(a, b) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


print("⏳ Embedding catalog…")
for p in ALL_PRODUCTS:
    p.embedding = _get_embedding(p.catalog_text())
print(f"✅ {len(ALL_PRODUCTS)} products embedded")


@traceable(name="recommendation-engine", run_type="retriever")
def recommend(viewed_ids: List[str], top_k: int = 3) -> List[Dict]:
    vectors = [CATALOG_INDEX[pid].embedding for pid in viewed_ids
               if pid in CATALOG_INDEX and CATALOG_INDEX[pid].embedding]
    if not vectors:
        return []
    session_vec = np.mean(vectors, axis=0).tolist()
    candidates  = [p for p in ALL_PRODUCTS if p.id not in viewed_ids and p.embedding]
    scored = sorted(candidates, key=lambda p: _cosine(session_vec, p.embedding), reverse=True)
    return scored[:top_k]

# =============================================================================
# AI STYLING ASSISTANT
# =============================================================================

CATALOG_CONTEXT = "\n".join(p.catalog_text() for p in ALL_PRODUCTS)

SYSTEM_PROMPT = f"""You are the Silver Trust styling assistant — a sharp, knowledgeable streetwear \
advisor for a German e-commerce brand. Your tone is direct, confident, and street-credible. \
You speak like a trusted friend in the store, not a generic chatbot.

RULES:
- Only recommend products from the catalog below. Never invent items.
- Always include the product ID and price when recommending something.
- Keep responses concise (3–5 sentences max per turn).
- If you don't know something, say so honestly.
- You are AI-powered. If asked, confirm this clearly (EU AI Act compliance).

SILVER TRUST CATALOG:
{CATALOG_CONTEXT}
"""


@traceable(name="styling-assistant", run_type="llm")
def _call_llm(messages: list) -> str:
    response = llm.invoke(messages)
    return response.content


def chat_with_assistant(user_message: str, history: list) -> tuple[str, list]:
    """
    history: list of {"role": "user"|"assistant", "content": str}
    Returns (assistant_reply, updated_history)
    """
    lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for turn in history:
        if turn["role"] == "user":
            lc_messages.append(HumanMessage(content=turn["content"]))
        else:
            lc_messages.append(AIMessage(content=turn["content"]))
    lc_messages.append(HumanMessage(content=user_message))

    reply = _call_llm(lc_messages)

    history = history + [
        {"role": "user",      "content": user_message},
        {"role": "assistant", "content": reply},
    ]
    return reply, history

# =============================================================================
# HTML HELPERS
# =============================================================================

BRAND_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
  .st-root { font-family: 'Inter', sans-serif; }

  /* ── Cookie banner ── */
  #cookie-banner {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
    background: #111; color: #fff;
    padding: 18px 28px;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 14px;
    font-family: 'Inter', sans-serif; font-size: 13px; line-height: 1.5;
    box-shadow: 0 -4px 20px rgba(0,0,0,.3);
  }
  #cookie-banner a { color: #aaa; text-decoration: underline; cursor: pointer; }
  .cookie-btn {
    padding: 9px 22px; border-radius: 6px; font-size: 13px;
    font-weight: 600; cursor: pointer; border: none;
  }
  .cookie-accept { background: #fff; color: #111; }
  .cookie-decline { background: transparent; color: #aaa;
                    border: 1px solid #555 !important; }

  /* ── Product card ── */
  .st-card {
    border: 1px solid #e8e8e8; border-radius: 14px; overflow: hidden;
    background: #fff; transition: box-shadow .2s;
  }
  .st-card:hover { box-shadow: 0 6px 24px rgba(0,0,0,.10); }
  .st-card img   { width: 100%; height: 300px; object-fit: cover; display: block; }
  .st-card-body  { padding: 18px; }
  .st-badge      { display: inline-block; background: #111; color: #fff;
                   font-size: 10px; padding: 3px 9px; border-radius: 20px;
                   letter-spacing: .5px; margin-bottom: 8px; }
  .st-category   { font-size: 11px; color: #999; text-transform: uppercase;
                   letter-spacing: 1px; margin-bottom: 4px; }
  .st-name       { font-size: 18px; font-weight: 700; margin-bottom: 6px; }
  .st-desc       { font-size: 13px; color: #555; line-height: 1.5; margin-bottom: 12px; }
  .st-sizes      { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 12px; }
  .st-size       { border: 1px solid #ccc; padding: 3px 9px; font-size: 11px;
                   border-radius: 4px; color: #333; }
  .st-tags       { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 14px; }
  .st-tag        { background: #f3f3f3; color: #666; padding: 3px 8px;
                   font-size: 10px; border-radius: 20px; }
  .st-footer     { display: flex; justify-content: space-between; align-items: center; }
  .st-price      { font-size: 22px; font-weight: 900; }
  .st-btn        { background: #111; color: #fff; border: none; padding: 10px 22px;
                   border-radius: 7px; font-size: 13px; font-weight: 600; cursor: pointer; }
  .st-btn:hover  { background: #333; }

  /* ── Rec card ── */
  .rec-card {
    border: 1px solid #e8e8e8; border-radius: 12px; overflow: hidden;
    background: #fff; display: flex; flex-direction: column;
  }
  .rec-card img  { width: 100%; height: 200px; object-fit: cover; }
  .rec-body      { padding: 12px; flex: 1; display: flex; flex-direction: column; }
  .rec-name      { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
  .rec-cat       { font-size: 10px; color: #999; text-transform: uppercase;
                   letter-spacing: 1px; margin-bottom: 6px; }
  .rec-price     { font-size: 16px; font-weight: 800; margin-top: auto; }
  .rec-score     { font-size: 10px; color: #888; margin-top: 4px; }

  /* ── Header ── */
  .st-header {
    background: #1a1a1a; color: #ffffff; padding: 20px 28px;
    display: flex; align-items: center; justify-content: space-between;
    border-radius: 12px; margin-bottom: 24px;
    border: 1px solid #333;
  }
  .st-logo       { font-size: 22px; font-weight: 900; letter-spacing: -0.5px;
                   color: #ffffff !important; }
  .st-tagline    { font-size: 12px; color: #cccccc !important; letter-spacing: 2px;
                   text-transform: uppercase; margin-top: 2px; }
  .st-ai-badge   { background: #ffffff; color: #111111; font-size: 11px; font-weight: 700;
                   padding: 4px 12px; border-radius: 20px; letter-spacing: .5px; }
</style>
"""


def _header_html() -> str:
    return f"""
    {BRAND_CSS}
    <div class="st-root">
      <div class="st-header">
        <div>
          <div class="st-logo">SILVER TRUST</div>
          <div class="st-tagline">Streetwear · Germany &amp; Europe</div>
        </div>
        <div class="st-ai-badge">AI-Powered ✦</div>
      </div>
    </div>
    """


def _cookie_banner_html() -> str:
    return f"""
    {BRAND_CSS}
    <div id="cookie-banner">
      <div style="flex:1;min-width:220px;color:#ffffff;font-size:13px;line-height:1.6;">
        🍪 <strong style="color:#ffffff;">We use cookies</strong> to personalise your experience and power our
        AI recommendation engine. Your data stays on EU servers (Frankfurt).
        <a href="#" style="color:#90caf9;text-decoration:underline;">Privacy Policy</a> ·
        <a href="#" style="color:#90caf9;text-decoration:underline;">Cookie Policy</a>
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <button class="cookie-btn cookie-decline"
          onclick="
            document.getElementById('cookie-banner').style.display='none';
            document.getElementById('cookie-status').innerText='❌ Cookies declined — recommendations disabled.';
          ">Decline</button>
        <button class="cookie-btn cookie-accept"
          onclick="
            document.getElementById('cookie-banner').style.display='none';
            document.getElementById('cookie-status').innerText='✅ Cookies accepted — recommendations enabled.';
          ">Accept all</button>
      </div>
    </div>
    <div id="cookie-status" style="
      font-family:Inter,sans-serif; font-size:12px; color:#888;
      padding: 6px 0 0 2px; min-height:18px;
    "></div>
    """


def _product_card_html(p: Product) -> str:
    sizes_html = "".join(f'<span class="st-size">{s}</span>' for s in p.sizes)
    tags_html  = "".join(f'<span class="st-tag">{t}</span>'  for t in p.tags)
    colours_html = "".join(
        f'<span title="{c}" style="display:inline-block;width:14px;height:14px;'
        f'border-radius:50%;background:{c.lower().replace(" ","")};'
        f'border:1px solid #ddd;margin-right:4px;"></span>'
        for c in p.colours
    )
    return f"""
    <div class="st-card">
      <div style="position:relative;">
        <img src="{p.image_url}" alt="{p.name}" style="width:100%;height:300px;object-fit:cover;display:block;" onerror="this.onerror=null;this.parentNode.innerHTML='<div style=&quot;height:300px;background:#1a1a1a;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#666;font-family:sans-serif;font-size:11px;letter-spacing:2px;text-transform:uppercase;&quot;><span style=&quot;font-size:32px;margin-bottom:8px;&quot;>🧥</span>Silver Trust</div>';" />
        <span class="st-badge" style="position:absolute;top:12px;right:12px;">NEW</span>
      </div>
      <div class="st-card-body">
        <div class="st-category">{p.category} · {p.id}</div>
        <div class="st-name">{p.name}</div>
        <div class="st-desc">{p.description}</div>
        <div style="margin-bottom:10px;">{colours_html}</div>
        <div class="st-sizes">{sizes_html}</div>
        <div class="st-tags">{tags_html}</div>
        <div class="st-footer">
          <span class="st-price">€{p.price:.2f}</span>
          <button class="st-btn">Add to Cart</button>
        </div>
      </div>
    </div>
    """


def _rec_card_html(p: Product, score: float) -> str:
    return f"""
    <div class="rec-card">
      <img src="{p.image_url}" alt="{p.name}" style="width:100%;height:200px;object-fit:cover;" onerror="this.onerror=null;this.parentNode.innerHTML='<div style=&quot;height:200px;background:#1a1a1a;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#666;font-family:sans-serif;font-size:10px;letter-spacing:2px;text-transform:uppercase;&quot;><span style=&quot;font-size:24px;margin-bottom:6px;&quot;>🧥</span>Silver Trust</div>';" />
      <div class="rec-body">
        <div class="rec-cat">{p.category}</div>
        <div class="rec-name">{p.name}</div>
        <div class="rec-price">€{p.price:.2f}</div>
        <div class="rec-score">Match: {int(score * 100)}%</div>
      </div>
    </div>
    """

# =============================================================================
# GRADIO APP
# =============================================================================

import gradio as gr



# ── Storefront tab content (static, built once) ───────────────────────────────
_storefront_cards = "".join(_product_card_html(p) for p in HERO_PRODUCTS)
STOREFRONT_HTML = f"""
{BRAND_CSS}
<div class="st-root">
  {_header_html()}
  <div style="margin-bottom:10px;">
    <div style="font-size:11px;letter-spacing:3px;color:#999;text-transform:uppercase;">
      New Arrivals</div>
    <div style="font-size:26px;font-weight:900;letter-spacing:-.5px;margin:4px 0 20px;">
      Drop 01 — Summer 2026</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;">
      {_storefront_cards}
    </div>
  </div>
</div>
"""


def build_rec_html(viewed_ids: List[str]) -> str:
    """Generate recommendation results HTML for selected products."""
    if not viewed_ids:
        return "<p style='color:#999;font-size:13px;'>Select at least one product above.</p>"
    recs = recommend(viewed_ids=viewed_ids, top_k=3)
    if not recs:
        return "<p style='color:#999;font-size:13px;'>No recommendations found.</p>"
    viewed_names = " + ".join(CATALOG_INDEX[pid].name for pid in viewed_ids)
    cards_html = ""
    for p in recs:
        score = _cosine(
            np.mean([CATALOG_INDEX[pid].embedding for pid in viewed_ids], axis=0).tolist(),
            p.embedding
        )
        cards_html += _rec_card_html(p, score)
    return f"""
    {BRAND_CSS}
    <div class="st-root" style="font-family:Inter,sans-serif;">
      <div style="font-size:11px;color:#999;letter-spacing:1px;
                  text-transform:uppercase;margin-bottom:4px;">
        Because you viewed</div>
      <div style="font-size:16px;font-weight:700;margin-bottom:16px;
                  font-style:italic;">{viewed_names}</div>
      <div style="display:grid;
                  grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
                  gap:16px;">
        {cards_html}
      </div>
      <div style="margin-top:14px;font-size:11px;color:#aaa;">
        Model: {EMBEDDING_MODEL} · Traced in LangSmith ·
        Project: {os.environ['LANGSMITH_PROJECT']}
      </div>
    </div>
    """


# ── App ────────────────────────────────────────────────────────────────────────
with gr.Blocks(title="Silver Trust — AI MVP") as demo:

    # Persistent state
    chat_history = gr.State([])   # list of {role, content} dicts

    # ── Tab 1: Storefront ─────────────────────────────────────────────────────
    with gr.Tab("🛍️  Storefront"):
        gr.HTML(_cookie_banner_html())
        gr.HTML(STOREFRONT_HTML)

    # ── Tab 2: Recommendations ────────────────────────────────────────────────
    with gr.Tab("✨  Recommendations"):
        gr.HTML(_header_html())
        gr.Markdown("### What did you look at?")
        gr.Markdown(
            "Select one or more products you viewed — the engine will rank "
            "the best matches from the rest of the catalog using embedding similarity."
        )

        product_choices = gr.CheckboxGroup(
            choices=[(p.name, p.id) for p in ALL_PRODUCTS],
            label="Viewed products",
            value=["ST-001"],
        )
        rec_btn = gr.Button("Get Recommendations →", variant="primary", size="lg")
        rec_output = gr.HTML()

        rec_btn.click(
            fn=build_rec_html,
            inputs=[product_choices],
            outputs=[rec_output],
        )

        # Show results on load with default selection
        demo.load(
            fn=build_rec_html,
            inputs=[product_choices],
            outputs=[rec_output],
        )

    # ── Tab 3: Styling Assistant ──────────────────────────────────────────────
    with gr.Tab("💬  Styling Assistant"):
        gr.HTML(_header_html())

        gr.HTML(f"""
        {BRAND_CSS}
        <div class="st-root" style="font-family:Inter,sans-serif;
             background:#f7f7f7;border-radius:12px;padding:16px 20px;
             margin-bottom:16px;display:flex;align-items:center;
             justify-content:space-between;flex-wrap:wrap;gap:8px;">
          <div>
            <div style="font-size:15px;font-weight:700;">
              Silver Trust Styling Assistant</div>
            <div style="font-size:12px;color:#777;margin-top:2px;">
              Ask about outfits, sizing, or styling advice — powered by AI
            </div>
          </div>
          <span style="background:#111;color:#fff;font-size:11px;font-weight:600;
                       padding:4px 12px;border-radius:20px;">
            AI-powered · EU AI Act compliant
          </span>
        </div>
        """)

        chatbot = gr.Chatbot(
            label="",
            height=420,
            show_label=False,
            avatar_images=(
                None,
                "https://api.dicebear.com/7.x/shapes/svg?seed=silvertrust&backgroundColor=111111",
            ),
        )

        with gr.Row():
            msg_input = gr.Textbox(
                placeholder='Try: "What goes with the Köln hoodie?" or "Build me a full outfit under €250"',
                label="",
                scale=5,
                show_label=False,
                container=False,
            )
            send_btn = gr.Button("Send →", variant="primary", scale=1, min_width=100)

        with gr.Row():
            reset_btn = gr.Button("🔄 New conversation", size="sm", variant="secondary")
            gr.Markdown(
                "<span style='font-size:11px;color:#aaa;line-height:2.2;'>"
                "Every message is traced in LangSmith · "
                f"Project: `{os.environ['LANGSMITH_PROJECT']}`</span>",
            )

        # Suggested starter questions
        gr.Markdown("**Quick starters:**")
        with gr.Row():
            s1 = gr.Button("What goes with the Köln hoodie?",     size="sm")
            s2 = gr.Button("Full outfit under €250",               size="sm")
            s3 = gr.Button("Best pick for cold weather?",          size="sm")
            s4 = gr.Button("Are you an AI?",                       size="sm")

        # ── Event handlers ────────────────────────────────────────────────────
        def respond(user_msg: str, history: list):
            if not user_msg.strip():
                return "", history, history
            _, updated = chat_with_assistant(user_msg, history)
            return "", updated, updated

        def reset_chat():
            return [], []

        def quick_send(msg: str, history: list):
            return respond(msg, history)

        send_btn.click(
            fn=respond,
            inputs=[msg_input, chat_history],
            outputs=[msg_input, chat_history, chatbot],
        )
        msg_input.submit(
            fn=respond,
            inputs=[msg_input, chat_history],
            outputs=[msg_input, chat_history, chatbot],
        )
        reset_btn.click(
            fn=reset_chat,
            outputs=[chat_history, chatbot],
        )
        for btn, q in [(s1, "What goes with the Köln hoodie?"),
                       (s2, "Build me a full outfit under €250"),
                       (s3, "Best pick for cold weather?"),
                       (s4, "Are you an AI?")]:
            btn.click(
                fn=lambda h, msg=q: respond(msg, h),
                inputs=[chat_history],
                outputs=[msg_input, chat_history, chatbot],
            )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        theme=gr.themes.Base(
            primary_hue="neutral",
            font=gr.themes.GoogleFont("Inter"),
        ),
        css=(
            ".gradio-container { max-width: 1100px !important; margin: 0 auto; }"
            " footer { display: none !important; }"
            " .tab-nav button { font-weight: 600; font-size: 14px; }"
        ),
    )
