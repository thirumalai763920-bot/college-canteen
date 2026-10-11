import html as _html
import os
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SEC Food Court",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =====================================================================
#  SETTINGS
# =====================================================================
COLLEGE = "Shreenivasa Engineering College"
ADMIN_PASSWORD = "12345"

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
F_PRODUCTS = os.path.join(DATA_DIR, "products.csv")
F_ORDERS = os.path.join(DATA_DIR, "orders.csv")
F_FEEDBACK = os.path.join(DATA_DIR, "feedback.csv")
F_NOTICES = os.path.join(DATA_DIR, "notices.csv")
F_COMPLAINTS = os.path.join(DATA_DIR, "complaints.csv")

PRODUCT_COLS = ["category", "item", "emoji", "price", "available"]
ORDER_COLS = ["token", "time", "name", "roll_no", "type", "items", "total", "status"]
FEEDBACK_COLS = ["time", "name", "item", "rating", "feedback"]
NOTICE_COLS = ["id", "time", "type", "message"]
COMPLAINT_COLS = ["time", "name", "type", "category", "message"]

STATUSES = ["Pending", "Ready", "Completed", "Cancelled"]
COMPLAINT_CATEGORIES = ["Food Quality", "Hygiene", "Price", "Service", "Other"]

# category -> (icon, colour)
CATS = {
    "Food": ("🍛", "#FF6B35"),
    "Juice & Cold Drinks": ("🥤", "#0EA5E9"),
    "Snacks": ("🍟", "#F59E0B"),
    "Others": ("🧴", "#8B5CF6"),
}
TAB_LABEL = {
    "Food": "🍛 Food",
    "Juice & Cold Drinks": "🥤 Juice & Drinks",
    "Snacks": "🍟 Snacks",
    "Others": "🧴 Hostel & Others",
}
NOTICE_TYPES = {
    "Today's Special": ("⭐", "#FF6B35"),
    "Timings": ("🕒", "#0EA5E9"),
    "Offer": ("🎉", "#10B981"),
    "Notice": ("📌", "#8B5CF6"),
}

# (category, item, emoji, price)  -> prices are sample prices, admin can edit
DEFAULT_PRODUCTS = [
    # ---- Food
    ("Food", "Dosa", "🥞", 40),
    ("Food", "Idli (2 pcs)", "🍥", 25),
    ("Food", "Pongal", "🍲", 35),
    ("Food", "Parotta", "🫓", 30),
    ("Food", "Veg Meals", "🍱", 70),
    ("Food", "Fried Rice", "🥘", 60),
    ("Food", "Veg Biryani", "🍛", 80),
    ("Food", "Chapati (2 pcs)", "🌯", 35),
    ("Food", "Lemon Rice", "🍋", 45),
    # ---- Juice & Cold Drinks
    ("Juice & Cold Drinks", "Tea", "🍵", 10),
    ("Juice & Cold Drinks", "Coffee", "☕", 15),
    ("Juice & Cold Drinks", "Orange Juice", "🍊", 30),
    ("Juice & Cold Drinks", "Watermelon Juice", "🍉", 30),
    ("Juice & Cold Drinks", "Mango Juice", "🥭", 35),
    ("Juice & Cold Drinks", "Pineapple Juice", "🍍", 35),
    ("Juice & Cold Drinks", "Grape Juice", "🍇", 35),
    ("Juice & Cold Drinks", "Pepsi", "🥤", 20),
    ("Juice & Cold Drinks", "Sprite", "🥤", 20),
    ("Juice & Cold Drinks", "Thums Up", "🥤", 20),
    ("Juice & Cold Drinks", "Buttermilk", "🥛", 15),
    ("Juice & Cold Drinks", "Cold Coffee", "🧋", 40),
    # ---- Snacks
    ("Snacks", "Ice Cream", "🍦", 20),
    ("Snacks", "Biscuit", "🍪", 10),
    ("Snacks", "Chips", "🍟", 20),
    ("Snacks", "Lays", "🥔", 20),
    ("Snacks", "Vada", "🍩", 8),
    ("Snacks", "Bajji", "🌶️", 10),
    ("Snacks", "Bonda", "🧆", 10),
    ("Snacks", "Veg Puff", "🥐", 20),
    ("Snacks", "Samosa", "🥟", 12),
    ("Snacks", "Murukku", "🍘", 15),
    # ---- Others (hostel essentials)
    ("Others", "Bathing Soap", "🧼", 35),
    ("Others", "Washing Soap", "🧼", 20),
    ("Others", "Toothbrush", "🪥", 30),
    ("Others", "Toothpaste", "🦷", 65),
    ("Others", "Shampoo (Bottle)", "🧴", 120),
    ("Others", "Coconut Oil", "🥥", 50),
    ("Others", "Detergent Powder", "🧺", 30),
    ("Others", "Face Wash", "🫧", 90),
    ("Others", "Comb", "💇", 20),
    ("Others", "Notebook", "📓", 60),
    ("Others", "Pen", "🖊️", 10),
    ("Others", "Water Bottle (1L)", "💧", 20),
]

# =====================================================================
#  STYLE
# =====================================================================
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

.stApp, .stApp p, .stApp label, .stApp input, .stApp textarea, .stApp button {
    font-family: 'Poppins', sans-serif;
}
#MainMenu, footer, .stAppDeployButton {display: none !important;}
.block-container {padding-top: 3.5rem; padding-bottom: 3rem; max-width: 1150px;}

/* ---------- hero ---------- */
.hero {
    position: relative; overflow: hidden; border-radius: 26px;
    padding: 34px 30px; margin-bottom: 18px; color: #fff;
    background: linear-gradient(120deg, #1F2937 0%, #9A3412 50%, #FF6B35 100%);
    box-shadow: 0 14px 34px rgba(154,52,18,0.35);
}
.hero:before {
    content: ""; position: absolute; right: -60px; top: -70px;
    width: 250px; height: 250px; border-radius: 50%; background: rgba(255,255,255,0.10);
}
.hero:after {
    content: ""; position: absolute; left: -40px; bottom: -90px;
    width: 210px; height: 210px; border-radius: 50%; background: rgba(255,154,68,0.20);
}
.hero-tag {
    position: relative; z-index: 1; display: inline-block; margin-bottom: 12px;
    background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.35);
    padding: 5px 16px; border-radius: 30px; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.16em;
}
.hero-title {position: relative; z-index: 1; font-size: 2.1rem; font-weight: 800; line-height: 1.25; color: #fff;}
.hero-title small {font-size: 0.45em; font-weight: 500; opacity: 0.85; margin-left: 6px;}
.hero-sub {position: relative; z-index: 1; margin-top: 10px; font-size: 1rem; opacity: 0.92;}

/* ---------- notice ticker ---------- */
.ticker {
    background: #FFF1E6; border: 1px dashed #FF9A44; border-radius: 14px;
    padding: 10px 18px; margin-bottom: 16px; color: #9A3412; font-weight: 500;
}

/* ---------- section titles ---------- */
.sec-title {font-size: 1.35rem; font-weight: 700; color: #1F2937; margin: 6px 0 2px 0;}
.sec-sub {color: #6B7280; font-size: 0.9rem; margin-bottom: 14px;}

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: #ffffff; padding: 6px; border-radius: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.stTabs button[data-baseweb="tab"] {border-radius: 12px; padding: 8px 18px; height: auto; font-weight: 600;}
.stTabs button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #FF6B35, #FF9A44);
}
.stTabs button[data-baseweb="tab"][aria-selected="true"] p {color: #ffffff !important;}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display: none;}

/* ---------- product cards (menu) ---------- */
.pcard {
    background: #ffffff; border-radius: 20px; padding: 18px 14px; text-align: center;
    margin-bottom: 14px; border-top: 5px solid var(--c);
    box-shadow: 0 4px 16px rgba(0,0,0,0.07); transition: all 0.2s ease; color: #1F2937;
}
.pcard:hover {transform: translateY(-4px); box-shadow: 0 12px 26px rgba(0,0,0,0.13);}
.pc-emoji {font-size: 2.7rem; line-height: 1.2;}
.pc-name {font-weight: 600; font-size: 1.02rem; margin-top: 6px;}
.pc-price {color: var(--c); font-weight: 800; font-size: 1.35rem; margin: 4px 0 8px 0;}
.pcard.soldout {opacity: 0.55; filter: grayscale(0.8);}
.badge {padding: 3px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;}
.badge.ok {background: #E6F6EA; color: #1B7F3B;}
.badge.no {background: #FDE7E7; color: #C62828;}

/* ---------- order rows ---------- */
.orow {
    display: flex; align-items: center; gap: 14px; background: #ffffff; color: #1F2937;
    border-radius: 16px; padding: 10px 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.orow.soldout {opacity: 0.5;}
.or-emoji {font-size: 2rem;}
.or-name {font-weight: 600;}
.or-price {color: #FF6B35; font-weight: 700; font-size: 0.95rem;}

/* ---------- bill ---------- */
.bill {
    background: #ffffff; color: #1F2937; border-radius: 22px; padding: 20px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.10); border-top: 6px solid #FF6B35; margin-bottom: 12px;
}
.bill-title {font-weight: 700; font-size: 1.15rem; margin-bottom: 10px;}
.bill-line {display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed #E5E7EB; font-size: 0.92rem;}
.bill-empty {color: #9CA3AF; text-align: center; padding: 14px 0;}
.bill-total {display: flex; justify-content: space-between; margin-top: 12px; font-size: 1.3rem; font-weight: 800; color: #FF6B35;}

/* ---------- receipt ---------- */
.receipt {
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5); border: 1px solid #6EE7B7; color: #065F46;
    border-radius: 20px; padding: 18px 22px; margin-bottom: 16px;
}
.r-top {font-weight: 700; font-size: 1.1rem;}
.r-token {font-size: 2.2rem; font-weight: 800; margin: 2px 0;}

/* ---------- notices ---------- */
.notice {
    background: #ffffff; color: #1F2937; border-radius: 16px; padding: 14px 18px;
    margin-bottom: 12px; border-left: 6px solid var(--c); box-shadow: 0 3px 12px rgba(0,0,0,0.07);
}
.n-head {display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;}
.n-tag {color: var(--c); font-weight: 700; font-size: 0.85rem;}
.n-time {color: #9CA3AF; font-size: 0.78rem;}
.n-msg {font-weight: 500;}

/* ---------- ratings ---------- */
.rate-big {
    background: linear-gradient(135deg, #FFF7ED, #FFEDD5); color: #9A3412; border-radius: 20px;
    padding: 18px; text-align: center; margin-bottom: 14px;
}
.rate-num {font-size: 2.8rem; font-weight: 800; line-height: 1.1;}
.bar-row {display: flex; align-items: center; gap: 10px; margin-bottom: 8px; font-size: 0.85rem; color: #1F2937;}
.bar-row span {width: 38%;}
.bar {flex: 1; height: 9px; background: #F3F4F6; border-radius: 10px; overflow: hidden;}
.bar i {display: block; height: 100%; background: linear-gradient(90deg, #FF6B35, #FF9A44); border-radius: 10px;}
.bar-row b {width: 22%; text-align: right;}
.review {background: #ffffff; color: #1F2937; border-radius: 14px; padding: 12px 16px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);}
.review small {color: #6B7280;}

/* ---------- info card ---------- */
.info-card {
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF); color: #3730A3;
    border-radius: 20px; padding: 20px; line-height: 1.7;
}

/* ---------- admin KPI ---------- */
.kpi {
    display: flex; align-items: center; gap: 12px; background: #ffffff; color: #1F2937;
    border-radius: 18px; padding: 16px; border-left: 6px solid var(--c);
    box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 12px;
}
.kpi-ico {font-size: 1.9rem;}
.kpi-val {font-size: 1.5rem; font-weight: 800; color: var(--c); line-height: 1.1;}
.kpi-lbl {font-size: 0.8rem; color: #6B7280; font-weight: 500;}

/* ---------- inputs & buttons ---------- */
.stTextInput input, .stTextArea textarea, .stNumberInput input {border-radius: 12px;}
[data-baseweb="select"] > div {border-radius: 12px;}
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #FF6B35, #FF9A44); color: #ffffff; border: none;
    border-radius: 12px; padding: 0.55rem 1.4rem; font-weight: 600; width: 100%;
    box-shadow: 0 4px 12px rgba(255,107,53,0.35); transition: all 0.2s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px); box-shadow: 0 8px 18px rgba(255,107,53,0.45); color: #ffffff; border: none;
}
.stButton > button:disabled {background: #E5E7EB; color: #9CA3AF; box-shadow: none;}

/* bill column sticks while scrolling (desktop only) */
div[data-testid="stColumn"]:has(.bill-anchor), div[data-testid="column"]:has(.bill-anchor) {
    position: sticky; top: 4.5rem; align-self: flex-start;
}
@media (max-width: 640px) {
    .hero-title {font-size: 1.45rem;}
    div[data-testid="stColumn"]:has(.bill-anchor), div[data-testid="column"]:has(.bill-anchor) {position: static;}
}
"""


def render(markup):
    """Render HTML (blank lines / indentation removed so Markdown never breaks it)."""
    lines = [ln.strip() for ln in markup.strip().splitlines() if ln.strip()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def esc(value):
    return _html.escape(str(value))


render(f"<style>{CSS}</style>")


# =====================================================================
#  DATA HELPERS
# =====================================================================
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def today():
    return datetime.now().strftime("%Y-%m-%d")


def read(file, cols):
    try:
        df = pd.read_csv(file)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=cols)
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df


def append(file, row, cols):
    pd.DataFrame([row])[cols].to_csv(file, mode="a", header=not os.path.exists(file), index=False)


def save(df, file):
    df.to_csv(file, index=False)


def load_products():
    if not os.path.exists(F_PRODUCTS):
        df = pd.DataFrame(DEFAULT_PRODUCTS, columns=["category", "item", "emoji", "price"])
        df["available"] = True
        save(df[PRODUCT_COLS], F_PRODUCTS)
    df = read(F_PRODUCTS, PRODUCT_COLS)
    df["emoji"] = df["emoji"].fillna("🍽️").replace("", "🍽️")
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).astype(int)
    df["available"] = df["available"].fillna(True).astype(bool)
    return df[PRODUCT_COLS]


def load_orders():
    df = read(F_ORDERS, ORDER_COLS)
    df["total"] = pd.to_numeric(df["total"], errors="coerce").fillna(0).astype(int)
    df["status"] = df["status"].replace("", "Pending").fillna("Pending")
    df["time"] = df["time"].astype(str)
    return df


def only_today(df):
    return df[df["time"].astype(str).str.startswith(today())]


# =====================================================================
#  SESSION + CALLBACKS
# =====================================================================
st.session_state.setdefault("is_admin", False)
st.session_state.setdefault("receipt", None)
st.session_state.setdefault("order_msg", None)
st.session_state.setdefault("login_error", False)


def qty_key(item):
    return f"qty::{item}"


def get_cart(products):
    cart = {}
    for _, r in products[products["available"]].iterrows():
        q = int(st.session_state.get(qty_key(r["item"]), 0) or 0)
        if q > 0:
            cart[r["item"]] = (q, int(r["price"]), r["emoji"])
    return cart


def place_order():
    s = st.session_state
    products = load_products()
    cart = get_cart(products)
    name = str(s.get("o_name", "")).strip()
    if not name:
        s["order_msg"] = "Please enter your name."
        return
    if not cart:
        s["order_msg"] = "Please add at least one item to your cart."
        return
    total = sum(q * p for q, p, _ in cart.values())
    orders = load_orders()
    token = len(only_today(orders)) + 1
    items_text = ", ".join(f"{i} x{q}" for i, (q, _, _) in cart.items())
    append(F_ORDERS, {
        "token": token, "time": now(), "name": name,
        "roll_no": str(s.get("o_roll", "")).strip(), "type": s.get("o_type", "Dine-in"),
        "items": items_text, "total": total, "status": "Pending",
    }, ORDER_COLS)
    s["receipt"] = {"token": token, "name": name, "items": items_text, "total": total}
    s["order_msg"] = None
    for item in cart:
        s[qty_key(item)] = 0
    s["o_name"] = ""
    s["o_roll"] = ""


def clear_receipt():
    st.session_state["receipt"] = None


def submit_feedback():
    s = st.session_state
    append(F_FEEDBACK, {
        "time": now(), "name": str(s.get("fb_name", "")).strip() or "Anonymous",
        "item": s.get("fb_item", ""), "rating": int(s.get("fb_rating", 5)),
        "feedback": str(s.get("fb_text", "")).strip(),
    }, FEEDBACK_COLS)
    s["fb_text"] = ""
    s["fb_name"] = ""
    s["fb_done"] = True


def submit_complaint():
    s = st.session_state
    text = str(s.get("c_text", "")).strip()
    if not text:
        s["c_error"] = True
        return
    append(F_COMPLAINTS, {
        "time": now(), "name": str(s.get("c_name", "")).strip() or "Anonymous",
        "type": s.get("c_type", "Complaint"), "category": s.get("c_cat", "Other"), "message": text,
    }, COMPLAINT_COLS)
    s["c_text"] = ""
    s["c_name"] = ""
    s["c_error"] = False
    s["c_done"] = s.get("c_type", "Complaint")


def admin_login():
    s = st.session_state
    if s.get("admin_pw", "") == ADMIN_PASSWORD:
        s["is_admin"] = True
        s["login_error"] = False
    else:
        s["login_error"] = True


def admin_logout():
    st.session_state["is_admin"] = False


def post_notice():
    s = st.session_state
    msg = str(s.get("a_nmsg", "")).strip()
    if not msg:
        s["a_nerror"] = True
        return
    append(F_NOTICES, {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"), "time": now(),
        "type": s.get("a_ntype", "Notice"), "message": msg,
    }, NOTICE_COLS)
    s["a_nmsg"] = ""
    s["a_nerror"] = False
    s["a_ndone"] = True


def delete_notice(nid):
    df = read(F_NOTICES, NOTICE_COLS)
    df = df[df["id"].astype(str) != str(nid)]
    save(df, F_NOTICES)


# =====================================================================
#  UI COMPONENTS
# =====================================================================
def hero(tag, tagline):
    render(f"""
    <div class="hero">
    <div class="hero-tag">{tag}</div>
    <div class="hero-title">{COLLEGE} <small>(Autonomous)</small></div>
    <div class="hero-sub">{tagline}</div>
    </div>
    """)


def section(title, sub=""):
    render(f'<div class="sec-title">{title}</div><div class="sec-sub">{sub}</div>')


def product_card(r):
    color = CATS.get(r["category"], ("", "#FF6B35"))[1]
    emoji, name, price = r["emoji"], esc(r["item"]), int(r["price"])
    if r["available"]:
        cls, badge = "pcard", '<span class="badge ok">● Available</span>'
    else:
        cls, badge = "pcard soldout", '<span class="badge no">● Sold out</span>'
    render(f"""
    <div class="{cls}" style="--c:{color}">
    <div class="pc-emoji">{emoji}</div>
    <div class="pc-name">{name}</div>
    <div class="pc-price">₹{price}</div>
    {badge}
    </div>
    """)


def order_row(r):
    cls = "orow" if r["available"] else "orow soldout"
    tag = "" if r["available"] else '<span class="badge no">Sold out</span>'
    emoji, name, price = r["emoji"], esc(r["item"]), int(r["price"])
    render(f"""
    <div class="{cls}">
    <div class="or-emoji">{emoji}</div>
    <div><div class="or-name">{name}</div><div class="or-price">₹{price} {tag}</div></div>
    </div>
    """)


def notice_card(r):
    emoji, color = NOTICE_TYPES.get(str(r["type"]), ("📌", "#FF6B35"))
    render(f"""
    <div class="notice" style="--c:{color}">
    <div class="n-head"><span class="n-tag">{emoji} {esc(r["type"])}</span><span class="n-time">{esc(r["time"])}</span></div>
    <div class="n-msg">{esc(r["message"])}</div>
    </div>
    """)


def review_card(r, who=True):
    stars = "⭐" * int(float(r["rating"]))
    text = esc(r["feedback"]) if str(r["feedback"]) not in ("", "nan") else "<i>No comment</i>"
    head = f"<b>{esc(r['name'])}</b> · " if who else ""
    render(f"""
    <div class="review">{head}{esc(r["item"])} {stars}<br>{text}<br><small>{esc(r["time"])}</small></div>
    """)


def kpi(icon, value, label, color):
    render(f"""
    <div class="kpi" style="--c:{color}"><div class="kpi-ico">{icon}</div>
    <div><div class="kpi-val">{value}</div><div class="kpi-lbl">{label}</div></div></div>
    """)


def csv_button(df, label, filename, key):
    st.download_button(label, df.to_csv(index=False).encode("utf-8"), file_name=filename, mime="text/csv", key=key)


# =====================================================================
#  SIDEBAR  (admin login is hidden from students here)
# =====================================================================
with st.sidebar:
    render('<div class="sec-title">🔒 Admin</div><div class="sec-sub">For canteen staff only</div>')
    if st.session_state["is_admin"]:
        st.success("Logged in as Admin")
        st.button("Logout", on_click=admin_logout, key="logout_btn")
    else:
        with st.form("login_form"):
            st.text_input("Password", type="password", key="admin_pw")
            st.form_submit_button("Login", on_click=admin_login)
        if st.session_state["login_error"]:
            st.error("Wrong password")


# =====================================================================
#  STUDENT VIEW
# =====================================================================
def student_view():
    products = load_products()
    notices = read(F_NOTICES, NOTICE_COLS)

    hero("🍽️ FOOD COURT", "Fresh food  •  Quick orders  •  Hostel essentials")

    if len(notices) > 0:
        last = notices.iloc[-1]
        emoji = NOTICE_TYPES.get(str(last["type"]), ("📌", ""))[0]
        render(f'<div class="ticker">{emoji} <b>{esc(last["type"])}:</b> {esc(last["message"])}</div>')

    tab_menu, tab_order, tab_fb, tab_notice, tab_comp = st.tabs(
        ["🍔 Menu", "🛒 Order", "⭐ Feedback", "📢 Notices", "📝 Complaints"]
    )

    # ------------------------------------------------------------ MENU
    with tab_menu:
        section("Digital Menu", "Everything available in our food court today")
        query = st.text_input("🔍 Search any item", key="menu_search", placeholder="Type dosa, juice, soap ...")
        cat_tabs = st.tabs([TAB_LABEL[c] for c in CATS])
        for cat, tab in zip(CATS, cat_tabs):
            with tab:
                items = products[products["category"] == cat]
                if query.strip():
                    items = items[items["item"].str.contains(query.strip(), case=False, na=False)]
                if items.empty:
                    st.info("No items found here.")
                    continue
                cols = st.columns(3)
                for n, (_, r) in enumerate(items.iterrows()):
                    with cols[n % 3]:
                        product_card(r)

    # ------------------------------------------------------------ ORDER
    with tab_order:
        rc = st.session_state.get("receipt")
        if rc:
            render(f"""
            <div class="receipt">
            <div class="r-top">✅ Order placed successfully!</div>
            <div class="r-token">Token #{int(rc["token"]):03d}</div>
            <div>{esc(rc["items"])}</div>
            <div><b>Total: ₹{int(rc["total"])}</b> — please pay at the counter and show this token.</div>
            </div>
            """)
            st.button("➕ Place another order", on_click=clear_receipt, key="new_order_btn")

        left, right = st.columns([2.1, 1], gap="large")

        with left:
            section("Choose your items", "Use the number box to set the quantity")
            order_tabs = st.tabs([TAB_LABEL[c] for c in CATS])
            for cat, tab in zip(CATS, order_tabs):
                with tab:
                    for _, r in products[products["category"] == cat].iterrows():
                        a, b = st.columns([3, 1.3], vertical_alignment="center")
                        with a:
                            order_row(r)
                        with b:
                            st.number_input(
                                f"Quantity of {r['item']}", min_value=0, max_value=10, step=1,
                                key=qty_key(r["item"]), label_visibility="collapsed",
                                disabled=not r["available"],
                            )

        with right:
            render('<div class="bill-anchor"></div>')
            cart = get_cart(products)
            total = sum(q * p for q, p, _ in cart.values())
            if cart:
                lines = "".join(
                    f'<div class="bill-line"><span>{e} {esc(i)} × {q}</span><b>₹{q * p}</b></div>'
                    for i, (q, p, e) in cart.items()
                )
            else:
                lines = '<div class="bill-empty">🛒 Your cart is empty</div>'
            render(f"""
            <div class="bill"><div class="bill-title">🧾 Your Order</div>{lines}
            <div class="bill-total"><span>Total</span><span>₹{total}</span></div></div>
            """)
            st.text_input("Your name *", key="o_name", placeholder="Enter your name")
            st.text_input("Roll no / Department (optional)", key="o_roll")
            st.selectbox("Order type", ["Dine-in", "Takeaway"], key="o_type")
            st.button("✅ Place Order", on_click=place_order, key="place_order_btn")
            if st.session_state.get("order_msg"):
                st.error(st.session_state["order_msg"])

    # ------------------------------------------------------------ FEEDBACK
    with tab_fb:
        section("Feedback & Rating", "Tell us how the food was — it helps us improve")
        fl, fr = st.columns([1.2, 1], gap="large")
        fb = read(F_FEEDBACK, FEEDBACK_COLS)
        fb["rating"] = pd.to_numeric(fb["rating"], errors="coerce").fillna(0)

        with fl:
            emoji_of = dict(zip(products["item"], products["emoji"]))
            options = ["Overall Food Court"] + products["item"].tolist()
            st.text_input("Your name (optional)", key="fb_name")
            st.selectbox("What are you rating?", options, key="fb_item",
                         format_func=lambda x: f"{emoji_of.get(x, '🍽️')} {x}")
            st.radio("Rating", [5, 4, 3, 2, 1], index=1, horizontal=True, key="fb_rating",
                     format_func=lambda n: "⭐" * n)
            st.text_area("Your feedback", key="fb_text", placeholder="What did you like or dislike?")
            st.button("Submit Feedback", on_click=submit_feedback, key="fb_btn")
            if st.session_state.pop("fb_done", False):
                st.success("Thank you for your feedback! 🙏")

        with fr:
            if len(fb) == 0:
                render('<div class="info-card">⭐ No ratings yet.<br>Be the first one to rate!</div>')
            else:
                avg = fb["rating"].mean()
                render(f'<div class="rate-big"><div class="rate-num">{avg:.1f} ⭐</div><div>Overall rating from {len(fb)} reviews</div></div>')
                g = fb.groupby("item")["rating"].agg(["mean", "count"]).sort_values("mean", ascending=False).head(6)
                bars = "".join(
                    f'<div class="bar-row"><span>{esc(i)}</span><div class="bar"><i style="width:{m / 5 * 100:.0f}%"></i></div><b>{m:.1f} ({int(c)})</b></div>'
                    for i, (m, c) in g.iterrows()
                )
                render(f'<div class="sec-title" style="font-size:1.05rem">Top rated</div>{bars}')
                render('<div class="sec-title" style="font-size:1.05rem;margin-top:14px">Recent reviews</div>')
                for _, r in fb.tail(3).iloc[::-1].iterrows():
                    review_card(r, who=False)

    # ------------------------------------------------------------ NOTICES
    with tab_notice:
        section("Canteen Announcements", "Today's special, timings and notices")
        if len(notices) == 0:
            render('<div class="info-card">📭 No announcements right now.<br>Check back later!</div>')
        else:
            for _, r in notices.iloc[::-1].iterrows():
                notice_card(r)

    # ------------------------------------------------------------ COMPLAINTS
    with tab_comp:
        section("Complaint & Suggestion Box", "Your message goes directly to the canteen management")
        cl, cr = st.columns([1.2, 1], gap="large")
        with cl:
            st.text_input("Your name (optional)", key="c_name")
            st.radio("Type", ["Complaint", "Suggestion"], horizontal=True, key="c_type")
            st.selectbox("Category", COMPLAINT_CATEGORIES, key="c_cat")
            st.text_area("Your message *", key="c_text", placeholder="Write here ...")
            st.button("Submit", on_click=submit_complaint, key="c_btn")
            if st.session_state.get("c_error"):
                st.error("Please write your message first.")
            done = st.session_state.pop("c_done", None)
            if done:
                st.success(f"Your {done.lower()} has been submitted. Thank you! 🙏")
        with cr:
            render("""
            <div class="info-card"><b>🔒 Private & safe</b><br>
            Only the canteen admin can read complaints and suggestions.<br><br>
            💡 Tell us about food quality, hygiene, prices, service, or ideas for new items.</div>
            """)


# =====================================================================
#  ADMIN VIEW
# =====================================================================
def admin_view():
    products = load_products()
    orders = load_orders()
    fb = read(F_FEEDBACK, FEEDBACK_COLS)
    fb["rating"] = pd.to_numeric(fb["rating"], errors="coerce").fillna(0)
    comp = read(F_COMPLAINTS, COMPLAINT_COLS)
    notices = read(F_NOTICES, NOTICE_COLS)

    hero("🔒 ADMIN PANEL", "Orders  •  Menu  •  Announcements  •  Feedback")

    t_dash, t_orders, t_menu, t_fb = st.tabs(
        ["📊 Dashboard", "🧾 Orders", "📋 Menu", "💬 Feedback & Complaints"]
    )

    today_orders = only_today(orders)
    today_valid = today_orders[today_orders["status"] != "Cancelled"]
    fb_today = fb[fb["time"].astype(str).str.startswith(today())]
    comp_today = comp[comp["time"].astype(str).str.startswith(today())]

    # ------------------------------------------------------------ DASHBOARD
    with t_dash:
        k = st.columns(5)
        with k[0]:
            kpi("💰", f"₹{int(today_valid['total'].sum())}", "Today's Sales", "#10B981")
        with k[1]:
            kpi("🧾", len(today_orders), "Today's Orders", "#FF6B35")
        with k[2]:
            kpi("⏳", int((orders["status"] == "Pending").sum()), "Pending Orders", "#F59E0B")
        with k[3]:
            kpi("⭐", f"{fb['rating'].mean():.1f}" if len(fb) else "–", "Avg Rating", "#8B5CF6")
        with k[4]:
            kpi("📝", len(comp_today), "New Complaints Today", "#EF4444")

        if len(comp_today) > 0:
            st.warning(f"⚠️ {len(comp_today)} new complaint/suggestion(s) received today. Scroll down to read them.")

        left, right = st.columns(2, gap="large")

        with left:
            section("📢 Quick Announcement", "Post today's special, timings or any notice")
            st.selectbox("Type", list(NOTICE_TYPES), key="a_ntype")
            st.text_area("Message", key="a_nmsg", placeholder="Eg: Today's special - Veg Biryani only ₹70!")
            st.button("📢 Post Announcement", on_click=post_notice, key="post_notice_btn")
            if st.session_state.get("a_nerror"):
                st.error("Please write a message.")
            if st.session_state.pop("a_ndone", False):
                st.success("Announcement posted! Students can see it now.")

            render('<div class="sec-title" style="font-size:1.05rem;margin-top:16px">Active announcements</div>')
            if len(notices) == 0:
                st.caption("No announcements posted.")
            for _, r in notices.iloc[::-1].iterrows():
                notice_card(r)
                st.button("🗑️ Delete", key=f"del_{r['id']}", on_click=delete_notice, args=(r["id"],))

        with right:
            section("⭐ Today's Feedback", f"{len(fb_today)} new")
            if fb_today.empty:
                st.caption("No feedback today yet.")
            for _, r in fb_today.iloc[::-1].iterrows():
                review_card(r)
            section("📝 Complaints & Suggestions", f"{len(comp_today)} new today")
            if comp_today.empty:
                st.caption("Nothing new today.")
            for _, r in comp_today.iloc[::-1].iterrows():
                render(f"""
                <div class="review"><b>{esc(r["name"])}</b> · {esc(r["type"])} · {esc(r["category"])}<br>
                {esc(r["message"])}<br><small>{esc(r["time"])}</small></div>
                """)

        section("📈 Sales – last 7 days")
        days = [(date.today() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        valid = orders[orders["status"] != "Cancelled"].copy()
        valid["day"] = valid["time"].str[:10]
        daily = valid.groupby("day")["total"].sum().reindex(days, fill_value=0)
        st.bar_chart(daily, color="#FF6B35")

    # ------------------------------------------------------------ ORDERS
    with t_orders:
        section("Orders", "Change the status and click Save")
        scope = st.radio("Show", ["Today", "All"], horizontal=True, key="ord_scope")
        view = (only_today(orders) if scope == "Today" else orders).sort_values("time", ascending=False)
        if view.empty:
            st.info("No orders yet.")
        else:
            edited = st.data_editor(
                view, hide_index=True, width="stretch", key="orders_editor",
                disabled=[c for c in ORDER_COLS if c != "status"],
                column_config={
                    "status": st.column_config.SelectboxColumn("Status", options=STATUSES, required=True),
                    "total": st.column_config.NumberColumn("Total", format="₹%d"),
                },
            )
            if st.button("💾 Save status changes", key="save_orders_btn"):
                orders.loc[edited.index, "status"] = edited["status"]
                save(orders, F_ORDERS)
                st.toast("Order status updated ✅")
                st.rerun()
        csv_button(orders, "⬇️ Download all orders (CSV)", "orders.csv", "dl_orders")
        with st.expander("⚠️ Danger zone"):
            sure = st.checkbox("I want to delete ALL orders", key="sure_orders")
            if st.button("Clear all orders", disabled=not sure, key="clear_orders_btn") and os.path.exists(F_ORDERS):
                os.remove(F_ORDERS)
                st.rerun()

    # ------------------------------------------------------------ MENU
    with t_menu:
        section("Menu Manager", "Edit price, tick / untick Available, or add and delete items. Then click Save.")
        edited_menu = st.data_editor(
            products, num_rows="dynamic", hide_index=True, width="stretch", key="menu_editor",
            column_config={
                "category": st.column_config.SelectboxColumn("Category", options=list(CATS), required=True),
                "item": st.column_config.TextColumn("Item", required=True),
                "emoji": st.column_config.TextColumn("Emoji", width="small"),
                "price": st.column_config.NumberColumn("Price (₹)", min_value=0, step=1, format="%d"),
                "available": st.column_config.CheckboxColumn("Available"),
            },
        )
        if st.button("💾 Save menu", key="save_menu_btn"):
            df = edited_menu.copy().dropna(subset=["item", "category"])
            df["item"] = df["item"].astype(str).str.strip()
            df = df[df["item"] != ""]
            df["emoji"] = df["emoji"].fillna("🍽️")
            df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).astype(int)
            df["available"] = df["available"].fillna(True).astype(bool)
            df = df.drop_duplicates("item")[PRODUCT_COLS]
            save(df, F_PRODUCTS)
            st.toast("Menu saved ✅")
            st.rerun()

    # ------------------------------------------------------------ FEEDBACK + COMPLAINTS
    with t_fb:
        sub_fb, sub_comp = st.tabs(["⭐ Feedback", "📝 Complaints & Suggestions"])
        with sub_fb:
            st.dataframe(fb.iloc[::-1], hide_index=True, width="stretch")
            csv_button(fb, "⬇️ Download feedback (CSV)", "feedback.csv", "dl_fb")
        with sub_comp:
            st.dataframe(comp.iloc[::-1], hide_index=True, width="stretch")
            csv_button(comp, "⬇️ Download complaints (CSV)", "complaints.csv", "dl_comp")


# =====================================================================
#  ROUTER
# =====================================================================
if st.session_state["is_admin"]:
    admin_view()
else:
    student_view()

render(f'<div style="text-align:center;color:#9CA3AF;font-size:0.8rem;margin-top:30px">© {COLLEGE} (Autonomous) · Food Court</div>')