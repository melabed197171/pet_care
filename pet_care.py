import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
import pytz
import hashlib
import pandas as pd

# =====================================
# إعداد الصفحة
# =====================================
st.set_page_config(
    page_title="VetFamily Alexandria - مركز الرعاية البيطرية المتكاملة",
    layout="wide",
    page_icon="🐾",
    initial_sidebar_state="expanded"
)

# =====================================
# المنطقة الزمنية
# =====================================
CAIRO_TZ = pytz.timezone('Africa/Cairo')

def get_cairo_time():
    return datetime.now(CAIRO_TZ)

# =====================================
# CSS المحسّن والمطور
# =====================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');

    * {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
    }

    .block-container {
        padding: 2rem 2rem;
        max-width: 1400px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        box-shadow: 0 20px 60px 0 rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.3);
        margin: 20px auto;
    }

    /* هيدر المشروع */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }

    .main-header h1 {
        color: white !important;
        font-size: 3rem !important;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        color: #f0f0f0;
        font-size: 1.3rem;
        margin: 10px 0 0 0;
    }

    /* الأزرار */
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    div.stButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
    }

    /* بطاقات المنتجات */
    .product-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        border: 2px solid #e0e0e0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }

    .product-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }

    .product-image {
        font-size: 80px;
        text-align: center;
        margin: 15px 0;
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.2));
    }

    .product-name {
        font-size: 1.5rem;
        font-weight: 800;
        color: #2d3748;
        margin: 10px 0;
        text-align: center;
    }

    .product-description {
        color: #718096;
        font-size: 1rem;
        text-align: center;
        margin: 10px 0;
        line-height: 1.6;
    }

    .product-price {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
        text-align: center;
        margin: 15px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    .old-price {
        color: #999;
        text-decoration: line-through;
        font-size: 1.2rem;
        margin-left: 10px;
    }

    /* شارات المنتج */
    .product-badge {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 5px;
    }

    .badge-new {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }

    .badge-sale {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #333;
    }

    .badge-popular {
        background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
        color: white;
    }

    /* حالة المخزون */
    .stock-badge {
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 700;
        text-align: center;
        margin: 10px 0;
    }

    .in-stock {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        color: #1e4620;
    }

    .low-stock {
        background: linear-gradient(135deg, #fdeb71 0%, #f8d800 100%);
        color: #664d03;
    }

    .out-stock {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #842029;
    }

    /* سلة التسوق */
    .cart-item {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-right: 4px solid #667eea;
    }

    .cart-total {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-size: 1.5rem;
        font-weight: 800;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }

    /* رسائل النجاح */
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4);
        animation: slideIn 0.5s ease;
    }

    @keyframes slideIn {
        from {
            transform: translateY(-30px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 10px;
        border-radius: 15px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: white;
        border-radius: 10px;
        padding: 0 25px;
        font-size: 1.1rem;
        font-weight: 700;
        color: #2d3748;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-3px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: #667eea !important;
    }

    /* الإشعارات */
    .notification-badge {
        background: #f5576c;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    /* الفئات */
    .category-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }

    .category-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }

    .category-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }

    .category-name {
        font-size: 1.2rem;
        font-weight: 700;
    }

    /* العروض الخاصة */
    .special-offer {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(250, 112, 154, 0.4);
        position: relative;
        overflow: hidden;
    }

    .special-offer::before {
        content: '🔥';
        position: absolute;
        font-size: 150px;
        opacity: 0.1;
        top: -30px;
        left: -30px;
    }

    /* النماذج */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* المقاييس */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
    }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* تحسينات إضافية */
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        margin: 30px 0;
        border-radius: 2px;
    }

    /* أيقونات مميزة */
    .feature-icon {
        font-size: 2.5rem;
        margin: 10px;
        filter: drop-shadow(0 3px 6px rgba(0,0,0,0.2));
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# دالة التشفير
# =====================================
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("VetFamily2024")

def check_login(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH

# =====================================
# تهيئة Session State
# =====================================
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

if 'show_adoption_form' not in st.session_state:
    st.session_state.show_adoption_form = False

if 'shopping_cart' not in st.session_state:
    st.session_state.shopping_cart = []

if 'adoption_requests' not in st.session_state:
    st.session_state.adoption_requests = []

if 'product_orders' not in st.session_state:
    st.session_state.product_orders = []

if 'subscriptions' not in st.session_state:
    st.session_state.subscriptions = []

if 'notifications' not in st.session_state:
    st.session_state.notifications = []

# =====================================
# قاعدة بيانات المنتجات البيطرية الشاملة
# =====================================
if 'products' not in st.session_state:
    st.session_state.products = {
        "طعام_القطط_الجاف": [
            {
                "id": 1,
                "name": "رويال كانين - قطط بالغة 2 كجم",
                "description": "طعام متوازن للقطط البالغة من 1-7 سنوات، يحتوي على جميع العناصر الغذائية الأساسية",
                "price": 450,
                "cost": 320,
                "icon": "🐱",
                "category": "طعام القطط الجاف",
                "stock": 25,
                "unit": "كيس 2 كجم",
                "brand": "Royal Canin",
                "country": "فرنسا",
                "features": ["بروتين 32%", "دهون 15%", "فيتامينات متكاملة", "أوميجا 3 و 6", "مناسب للفراء اللامع"],
                "badges": ["popular", "premium"],
                "image_url": ""
            },
            {
                "id": 2,
                "name": "رويال كانين كيتن - قطط صغيرة 1.5 كجم",
                "description": "تركيبة خاصة للقطط الصغيرة من شهرين إلى 12 شهر، تدعم النمو الصحي",
                "price": 400,
                "cost": 280,
                "icon": "🐈",
                "category": "طعام القطط الجاف",
                "stock": 18,
                "unit": "كيس 1.5 كجم",
                "brand": "Royal Canin",
                "country": "فرنسا",
                "features": ["سهل الهضم", "دعم جهاز المناعة", "تقوية العظام", "طاقة عالية", "قطع صغيرة الحجم"],
                "badges": ["new", "recommended"],
                "image_url": ""
            },
            {
                "id": 3,
                "name": "بريميوم كات - قطط 1 كجم (محلي)",
                "description": "طعام محلي عالي الجودة بسعر اقتصادي",
                "price": 70,
                "cost": 45,
                "icon": "🐱",
                "category": "طعام القطط الجاف",
                "stock": 40,
                "unit": "كيس 1 كجم",
                "brand": "Premium Cat",
                "country": "مصر",
                "features": ["جودة جيدة", "سعر مناسب", "بروتين 28%", "فيتامينات"],
                "badges": ["sale"],
                "image_url": ""
            },
            {
                "id": 4,
                "name": "هيلز ساينس دايت - قطط 1.5 كجم",
                "description": "طعام علمي متقدم من هيلز للقطط البالغة",
                "price": 520,
                "cost": 380,
                "icon": "🐱",
                "category": "طعام القطط الجاف",
                "stock": 12,
                "unit": "كيس 1.5 كجم",
                "brand": "Hill's Science Diet",
                "country": "أمريكا",
                "features": ["تركيبة علمية", "مضادات أكسدة", "صحة الكلى", "هضم سهل"],
                "badges": ["premium", "vet-recommended"],
                "image_url": ""
            }
        ],
        
        "طعام_القطط_الرطب": [
            {
                "id": 5,
                "name": "ويسكاس - تونة في جيلي 85 جم",
                "description": "وجبة رطبة لذيذة من التونة الطبيعية",
                "price": 25,
                "cost": 15,
                "icon": "🐟",
                "category": "طعام القطط الرطب",
                "stock": 100,
                "unit": "علبة 85 جم",
                "brand": "Whiskas",
                "country": "تايلاند",
                "features": ["تونة طبيعية 100%", "غني بالبروتين", "رطوبة عالية", "بدون ألوان صناعية"],
                "badges": ["popular"],
                "image_url": ""
            },
            {
                "id": 6,
                "name": "شيبا - دجاج مشوي 85 جم",
                "description": "وجبة فاخرة من الدجاج المشوي",
                "price": 30,
                "cost": 20,
                "icon": "🍗",
                "category": "طعام القطط الرطب",
                "stock": 80,
                "unit": "علبة 85 جم",
                "brand": "Sheba",
                "country": "تايلاند",
                "features": ["دجاج مشوي", "طعم لذيذ", "قطع كبيرة", "صوص شهي"],
                "badges": ["premium"],
                "image_url": ""
            },
            {
                "id": 7,
                "name": "فانسي فيست - سلمون 85 جم",
                "description": "سلمون طازج في صلصة خاصة",
                "price": 28,
                "cost": 18,
                "icon": "🐟",
                "category": "طعام القطط الرطب",
                "stock": 60,
                "unit": "علبة 85 جم",
                "brand": "Fancy Feast",
                "country": "أمريكا",
                "features": ["سلمون حقيقي", "أوميجا 3", "صحة الجلد", "بدون حبوب"],
                "badges": ["new"],
                "image_url": ""
            }
        ],

        "طعام_الكلاب_الجاف": [
            {
                "id": 8,
                "name": "رويال كانين - كلاب كبيرة 3 كجم",
                "description": "تركيبة متطورة للكلاب الكبيرة النشطة فوق 25 كجم",
                "price": 550,
                "cost": 380,
                "icon": "🐕",
                "category": "طعام الكلاب الجاف",
                "stock": 20,
                "unit": "كيس 3 كجم",
                "brand": "Royal Canin",
                "country": "فرنسا",
                "features": ["دعم المفاصل", "طاقة عالية", "بروتين 30%", "جلوكوزامين", "كوندرويتين"],
                "badges": ["popular", "premium"],
                "image_url": ""
            },
            {
                "id": 9,
                "name": "بيديجري - كلاب بالغة 2.5 كجم",
                "description": "طعام متوازن للكلاب البالغة من جميع الأحجام",
                "price": 320,
                "cost": 220,
                "icon": "🐕",
                "category": "طعام الكلاب الجاف",
                "stock": 30,
                "unit": "كيس 2.5 كجم",
                "brand": "Pedigree",
                "country": "تايلاند",
                "features": ["فيتامينات متكاملة", "دجاج حقيقي", "سهل الهضم", "أسنان صحية"],
                "badges": ["sale"],
                "image_url": ""
            },
            {
                "id": 10,
                "name": "هيلز - كلاب صغيرة 1.5 كجم",
                "description": "طعام خاص للسلالات الصغيرة أقل من 10 كجم",
                "price": 450,
                "cost": 300,
                "icon": "🐕",
                "category": "طعام الكلاب الجاف",
                "stock": 15,
                "unit": "كيس 1.5 كجم",
                "brand": "Hill's",
                "country": "أمريكا",
                "features": ["قطع صغيرة", "سهل المضغ", "طاقة عالية", "صحة الأسنان"],
                "badges": ["recommended"],
                "image_url": ""
            }
        ],

        "الرمل_والنظافة": [
            {
                "id": 11,
                "name": "كات ساند - رمل متكتل 5 كجم",
                "description": "رمل بنتونايت متكتل سريع الامتصاص برائحة اللافندر",
                "price": 90,
                "cost": 55,
                "icon": "🏖️",
                "category": "الرمل والنظافة",
                "stock": 50,
                "unit": "كيس 5 كجم",
                "brand": "Cat Sand",
                "country": "مصر",
                "features": ["سريع التكتل", "امتصاص فائق", "معطر", "اقتصادي", "قليل الغبار"],
                "badges": ["popular", "sale"],
                "image_url": ""
            },
            {
                "id": 12,
                "name": "إيفر كلين - رمل بريميوم 6 كجم",
                "description": "رمل متطور مع تقنية منع الروائح",
                "price": 180,
                "cost": 120,
                "icon": "🏖️",
                "category": "الرمل والنظافة",
                "stock": 25,
                "unit": "كيس 6 كجم",
                "brand": "Ever Clean",
                "country": "أمريكا",
                "features": ["تكتل قوي", "تحكم في الروائح", "خالي من الغبار", "مضاد بكتيريا"],
                "badges": ["premium"],
                "image_url": ""
            },
            {
                "id": 13,
                "name": "صندوق رمل قطط مع غطاء",
                "description": "صندوق رمل بلاستيك عالي الجودة مع غطاء ومجرفة",
                "price": 150,
                "cost": 90,
                "icon": "🚽",
                "category": "الرمل والنظافة",
                "stock": 15,
                "unit": "قطعة",
                "brand": "Pet Home",
                "country": "الصين",
                "features": ["سهل التنظيف", "مع مجرفة", "غطاء مانع للروائح", "قاعدة مانعة للانزلاق"],
                "badges": ["new"],
                "image_url": ""
            }
        ],

        "الصحة_والأدوية": [
            {
                "id": 14,
                "name": "شامبو بيتكين الطبي 500 مل",
                "description": "شامبو طبي مضاد للحساسية والبراغيث",
                "price": 130,
                "cost": 70,
                "icon": "🧴",
                "category": "الصحة والأدوية",
                "stock": 30,
                "unit": "زجاجة 500 مل",
                "brand": "Petkin",
                "country": "مصر",
                "features": ["مضاد حساسية", "مضاد براغيث", "رائحة منعشة", "آمن تماماً", "للقطط والكلاب"],
                "badges": ["vet-recommended"],
                "image_url": ""
            },
            {
                "id": 15,
                "name": "فرونت لاين - قطرات ضد البراغيث",
                "description": "أقوى علاج للبراغيث والقراد للقطط والكلاب",
                "price": 150,
                "cost": 85,
                "icon": "💧",
                "category": "الصحة والأدوية",
                "stock": 20,
                "unit": "أمبول واحد",
                "brand": "Frontline",
                "country": "فرنسا",
                "features": ["حماية شهرية", "فعال 100%", "سهل الاستخدام", "آمن للحيوانات"],
                "badges": ["premium", "vet-recommended"],
                "image_url": ""
            },
            {
                "id": 16,
                "name": "سيريستو - طوق ضد البراغيث",
                "description": "طوق طبي يوفر حماية لمدة 8 شهور",
                "price": 170,
                "cost": 95,
                "icon": "⭕",
                "category": "الصحة والأدوية",
                "stock": 15,
                "unit": "طوق واحد",
                "brand": "Seresto",
                "country": "ألمانيا",
                "features": ["حماية 8 شهور", "ضد البراغيث والقراد", "مقاوم للماء", "آمن"],
                "badges": ["premium"],
                "image_url": ""
            },
            {
                "id": 17,
                "name": "مالت باست - معجون مضاد لكرات الشعر",
                "description": "معجون لذيذ يساعد على التخلص من كرات الشعر",
                "price": 95,
                "cost": 55,
                "icon": "🧪",
                "category": "الصحة والأدوية",
                "stock": 25,
                "unit": "أنبوب 100 جم",
                "brand": "Malt Paste",
                "country": "ألمانيا",
                "features": ["طعم سمك", "سهل الاستخدام", "فعال", "طبيعي"],
                "badges": ["recommended"],
                "image_url": ""
            },
            {
                "id": 18,
                "name": "قطرة عين فيتامين A",
                "description": "قطرة مطهرة ومعالجة لالتهابات العين",
                "price": 85,
                "cost": 45,
                "icon": "👁️",
                "category": "الصحة والأدوية",
                "stock": 18,
                "unit": "زجاجة 15 مل",
                "brand": "Pet Vision",
                "country": "مصر",
                "features": ["مطهرة", "آمنة", "سريعة المفعول", "بدون آثار جانبية"],
                "badges": ["vet-recommended"],
                "image_url": ""
            }
        ],

        "الإكسسوارات": [
            {
                "id": 19,
                "name": "طوق جلد طبيعي مع جرس",
                "description": "طوق جلد أصلي عالي الجودة قابل للتعديل",
                "price": 80,
                "cost": 35,
                "icon": "🎀",
                "category": "الإكسسوارات",
                "stock": 35,
                "unit": "قطعة",
                "brand": "Pet Style",
                "country": "تركيا",
                "features": ["جلد طبيعي", "قابل للتعديل", "جرس معدني", "متين", "ألوان متعددة"],
                "badges": ["popular"],
                "image_url": ""
            },
            {
                "id": 20,
                "name": "سلسلة مشي نايلون قوية",
                "description": "سلسلة مشي متينة للكلاب المتوسطة والكبيرة",
                "price": 90,
                "cost": 40,
                "icon": "🦮",
                "category": "الإكسسوارات",
                "stock": 25,
                "unit": "قطعة 1.5 متر",
                "brand": "Strong Lead",
                "country": "الصين",
                "features": ["نايلون قوي", "مقبض مريح", "حلقة معدنية", "طول 1.5 م"],
                "badges": ["sale"],
                "image_url": ""
            },
            {
                "id": 21,
                "name": "حقيبة نقل فاخرة",
                "description": "حقيبة نقل آمنة ومريحة للسفر والعيادات",
                "price": 350,
                "cost": 200,
                "icon": "🎒",
                "category": "الإكسسوارات",
                "stock": 10,
                "unit": "حقيبة مقاس متوسط",
                "brand": "Travel Pet",
                "country": "الصين",
                "features": ["تهوية ممتازة", "خفيفة الوزن", "سهلة الحمل", "آمنة", "قابلة للطي"],
                "badges": ["premium"],
                "image_url": ""
            },
            {
                "id": 22,
                "name": "سرير فاخر للكلاب - مقاس كبير",
                "description": "سرير مريح وفاخر بقماش قابل للإزالة والغسل",
                "price": 450,
                "cost": 250,
                "icon": "🛏️",
                "category": "الإكسسوارات",
                "stock": 8,
                "unit": "سرير 80×60 سم",
                "brand": "Comfy Pet",
                "country": "تركيا",
                "features": ["قماش فاخر", "قابل للغسل", "إسفنج طبي", "مريح ودافئ", "قاعدة مانعة للانزلاق"],
                "badges": ["premium", "new"],
                "image_url": ""
            }
        ],

        "الألعاب": [
            {
                "id": 23,
                "name": "فأر إلكتروني تفاعلي",
                "description": "لعبة إلكترونية تتحرك تلقائياً لتسلية القطط",
                "price": 120,
                "cost": 60,
                "icon": "🐭",
                "category": "الألعاب",
                "stock": 20,
                "unit": "قطعة",
                "brand": "Smart Toy",
                "country": "الصين",
                "features": ["حركة تلقائية", "آمنة", "بطاريات قابلة للشحن", "متينة"],
                "badges": ["new", "popular"],
                "image_url": ""
            },
            {
                "id": 24,
                "name": "كرة مطاطية بجرس",
                "description": "كرة ملونة بجرس داخلي لتسلية القطط",
                "price": 25,
                "cost": 12,
                "icon": "⚽",
                "category": "الألعاب",
                "stock": 50,
                "unit": "قطعة",
                "brand": "Play Ball",
                "country": "مصر",
                "features": ["مطاط آمن", "جرس داخلي", "ألوان زاهية", "سهلة الحمل"],
                "badges": ["sale"],
                "image_url": ""
            },
            {
                "id": 25,
                "name": "عصا ريش للعب",
                "description": "عصا مع ريش ملون لتحفيز غريزة الصيد",
                "price": 40,
                "cost": 18,
                "icon": "🪶",
                "category": "الألعاب",
                "stock": 30,
                "unit": "قطعة",
                "brand": "Feather Fun",
                "country": "الصين",
                "features": ["ريش طبيعي", "عصا مرنة", "آمنة", "تمرين صحي"],
                "badges": ["recommended"],
                "image_url": ""
            },
            {
                "id": 26,
                "name": "عظمة مضغ للكلاب",
                "description": "عظمة صحية للمضغ تنظف الأسنان",
                "price": 35,
                "cost": 18,
                "icon": "🦴",
                "category": "الألعاب",
                "stock": 40,
                "unit": "قطعة",
                "brand": "Chew Bone",
                "country": "تايلاند",
                "features": ["طبيعية 100%", "تنظف الأسنان", "تقوي الفكين", "طعم لذيذ"],
                "badges": ["popular"],
                "image_url": ""
            }
        ],

        "أطباق_ومعدات_التغذية": [
            {
                "id": 27,
                "name": "طقم أطباق ستانلس ستيل",
                "description": "طقم طبقين للطعام والماء من الستانلس ستيل",
                "price": 65,
                "cost": 30,
                "icon": "🥘",
                "category": "أطباق ومعدات التغذية",
                "stock": 25,
                "unit": "طقم قطعتين",
                "brand": "Steel Bowl",
                "country": "الصين",
                "features": ["ستانلس ستيل", "سهل التنظيف", "مانع للانزلاق", "متين"],
                "badges": ["popular"],
                "image_url": ""
            },
            {
                "id": 28,
                "name": "نافورة مياه أوتوماتيك",
                "description": "نافورة مياه كهربائية تشجع على الشرب",
                "price": 280,
                "cost": 160,
                "icon": "⛲",
                "category": "أطباق ومعدات التغذية",
                "stock": 12,
                "unit": "قطعة 2 لتر",
                "brand": "Water Fountain",
                "country": "الصين",
                "features": ["فلتر كربوني", "هادئة", "سعة 2 لتر", "سهلة التنظيف"],
                "badges": ["premium", "new"],
                "image_url": ""
            },
            {
                "id": 29,
                "name": "موزع طعام أوتوماتيك",
                "description": "موزع طعام بتوقيت لضمان تغذية منتظمة",
                "price": 450,
                "cost": 280,
                "icon": "🍽️",
                "category": "أطباق ومعدات التغذية",
                "stock": 8,
                "unit": "قطعة 3 لتر",
                "brand": "Auto Feeder",
                "country": "الصين",
                "features": ["4 وجبات يومياً", "مؤقت رقمي", "تسجيل صوتي", "سعة 3 لتر"],
                "badges": ["premium"],
                "image_url": ""
            }
        ],

        "العناية_والتجميل": [
            {
                "id": 30,
                "name": "فرشاة تمشيط احترافية",
                "description": "فرشاة مزدوجة لفك التشابك وتلميع الفراء",
                "price": 50,
                "cost": 22,
                "icon": "🪮",
                "category": "العناية والتجميل",
                "stock": 20,
                "unit": "قطعة",
                "brand": "Grooming Pro",
                "country": "الصين",
                "features": ["أسنان ناعمة", "مقبض مريح", "للفراء الطويل والقصير", "مضادة للكهرباء الساكنة"],
                "badges": ["recommended"],
                "image_url": ""
            },
            {
                "id": 31,
                "name": "مقص أظافر احترافي",
                "description": "مقص أظافر آمن بحماية من القص الزائد",
                "price": 75,
                "cost": 35,
                "icon": "✂️",
                "category": "العناية والتجميل",
                "stock": 15,
                "unit": "قطعة",
                "brand": "Nail Clipper",
                "country": "ألمانيا",
                "features": ["شفرة حادة", "واقي أمان", "مقبض مطاطي", "للقطط والكلاب"],
                "badges": ["premium"],
                "image_url": ""
            },
            {
                "id": 32,
                "name": "مناديل تنظيف معطرة",
                "description": "مناديل مبللة معطرة للتنظيف السريع",
                "price": 45,
                "cost": 22,
                "icon": "🧻",
                "category": "العناية والتجميل",
                "stock": 35,
                "unit": "علبة 80 منديل",
                "brand": "Fresh Wipes",
                "country": "مصر",
                "features": ["آمنة 100%", "معطرة", "مضادة للبكتيريا", "للاستخدام اليومي"],
                "badges": ["popular"],
                "image_url": ""
            },
            {
                "id": 33,
                "name": "طقم العناية بالأسنان",
                "description": "فرشاة أسنان + معجون بنكهة اللحم",
                "price": 110,
                "cost": 55,
                "icon": "🪥",
                "category": "العناية والتجميل",
                "stock": 18,
                "unit": "طقم",
                "brand": "Dental Kit",
                "country": "أمريكا",
                "features": ["فرشاة ناعمة", "نكهة لحم", "مضاد للجير", "وقاية من التسوس"],
                "badges": ["vet-recommended"],
                "image_url": ""
            }
        ],

        "الفيتامينات_والمكملات": [
            {
                "id": 34,
                "name": "مالتي فيتامين للقطط",
                "description": "فيتامينات متعددة لصحة أفضل",
                "price": 160,
                "cost": 90,
                "icon": "💊",
                "category": "الفيتامينات والمكملات",
                "stock": 15,
                "unit": "علبة 60 قرص",
                "brand": "Pet Vitamin",
                "country": "أمريكا",
                "features": ["فيتامينات متكاملة", "تقوية المناعة", "طعم سمك", "سهلة البلع"],
                "badges": ["vet-recommended"],
                "image_url": ""
            },
            {
                "id": 35,
                "name": "أوميجا 3 للفراء اللامع",
                "description": "كبسولات زيت السمك لفراء صحي",
                "price": 140,
                "cost": 80,
                "icon": "🐟",
                "category": "الفيتامينات والمكملات",
                "stock": 12,
                "unit": "علبة 90 كبسولة",
                "brand": "Omega Plus",
                "country": "النرويج",
                "features": ["زيت سمك نقي", "أوميجا 3 و 6", "فراء لامع", "جلد صحي"],
                "badges": ["premium"],
                "image_url": ""
            },
            {
                "id": 36,
                "name": "مكمل المفاصل للكلاب",
                "description": "جلوكوزامين وكوندرويتين لدعم المفاصل",
                "price": 180,
                "cost": 110,
                "icon": "🦴",
                "category": "الفيتامينات والمكملات",
                "stock": 10,
                "unit": "علبة 60 قرص",
                "brand": "Joint Support",
                "country": "أمريكا",
                "features": ["جلوكوزامين", "كوندرويتين", "لكبار السن", "طعم لذيذ"],
                "badges": ["vet-recommended", "premium"],
                "image_url": ""
            }
        ]
    }

# =====================================
# الباقات الطبية
# =====================================
if 'packages' not in st.session_state:
    st.session_state.packages = {
        "الباقة البرونزية": {
            "price": 200,
            "duration": "شهرياً",
            "description": "باقة أساسية للرعاية الشهرية",
            "icon": "🥉",
            "color": "#CD7F32",
            "features": [
                "استشارتان هاتفيتان شهرياً",
                "استشارة واتساب مفتوحة",
                "خصم 10% على الأدوية والمستلزمات",
                "متابعة الحالة الصحية",
                "نصائح غذائية مجانية"
            ]
        },
        "الباقة الفضية": {
            "price": 400,
            "duration": "شهرياً",
            "description": "رعاية متقدمة مع فحوصات دورية",
            "icon": "🥈",
            "color": "#C0C0C0",
            "features": [
                "4 استشارات (عيادة أو هاتف)",
                "فحص شامل مجاني",
                "خصم 20% على جميع المنتجات",
                "أولوية في الحجز",
                "متابعة دورية أسبوعية",
                "استشارة تغذية متخصصة"
            ]
        },
        "الباقة الذهبية": {
            "price": 700,
            "duration": "شهرياً",
            "description": "رعاية VIP شاملة ومتكاملة",
            "icon": "🥇",
            "color": "#FFD700",
            "features": [
                "استشارات غير محدودة",
                "زيارة منزلية مجانية",
                "فحص شامل شهري",
                "جميع التطعيمات الأساسية",
                "خصم 30% على المنتجات",
                "خط ساخن طوارئ 24/7",
                "أولوية قصوى في جميع الخدمات",
                "ملف طبي إلكتروني"
            ]
        },
        "الباقة الماسية": {
            "price": 1200,
            "duration": "شهرياً",
            "description": "الباقة الأشمل - رعاية ملكية",
            "icon": "💎",
            "color": "#B9F2FF",
            "features": [
                "كل مميزات الباقة الذهبية",
                "زيارتان منزليتان شهرياً",
                "تحاليل مجانية (شاملة)",
                "عمليات صغرى بسعر التكلفة",
                "رعاية كاملة أثناء السفر",
                "شريحة تتبع GPS مجانية",
                "توصيل مجاني للمنتجات",
                "جلسة تجميل شهرية",
                "مدرب سلوك (استشارة)",
                "خصم 40% على كل شيء"
            ]
        }
    }

# =====================================
# دوال مساعدة
# =====================================

def add_to_cart(product):
    """إضافة منتج للسلة"""
    for item in st.session_state.shopping_cart:
        if item['id'] == product['id']:
            if item['quantity'] < product['stock']:
                item['quantity'] += 1
                return True
            else:
                return False
    
    cart_item = product.copy()
    cart_item['quantity'] = 1
    st.session_state.shopping_cart.append(cart_item)
    return True

def remove_from_cart(product_id):
    """إزالة منتج من السلة"""
    st.session_state.shopping_cart = [
        item for item in st.session_state.shopping_cart 
        if item['id'] != product_id
    ]

def update_cart_quantity(product_id, new_quantity):
    """تحديث كمية منتج في السلة"""
    for item in st.session_state.shopping_cart:
        if item['id'] == product_id:
            if new_quantity <= 0:
                remove_from_cart(product_id)
            else:
                item['quantity'] = new_quantity
            break

def get_cart_total():
    """حساب إجمالي السلة"""
    return sum(item['price'] * item['quantity'] for item in st.session_state.shopping_cart)

def get_cart_count():
    """عدد المنتجات في السلة"""
    return sum(item['quantity'] for item in st.session_state.shopping_cart)

def save_product_order(cart_items, customer_info):
    """حفظ طلب منتجات"""
    try:
        cairo_time = get_cairo_time()
        total_price = get_cart_total()
        
        order = {
            "id": len(st.session_state.product_orders) + 1,
            "items": [
                {
                    "name": item['name'],
                    "quantity": item['quantity'],
                    "price": item['price'],
                    "total": item['price'] * item['quantity']
                }
                for item in cart_items
            ],
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
        
        # إشعار
        notification = {
            "type": "product_order",
            "message": f"طلب منتجات جديد من {customer_info['name']}",
            "details": f"إجمالي: {total_price} ج.م - عدد المنتجات: {len(cart_items)}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "order": order
        }
        st.session_state.notifications.insert(0, notification)
        
        # تفريغ السلة
        st.session_state.shopping_cart = []
        
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الطلب: {e}")
        return False

def save_subscription(package_name, package_data, customer_info):
    """حفظ اشتراك في باقة"""
    try:
        cairo_time = get_cairo_time()
        
        subscription = {
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
        
        st.session_state.subscriptions.append(subscription)
        
        # إشعار
        notification = {
            "type": "subscription",
            "message": f"اشتراك جديد في {package_name}",
            "details": f"{customer_info['name']} - {package_data['price']} ج.م/{package_data['duration']}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "subscription": subscription
        }
        st.session_state.notifications.insert(0, notification)
        
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الاشتراك: {e}")
        return False

def save_adoption_request(adoption_info):
    """حفظ طلب تبني"""
    try:
        cairo_time = get_cairo_time()
        
        request = {
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
        
        st.session_state.adoption_requests.append(request)
        
        # إشعار
        notification = {
            "type": "adoption",
            "message": f"طلب تبني جديد - {adoption_info['pet_type']}",
            "details": f"{adoption_info['name']} - {adoption_info['phone']}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "request": request
        }
        st.session_state.notifications.insert(0, notification)
        
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ طلب التبني: {e}")
        return False

def get_badge_html(badges):
    """توليد HTML للشارات"""
    badge_html = ""
    badge_map = {
        "new": ("جديد", "badge-new"),
        "sale": ("عرض", "badge-sale"),
        "popular": ("الأكثر مبيعاً", "badge-popular"),
        "premium": ("بريميوم", "badge-premium"),
        "recommended": ("موصى به", "badge-recommended"),
        "vet-recommended": ("موصى به من الأطباء", "badge-vet")
    }
    
    for badge in badges:
        if badge in badge_map:
            text, css_class = badge_map[badge]
            badge_html += f'<span class="product-badge {css_class}">{text}</span>'
    
    return badge_html

def display_product_card(product):
    """عرض بطاقة منتج"""
    # حالة المخزون
    if product['stock'] > 10:
        stock_class = "in-stock"
        stock_text = f"✅ متوفر ({product['stock']} قطعة)"
    elif product['stock'] > 0:
        stock_class = "low-stock"
        stock_text = f"⚠️ كمية محدودة ({product['stock']} قطعة)"
    else:
        stock_class = "out-stock"
        stock_text = "❌ نفذ من المخزون"
    
    # الشارات
    badges_html = get_badge_html(product.get('badges', []))
    
    # البطاقة
    st.markdown(f"""
    <div class='product-card'>
        <div class='product-image'>{product['icon']}</div>
        <div class='product-name'>{product['name']}</div>
        <div>{badges_html}</div>
        <div class='product-description'>{product['description']}</div>
        <div class='product-price'>{product['price']} ج.م</div>
        <div style='text-align: center; color: #718096; font-size: 0.9rem;'>
            📦 {product['unit']} | 🏷️ {product['brand']}
        </div>
        <div class='stock-badge {stock_class}'>{stock_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # التفاصيل
    with st.expander("📋 المميزات والتفاصيل"):
        for feature in product['features']:
            st.write(f"✓ {feature}")
        st.write(f"**🌍 بلد المنشأ:** {product['country']}")
    
    # زر الإضافة للسلة
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if product['stock'] > 0:
            if st.button(f"🛒 أضف للسلة", key=f"add_{product['id']}", use_container_width=True):
                if add_to_cart(product):
                    st.success(f"✅ تمت الإضافة إلى السلة!")
                    st.rerun()
                else:
                    st.warning("⚠️ الكمية المتاحة في المخزون محدودة")
        else:
            st.button("نفذ من المخزون ❌", disabled=True, use_container_width=True)
    
    with col2:
        # عرض سعر التكلفة للمدير فقط
        if st.session_state.is_logged_in:
            profit = product['price'] - product['cost']
            profit_percent = (profit / product['cost']) * 100
            st.caption(f"💰 {product['cost']} ج")
            st.caption(f"📈 +{profit_percent:.0f}%")

# =====================================
# الهيدر الرئيسي
# =====================================
st.markdown("""
<div class='main-header'>
    <h1>🐾 VetFamily Alexandria 🐾</h1>
    <p>مركز الرعاية البيطرية المتكاملة - الإسكندرية</p>
    <p style='font-size: 1rem; margin-top: 10px;'>
        🩺 أطباء بيطريون متخصصون | 🍖 طعام بريميوم أصلي | 🚗 توصيل مجاني
    </p>
</div>
""", unsafe_allow_html=True)

# أزرار الإجراءات السريعة
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

# =====================================
# التبويبات الرئيسية
# =====================================
if st.session_state.is_logged_in:
    tabs = st.tabs([
        "🏪 المتجر",
        "💎 الباقات الطبية",
        "🩺 الاستشارات",
        "📊 لوحة التحكم",
        "📦 طلبات المنتجات",
        "💳 الاشتراكات",
        "🏠 طلبات التبني"
    ])
    tab_shop, tab_packages, tab_consult, tab_dashboard, tab_orders, tab_subs, tab_adopt = tabs
else:
    tabs = st.tabs([
        "🏪 المتجر",
        "💎 الباقات الطبية",
        "🩺 الاستشارات",
        "ℹ️ من نحن"
    ])
    tab_shop, tab_packages, tab_consult, tab_about = tabs

# =====================================
# تبويب المتجر
# =====================================
with tab_shop:
    st.write("## 🛒 متجر المستلزمات البيطرية")
    st.write("### أفضل المنتجات البيطرية بأسعار منافسة 🎯")
    
    # فلاتر البحث
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
        # فلترة حسب الفئة
        if selected_category != "الكل" and category_key != selected_category:
            continue
        
        # عنوان الفئة
        category_name = products[0]['category'] if products else category_key
        st.markdown(f"### 📦 {category_name}")
        
        # فلترة المنتجات
        filtered_products = products
        
        if search_term:
            filtered_products = [
                p for p in products 
                if search_term.lower() in p['name'].lower() or 
                   search_term.lower() in p['brand'].lower() or
                   search_term.lower() in p['description'].lower()
            ]
        
        if not filtered_products:
            continue
        
        # ترتيب المنتجات
        if sort_option == "السعر: الأقل":
            filtered_products = sorted(filtered_products, key=lambda x: x['price'])
        elif sort_option == "السعر: الأعلى":
            filtered_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)
        
        # عرض المنتجات في أعمدة
        cols = st.columns(3)
        for idx, product in enumerate(filtered_products):
            with cols[idx % 3]:
                display_product_card(product)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =====================================
# تبويب الباقات الطبية
# =====================================
with tab_packages:
    st.write("## 💎 الباقات الطبية - اختر الأنسب لك")
    st.write("### رعاية طبية متكاملة بأسعار تنافسية")
    
    # عرض الباقات
    for package_name, package_data in st.session_state.packages.items():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {package_data['color']}22 0%, {package_data['color']}44 100%); 
                    padding: 30px; border-radius: 20px; margin: 20px 0; 
                    border: 3px solid {package_data['color']}; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
            <h2 style='text-align: center; color: #2d3748;'>{package_data['icon']} {package_name}</h2>
            <p style='text-align: center; font-size: 1.1rem; color: #4a5568;'>{package_data['description']}</p>
            <h1 style='text-align: center; color: {package_data['color']}; margin: 20px 0;'>
                {package_data['price']} ج.م / {package_data['duration']}
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        # المميزات
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### ✨ المميزات:")
            for feature in package_data['features']:
                st.write(f"✅ {feature}")
        
        with col2:
            st.write("### 📝 اشترك الآن")
            with st.form(f"package_form_{package_name}"):
                sub_name = st.text_input("الاسم الكامل:", key=f"sub_name_{package_name}")
                sub_phone = st.text_input("رقم الواتساب:", key=f"sub_phone_{package_name}")
                sub_address = st.text_input("العنوان:", key=f"sub_address_{package_name}")
                
                submitted = st.form_submit_button("🎯 اشترك الآن", use_container_width=True)
                
                if submitted:
                    if sub_name and sub_phone:
                        customer_info = {
                            "name": sub_name,
                            "phone": sub_phone,
                            "address": sub_address
                        }
                        
                        if save_subscription(package_name, package_data, customer_info):
                            st.markdown(f"""
                            <div class='success-message'>
                                🎉 تم الاشتراك بنجاح في {package_name}!<br>
                                سيتم التواصل معك قريباً 📞
                            </div>
                            """, unsafe_allow_html=True)
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("⚠️ برجاء إدخال الاسم ورقم الهاتف")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =====================================
# تبويب الاستشارات
# =====================================
with tab_consult:
    st.write("## 🩺 الاستشارات البيطرية")
    st.write("### فريق من الأطباء البيطريين المتخصصين في خدمتك")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 20px; color: white;'>
            <h3 style='color: white;'>👨‍⚕️ فريقنا الطبي</h3>
            <ul style='font-size: 1.1rem; line-height: 2;'>
                <li>أطباء بيطريون معتمدون</li>
                <li>خبرة واسعة في جميع التخصصات</li>
                <li>متابعة دورية ومستمرة</li>
                <li>استشارات على مدار الساعة</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 30px; border-radius: 20px; color: white;'>
            <h3 style='color: white;'>📋 خدماتنا</h3>
            <ul style='font-size: 1.1rem; line-height: 2;'>
                <li>الكشف والفحص الشامل</li>
                <li>التطعيمات والتحصينات</li>
                <li>العمليات الجراحية</li>
                <li>التحاليل الطبية</li>
                <li>الأشعة والتشخيص</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # أسعار الخدمات
    st.write("### 💰 أسعار الخدمات")
    
    services = [
        {"name": "استشارة هاتفية", "price": "مجاني", "icon": "📞"},
        {"name": "استشارة في العيادة", "price": "100 ج.م", "icon": "🏥"},
        {"name": "كشف + تطعيم", "price": "150 ج.م", "icon": "💉"},
        {"name": "زيارة منزلية", "price": "250 ج.م", "icon": "🏠"},
        {"name": "فحص شامل", "price": "300 ج.م", "icon": "🔬"},
        {"name": "عملية صغرى", "price": "500 ج.م+", "icon": "⚕️"}
    ]
    
    cols = st.columns(3)
    for idx, service in enumerate(services):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style='background: white; padding: 20px; border-radius: 15px; 
                        text-align: center; border: 2px solid #667eea; margin: 10px 0;'>
                <div style='font-size: 3rem;'>{service['icon']}</div>
                <h4 style='color: #2d3748; margin: 10px 0;'>{service['name']}</h4>
                <h3 style='color: #667eea;'>{service['price']}</h3>
            </div>
            """, unsafe_allow_html=True)

# =====================================
# لوحة التحكم (للمدير فقط)
# =====================================
if st.session_state.is_logged_in:
    with tab_dashboard:
        st.write("## 📊 لوحة التحكم الرئيسية")
        
        cairo_time = get_cairo_time()
        st.info(f"🕐 الوقت الحالي: {cairo_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if st.button("🔓 تسجيل الخروج", use_container_width=True):
            st.session_state.is_logged_in = False
            st.rerun()
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # الإحصائيات الرئيسية
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📦 طلبات المنتجات",
                len(st.session_state.product_orders),
                delta=f"+{len([o for o in st.session_state.product_orders if o['status'] == 'جديد - في انتظار التواصل'])}"
            )
        
        with col2:
            total_product_revenue = sum(order['total_price'] for order in st.session_state.product_orders)
            st.metric(
                "💰 إيرادات المنتجات",
                f"{total_product_revenue:,} ج.م"
            )
        
        with col3:
            st.metric(
                "💳 الاشتراكات",
                len(st.session_state.subscriptions),
                delta=f"+{len([s for s in st.session_state.subscriptions if s['status'] == 'جديد - في انتظار التواصل'])}"
            )
        
        with col4:
            total_sub_revenue = sum(sub['price'] for sub in st.session_state.subscriptions)
            st.metric(
                "💰 إيرادات الباقات",
                f"{total_sub_revenue:,} ج.م"
            )
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # الإشعارات
        st.write("### 🔔 الإشعارات الأخيرة")
        
        if st.session_state.notifications:
            for notif in st.session_state.notifications[:10]:
                notif_type = notif['type']
                
                if notif_type == 'product_order':
                    bg_color = "#667eea"
                elif notif_type == 'subscription':
                    bg_color = "#f093fb"
                elif notif_type == 'adoption':
                    bg_color = "#38ef7d"
                else:
                    bg_color = "#764ba2"
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%); 
                            padding: 20px; border-radius: 15px; color: white; margin: 10px 0;'>
                    <h4 style='margin: 0; color: white;'>{notif['message']}</h4>
                    <p style='margin: 10px 0 0 0; font-size: 0.9rem;'>
                        {notif['details']}<br>
                        📅 {notif['date']} | ⏰ {notif['timestamp']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد إشعارات جديدة")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # تحليلات إضافية
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 📈 أكثر المنتجات طلباً")
            # هنا يمكن إضافة تحليل للمنتجات الأكثر مبيعاً
            st.info("قريباً: تحليلات مفصلة")
        
        with col2:
            st.write("### 📊 إحصائيات الباقات")
            # هنا يمكن إضافة تحليل للباقات
            st.info("قريباً: تحليلات مفصلة")
    
    # =====================================
    # تبويب طلبات المنتجات
    # =====================================
    with tab_orders:
        st.write("## 📦 إدارة طلبات المنتجات")
        
        if st.session_state.product_orders:
            for order in reversed(st.session_state.product_orders):
                st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 15px; 
                            margin: 15px 0; border-right: 5px solid #667eea;'>
                    <h4>طلب #{order['id']} - {order['customer_name']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
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
                
                # المنتجات المطلوبة
                st.write("**المنتجات:**")
                for item in order['items']:
                    st.write(f"• {item['name']} - الكمية: {item['quantity']} × {item['price']} ج.م = {item['total']} ج.م")
                
                if order.get('notes'):
                    st.write(f"**📝 ملاحظات:** {order['notes']}")
                
                # تحديث الحالة
                col_status, col_btn = st.columns([4, 1])
                
                with col_status:
                    status_options = ["جديد - في انتظار التواصل", "تم التواصل", "قيد التجهيز", "جاهز للتوصيل", "تم التوصيل", "ملغي"]
                    new_status = st.selectbox(
                        "الحالة:",
                        status_options,
                        index=status_options.index(order['status']),
                        key=f"status_order_{order['id']}"
                    )
                
                with col_btn:
                    if st.button("💾 حفظ", key=f"save_order_{order['id']}"):
                        for o in st.session_state.product_orders:
                            if o['id'] == order['id']:
                                o['status'] = new_status
                        st.success("✅ تم الحفظ")
                        st.rerun()
                
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد طلبات منتجات حتى الآن")
    
    # =====================================
    # تبويب الاشتراكات
    # =====================================
    with tab_subs:
        st.write("## 💳 إدارة الاشتراكات في الباقات")
        
        if st.session_state.subscriptions:
            for sub in reversed(st.session_state.subscriptions):
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb22 0%, #f5576c22 100%); 
                            padding: 20px; border-radius: 15px; margin: 15px 0; 
                            border: 2px solid #f093fb;'>
                    <h4>{sub['package_name']} - {sub['customer_name']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**📞 الهاتف:** {sub['customer_phone']}")
                    st.write(f"**📍 العنوان:** {sub['customer_address']}")
                    st.write(f"**💰 السعر:** {sub['price']} ج.م/{sub['duration']}")
                
                with col2:
                    st.write(f"**📅 تاريخ البدء:** {sub['start_date']}")
                    st.write(f"**📅 تاريخ الانتهاء:** {sub['end_date']}")
                    st.write(f"**⏰ وقت الطلب:** {sub['time']}")
                
                # تحديث الحالة
                col_status, col_btn = st.columns([4, 1])
                
                with col_status:
                    status_options = ["جديد - في انتظار التواصل", "نشط", "منتهي", "ملغي"]
                    new_status = st.selectbox(
                        "الحالة:",
                        status_options,
                        index=status_options.index(sub['status']) if sub['status'] in status_options else 0,
                        key=f"status_sub_{sub['id']}"
                    )
                
                with col_btn:
                    if st.button("💾 حفظ", key=f"save_sub_{sub['id']}"):
                        for s in st.session_state.subscriptions:
                            if s['id'] == sub['id']:
                                s['status'] = new_status
                        st.success("✅ تم الحفظ")
                        st.rerun()
                
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد اشتراكات حتى الآن")
    
    # =====================================
    # تبويب طلبات التبني
    # =====================================
    with tab_adopt:
        st.write("## 🏠 إدارة طلبات التبني")
        
        if st.session_state.adoption_requests:
            for req in reversed(st.session_state.adoption_requests):
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #38ef7d22 0%, #11998e22 100%); 
                            padding: 20px; border-radius: 15px; margin: 15px 0; 
                            border: 2px solid #38ef7d;'>
                    <h4>طلب #{req['id']} - {req['customer_name']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**📞 الهاتف:** {req['customer_phone']}")
                    st.write(f"**📍 العنوان:** {req['customer_address']}")
                    st.write(f"**🐾 نوع الحيوان:** {req['pet_type']}")
                
                with col2:
                    st.write(f"**📅 التاريخ:** {req['date']}")
                    st.write(f"**⏰ الوقت:** {req['time']}")
                    if req.get('pet_age'):
                        st.write(f"**🎂 العمر المفضل:** {req['pet_age']}")
                
                if req.get('experience'):
                    st.write(f"**📚 الخبرة:** {req['experience']}")
                
                if req.get('home_type'):
                    st.write(f"**🏡 نوع السكن:** {req['home_type']}")
                
                if req.get('notes'):
                    st.write(f"**📝 ملاحظات:** {req['notes']}")
                
                # تحديث الحالة
                col_status, col_btn = st.columns([4, 1])
                
                with col_status:
                    status_options = ["جديد - في انتظار التواصل", "تم التواصل", "تمت الموافقة", "تم التبني", "مرفوض"]
                    new_status = st.selectbox(
                        "الحالة:",
                        status_options,
                        index=status_options.index(req['status']) if req['status'] in status_options else 0,
                        key=f"status_adopt_{req['id']}"
                    )
                
                with col_btn:
                    if st.button("💾 حفظ", key=f"save_adopt_{req['id']}"):
                        for r in st.session_state.adoption_requests:
                            if r['id'] == req['id']:
                                r['status'] = new_status
                        st.success("✅ تم الحفظ")
                        st.rerun()
                
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد طلبات تبني حتى الآن")

else:
    # =====================================
    # تبويب من نحن (للزوار)
    # =====================================
    with tab_about:
        st.write("## ℹ️ عن VetFamily Alexandria")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 40px; border-radius: 20px; color: white; text-align: center;'>
            <h2 style='color: white; margin-bottom: 20px;'>🐾 نحن عائلتك البيطرية في الإسكندرية</h2>
            <p style='font-size: 1.2rem; line-height: 1.8;'>
                مركز متكامل يجمع بين الخبرة الطبية والاحترافية في تقديم أفضل رعاية لحيوانك الأليف
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='text-align: center; padding: 30px; background: white; 
                        border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                <div style='font-size: 4rem;'>👨‍⚕️</div>
                <h3>أطباء متخصصون</h3>
                <p>فريق من الأطباء البيطريين ذوي الخبرة الواسعة</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='text-align: center; padding: 30px; background: white; 
                        border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                <div style='font-size: 4rem;'>🏆</div>
                <h3>منتجات أصلية</h3>
                <p>جميع منتجاتنا أصلية 100% من أفضل العلامات العالمية</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='text-align: center; padding: 30px; background: white; 
                        border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                <div style='font-size: 4rem;'>🚗</div>
                <h3>توصيل مجاني</h3>
                <p>خدمة توصيل سريعة ومجانية لجميع أنحاء الإسكندرية</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        st.write("### 📞 تواصل معنا")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - **📍 العنوان:** كرموز - الإسكندرية
            - **📞 الهاتف:** 01xxxxxxxxx
            - **💬 واتساب:** 01xxxxxxxxx
            """)
        
        with col2:
            st.markdown("""
            - **🕐 مواعيد العمل:** يومياً من 9 ص - 9 م
            - **📧 البريد الإلكتروني:** info@vetfamily-alex.com
            - **🌐 الموقع:** www.vetfamily-alex.com
            """)

# =====================================
# قسم إتمام الطلب (السلة)
# =====================================
if st.session_state.shopping_cart:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.write("## 🛒 إتمام طلبك")
    
    total = get_cart_total()
    
    st.markdown(f"""
    <div class='cart-total'>
        💰 إجمالي الطلب: {total:,} ج.م
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        customer_name = st.text_input("الاسم الكامل *", key="checkout_name")
    
    with col2:
        customer_phone = st.text_input("رقم الواتساب *", key="checkout_phone")
    
    with col3:
        customer_address = st.text_input("عنوان التوصيل *", key="checkout_address")
    
    customer_notes = st.text_area("ملاحظات إضافية (اختياري)", key="checkout_notes")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("✅ تأكيد الطلب", use_container_width=True, type="primary"):
            if customer_name and customer_phone and customer_address:
                customer_info = {
                    "name": customer_name,
                    "phone": customer_phone,
                    "address": customer_address,
                    "notes": customer_notes
                }
                
                if save_product_order(st.session_state.shopping_cart, customer_info):
                    st.markdown(f"""
                    <div class='success-message'>
                        🎉 تم إرسال طلبك بنجاح! 🎉<br>
                        💰 إجمالي الطلب: {total:,} ج.م<br>
                        📞 سيتم التواصل معك للتأكيد والتوصيل<br>
                        🙏 شكراً لثقتك في VetFamily Alexandria
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    st.rerun()
            else:
                st.error("⚠️ برجاء إدخال جميع البيانات المطلوبة")
    
    with col_btn2:
        if st.button("🗑️ تفريغ السلة", use_container_width=True):
            st.session_state.shopping_cart = []
            st.rerun()

# =====================================
# نموذج التبني
# =====================================
if st.session_state.show_adoption_form:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%); 
                padding: 30px; border-radius: 20px; text-align: center; color: white;'>
        <h2 style='color: white;'>🏠 نموذج طلب التبني 🐾</h2>
        <p style='font-size: 1.1rem;'>ساعد حيوان أليف في إيجاد منزل دافئ</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("adoption_form"):
        st.write("### 👤 بياناتك الشخصية")
        
        col1, col2 = st.columns(2)
        
        with col1:
            adopt_name = st.text_input("الاسم الكامل *")
            adopt_phone = st.text_input("رقم الواتساب *")
        
        with col2:
            adopt_address = st.text_input("العنوان الكامل *")
            adopt_home = st.selectbox("نوع السكن:", ["شقة", "فيلا", "منزل مستقل", "آخر"])
        
        st.write("### 🐾 بيانات الحيوان المرغوب")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pet_type = st.selectbox("نوع الحيوان *:", 
                ["قطة 🐱", "كلب 🐕", "طائر 🐦", "أرنب 🐰", "سلحفاة 🐢", "أخرى"])
        
        with col2:
            pet_age = st.selectbox("العمر المفضل:",
                ["صغير (أقل من سنة)", "متوسط (1-3 سنوات)", "كبير (أكثر من 3 سنوات)", "لا يهم"])
        
        adopt_experience = st.radio("هل لديك خبرة سابقة في تربية الحيوانات؟",
            ["نعم، لدي خبرة", "لا، هذه أول مرة", "لدي خبرة بسيطة"])
        
        adopt_notes = st.text_area("ملاحظات أو متطلبات خاصة:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            submitted = st.form_submit_button("📝 إرسال الطلب", use_container_width=True, type="primary")
        
        with col2:
            cancelled = st.form_submit_button("❌ إلغاء", use_container_width=True)
        
        if submitted:
            if adopt_name and adopt_phone and adopt_address:
                adoption_info = {
                    "name": adopt_name,
                    "phone": adopt_phone,
                    "address": adopt_address,
                    "home_type": adopt_home,
                    "pet_type": pet_type,
                    "pet_age": pet_age,
                    "experience": adopt_experience,
                    "notes": adopt_notes
                }
                
                if save_adoption_request(adoption_info):
                    st.markdown("""
                    <div class='success-message'>
                        🎉 تم إرسال طلب التبني بنجاح! 🏠<br>
                        سيتم التواصل معك قريباً لترتيب الزيارة<br>
                        شكراً لك على منح حيوان أليف فرصة حياة جديدة 💚
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    st.session_state.show_adoption_form = False
                    st.rerun()
            else:
                st.error("⚠️ برجاء إدخال جميع البيانات المطلوبة")
        
        if cancelled:
            st.session_state.show_adoption_form = False
            st.rerun()

# =====================================
# الشريط الجانبي
# =====================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2 style='color: white;'>🐾 VetFamily</h2>
        <p style='color: white;'>الإسكندرية</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # السلة
    st.write("### 🛒 سلة التسوق")
    
    if st.session_state.shopping_cart:
        total_cart = 0
        for item in st.session_state.shopping_cart:
            st.write(f"**{item['name']}**")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                new_qty = st.number_input(
                    "الكمية:",
                    min_value=1,
                    max_value=item['stock'],
                    value=item['quantity'],
                    key=f"cart_qty_{item['id']}",
                    label_visibility="collapsed"
                )
                
                if new_qty != item['quantity']:
                    update_cart_quantity(item['id'], new_qty)
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"remove_{item['id']}"):
                    remove_from_cart(item['id'])
                    st.rerun()
            
            item_total = item['price'] * item['quantity']
            total_cart += item_total
            
            st.write(f"{item['quantity']} × {item['price']} = {item_total} ج.م")
            st.markdown("---")
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 15px; border-radius: 10px; text-align: center; color: white;'>
            <h3 style='margin: 0; color: white;'>💰 الإجمالي</h3>
            <h2 style='margin: 10px 0 0 0; color: white;'>{total_cart:,} ج.م</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ تفريغ السلة", use_container_width=True):
            st.session_state.shopping_cart = []
            st.rerun()
    else:
        st.info("السلة فارغة")
    
    st.markdown("---")
    
    # معلومات الاتصال
    st.write("### 📞 تواصل معنا")
    st.markdown("""
    - **📍** كرموز - الإسكندرية
    - **📞** 01xxxxxxxxx
    - **💬** واتساب
    - **🕐** 9 ص - 9 م (يومياً)
    """)
    
    st.markdown("---")
    
    # تسجيل دخول المدير
    if not st.session_state.is_logged_in:
        st.write("### 🔐 دخول المدير")
        
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم:", key="login_user")
            password = st.text_input("كلمة المرور:", type="password", key="login_pass")
            
            if st.form_submit_button("🔓 دخول", use_container_width=True):
                if check_login(username, password):
                    st.session_state.is_logged_in = True
                    st.success("✅ تم الدخول بنجاح")
                    st.rerun()
                else:
                    st.error("❌ خطأ في البيانات")
    else:
        st.success("✅ مسجل دخول كمدير")
        
        cairo_time = get_cairo_time()
        st.info(f"🕐 {cairo_time.strftime('%H:%M')}")
        
        # إحصائيات سريعة
        st.metric("📦 الطلبات", len(st.session_state.product_orders))
        st.metric("💳 الاشتراكات", len(st.session_state.subscriptions))
        st.metric("🏠 التبني", len(st.session_state.adoption_requests))
        st.metric("🔔 الإشعارات", len(st.session_state.notifications))

# =====================================
# الفوتر
# =====================================
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; color: white; margin-top: 50px;'>
    <h3 style='color: white;'>🐾 VetFamily Alexandria 🐾</h3>
    <p>مركز الرعاية البيطرية المتكاملة</p>
    <p style='font-size: 0.9rem; margin-top: 15px;'>
        📍 كرموز - الإسكندرية | 📞 01xxxxxxxxx | 💬 واتساب<br>
        © 2024 VetFamily Alexandria. جميع الحقوق محفوظة.
    </p>
</div>
""", unsafe_allow_html=True)