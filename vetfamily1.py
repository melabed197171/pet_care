
import streamlit as st
import urllib.parse
import json
import os
import hashlib
import copy

# =============================================
# إعدادات الصفحة
# =============================================
st.set_page_config(
    page_title="Vet Family Care",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================
# ثوابت
# =============================================
WA_NUMBER = "201022395878"
PHONE = "01022395878"
LOCATION = "محرم بك - الإسكندرية"

ADMIN_USER = "melabed"
ADMIN_PASS_HASH = hashlib.sha256("Ma3902242$".encode()).hexdigest()

DB_FILE = "vetfamily_care_products_db.json"

# =============================================
# بيانات المنتجات
# =============================================
RAW_PRODUCTS = """
رمل القطط|1|كات ساند بنتونايت 5 كجم|رمل متكتل برائحة اللافندر، امتصاص سريع.|90|🏖️|45|كيس 5 كجم|Cat Sand|popular,sale
رمل القطط|2|رمل كربون نشط 5 لتر|تركيبة كربون لامتصاص الروائح القوية.|180|⚫|20|كيس 5 لتر|Carbon Cat|premium
رمل القطط|3|رمل سيليكا كريستال 3.8 لتر|حبيبات شفافة، عمر افتراضي أطول.|180|💎|12|كيس 3.8 لتر|SilicaCare|premium
رمل القطط|4|رمل طبيعي ذرة 6 كجم|رمل نباتي صديق للبيئة.|140|🌽|8|كيس 6 كجم|EcoPaw|new,vet
رمل القطط|5|رمل توفو طبيعي 6 لتر|رمل نباتي فاخر، سريع التكتل.|210|🌱|10|كيس 6 لتر|Tofu Cat|recommended
رمل القطط|6|رمل اقتصادي 10 كجم|مناسب للمنازل متعددة القطط.|150|📦|35|كيس 10 كجم|Easy Sand|sale
صناديق وأدوات|7|صندوق رمل مفتوح كبير|عملي وسهل التنظيف.|130|🚽|18|قطعة|PetHome|popular
صناديق وأدوات|8|صندوق رمل مغلق مع فلتر|يقلل الروائح ويمنع التطاير.|220|🏠|15|قطعة|PetHome|premium
صناديق وأدوات|9|مجرفة رمل معدنية|قوية بفتحات دقيقة.|45|🥄|30|قطعة|CleanScoop|sale
صناديق وأدوات|10|حصيرة عازل رمل 60×40|تمسك الرمل المتساقط.|85|🟫|20|قطعة|PawMat|new
صناديق وأدوات|11|أكياس فضلات معطرة|للتخلص السهل من الفضلات.|60|🛍️|40|رول|CleanBag|popular
صناديق وأدوات|12|بودرة مزيل روائح|تضاف للرمل لتقليل الروائح.|75|🧂|16|عبوة|Odor Stop|vet
أطباق ومياه|13|طبق مزدوج ستانلس|للطعام والمياه، ثابت.|95|🍽️|22|قطعة|FoodPet|popular
أطباق ومياه|14|طبق أكل مانع للانزلاق|بلاستيك قوي للحيوانات الصغيرة.|55|🥣|30|قطعة|Easy Bowl|sale
أطباق ومياه|15|نافورة مياه 1.8 لتر|تشجع على الشرب، مياه متجددة.|450|⛲|7|قطعة|AquaPet|premium
أطباق ومياه|16|زجاجة مياه خروج|عملية للرحلات.|120|🚰|14|قطعة|Travel Drink|new
إكسسوارات|17|طوق جلد مع جرس|أنيق وقابل للتعديل.|80|🎀|35|قطعة|PetStyle|popular
إكسسوارات|18|سلسلة مشي نايلون 1.5م|قوية بمقبض مريح.|95|🦮|22|قطعة|WalkEasy|sale
إكسسوارات|19|هارنس قطط قابل للتعديل|آمن للخروج.|150|🧷|13|قطعة|SafeWalk|recommended
إكسسوارات|20|حقيبة نقل شبكية|خفيفة بتهوية ممتازة.|280|🎒|10|مقاس متوسط|TravelPet|premium
ألعاب وخدش|21|فأر إلكتروني متحرك|لعبة تفاعلية لتنشيط الصيد.|120|🐭|18|قطعة|SmartPlay|new
ألعاب وخدش|22|عمود خدش كرتون|يحمي الأثاث ويشحذ المخالب.|160|📦|14|قطعة|ScratchPro|sale
ألعاب وخدش|23|كرة ريش مع جرس|خفيفة وملونة.|25|🪶|50|3 قطع|FeatherFun|popular
ألعاب وخدش|24|سنارة ريش للقطط|لزيادة النشاط.|65|🎣|24|قطعة|Play Stick|recommended
عناية وتنظيف|25|فرشاة فك التشابك|للفراء الطويل والقصير.|55|🪮|25|قطعة|GroomPro|vet
عناية وتنظيف|26|مقص أظافر بواقي|يمنع القص الزائد.|70|✂️|16|قطعة|SafeClip|premium
عناية وتنظيف|27|مناديل مبللة 80 منديل|تنظيف سريع وآمن.|40|🧻|40|علبة|FreshPaw|sale
عناية وتنظيف|28|شامبو جاف للقطط|تنظيف بدون مياه.|110|🧴|11|عبوة|Dry Clean|new
"""

def build_default_products():
    data = {}
    for line in RAW_PRODUCTS.strip().splitlines():
        cat, pid, name, desc, price, icon, stock, unit, brand, badges = line.split("|")
        data.setdefault(cat, []).append({
            "id": int(pid),
            "name": name,
            "desc": desc,
            "price": int(price),
            "icon": icon,
            "stock": int(stock),
            "unit": unit,
            "brand": brand,
            "country": "مصر",
            "badges": [b for b in badges.split(",") if b],
            "features": ["جودة ممتازة", "مناسب للاستخدام اليومي", desc],
        })
    return data

DEFAULT_PRODUCTS = build_default_products()

# =============================================
# تحميل / حفظ البيانات
# =============================================
def load_products():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return copy.deepcopy(DEFAULT_PRODUCTS)

def save_products(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"خطأ في الحفظ: {e}")
        return False

if "products" not in st.session_state:
    st.session_state.products = load_products()

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False

# =============================================
# CSS
# =============================================
st.markdown(
    """
<style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
        background-attachment: fixed;
    }

    html, body, [data-testid="stAppViewContainer"], .main, .block-container {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .block-container {
        max-width: 100% !important;
        padding: 1rem 1.5rem !important;
    }

    [data-testid="stMarkdownContainer"],
    .stMarkdown,
    label,
    [data-testid="stWidgetLabel"],
    input,
    textarea,
    [data-baseweb="select"],
    div[data-testid="column"],
    [data-testid="stExpander"] {
        direction: rtl !important;
        text-align: right !important;
    }

    .header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: #fff;
        padding: 25px 16px;
        border-radius: 18px;
        text-align: center !important;
        margin-bottom: 16px;
        box-shadow: 0 6px 20px rgba(30,60,114,0.15);
    }

    .header h1 {
        margin: 0;
        font-size: clamp(1.8rem, 4vw, 2.6rem);
        font-weight: 900;
    }

    .header p {
        margin: 8px 0 0;
        font-size: 1.05rem;
        opacity: 0.95;
    }

    .main-title {
        text-align: center !important;
        font-size: 2.4rem !important;
        font-weight: 900 !important;
        color: #1e3c72 !important;
        margin: 15px 0 8px !important;
    }

    .main-subtitle {
        text-align: center !important;
        font-size: 1.2rem !important;
        color: #475569 !important;
        margin: 0 0 14px !important;
    }

    .section-title {
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        color: #1e3c72 !important;
        margin: 16px 0 8px !important;
        text-align: right !important;
        border-right: 5px solid #667eea;
        padding-right: 10px;
    }

    .cat-title {
        font-size: 1.45rem !important;
        font-weight: 900 !important;
        color: #1e3c72 !important;
        margin: 14px 0 8px !important;
        text-align: right !important;
        border-right: 4px solid #764ba2;
        padding-right: 8px;
    }

    /* ==============================
       بوكس المنتجات
    ============================== */
    .card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transition: all 0.25s ease;
        height: 100%;
        text-align: right !important;
        position: relative;
        overflow: hidden;
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 28px rgba(0,0,0,0.14);
    }

    .card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        left: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transform-origin: right;
        transition: transform 0.3s ease;
    }

    .card:hover::before {
        transform: scaleX(1);
    }

    .icon {
        font-size: 34px !important;
        margin-bottom: 8px;
        line-height: 1;
        text-align: right !important;
    }

    .name {
        font-size: 19px !important;
        font-weight: 900;
        color: #1e293b;
        line-height: 1.45;
        min-height: 58px;
        margin-top: 4px;
        text-align: right !important;
    }

    .desc {
        color: #475569;
        font-size: 15.5px !important;
        margin-top: 8px;
        min-height: 48px;
        line-height: 1.6;
        font-weight: 600;
        text-align: right !important;
    }

    .price {
        color: #16a34a;
        font-weight: 900;
        font-size: 24px !important;
        margin-top: 12px;
        text-align: right !important;
    }

    .meta {
        color: #475569;
        font-size: 14.5px !important;
        margin-top: 10px;
        line-height: 1.7;
        font-weight: 700;
        text-align: right !important;
    }

    .stock {
        display: inline-block;
        margin-top: 12px;
        padding: 6px 13px;
        border-radius: 8px;
        font-size: 13.5px !important;
        font-weight: 900;
    }

    .ok { background: #dcfce7; color: #166534; }
    .low { background: #fef9c3; color: #854d0e; }
    .out { background: #fee2e2; color: #7f1d1d; }

    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 10px !important;
        font-weight: 800;
        margin: 2px;
        color: #fff;
    }

    .b-new { background: #10b981; }
    .b-sale { background: #ef4444; }
    .b-pop { background: #6366f1; }
    .b-prem { background: #a855f7; }
    .b-rec { background: #0ea5e9; }
    .b-vet { background: #22c55e; }

    /* =========================================
       زر أطلب المنتج عبر الوتساب
    ========================================= */
    .wa-product-btn {
        display: block;
        width: 100%;
        background: linear-gradient(135deg, #25D366, #128C7E) !important;
        color: #ffffff !important;
        text-align: center !important;
        text-decoration: none !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 15px 18px !important;
        border-radius: 14px !important;
        margin-top: 12px !important;
        box-shadow: 0 6px 16px rgba(37, 211, 102, 0.30);
        border: 2px solid #25D366 !important;
        transition: all 0.25s ease;
        line-height: 1.3;
    }

    .wa-product-btn:hover {
        background: linear-gradient(135deg, #128C7E, #075E54) !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(18, 140, 126, 0.35);
        text-decoration: none !important;
    }

    div[data-testid="stLinkButton"] button {
        background-color: #25D366 !important;
        color: white !important;
        border-color: #25D366 !important;
        font-weight: 900 !important;
        padding: 10px 15px !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
    }

    div[data-testid="stLinkButton"] button:hover {
        background-color: #128C7E !important;
        color: white !important;
        border-color: #128C7E !important;
    }

    .stButton > button {
        font-size: 0.9rem !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        padding: 7px 12px !important;
    }

    .divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        margin: 16px 0;
        opacity: 0.8;
    }

    .quick-info {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        border-radius: 12px;
        padding: 12px 14px;
        margin: 12px 0;
        font-size: 1rem;
        color: white;
        box-shadow: 0 4px 14px rgba(34, 197, 94, 0.20);
        border: 1px solid rgba(255,255,255,0.15);
        font-weight: 700;
    }

    .admin-bar {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        color: white;
        padding: 8px 14px;
        border-radius: 10px;
        text-align: center;
        font-weight: 900;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }

    .footer {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: #fff;
        padding: 16px;
        border-radius: 14px;
        text-align: center !important;
        margin-top: 20px;
    }

    .footer h3 {
        font-size: 1.3rem;
        margin: 0 0 4px;
        font-weight: 900;
    }

    .footer p {
        font-size: 0.95rem;
        margin: 0;
        opacity: 0.9;
        font-weight: 700;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem !important;
        }

        .card {
            padding: 13px !important;
        }

        .name {
            font-size: 16px !important;
            min-height: auto;
        }

        .desc {
            font-size: 13.5px !important;
            min-height: auto;
        }

        .icon {
            font-size: 26px !important;
        }

        .price {
            font-size: 20px !important;
        }

        .meta {
            font-size: 12.5px !important;
        }

        .wa-product-btn {
            font-size: 18px !important;
            padding: 12px 14px !important;
        }

        .main-title {
            font-size: 1.8rem !important;
        }

        .section-title {
            font-size: 1.3rem !important;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# =============================================
# دوال مساعدة
# =============================================
def wa_link(text):
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(text)}"

def badge_html(badges):
    m = {
        "new": ("جديد", "b-new"),
        "sale": ("عرض", "b-sale"),
        "popular": ("الأكثر طلباً", "b-pop"),
        "premium": ("بريميوم", "b-prem"),
        "recommended": ("موصى به", "b-rec"),
        "vet": ("موصى طبياً", "b-vet"),
    }
    return "".join(
        f'<span class="badge {c}">{t}</span>'
        for b in (badges or [])
        if b in m
        for t, c in [m[b]]
    )

def product_msg(p):
    return (
        "مرحباً Vet Family Care 🐾\n"
        "أود طلب المنتج التالي:\n\n"
        f"🛒 المنتج: {p['name']}\n"
        f"💰 السعر: {p['price']} ج.م\n"
        f"📦 الوحدة: {p['unit']}\n"
        f"🏷️ الماركة: {p['brand']}\n\n"
        "برجاء التأكيد 🙏"
    )

def get_stock_status(p):
    s = int(p["stock"])
    if s > 10:
        return "ok", f"✅ متوفر ({s})"
    elif s > 0:
        return "low", f"⚠️ محدود ({s})"
    else:
        return "out", "❌ نفذ"

def flatten_products():
    items = []
    for cat, lst in st.session_state.products.items():
        for it in lst:
            x = it.copy()
            x["category"] = cat
            items.append(x)
    return items

def get_next_id():
    items = flatten_products()
    return (max([int(p["id"]) for p in items]) + 1) if items else 1

def check_admin(u, p):
    return u == ADMIN_USER and hashlib.sha256(p.encode()).hexdigest() == ADMIN_PASS_HASH

def show_product_card(p):
    sc, st_txt = get_stock_status(p)

    st.markdown(f"""
    <div class="card">
        <div class="icon">{p.get('icon', '📦')}</div>
        <div class="name">{p.get('name', '')}</div>
        <div>{badge_html(p.get('badges'))}</div>
        <div class="desc">{p.get('desc', '')}</div>
        <div class="price">{p.get('price', 0)} ج.م</div>
        <div class="meta">📦 {p.get('unit', '')} | 🏷️ {p.get('brand', '')}</div>
        <div class="stock {sc}">{st_txt}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 التفاصيل", expanded=False):
        for f in p.get("features", []):
            st.write(f"• {f}")

    if int(p["stock"]) > 0:
        st.markdown(
            f"""
            <a class="wa-product-btn" href="{wa_link(product_msg(p))}" target="_blank">
                🟢 أطلب المنتج عبر الوتساب
            </a>
            """,
            unsafe_allow_html=True
        )
    else:
        st.button("نفذ", disabled=True, use_container_width=True, key=f"out_{p['id']}")

# =============================================
# الهيدر
# =============================================
st.markdown("""
<div class="header">
    <h1>🐾 Vet Family Care</h1>
    <p>كل ما يحتاجه أليفك — اطلب المنتج عبر الوتساب مباشرة</p>
</div>
""", unsafe_allow_html=True)

# =============================================
# أزرار سريعة
# =============================================
b1, b2, b3 = st.columns(3)

with b1:
    st.link_button(
        "💬 استفسر عبر الوتساب",
        wa_link("مرحباً Vet Family Care 🐾 أريد الاستفسار عن الرمل والمستلزمات."),
        use_container_width=True,
    )

with b2:
    st.link_button(
        "💬 أطلب عبر الوتساب",
        wa_link("مرحباً Vet Family Care 🐾 أريد معرفة المنتجات المتاحة."),
        use_container_width=True,
    )

with b3:
    label = "🔓 خروج المدير" if st.session_state.is_admin else "🔐 دخول المدير"
    if st.button(label, use_container_width=True):
        if st.session_state.is_admin:
            st.session_state.is_admin = False
            st.session_state.show_admin_login = False
        else:
            st.session_state.show_admin_login = not st.session_state.show_admin_login
        st.rerun()

# =============================================
# دخول المدير
# =============================================
if st.session_state.show_admin_login and not st.session_state.is_admin:
    with st.expander("🔐 تسجيل دخول المدير", expanded=True):
        lc1, lc2, lc3 = st.columns([2, 2, 1])
        with lc1:
            adm_user = st.text_input("اسم المستخدم", key="adm_user")
        with lc2:
            adm_pass = st.text_input("كلمة المرور", type="password", key="adm_pass")
        with lc3:
            st.write("")
            if st.button("دخول 🔓", use_container_width=True):
                if check_admin(adm_user, adm_pass):
                    st.session_state.is_admin = True
                    st.session_state.show_admin_login = False
                    st.success("✅ تم الدخول")
                    st.rerun()
                else:
                    st.error("❌ بيانات خاطئة")

if st.session_state.is_admin:
    st.markdown('<div class="admin-bar">⚙️ وضع المدير نشط</div>', unsafe_allow_html=True)

# =============================================
# العنوان
# =============================================
st.markdown('<div class="main-title">🛒 منتجاتنا</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">تشكيلة واسعة من الرمل والمستلزمات</div>', unsafe_allow_html=True)

# =============================================
# إحصائيات
# =============================================
all_products = flatten_products()

m1, m2, m3, m4 = st.columns(4)
m1.metric("المنتجات", len(all_products))
m2.metric("متوفر", len([x for x in all_products if int(x["stock"]) > 0]))
m3.metric("الأقسام", len(st.session_state.products))
m4.metric("العروض", len([x for x in all_products if "sale" in x.get("badges", [])]))

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =============================================
# بحث وفرز
# =============================================
st.markdown('<div class="section-title">🔎 بحث وفرز</div>', unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns([2, 2, 1, 1])

with f1:
    query = st.text_input("ابحث", placeholder="اسم أو ماركة...")
with f2:
    cat_sel = st.selectbox("القسم", ["الكل"] + list(st.session_state.products.keys()))
with f3:
    sort = st.selectbox("ترتيب", ["الأحدث", "السعر: الأقل", "السعر: الأعلى"])
with f4:
    avail = st.checkbox("المتوفر فقط")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =============================================
# عرض المنتجات
# =============================================
st.markdown('<div class="main-title">📦 القائمة</div>', unsafe_allow_html=True)

def matches(p):
    if avail and int(p["stock"]) <= 0:
        return False
    if not query.strip():
        return True
    q = query.lower()
    return (
        q in p.get("name", "").lower()
        or q in p.get("brand", "").lower()
        or q in p.get("desc", "").lower()
    )

cats = st.session_state.products.keys() if cat_sel == "الكل" else [cat_sel]
found = False

for cat in cats:
    items = [p.copy() for p in st.session_state.products[cat] if matches(p)]

    if not items:
        continue

    found = True

    if sort == "السعر: الأقل":
        items = sorted(items, key=lambda x: int(x["price"]))
    elif sort == "السعر: الأعلى":
        items = sorted(items, key=lambda x: int(x["price"]), reverse=True)

    st.markdown(f'<div class="cat-title">📦 {cat}</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, p in enumerate(items):
        with cols[i % 4]:
            show_product_card(p)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if not found:
    st.warning("لا توجد نتائج.")

st.markdown("""
<div class="quick-info">
    💡 اضغط زر <b>🟢 أطلب المنتج عبر الوتساب</b> تحت أي منتج وسيتم فتح المحادثة مباشرة برسالة جاهزة.
</div>
""", unsafe_allow_html=True)

# =============================================
# لوحة التحكم
# =============================================
if st.session_state.is_admin:
    st.markdown('<div class="main-title">⚙️ لوحة التحكم</div>', unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs(["📊 ملخص", "➕ إضافة", "✏️ تعديل / حذف", "📂 أقسام", "💾 نسخ"])

    with t1:
        st.markdown('<div class="section-title">الملخص</div>', unsafe_allow_html=True)
        val = sum(int(p["price"]) * int(p["stock"]) for p in all_products)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("قيمة المخزون", f"{val:,} ج.م")
        c2.metric("المنتجات", len(all_products))
        c3.metric("قاربت النفاذ", len([p for p in all_products if 0 < int(p["stock"]) <= 10]))
        c4.metric("نفذت", len([p for p in all_products if int(p["stock"]) == 0]))

    with t2:
        st.markdown('<div class="section-title">إضافة منتج</div>', unsafe_allow_html=True)
        with st.form("add_frm", clear_on_submit=True):
            cc1, cc2 = st.columns(2)
            with cc1:
                n_name = st.text_input("الاسم *")
                n_price = st.number_input("السعر", min_value=0, value=100)
                n_stock = st.number_input("الكمية", min_value=0, value=10)
                n_brand = st.text_input("الماركة", value="عام")
            with cc2:
                n_cat = st.selectbox("القسم", list(st.session_state.products.keys()))
                n_icon = st.text_input("الأيقونة", value="📦")
                n_unit = st.text_input("الوحدة", value="قطعة")
                n_badges = st.multiselect(
                    "شارات",
                    ["new", "sale", "popular", "premium", "recommended", "vet"]
                )
            n_desc = st.text_area("الوصف *", height=70)
            n_feat = st.text_area("المميزات", height=70)

            if st.form_submit_button("حفظ", type="primary", use_container_width=True):
                if n_name and n_desc:
                    st.session_state.products[n_cat].append({
                        "id": get_next_id(),
                        "name": n_name,
                        "desc": n_desc,
                        "price": int(n_price),
                        "icon": n_icon,
                        "stock": int(n_stock),
                        "unit": n_unit,
                        "brand": n_brand,
                        "country": "مصر",
                        "badges": n_badges,
                        "features": [f.strip() for f in n_feat.split("\n") if f.strip()] or [n_desc],
                    })
                    save_products(st.session_state.products)
                    st.success("تمت الإضافة")
                    st.rerun()
                else:
                    st.error("الاسم والوصف مطلوبان")

    with t3:
        st.markdown('<div class="section-title">تعديل / حذف</div>', unsafe_allow_html=True)
        all_products = flatten_products()

        if all_products:
            opts = {f"{p.get('icon', '📦')} {p['name']}": p for p in all_products}
            sel = st.selectbox("اختر منتج", list(opts.keys()))
            p = opts[sel]

            with st.form(f"edit_{p['id']}"):
                ec1, ec2 = st.columns(2)
                with ec1:
                    e_name = st.text_input("الاسم", value=p["name"])
                    e_price = st.number_input("السعر", min_value=0, value=int(p["price"]))
                    e_stock = st.number_input("الكمية", min_value=0, value=int(p["stock"]))
                    e_brand = st.text_input("الماركة", value=p["brand"])
                with ec2:
                    cats_list = list(st.session_state.products.keys())
                    e_cat = st.selectbox("القسم", cats_list, index=cats_list.index(p["category"]))
                    e_icon = st.text_input("الأيقونة", value=p.get("icon", "📦"))
                    e_unit = st.text_input("الوحدة", value=p.get("unit", "قطعة"))
                    e_badges = st.multiselect(
                        "شارات",
                        ["new", "sale", "popular", "premium", "recommended", "vet"],
                        default=p.get("badges", [])
                    )
                e_desc = st.text_area("الوصف", value=p.get("desc", ""), height=70)
                e_feat = st.text_area("المميزات", value="\n".join(p.get("features", [])), height=70)

                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.form_submit_button("حفظ التعديل", type="primary", use_container_width=True):
                        old_cat = p["category"]
                        st.session_state.products[old_cat] = [
                            x for x in st.session_state.products[old_cat]
                            if int(x["id"]) != int(p["id"])
                        ]
                        new_item = {
                            "id": int(p["id"]),
                            "name": e_name,
                            "desc": e_desc,
                            "price": int(e_price),
                            "icon": e_icon,
                            "stock": int(e_stock),
                            "unit": e_unit,
                            "brand": e_brand,
                            "country": p.get("country", "مصر"),
                            "badges": e_badges,
                            "features": [f.strip() for f in e_feat.split("\n") if f.strip()] or [e_desc],
                        }
                        st.session_state.products[e_cat].append(new_item)
                        save_products(st.session_state.products)
                        st.success("تم الحفظ")
                        st.rerun()

                with bc2:
                    if st.form_submit_button("حذف المنتج", use_container_width=True):
                        old_cat = p["category"]
                        st.session_state.products[old_cat] = [
                            x for x in st.session_state.products[old_cat]
                            if int(x["id"]) != int(p["id"])
                        ]
                        save_products(st.session_state.products)
                        st.success("تم الحذف")
                        st.rerun()
        else:
            st.info("لا توجد منتجات")

    with t4:
        st.markdown('<div class="section-title">إدارة الأقسام</div>', unsafe_allow_html=True)

        for cat in list(st.session_state.products.keys()):
            c1, c2 = st.columns([4, 1])
            c1.write(f"📁 {cat} ({len(st.session_state.products[cat])})")
            if c2.button("حذف", key=f"d_{cat}"):
                if not st.session_state.products[cat]:
                    del st.session_state.products[cat]
                    save_products(st.session_state.products)
                    st.rerun()
                else:
                    st.error("القسم ليس فارغاً")

        nc1, nc2 = st.columns([3, 1])
        new_cat = nc1.text_input("قسم جديد")
        if nc2.button("إضافة", type="primary"):
            if new_cat and new_cat not in st.session_state.products:
                st.session_state.products[new_cat] = []
                save_products(st.session_state.products)
                st.rerun()
            else:
                st.error("اسم القسم فارغ أو موجود بالفعل")

    with t5:
        st.markdown('<div class="section-title">النسخ الاحتياطي</div>', unsafe_allow_html=True)

        st.download_button(
            "تحميل النسخة",
            json.dumps(st.session_state.products, ensure_ascii=False, indent=2),
            file_name="vetfamily_care_backup.json",
            mime="application/json",
            use_container_width=True
        )

        up = st.file_uploader("استعادة", type=["json"])
        if up:
            try:
                data = json.load(up)
                if st.button("تطبيق الاستعادة", type="primary", use_container_width=True):
                    st.session_state.products = data
                    save_products(data)
                    st.success("تمت الاستعادة")
                    st.rerun()
            except:
                st.error("ملف غير صالح")

        if st.button("البيانات الافتراضية", use_container_width=True):
            st.session_state.products = copy.deepcopy(DEFAULT_PRODUCTS)
            save_products(st.session_state.products)
            st.rerun()

# =============================================
# الفوتر
# =============================================
st.markdown(f"""
<div class="footer">
    <h3>🐾 Vet Family Care</h3>
    <p>📍 {LOCATION} | 📞 {PHONE} | 🟢 أطلب المنتج عبر الوتساب</p>
</div>
""", unsafe_allow_html=True)
