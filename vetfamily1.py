import streamlit as st
from datetime import datetime, timedelta
import pytz
import hashlib
import urllib.parse

st.set_page_config(
    page_title="المركز للرعاية البيطرية المتكاملة - VetFamily Alexandria",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

CAIRO_TZ = pytz.timezone('Africa/Cairo')

def get_cairo_time():
    return datetime.now(CAIRO_TZ)

st.markdown("""
<style>
    .block-container {
        max-width: 100% !important;
        padding: 1rem 2rem !important;
        direction: rtl !important;
    }
    [data-testid="stAppViewContainer"], .main, .stMarkdown {
        text-align: right !important;
        direction: rtl !important;
    }
    h1, h2, h3, p, span, div {
        font-weight: 900 !important;
    }
    .main-header {
        text-align: center !important;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        width: 100%;
    }
    .main-header h1 {
        font-size: clamp(2rem, 5vw, 3.5rem) !important;
        color: white !important;
        text-align: center !important;
    }

    /* ========== بطاقة المنتج ========== */
    .product-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        direction: rtl;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    .product-name {
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        color: #1e3c72 !important;
        margin: 15px 0 10px 0 !important;
        line-height: 1.4 !important;
        text-align: center !important;
    }
    .product-description {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #718096 !important;
        margin: 8px 0 !important;
        line-height: 1.6 !important;
        text-align: center !important;
    }
    .product-price {
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        color: #28a745 !important;
        margin: 12px 0 !important;
        text-align: center !important;
    }
    .product-image {
        font-size: 4rem !important;
        text-align: center !important;
        margin: 10px 0 !important;
    }
    .product-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        margin: 3px;
        color: white;
    }
    .badge-new     { background: linear-gradient(135deg, #11998e, #38ef7d); }
    .badge-sale    { background: linear-gradient(135deg, #ff416c, #ff4b2b); }
    .badge-popular { background: linear-gradient(135deg, #667eea, #764ba2); }

    .stock-badge { text-align:center; padding:6px 12px; border-radius:10px; font-size:0.85rem; font-weight:700; margin-top:10px; }
    .in-stock    { background:#d4edda; color:#155724; }
    .low-stock   { background:#fff3cd; color:#856404; }
    .out-stock   { background:#f8d7da; color:#721c24; }

    /* ========== نافذة تأكيد الإضافة ========== */
    .cart-confirm-box {
        background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
        border: 3px solid #28a745;
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        text-align: center;
        direction: rtl;
        box-shadow: 0 10px 40px rgba(40,167,69,0.2);
        animation: slideIn 0.3s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .cart-confirm-title {
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        color: #155724 !important;
        margin-bottom: 8px !important;
    }
    .cart-confirm-product {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #1e3c72 !important;
        background: #e8f5e9;
        padding: 10px 20px;
        border-radius: 10px;
        margin: 10px auto !important;
        display: inline-block;
    }
    .cart-confirm-subtitle {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #555 !important;
        margin: 15px 0 !important;
    }

    /* ========== بطاقة العروض ========== */
    .item-box {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        direction: rtl;
        text-align: right;
    }
    .item-title {
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        color: #1e3c72 !important;
        margin-bottom: 10px !important;
    }
    .item-desc {
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #718096 !important;
        margin-bottom: 12px !important;
    }
    .item-price {
        font-size: 1.5rem !important;
        font-weight: 900 !important;
    }

    .offers-title {
        font-size: 2rem !important;
        font-weight: 900 !important;
        color: #ff4b4b !important;
        text-align: center !important;
        margin: 20px 0 !important;
        padding: 15px;
        background: #fff5f5;
        border-radius: 15px;
        border: 2px dashed #ff4b4b;
    }
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 30px 0;
        border-radius: 10px;
    }
    .cart-total {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 900;
        margin: 20px 0;
    }
    .success-message {
        background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# بيانات التواصل
# =============================================
WHATSAPP_NUMBER = "201022395878"
FACEBOOK_URL   = "https://www.facebook.com/share/p/1Dgba12hfT/"

# =============================================
# دالة عرض عناصر العروض
# =============================================
def render_item(name, price, desc, is_medical=False):
    accent_color = "#d9534f" if is_medical else "#28a745"
    box_class    = "item-box medical-box" if is_medical else "item-box"
    msg     = urllib.parse.quote(f"مرحباً VetFamily، أود طلب: {name}")
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={msg}"

    st.markdown(f'''
    <div class="{box_class}" style="border-right: 10px solid {accent_color};">
        <div class="item-title">{name}</div>
        <div class="item-desc">{desc}</div>
        <div class="item-price" style="color:{accent_color};">السعر: {price}</div>
    </div>
    ''', unsafe_allow_html=True)
    st.link_button(f"طلب {name} عبر واتساب 💬", wa_link)

# =============================================
# Session State
# =============================================
def hash_password(p):
    return hashlib.sha256(p.encode('utf-8')).hexdigest()

ADMIN_USERNAME    = "melabed"
ADMIN_PASSWORD_HASH = hash_password("Ma3902242$")

def check_login(u, p):
    return u == ADMIN_USERNAME and hash_password(p) == ADMIN_PASSWORD_HASH

defaults = {
    'is_logged_in': False,
    'show_adoption_form': False,
    'shopping_cart': [],
    'adoption_requests': [],
    'product_orders': [],
    'subscriptions': [],
    'notifications': [],
    # ===== متغيرات نافذة التأكيد =====
    'show_cart_confirm': False,   # هل تظهر النافذة؟
    'last_added_product': None,   # آخر منتج أُضيف
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if 'products' not in st.session_state:
    st.session_state.products = {
        "طعام_القطط_الجاف": [
            {
                "id": 1,
                "name": "رويال كانين - قطط بالغة 2 كجم",
                "description": "طعام متوازن للقطط البالغة من 1-7 سنوات، يحتوي على جميع العناصر الغذائية الأساسية",
                "price": 450, "cost": 320, "icon": "🐱",
                "category": "طعام القطط الجاف", "stock": 25,
                "unit": "كيس 2 كجم", "brand": "Royal Canin", "country": "فرنسا",
                "features": ["بروتين 32%", "دهون 15%", "فيتامينات متكاملة", "أوميجا 3 و 6", "مناسب للفراء اللامع"],
                "badges": ["popular", "premium"],
            },
            {
                "id": 2,
                "name": "رويال كانين كيتن - قطط صغيرة 1.5 كجم",
                "description": "تركيبة خاصة للقطط الصغيرة من شهرين إلى 12 شهر، تدعم النمو الصحي",
                "price": 400, "cost": 280, "icon": "🐈",
                "category": "طعام القطط الجاف", "stock": 18,
                "unit": "كيس 1.5 كجم", "brand": "Royal Canin", "country": "فرنسا",
                "features": ["سهل الهضم", "دعم جهاز المناعة", "تقوية العظام", "طاقة عالية", "قطع صغيرة الحجم"],
                "badges": ["new", "recommended"],
            },
            {
                "id": 3,
                "name": "بريميوم كات - قطط 1 كجم (محلي)",
                "description": "طعام محلي عالي الجودة بسعر اقتصادي",
                "price": 70, "cost": 45, "icon": "🐱",
                "category": "طعام القطط الجاف", "stock": 40,
                "unit": "كيس 1 كجم", "brand": "Premium Cat", "country": "مصر",
                "features": ["جودة جيدة", "سعر مناسب", "بروتين 28%", "فيتامينات"],
                "badges": ["sale"],
            }
        ],
        "طعام_القطط_الرطب": [
            {
                "id": 5,
                "name": "ويسكاس - تونة في جيلي 85 جم",
                "description": "وجبة رطبة لذيذة من التونة الطبيعية",
                "price": 25, "cost": 15, "icon": "🐟",
                "category": "طعام القطط الرطب", "stock": 100,
                "unit": "علبة 85 جم", "brand": "Whiskas", "country": "تايلاند",
                "features": ["تونة طبيعية 100%", "غني بالبروتين", "رطوبة عالية", "بدون ألوان صناعية"],
                "badges": ["popular"],
            },
            {
                "id": 6,
                "name": "شيبا - دجاج مشوي 85 جم",
                "description": "وجبة فاخرة من الدجاج المشوي",
                "price": 30, "cost": 20, "icon": "🍗",
                "category": "طعام القطط الرطب", "stock": 80,
                "unit": "علبة 85 جم", "brand": "Sheba", "country": "تايلاند",
                "features": ["دجاج مشوي", "طعم لذيذ", "قطع كبيرة", "صوص شهي"],
                "badges": ["premium"],
            }
        ],
        "طعام_الكلاب_الجاف": [
            {
                "id": 8,
                "name": "رويال كانين - كلاب كبيرة 3 كجم",
                "description": "تركيبة متطورة للكلاب الكبيرة النشطة فوق 25 كجم",
                "price": 550, "cost": 380, "icon": "🐕",
                "category": "طعام الكلاب الجاف", "stock": 20,
                "unit": "كيس 3 كجم", "brand": "Royal Canin", "country": "فرنسا",
                "features": ["دعم المفاصل", "طاقة عالية", "بروتين 30%", "جلوكوزامين", "كوندرويتين"],
                "badges": ["popular", "premium"],
            },
            {
                "id": 9,
                "name": "بيديجري - كلاب بالغة 2.5 كجم",
                "description": "طعام متوازن للكلاب البالغة من جميع الأحجام",
                "price": 320, "cost": 220, "icon": "🐕",
                "category": "طعام الكلاب الجاف", "stock": 30,
                "unit": "كيس 2.5 كجم", "brand": "Pedigree", "country": "تايلاند",
                "features": ["فيتامينات متكاملة", "دجاج حقيقي", "سهل الهضم", "أسنان صحية"],
                "badges": ["sale"],
            }
        ],
        "الرمل_والنظافة": [
            {
                "id": 11,
                "name": "كات ساند - رمل متكتل 5 كجم",
                "description": "رمل بنتونايت متكتل سريع الامتصاص برائحة اللافندر",
                "price": 90, "cost": 55, "icon": "🏖️",
                "category": "الرمل والنظافة", "stock": 50,
                "unit": "كيس 5 كجم", "brand": "Cat Sand", "country": "مصر",
                "features": ["سريع التكتل", "امتصاص فائق", "معطر", "اقتصادي", "قليل الغبار"],
                "badges": ["popular", "sale"],
            },
            {
                "id": 13,
                "name": "صندوق رمل قطط مع غطاء",
                "description": "صندوق رمل بلاستيك عالي الجودة مع غطاء ومجرفة",
                "price": 150, "cost": 90, "icon": "🚽",
                "category": "الرمل والنظافة", "stock": 15,
                "unit": "قطعة", "brand": "Pet Home", "country": "الصين",
                "features": ["سهل التنظيف", "مع مجرفة", "غطاء مانع للروائح", "قاعدة مانعة للانزلاق"],
                "badges": ["new"],
            }
        ],
        "الصحة_والأدوية": [
            {
                "id": 14,
                "name": "شامبو بيتكين الطبي 500 مل",
                "description": "شامبو طبي مضاد للحساسية والبراغيث",
                "price": 130, "cost": 70, "icon": "🧴",
                "category": "الصحة والأدوية", "stock": 30,
                "unit": "زجاجة 500 مل", "brand": "Petkin", "country": "مصر",
                "features": ["مضاد حساسية", "مضاد براغيث", "رائحة منعشة", "آمن تماماً", "للقطط والكلاب"],
                "badges": ["vet-recommended"],
            },
            {
                "id": 15,
                "name": "فرونت لاين - قطرات ضد البراغيث",
                "description": "أقوى علاج للبراغيث والقراد للقطط والكلاب",
                "price": 150, "cost": 85, "icon": "💧",
                "category": "الصحة والأدوية", "stock": 20,
                "unit": "أمبول واحد", "brand": "Frontline", "country": "فرنسا",
                "features": ["حماية شهرية", "فعال 100%", "سهل الاستخدام", "آمن للحيوانات"],
                "badges": ["premium", "vet-recommended"],
            },
            {
                "id": 18,
                "name": "قطرة عين فيتامين A",
                "description": "قطرة مطهرة ومعالجة لالتهابات العين",
                "price": 85, "cost": 45, "icon": "👁️",
                "category": "الصحة والأدوية", "stock": 18,
                "unit": "زجاجة 15 مل", "brand": "Pet Vision", "country": "مصر",
                "features": ["مطهرة", "آمنة", "سريعة المفعول", "بدون آثار جانبية"],
                "badges": ["vet-recommended"],
            }
        ],
        "الإكسسوارات": [
            {
                "id": 19,
                "name": "طوق جلد طبيعي مع جرس",
                "description": "طوق جلد أصلي عالي الجودة قابل للتعديل",
                "price": 80, "cost": 35, "icon": "🎀",
                "category": "الإكسسوارات", "stock": 35,
                "unit": "قطعة", "brand": "Pet Style", "country": "تركيا",
                "features": ["جلد طبيعي", "قابل للتعديل", "جرس معدني", "متين", "ألوان متعددة"],
                "badges": ["popular"],
            },
            {
                "id": 20,
                "name": "سلسلة مشي نايلون قوية",
                "description": "سلسلة مشي متينة للكلاب المتوسطة والكبيرة",
                "price": 90, "cost": 40, "icon": "🦮",
                "category": "الإكسسوارات", "stock": 25,
                "unit": "قطعة 1.5 متر", "brand": "Strong Lead", "country": "الصين",
                "features": ["نايلون قوي", "مقبض مريح", "حلقة معدنية", "طول 1.5 م"],
                "badges": ["sale"],
            },
            {
                "id": 21,
                "name": "حقيبة نقل فاخرة",
                "description": "حقيبة نقل آمنة ومريحة للسفر والعيادات",
                "price": 350, "cost": 200, "icon": "🎒",
                "category": "الإكسسوارات", "stock": 10,
                "unit": "حقيبة مقاس متوسط", "brand": "Travel Pet", "country": "الصين",
                "features": ["تهوية ممتازة", "خفيفة الوزن", "سهلة الحمل", "آمنة", "قابلة للطي"],
                "badges": ["premium"],
            }
        ],
        "الألعاب": [
            {
                "id": 23,
                "name": "فأر إلكتروني تفاعلي",
                "description": "لعبة إلكترونية تتحرك تلقائياً لتسلية القطط",
                "price": 120, "cost": 60, "icon": "🐭",
                "category": "الألعاب", "stock": 20,
                "unit": "قطعة", "brand": "Smart Toy", "country": "الصين",
                "features": ["حركة تلقائية", "آمنة", "بطاريات قابلة للشحن", "متينة"],
                "badges": ["new", "popular"],
            },
            {
                "id": 24,
                "name": "كرة مطاطية بجرس",
                "description": "كرة ملونة بجرس داخلي لتسلية القطط",
                "price": 25, "cost": 12, "icon": "⚽",
                "category": "الألعاب", "stock": 50,
                "unit": "قطعة", "brand": "Play Ball", "country": "مصر",
                "features": ["مطاط آمن", "جرس داخلي", "ألوان زاهية", "سهلة الحمل"],
                "badges": ["sale"],
            }
        ],
        "أطباق_ومعدات_التغذية": [
            {
                "id": 27,
                "name": "طقم أطباق ستانلس ستيل",
                "description": "طقم طبقين للطعام والماء من الستانلس ستيل",
                "price": 65, "cost": 30, "icon": "🥘",
                "category": "أطباق ومعدات التغذية", "stock": 25,
                "unit": "طقم قطعتين", "brand": "Steel Bowl", "country": "الصين",
                "features": ["ستانلس ستيل", "سهل التنظيف", "مانع للانزلاق", "متين"],
                "badges": ["popular"],
            },
            {
                "id": 28,
                "name": "نافورة مياه أوتوماتيك",
                "description": "نافورة مياه كهربائية تشجع على الشرب",
                "price": 280, "cost": 160, "icon": "⛲",
                "category": "أطباق ومعدات التغذية", "stock": 12,
                "unit": "قطعة 2 لتر", "brand": "Water Fountain", "country": "الصين",
                "features": ["فلتر كربوني", "هادئة", "سعة 2 لتر", "سهلة التنظيف"],
                "badges": ["premium", "new"],
            }
        ],
        "العناية_والتجميل": [
            {
                "id": 30,
                "name": "فرشاة تمشيط احترافية",
                "description": "فرشاة مزدوجة لفك التشابك وتلميع الفراء",
                "price": 50, "cost": 22, "icon": "🪮",
                "category": "العناية والتجميل", "stock": 20,
                "unit": "قطعة", "brand": "Grooming Pro", "country": "الصين",
                "features": ["أسنان ناعمة", "مقبض مريح", "للفراء الطويل والقصير", "مضادة للكهرباء الساكنة"],
                "badges": ["recommended"],
            },
            {
                "id": 31,
                "name": "مقص أظافر احترافي",
                "description": "مقص أظافر آمن بحماية من القص الزائد",
                "price": 75, "cost": 35, "icon": "✂️",
                "category": "العناية والتجميل", "stock": 15,
                "unit": "قطعة", "brand": "Nail Clipper", "country": "ألمانيا",
                "features": ["شفرة حادة", "واقي أمان", "مقبض مطاطي", "للقطط والكلاب"],
                "badges": ["premium"],
            },
            {
                "id": 32,
                "name": "مناديل تنظيف معطرة",
                "description": "مناديل مبللة معطرة للتنظيف السريع",
                "price": 45, "cost": 22, "icon": "🧻",
                "category": "العناية والتجميل", "stock": 35,
                "unit": "علبة 80 منديل", "brand": "Fresh Wipes", "country": "مصر",
                "features": ["آمنة 100%", "معطرة", "مضادة للبكتيريا", "للاستخدام اليومي"],
                "badges": ["popular"],
            }
        ],
        "الفيتامينات_والمكملات": [
            {
                "id": 34,
                "name": "مالتي فيتامين للقطط",
                "description": "فيتامينات متعددة لصحة أفضل",
                "price": 160, "cost": 90, "icon": "💊",
                "category": "الفيتامينات والمكملات", "stock": 15,
                "unit": "علبة 60 قرص", "brand": "Pet Vitamin", "country": "أمريكا",
                "features": ["فيتامينات متكاملة", "تقوية المناعة", "طعم سمك", "سهلة البلع"],
                "badges": ["vet-recommended"],
            }
        ]
    }

if 'packages' not in st.session_state:
    st.session_state.packages = {
        "الباقة البرونزية": {
            "price": 200, "duration": "شهرياً",
            "description": "باقة أساسية للرعاية الشهرية",
            "icon": "🥉", "color": "#CD7F32",
            "features": ["استشارتان هاتفيتان شهرياً", "استشارة واتساب مفتوحة",
                         "خصم 10% على الأدوية والمستلزمات", "متابعة الحالة الصحية", "نصائح غذائية مجانية"]
        },
        "الباقة الفضية": {
            "price": 400, "duration": "شهرياً",
            "description": "رعاية متقدمة مع فحوصات دورية",
            "icon": "🥈", "color": "#C0C0C0",
            "features": ["4 استشارات (عيادة أو هاتف)", "فحص شامل مجاني",
                         "خصم 20% على جميع المنتجات", "أولوية في الحجز",
                         "متابعة دورية أسبوعية", "استشارة تغذية متخصصة"]
        },
        "الباقة الذهبية": {
            "price": 700, "duration": "شهرياً",
            "description": "رعاية VIP شاملة ومتكاملة",
            "icon": "🥇", "color": "#FFD700",
            "features": ["استشارات غير محدودة", "زيارة منزلية مجانية",
                         "فحص شامل شهري", "جميع التطعيمات الأساسية",
                         "خصم 30% على المنتجات", "خط ساخن طوارئ 24/7",
                         "أولوية قصوى في جميع الخدمات", "ملف طبي إلكتروني"]
        },
        "الباقة الماسية": {
            "price": 1200, "duration": "شهرياً",
            "description": "الباقة الأشمل - رعاية ملكية",
            "icon": "💎", "color": "#B9F2FF",
            "features": ["كل مميزات الباقة الذهبية", "زيارتان منزليتان شهرياً",
                         "تحاليل مجانية (شاملة)", "عمليات صغرى بسعر التكلفة",
                         "رعاية كاملة أثناء السفر", "شريحة تتبع GPS مجانية",
                         "توصيل المنتجات متاح برسوم", "جلسة تجميل شهرية",
                         "مدرب سلوك (استشارة)", "خصم 40% على كل شيء"]
        }
    }

# =============================================
# دوال السلة
# =============================================
def add_to_cart(product):
    for item in st.session_state.shopping_cart:
        if item['id'] == product['id']:
            if item['quantity'] < product['stock']:
                item['quantity'] += 1
                return True
            return False
    cart_item = product.copy()
    cart_item['quantity'] = 1
    st.session_state.shopping_cart.append(cart_item)
    return True

def remove_from_cart(product_id):
    st.session_state.shopping_cart = [
        i for i in st.session_state.shopping_cart if i['id'] != product_id
    ]

def update_cart_quantity(product_id, new_quantity):
    for item in st.session_state.shopping_cart:
        if item['id'] == product_id:
            if new_quantity <= 0:
                remove_from_cart(product_id)
            else:
                item['quantity'] = new_quantity
            break

def get_cart_total():
    return sum(i['price'] * i['quantity'] for i in st.session_state.shopping_cart)

def get_cart_count():
    return sum(i['quantity'] for i in st.session_state.shopping_cart)

def build_whatsapp_cart_message():
    """بناء رسالة واتساب تحتوي على كل محتويات السلة"""
    lines = ["مرحباً VetFamily 🐾، أود طلب المنتجات التالية:\n"]
    for item in st.session_state.shopping_cart:
        lines.append(f"• {item['name']} - الكمية: {item['quantity']} - السعر: {item['price'] * item['quantity']} ج.م")
    lines.append(f"\n💰 الإجمالي: {get_cart_total():,} ج.م")
    lines.append("برجاء التواصل لتأكيد الطلب 🙏")
    return urllib.parse.quote("\n".join(lines))

def save_product_order(cart_items, customer_info):
    try:
        cairo_time = get_cairo_time()
        total_price = get_cart_total()
        order = {
            "id": len(st.session_state.product_orders) + 1,
            "items": [{"name": i['name'], "quantity": i['quantity'],
                       "price": i['price'], "total": i['price'] * i['quantity']}
                      for i in cart_items],
            "total_price": total_price,
            "customer_name": customer_info["name"],
            "customer_phone": customer_info["phone"],
            "customer_address": customer_info.get("address", ""),
            "notes": customer_info.get("notes", ""),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "time": cairo_time.strftime("%H:%M:%S"),
            "status": "جديد - في انتظار التواصل"
        }
        st.session_state.product_orders.append(order)
        st.session_state.notifications.insert(0, {
            "type": "product_order",
            "message": f"طلب منتجات جديد من {customer_info['name']}",
            "details": f"إجمالي: {total_price} ج.م - عدد المنتجات: {len(cart_items)}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "order": order
        })
        st.session_state.shopping_cart = []
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الطلب: {e}")
        return False

def save_subscription(package_name, package_data, customer_info):
    try:
        cairo_time = get_cairo_time()
        sub = {
            "id": len(st.session_state.subscriptions) + 1,
            "package_name": package_name,
            "price": package_data['price'],
            "duration": package_data['duration'],
            "customer_name": customer_info["name"],
            "customer_phone": customer_info["phone"],
            "customer_address": customer_info.get("address", ""),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "time": cairo_time.strftime("%H:%M:%S"),
            "status": "جديد - في انتظار التواصل",
            "start_date": cairo_time.strftime("%Y-%m-%d"),
            "end_date": (cairo_time + timedelta(days=30)).strftime("%Y-%m-%d")
        }
        st.session_state.subscriptions.append(sub)
        st.session_state.notifications.insert(0, {
            "type": "subscription",
            "message": f"اشتراك جديد في {package_name}",
            "details": f"{customer_info['name']} - {package_data['price']} ج.م/{package_data['duration']}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "subscription": sub
        })
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الاشتراك: {e}")
        return False

def save_adoption_request(adoption_info):
    try:
        cairo_time = get_cairo_time()
        req = {
            "id": len(st.session_state.adoption_requests) + 1,
            "customer_name": adoption_info["name"],
            "customer_phone": adoption_info["phone"],
            "customer_address": adoption_info.get("address", ""),
            "pet_type": adoption_info["pet_type"],
            "pet_age": adoption_info.get("pet_age", ""),
            "experience": adoption_info.get("experience", ""),
            "home_type": adoption_info.get("home_type", ""),
            "notes": adoption_info.get("notes", ""),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "time": cairo_time.strftime("%H:%M:%S"),
            "status": "جديد - في انتظار التواصل"
        }
        st.session_state.adoption_requests.append(req)
        st.session_state.notifications.insert(0, {
            "type": "adoption",
            "message": f"طلب تبني جديد - {adoption_info['pet_type']}",
            "details": f"{adoption_info['name']} - {adoption_info['phone']}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "request": req
        })
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ طلب التبني: {e}")
        return False

def get_badge_html(badges):
    badge_map = {
        "new": ("جديد", "badge-new"),
        "sale": ("عرض", "badge-sale"),
        "popular": ("الأكثر مبيعاً", "badge-popular"),
        "premium": ("بريميوم", "badge-popular"),
        "recommended": ("موصى به", "badge-new"),
        "vet-recommended": ("موصى به من الأطباء", "badge-sale")
    }
    html = ""
    for b in badges:
        if b in badge_map:
            text, cls = badge_map[b]
            html += f'<span class="product-badge {cls}">{text}</span>'
    return html

# =============================================
# نافذة تأكيد الإضافة للسلة  ← الجديد
# =============================================
def show_cart_confirm_dialog(product):
    """تعرض نافذة منبثقة بعد إضافة المنتج للسلة مع 3 خيارات"""

    msg_single  = urllib.parse.quote(
        f"مرحباً VetFamily 🐾، أود طلب: {product['name']}\n"
        f"السعر: {product['price']} ج.م\nبرجاء التواصل لتأكيد الطلب 🙏"
    )
    wa_single = f"https://wa.me/{WHATSAPP_NUMBER}?text={msg_single}"
    wa_cart   = f"https://wa.me/{WHATSAPP_NUMBER}?text={build_whatsapp_cart_message()}"

    st.markdown(f"""
    <div class="cart-confirm-box">
        <div class="cart-confirm-title">✅ تمت الإضافة للسلة بنجاح!</div>
        <div class="cart-confirm-product">{product['icon']} {product['name']}</div>
        <div class="cart-confirm-subtitle">💰 السعر: {product['price']} ج.م &nbsp;|&nbsp; 🛒 إجمالي السلة: {get_cart_total():,} ج.م</div>
        <div class="cart-confirm-subtitle">ماذا تريد أن تفعل الآن؟</div>
    </div>
    """, unsafe_allow_html=True)

    # ثلاثة أزرار جنباً إلى جنب
    c1, c2, c3 = st.columns(3)

    with c1:
        # زر إغلاق النافذة والاستمرار في التسوق
        if st.button("🛍️ استكمال التسوق", use_container_width=True, key="confirm_continue"):
            st.session_state.show_cart_confirm = False
            st.session_state.last_added_product = None
            st.rerun()

    with c2:
        # رابط واتساب لطلب هذا المنتج فقط
        st.link_button(
            "📱 طلب هذا المنتج عبر واتساب",
            wa_single,
            use_container_width=True
        )

    with c3:
        # رابط واتساب بكل محتويات السلة
        st.link_button(
            f"🛒 إرسال السلة كاملة ({get_cart_count()} منتج)",
            wa_cart,
            use_container_width=True
        )

    # زر إتمام الطلب الرسمي
    if st.button("✅ إتمام الطلب والدفع", use_container_width=True,
                 type="primary", key="confirm_checkout"):
        st.session_state.show_cart_confirm = False
        st.session_state.last_added_product = None
        st.rerun()

# =============================================
# بطاقة عرض المنتج  ← معدّلة
# =============================================
def display_product_card(product):
    if product['stock'] > 10:
        stock_class, stock_text = "in-stock",  f"✅ متوفر ({product['stock']} قطعة)"
    elif product['stock'] > 0:
        stock_class, stock_text = "low-stock", f"⚠️ كمية محدودة ({product['stock']} قطعة)"
    else:
        stock_class, stock_text = "out-stock", "❌ نفذ من المخزون"

    badges_html = get_badge_html(product.get('badges', []))

    st.markdown(f"""
    <div class='product-card'>
        <div class='product-image'>{product['icon']}</div>
        <div class='product-name'>{product['name']}</div>
        <div>{badges_html}</div>
        <div class='product-description'>{product['description']}</div>
        <div class='product-price'>{product['price']} ج.م</div>
        <div style='text-align:center;color:#718096;font-size:0.85rem;font-weight:500;'>
            📦 {product['unit']} | 🏷️ {product['brand']}
        </div>
        <div class='stock-badge {stock_class}'>{stock_text}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 المميزات والتفاصيل"):
        for f in product['features']:
            st.write(f"✓ {f}")
        st.write(f"**🌍 بلد المنشأ:** {product['country']}")

    col1, col2 = st.columns([3, 1])
    with col1:
        if product['stock'] > 0:
            if st.button("🛒 أضف للسلة", key=f"add_{product['id']}", use_container_width=True):
                if add_to_cart(product):
                    # ✅ تفعيل نافذة التأكيد
                    st.session_state.show_cart_confirm  = True
                    st.session_state.last_added_product = product
                    st.rerun()
                else:
                    st.warning("⚠️ الكمية المتاحة في المخزون محدودة")
        else:
            st.button("نفذ من المخزون ❌", disabled=True, use_container_width=True)

    with col2:
        if st.session_state.is_logged_in:
            profit = product['price'] - product['cost']
            profit_pct = (profit / product['cost']) * 100
            st.caption(f"💰 {product['cost']} ج")
            st.caption(f"📈 +{profit_pct:.0f}%")

# =============================================
# العنوان الرئيسي
# =============================================
st.markdown("""
<div class='main-header'>
    <h1>🐾 VetFamily Alexandria 🐾</h1>
    <p>مركز الرعاية البيطرية المتكاملة - الإسكندرية</p>
    <p style='font-size:1rem;margin-top:10px;'>
        🩺 أطباء بيطريون متخصصون | 🍖 طعام بريميوم أصلي | 🚗 توصيل متاح
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================
# نافذة التأكيد (تظهر في أعلى الصفحة فور الإضافة)
# =============================================
if st.session_state.show_cart_confirm and st.session_state.last_added_product:
    show_cart_confirm_dialog(st.session_state.last_added_product)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =============================================
# أزرار الصفحة الرئيسية
# =============================================
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("❤️ أعجبني", use_container_width=True):
        st.balloons()
        st.success("شكراً لدعمك! 🙏")
with col2:
    cart_count = get_cart_count()
    cart_label = f"🛒 السلة ({cart_count})" if cart_count > 0 else "🛒 السلة"
    if st.button(cart_label, use_container_width=True):
        st.info("⬅️ افتح الشريط الجانبي لعرض السلة")
with col3:
    if st.button("🏠 تبني الآن", use_container_width=True):
        st.session_state.show_adoption_form = True
        st.info("⬇️ انتقل لأسفل الصفحة لملء نموذج التبني")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =============================================
# التبويبات
# =============================================
if st.session_state.is_logged_in:
    tabs = st.tabs(["🏪 المتجر","💎 الباقات الطبية","🩺 الاستشارات",
                    "📊 لوحة التحكم","📦 طلبات المنتجات","💳 الاشتراكات","🏠 طلبات التبني"])
    tab_shop, tab_packages, tab_consult, tab_dashboard, tab_orders, tab_subs, tab_adopt = tabs
else:
    tabs = st.tabs(["🏪 المتجر","💎 الباقات الطبية","🩺 الاستشارات","ℹ️ من نحن"])
    tab_shop, tab_packages, tab_consult, tab_about = tabs

# =============================================
# تبويب المتجر
# =============================================
with tab_shop:
    st.write("## 🛒 متجر المستلزمات البيطرية")
    st.write("### أفضل المنتجات البيطرية بأسعار منافسة 🎯")

    # عروض اليوم
    st.markdown('<div class="offers-title">🔥 عروض اليوم الحصرية</div>', unsafe_allow_html=True)
    daily_offers = [
        {"name": "📦 رويال كانين قطط - 2 كجم", "price": "550 ج.م بدلاً من 650", "desc": "عرض خاص لدعم صحة أليفك."},
        {"name": "🐱 رمل قطط كربون - 5 لتر",   "price": "180 ج.م بدلاً من 220", "desc": "أفضل حماية من الروائح."},
    ]
    offer_cols = st.columns(len(daily_offers))
    for i, offer in enumerate(daily_offers):
        with offer_cols[i]:
            render_item(offer['name'], offer['price'], offer['desc'])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # بحث وفلترة
    col_search, col_category, col_sort = st.columns([2, 2, 1])
    with col_search:
        search_term = st.text_input("🔍 ابحث عن منتج:", placeholder="اكتب اسم المنتج أو العلامة التجارية...")
    with col_category:
        all_categories = ["الكل"] + list(st.session_state.products.keys())
        selected_category = st.selectbox("📂 اختر الفئة:", all_categories)
    with col_sort:
        sort_option = st.selectbox("ترتيب:", ["الأحدث", "السعر: الأقل", "السعر: الأعلى", "الأكثر مبيعاً"])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # عرض المنتجات
    for category_key, products in st.session_state.products.items():
        if selected_category != "الكل" and category_key != selected_category:
            continue
        category_name = products[0]['category'] if products else category_key
        st.markdown(f"### 📦 {category_name}")

        filtered_products = products
        if search_term:
            filtered_products = [
                p for p in products
                if search_term.lower() in p['name'].lower()
                or search_term.lower() in p['brand'].lower()
                or search_term.lower() in p['description'].lower()
            ]
        if not filtered_products:
            continue

        if sort_option == "السعر: الأقل":
            filtered_products = sorted(filtered_products, key=lambda x: x['price'])
        elif sort_option == "السعر: الأعلى":
            filtered_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)

        cols = st.columns(3)
        for idx, product in enumerate(filtered_products):
            with cols[idx % 3]:
                display_product_card(product)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =============================================
# تبويب الباقات
# =============================================
with tab_packages:
    st.write("## 💎 الباقات الطبية - اختر الأنسب لك")
    for package_name, package_data in st.session_state.packages.items():
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,{package_data['color']}22 0%,{package_data['color']}44 100%);
                    padding:30px;border-radius:20px;margin:20px 0;
                    border:3px solid {package_data['color']};box-shadow:0 10px 30px rgba(0,0,0,0.1);'>
            <h2 style='text-align:center;color:#2d3748;'>{package_data['icon']} {package_name}</h2>
            <p style='text-align:center;font-size:1.1rem;color:#4a5568;'>{package_data['description']}</p>
            <h1 style='text-align:center;color:{package_data['color']};margin:20px 0;'>
                {package_data['price']} ج.م / {package_data['duration']}
            </h1>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("### ✨ المميزات:")
            for feature in package_data['features']:
                st.write(f"✅ {feature}")
        with col2:
            st.write("### 📝 اشترك الآن")
            with st.form(f"package_form_{package_name}"):
                sub_name    = st.text_input("الاسم الكامل:",  key=f"sub_name_{package_name}")
                sub_phone   = st.text_input("رقم الواتساب:",  key=f"sub_phone_{package_name}")
                sub_address = st.text_input("العنوان:",        key=f"sub_address_{package_name}")
                if st.form_submit_button("🎯 اشترك الآن", use_container_width=True):
                    if sub_name and sub_phone:
                        if save_subscription(package_name, package_data,
                                             {"name": sub_name, "phone": sub_phone, "address": sub_address}):
                            st.markdown(f"<div class='success-message'>🎉 تم الاشتراك بنجاح في {package_name}!<br>سيتم التواصل معك قريباً 📞</div>",
                                        unsafe_allow_html=True)
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("⚠️ برجاء إدخال الاسم ورقم الهاتف")

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =============================================
# تبويب الاستشارات
# =============================================
with tab_consult:
    st.write("## 🩺 الاستشارات البيطرية")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:30px;border-radius:20px;color:white;'>
            <h3 style='color:white;'>👨‍⚕️ فريقنا الطبي</h3>
            <ul style='font-size:1.1rem;line-height:2;'>
                <li>أطباء بيطريون معتمدون</li>
                <li>خبرة واسعة في جميع التخصصات</li>
                <li>متابعة دورية ومستمرة</li>
                <li>استشارات على مدار الساعة</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);padding:30px;border-radius:20px;color:white;'>
            <h3 style='color:white;'>📋 خدماتنا</h3>
            <ul style='font-size:1.1rem;line-height:2;'>
                <li>الكشف والفحص الشامل</li>
                <li>التطعيمات والتحصينات</li>
                <li>العمليات الجراحية</li>
                <li>التحاليل الطبية</li>
                <li>الأشعة والتشخيص</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.write("### 💰 أسعار الخدمات")
    services = [
        {"name": "استشارة هاتفية",     "price": "مجاني",    "icon": "📞"},
        {"name": "استشارة في العيادة", "price": "100 ج.م",  "icon": "🏥"},
        {"name": "كشف + تطعيم",        "price": "150 ج.م",  "icon": "💉"},
        {"name": "زيارة منزلية",        "price": "250 ج.م",  "icon": "🏠"},
        {"name": "فحص شامل",           "price": "300 ج.م",  "icon": "🔬"},
        {"name": "عملية صغرى",         "price": "500 ج.م+", "icon": "⚕️"}
    ]
    cols = st.columns(3)
    for idx, service in enumerate(services):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style='background:white;padding:20px;border-radius:15px;text-align:center;border:2px solid #667eea;margin:10px 0;'>
                <div style='font-size:3rem;'>{service['icon']}</div>
                <h4 style='color:#2d3748;margin:10px 0;'>{service['name']}</h4>
                <h3 style='color:#667eea;'>{service['price']}</h3>
            </div>""", unsafe_allow_html=True)

# =============================================
# تبويبات المدير
# =============================================
if st.session_state.is_logged_in:
    with tab_dashboard:
        st.write("## 📊 لوحة التحكم الرئيسية")
        cairo_time = get_cairo_time()
        st.info(f"🕐 الوقت الحالي: {cairo_time.strftime('%Y-%m-%d %H:%M:%S')}")
        if st.button("🔓 تسجيل الخروج", use_container_width=True):
            st.session_state.is_logged_in = False
            st.rerun()
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("📦 طلبات المنتجات", len(st.session_state.product_orders))
        with col2: st.metric("💰 إيرادات المنتجات", f"{sum(o['total_price'] for o in st.session_state.product_orders):,} ج.م")
        with col3: st.metric("💳 الاشتراكات", len(st.session_state.subscriptions))
        with col4: st.metric("💰 إيرادات الباقات", f"{sum(s['price'] for s in st.session_state.subscriptions):,} ج.م")
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.write("### 🔔 الإشعارات الأخيرة")
        if st.session_state.notifications:
            for notif in st.session_state.notifications[:10]:
                bg = {"product_order": "#667eea", "subscription": "#f093fb", "adoption": "#38ef7d"}.get(notif['type'], "#764ba2")
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,{bg} 0%,{bg}dd 100%);
                            padding:20px;border-radius:15px;color:white;margin:10px 0;'>
                    <h4 style='margin:0;color:white;'>{notif['message']}</h4>
                    <p style='margin:10px 0 0 0;font-size:0.9rem;'>{notif['details']}<br>📅 {notif['date']} | ⏰ {notif['timestamp']}</p>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("لا توجد إشعارات جديدة")

    with tab_orders:
        st.write("## 📦 إدارة طلبات المنتجات")
        if st.session_state.product_orders:
            for order in reversed(st.session_state.product_orders):
                st.markdown(f"<div style='background:#f8f9fa;padding:20px;border-radius:15px;margin:15px 0;border-right:5px solid #667eea;'><h4>طلب #{order['id']} - {order['customer_name']}</h4></div>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**📞 الهاتف:** {order['customer_phone']}")
                    st.write(f"**📍 العنوان:** {order['customer_address']}")
                with col2:
                    st.write(f"**📅 التاريخ:** {order['date']}")
                    st.write(f"**⏰ الوقت:** {order['time']}")
                with col3:
                    st.write(f"**💰 الإجمالي:** {order['total_price']} ج.م")
                    st.write(f"**📦 عدد المنتجات:** {len(order['items'])}")
                for item in order['items']:
                    st.write(f"• {item['name']} × {item['quantity']} = {item['total']} ج.م")
                if order.get('notes'): st.write(f"**📝 ملاحظات:** {order['notes']}")
                col_s, col_b = st.columns([4, 1])
                with col_s:
                    opts = ["جديد - في انتظار التواصل", "تم التواصل", "قيد التجهيز", "جاهز للتوصيل", "تم التوصيل", "ملغي"]
                    new_s = st.selectbox("الحالة:", opts, index=opts.index(order['status']), key=f"status_order_{order['id']}")
                with col_b:
                    if st.button("💾 حفظ", key=f"save_order_{order['id']}"):
                        for o in st.session_state.product_orders:
                            if o['id'] == order['id']: o['status'] = new_s
                        st.success("✅ تم الحفظ"); st.rerun()
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد طلبات منتجات حتى الآن")

    with tab_subs:
        st.write("## 💳 إدارة الاشتراكات في الباقات")
        if st.session_state.subscriptions:
            for sub in reversed(st.session_state.subscriptions):
                st.markdown(f"<div style='background:linear-gradient(135deg,#f093fb22 0%,#f5576c22 100%);padding:20px;border-radius:15px;margin:15px 0;border:2px solid #f093fb;'><h4>{sub['package_name']} - {sub['customer_name']}</h4></div>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**📞 الهاتف:** {sub['customer_phone']}")
                    st.write(f"**💰 السعر:** {sub['price']} ج.م/{sub['duration']}")
                with col2:
                    st.write(f"**📅 تاريخ البدء:** {sub['start_date']}")
                    st.write(f"**📅 تاريخ الانتهاء:** {sub['end_date']}")
                col_s, col_b = st.columns([4, 1])
                with col_s:
                    opts = ["جديد - في انتظار التواصل", "نشط", "منتهي", "ملغي"]
                    new_s = st.selectbox("الحالة:", opts, index=opts.index(sub['status']) if sub['status'] in opts else 0, key=f"status_sub_{sub['id']}")
                with col_b:
                    if st.button("💾 حفظ", key=f"save_sub_{sub['id']}"):
                        for s in st.session_state.subscriptions:
                            if s['id'] == sub['id']: s['status'] = new_s
                        st.success("✅ تم الحفظ"); st.rerun()
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد اشتراكات حتى الآن")

    with tab_adopt:
        st.write("## 🏠 إدارة طلبات التبني")
        if st.session_state.adoption_requests:
            for req in reversed(st.session_state.adoption_requests):
                st.markdown(f"<div style='background:linear-gradient(135deg,#38ef7d22 0%,#11998e22 100%);padding:20px;border-radius:15px;margin:15px 0;border:2px solid #38ef7d;'><h4>طلب #{req['id']} - {req['customer_name']}</h4></div>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**📞 الهاتف:** {req['customer_phone']}")
                    st.write(f"**🐾 نوع الحيوان:** {req['pet_type']}")
                with col2:
                    st.write(f"**📅 التاريخ:** {req['date']}")
                    if req.get('pet_age'): st.write(f"**🎂 العمر المفضل:** {req['pet_age']}")
                if req.get('experience'): st.write(f"**📚 الخبرة:** {req['experience']}")
                if req.get('notes'):      st.write(f"**📝 ملاحظات:** {req['notes']}")
                col_s, col_b = st.columns([4, 1])
                with col_s:
                    opts = ["جديد - في انتظار التواصل", "تم التواصل", "تمت الموافقة", "تم التبني", "مرفوض"]
                    new_s = st.selectbox("الحالة:", opts, index=opts.index(req['status']) if req['status'] in opts else 0, key=f"status_adopt_{req['id']}")
                with col_b:
                    if st.button("💾 حفظ", key=f"save_adopt_{req['id']}"):
                        for r in st.session_state.adoption_requests:
                            if r['id'] == req['id']: r['status'] = new_s
                        st.success("✅ تم الحفظ"); st.rerun()
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد طلبات تبني حتى الآن")

else:
    with tab_about:
        st.write("## ℹ️ عن VetFamily Alexandria")
        st.markdown("""
        <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
                    padding:40px;border-radius:20px;color:white;text-align:center;'>
            <h2 style='color:white;margin-bottom:20px;'>🐾 نحن عائلتك البيطرية في الإسكندرية</h2>
            <p style='font-size:1.2rem;line-height:1.8;'>مركز متكامل يجمع بين الخبرة الطبية والاحترافية</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        for col, icon, title, desc in [
            (col1, "👨‍⚕️", "أطباء متخصصون", "فريق من الأطباء البيطريين ذوي الخبرة الواسعة"),
            (col2, "🏆", "منتجات أصلية",  "جميع منتجاتنا أصلية 100% من أفضل العلامات العالمية"),
            (col3, "🚗", "توصيل سريع",   "خدمة توصيل سريعة لجميع أنحاء الإسكندرية"),
        ]:
            with col:
                st.markdown(f"""
                <div style='text-align:center;padding:30px;background:white;border-radius:15px;box-shadow:0 5px 15px rgba(0,0,0,0.1);'>
                    <div style='font-size:4rem;'>{icon}</div>
                    <h3>{title}</h3><p>{desc}</p>
                </div>""", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.write("### 📞 تواصل معنا")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("- **📍 العنوان:** محرم بك - الإسكندرية\n- **📞 الهاتف:** 01xxxxxxxxx")
        with col2:
            st.markdown("- **🕐 مواعيد العمل:** يومياً من 9 ص - 9 م\n- **📧** info@vetfamily-alex.com")

# =============================================
# إتمام الطلب
# =============================================
if st.session_state.shopping_cart:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.write("## 🛒 إتمام طلبك")
    total = get_cart_total()
    st.markdown(f"<div class='cart-total'>💰 إجمالي الطلب: {total:,} ج.م</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: customer_name    = st.text_input("الاسم الكامل *",    key="checkout_name")
    with col2: customer_phone   = st.text_input("رقم الواتساب *",    key="checkout_phone")
    with col3: customer_address = st.text_input("عنوان التوصيل *",   key="checkout_address")
    customer_notes = st.text_area("ملاحظات إضافية (اختياري)", key="checkout_notes")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✅ تأكيد الطلب", use_container_width=True, type="primary"):
            if customer_name and customer_phone and customer_address:
                if save_product_order(st.session_state.shopping_cart,
                                      {"name": customer_name, "phone": customer_phone,
                                       "address": customer_address, "notes": customer_notes}):
                    st.markdown(f"<div class='success-message'>🎉 تم إرسال طلبك بنجاح!<br>💰 الإجمالي: {total:,} ج.م<br>📞 سيتم التواصل معك للتأكيد</div>",
                                unsafe_allow_html=True)
                    st.balloons(); st.rerun()
            else:
                st.error("⚠️ برجاء إدخال جميع البيانات المطلوبة")
    with col_btn2:
        if st.button("🗑️ تفريغ السلة", use_container_width=True):
            st.session_state.shopping_cart = []; st.rerun()

# =============================================
# نموذج التبني
# =============================================
if st.session_state.show_adoption_form:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:linear-gradient(135deg,#38ef7d 0%,#11998e 100%);
                padding:30px;border-radius:20px;text-align:center;color:white;'>
        <h2 style='color:white;'>🏠 نموذج طلب التبني 🐾</h2>
        <p style='font-size:1.1rem;'>ساعد حيوان أليف في إيجاد منزل دافئ</p>
    </div>""", unsafe_allow_html=True)

    with st.form("adoption_form"):
        col1, col2 = st.columns(2)
        with col1:
            adopt_name  = st.text_input("الاسم الكامل *")
            adopt_phone = st.text_input("رقم الواتساب *")
        with col2:
            adopt_address = st.text_input("العنوان الكامل *")
            adopt_home    = st.selectbox("نوع السكن:", ["شقة", "فيلا", "منزل مستقل", "آخر"])
        col1, col2 = st.columns(2)
        with col1: pet_type = st.selectbox("نوع الحيوان *:", ["قطة 🐱", "كلب 🐕", "طائر 🐦", "أرنب 🐰", "سلحفاة 🐢", "أخرى"])
        with col2: pet_age  = st.selectbox("العمر المفضل:", ["صغير (أقل من سنة)", "متوسط (1-3 سنوات)", "كبير (أكثر من 3 سنوات)", "لا يهم"])
        adopt_experience = st.radio("هل لديك خبرة سابقة؟", ["نعم، لدي خبرة", "لا، هذه أول مرة", "لدي خبرة بسيطة"])
        adopt_notes = st.text_area("ملاحظات أو متطلبات خاصة:")
        col1, col2 = st.columns(2)
        with col1: submitted = st.form_submit_button("📝 إرسال الطلب", use_container_width=True, type="primary")
        with col2: cancelled = st.form_submit_button("❌ إلغاء", use_container_width=True)
        if submitted:
            if adopt_name and adopt_phone and adopt_address:
                if save_adoption_request({"name": adopt_name, "phone": adopt_phone,
                                          "address": adopt_address, "home_type": adopt_home,
                                          "pet_type": pet_type, "pet_age": pet_age,
                                          "experience": adopt_experience, "notes": adopt_notes}):
                    st.markdown("<div class='success-message'>🎉 تم إرسال طلب التبني بنجاح! 🏠<br>سيتم التواصل معك قريباً 💚</div>",
                                unsafe_allow_html=True)
                    st.balloons()
                    st.session_state.show_adoption_form = False; st.rerun()
            else:
                st.error("⚠️ برجاء إدخال جميع البيانات المطلوبة")
        if cancelled:
            st.session_state.show_adoption_form = False; st.rerun()

# =============================================
# الشريط الجانبي
# =============================================
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:20px;'><h2 style='color:white;'>🐾 VetFamily</h2><p style='color:white;'>الإسكندرية</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("### 🛒 سلة التسوق")
    if st.session_state.shopping_cart:
        total_cart = 0
        for item in st.session_state.shopping_cart:
            st.write(f"**{item['name']}**")
            col1, col2 = st.columns([2, 1])
            with col1:
                new_qty = st.number_input("الكمية:", min_value=1, max_value=item['stock'],
                                          value=item['quantity'], key=f"cart_qty_{item['id']}",
                                          label_visibility="collapsed")
                if new_qty != item['quantity']:
                    update_cart_quantity(item['id'], new_qty); st.rerun()
            with col2:
                if st.button("🗑️", key=f"remove_{item['id']}"):
                    remove_from_cart(item['id']); st.rerun()
            item_total = item['price'] * item['quantity']
            total_cart += item_total
            st.write(f"{item['quantity']} × {item['price']} = {item_total} ج.م")
            st.markdown("---")
        st.markdown(f"<div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:15px;border-radius:10px;text-align:center;color:white;'><h3 style='margin:0;color:white;'>💰 الإجمالي</h3><h2 style='margin:10px 0 0 0;color:white;'>{total_cart:,} ج.م</h2></div>", unsafe_allow_html=True)

        # زر واتساب للسلة كاملة في الشريط الجانبي
        st.markdown("---")
        st.link_button(
            f"📱 طلب السلة كاملة عبر واتساب ({get_cart_count()} منتج)",
            f"https://wa.me/{WHATSAPP_NUMBER}?text={build_whatsapp_cart_message()}",
            use_container_width=True
        )
        if st.button("🗑️ تفريغ السلة", use_container_width=True):
            st.session_state.shopping_cart = []; st.rerun()
    else:
        st.info("السلة فارغة")

    st.markdown("---")
    st.write("### 📞 تواصل معنا")
    st.markdown("- **📍** محرم بك - الإسكندرية\n- **📞** 01xxxxxxxxx\n- **🕐** 9 ص - 9 م (يومياً)")
    st.markdown("---")

    if not st.session_state.is_logged_in:
        st.write("### 🔐 دخول المدير")
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم:", key="login_user")
            password = st.text_input("كلمة المرور:", type="password", key="login_pass")
            if st.form_submit_button("🔓 دخول", use_container_width=True):
                if check_login(username, password):
                    st.session_state.is_logged_in = True
                    st.success("✅ تم الدخول بنجاح"); st.rerun()
                else:
                    st.error("❌ خطأ في البيانات")
    else:
        st.success("✅ مسجل دخول كمدير")
        cairo_time = get_cairo_time()
        st.info(f"🕐 {cairo_time.strftime('%H:%M')}")
        st.metric("📦 الطلبات",    len(st.session_state.product_orders))
        st.metric("💳 الاشتراكات", len(st.session_state.subscriptions))
        st.metric("🏠 التبني",     len(st.session_state.adoption_requests))
        st.metric("🔔 الإشعارات",  len(st.session_state.notifications))

# =============================================
# الفوتر
# =============================================
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;padding:30px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
            border-radius:20px;color:white;margin-top:50px;'>
    <h3 style='color:white;'>🐾 VetFamily Alexandria 🐾</h3>
    <p>مركز الرعاية البيطرية المتكاملة</p>
    <p style='font-size:0.9rem;margin-top:15px;'>
        📍 محرم بك - الإسكندرية | 📞 01xxxxxxxxx | 💬 واتساب<br>
        © 2024 VetFamily Alexandria. جميع الحقوق محفوظة.
    </p>
</div>""", unsafe_allow_html=True)