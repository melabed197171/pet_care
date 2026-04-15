import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# إعداد الصفحة وتصحيح الخطأ البرمجي في التنسيق
st.set_page_config(page_title="VetFamily Alexandria", layout="wide")

# رابط الجدول (تأكد أن صلاحية الرابط هي "محرر" Editor من جوجل شيت)
URL = "https://docs.google.com/spreadsheets/d/1kQ1junWnmyfwKPYj-Jm2QeCLlJ4dwmiMXkystV8dc7k/edit?usp=sharing"

# الاتصال بجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

def save_to_sheets(name, phone, product):
    try:
        # قراءة البيانات الحالية
        existing_data = conn.read(spreadsheet=URL)
        # إنشاء السطر الجديد
        new_data = pd.DataFrame([{
            "التاريخ": datetime.now(pytz.timezone('Africa/Cairo')).strftime("%Y-%m-%d %H:%M"),
            "اسم العميل": name,
            "المنتج": product,
            "رقم الهاتف": phone
        }])
        # الدمج والتحديث
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        conn.update(spreadsheet=URL, data=updated_df)
        return True
    except Exception as e:
        st.error(f"حدث خطأ في الحفظ: {e}")
        return False

# تصميم الواجهة - تم إصلاح كود الـ CSS هنا
st.markdown("""
<style>
    .header-box {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 30px; border-radius: 15px; color: white; text-align: center;
    }
    .card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>🐾 VetFamily Alexandria</h1><p>مركز الرعاية المتكاملة</p></div>', unsafe_allow_html=True)

# عرض المنتجات (مثال)
st.write("## 🛒 متجرنا")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card"><h3>رويال كانين - قطط</h3><h2>450 ج.م</h2></div>', unsafe_allow_html=True)
    with st.expander("📝 اطلب الآن"):
        name = st.text_input("الاسم", key="name1")
        phone = st.text_input("رقم الموبايل", key="phone1")
        if st.button("تأكيد الحفظ", key="btn1"):
            if name and phone:
                if save_to_sheets(name, phone, "رويال كانين قطط"):
                    st.success("✅ تم حفظ الطلب في جدول جوجل!")
                    st.balloons()
            else:
                st.warning("يرجى ملء البيانات")

# الفوتر
st.markdown("---")
st.caption("VetFamily Alexandria - 2026")
        f"💰 السعر: {product['price']} ج.م\n"
        f"📦 الوحدة: {product['unit']}\n\n"
        f"برجاء التواصل لتأكيد الطلب والتوصيل 🙏"
    )

def package_wa_msg(pkg_name, pkg_data):
    features = "\n".join([f"✅ {f}" for f in pkg_data['features']])
    return wa_link(
        f"مرحباً VetFamily 🐾\n"
        f"أود الاشتراك في:\n\n"
        f"{pkg_data['icon']} {pkg_name}\n"
        f"💰 السعر: {pkg_data['price']} ج.م / {pkg_data['duration']}\n\n"
        f"المميزات:\n{features}\n\n"
        f"برجاء التواصل لتأكيد الاشتراك 🙏"
    )

def adoption_wa_msg(pet_type=""):
    return wa_link(
        f"مرحباً VetFamily 🐾\n"
        f"أود التبني 🏠\n\n"
        f"نوع الحيوان المرغوب: {pet_type}\n\n"
        f"برجاء التواصل لاستكمال الإجراءات 🙏"
    )

def get_badge_html(badges):
    m = {
        "new":("جديد","badge-new"),
        "sale":("عرض","badge-sale"),
        "popular":("الأكثر مبيعاً","badge-popular"),
        "premium":("بريميوم","badge-premium"),
        "recommended":("موصى به","badge-recommended"),
        "vet":("موصى طبياً","badge-vet"),
    }
    return "".join(
        f'<span class="product-badge {c}">{t}</span>'
        for b in badges if b in m for t, c in [m[b]]
    )

# =============================================
# حفظ طلبات التبني (للأرشيف فقط)
# =============================================
def save_adoption(info):
    try:
        ct = get_now()
        req = {
            "id":             len(st.session_state.db["adoption"]) + 1,
            "date":           ct.strftime("%Y-%m-%d"),
            "time":           ct.strftime("%H:%M:%S"),
            "customer_name":  info["name"],
            "customer_phone": info["phone"],
            "customer_address": info.get("address", ""),
            "pet_type":       info["pet_type"],
            "pet_age":        info.get("pet_age", ""),
            "home_type":      info.get("home_type", ""),
            "experience":     info.get("experience", ""),
            "notes":          info.get("notes", ""),
            "status":         "تم التواصل عبر الواتساب"
        }
        st.session_state.db["adoption"].append(req)
        save_db()
        return True
    except Exception as e:
        st.error(f"خطأ: {e}")
        return False

# =============================================
# بيانات المنتجات
# =============================================
if "products" not in st.session_state:
    st.session_state.products = {
        "طعام_القطط_الجاف": [
            {"id":1,"name":"رويال كانين - قطط بالغة 2 كجم","desc":"طعام متوازن للقطط البالغة من 1-7 سنوات","price":450,"cost":320,"icon":"🐱","stock":25,"unit":"كيس 2 كجم","brand":"Royal Canin","country":"فرنسا","features":["بروتين 32%","فيتامينات متكاملة","أوميجا 3 و 6"],"badges":["popular","premium"]},
            {"id":2,"name":"رويال كانين كيتن - قطط صغيرة 1.5 كجم","desc":"تركيبة للقطط الصغيرة من شهرين إلى 12 شهر","price":400,"cost":280,"icon":"🐈","stock":18,"unit":"كيس 1.5 كجم","brand":"Royal Canin","country":"فرنسا","features":["سهل الهضم","دعم المناعة","تقوية العظام"],"badges":["new","recommended"]},
            {"id":3,"name":"بريميوم كات - قطط 1 كجم","desc":"طعام محلي عالي الجودة بسعر اقتصادي","price":70,"cost":45,"icon":"🐱","stock":40,"unit":"كيس 1 كجم","brand":"Premium Cat","country":"مصر","features":["جودة جيدة","سعر مناسب","بروتين 28%"],"badges":["sale"]},
        ],
        "طعام_القطط_الرطب": [
            {"id":5,"name":"ويسكاس - تونة في جيلي 85 جم","desc":"وجبة رطبة لذيذة من التونة الطبيعية","price":25,"cost":15,"icon":"🐟","stock":100,"unit":"علبة 85 جم","brand":"Whiskas","country":"تايلاند","features":["تونة طبيعية","غني بالبروتين","رطوبة عالية"],"badges":["popular"]},
            {"id":6,"name":"شيبا - دجاج مشوي 85 جم","desc":"وجبة فاخرة من الدجاج المشوي","price":30,"cost":20,"icon":"🍗","stock":80,"unit":"علبة 85 جم","brand":"Sheba","country":"تايلاند","features":["دجاج مشوي","طعم لذيذ","قطع كبيرة"],"badges":["premium"]},
        ],
        "طعام_الكلاب_الجاف": [
            {"id":8,"name":"رويال كانين - كلاب كبيرة 3 كجم","desc":"تركيبة للكلاب الكبيرة فوق 25 كجم","price":550,"cost":380,"icon":"🐕","stock":20,"unit":"كيس 3 كجم","brand":"Royal Canin","country":"فرنسا","features":["دعم المفاصل","بروتين 30%","طاقة عالية"],"badges":["popular","premium"]},
            {"id":9,"name":"بيديجري - كلاب بالغة 2.5 كجم","desc":"طعام متوازن للكلاب البالغة","price":320,"cost":220,"icon":"🐕","stock":30,"unit":"كيس 2.5 كجم","brand":"Pedigree","country":"تايلاند","features":["فيتامينات متكاملة","دجاج حقيقي","سهل الهضم"],"badges":["sale"]},
        ],
        "الرمل_والنظافة": [
            {"id":11,"name":"كات ساند - رمل متكتل 5 كجم","desc":"رمل بنتونايت برائحة اللافندر","price":90,"cost":55,"icon":"🏖️","stock":50,"unit":"كيس 5 كجم","brand":"Cat Sand","country":"مصر","features":["سريع التكتل","امتصاص فائق","معطر"],"badges":["popular","sale"]},
            {"id":13,"name":"صندوق رمل قطط مع غطاء","desc":"صندوق بلاستيك عالي الجودة مع مجرفة","price":150,"cost":90,"icon":"🚽","stock":15,"unit":"قطعة","brand":"Pet Home","country":"الصين","features":["سهل التنظيف","مع مجرفة","غطاء مانع للروائح"],"badges":["new"]},
        ],
        "الصحة_والأدوية": [
            {"id":14,"name":"شامبو بيتكين الطبي 500 مل","desc":"شامبو طبي مضاد للحساسية والبراغيث","price":130,"cost":70,"icon":"🧴","stock":30,"unit":"زجاجة 500 مل","brand":"Petkin","country":"مصر","features":["مضاد حساسية","مضاد براغيث","آمن تماماً"],"badges":["vet"]},
            {"id":15,"name":"فرونت لاين - قطرات ضد البراغيث","desc":"أقوى علاج للبراغيث والقراد","price":150,"cost":85,"icon":"💧","stock":20,"unit":"أمبول واحد","brand":"Frontline","country":"فرنسا","features":["حماية شهرية","فعال 100%","سهل الاستخدام"],"badges":["premium","vet"]},
            {"id":18,"name":"قطرة عين فيتامين A","desc":"قطرة مطهرة لالتهابات العين","price":85,"cost":45,"icon":"👁️","stock":18,"unit":"زجاجة 15 مل","brand":"Pet Vision","country":"مصر","features":["مطهرة","آمنة","سريعة المفعول"],"badges":["vet"]},
        ],
        "الإكسسوارات": [
            {"id":19,"name":"طوق جلد طبيعي مع جرس","desc":"طوق جلد أصلي قابل للتعديل","price":80,"cost":35,"icon":"🎀","stock":35,"unit":"قطعة","brand":"Pet Style","country":"تركيا","features":["جلد طبيعي","قابل للتعديل","جرس معدني"],"badges":["popular"]},
            {"id":20,"name":"سلسلة مشي نايلون قوية","desc":"سلسلة للكلاب المتوسطة والكبيرة","price":90,"cost":40,"icon":"🦮","stock":25,"unit":"قطعة 1.5 متر","brand":"Strong Lead","country":"الصين","features":["نايلون قوي","مقبض مريح","طول 1.5 م"],"badges":["sale"]},
            {"id":21,"name":"حقيبة نقل فاخرة","desc":"حقيبة آمنة للسفر والعيادات","price":350,"cost":200,"icon":"🎒","stock":10,"unit":"مقاس متوسط","brand":"Travel Pet","country":"الصين","features":["تهوية ممتازة","خفيفة الوزن","قابلة للطي"],"badges":["premium"]},
        ],
        "الألعاب": [
            {"id":23,"name":"فأر إلكتروني تفاعلي","desc":"يتحرك تلقائياً لتسلية القطط","price":120,"cost":60,"icon":"🐭","stock":20,"unit":"قطعة","brand":"Smart Toy","country":"الصين","features":["حركة تلقائية","آمنة","شحن USB"],"badges":["new","popular"]},
            {"id":24,"name":"كرة مطاطية بجرس","desc":"كرة ملونة بجرس داخلي","price":25,"cost":12,"icon":"⚽","stock":50,"unit":"قطعة","brand":"Play Ball","country":"مصر","features":["مطاط آمن","جرس داخلي","ألوان زاهية"],"badges":["sale"]},
        ],
        "العناية_والتجميل": [
            {"id":30,"name":"فرشاة تمشيط احترافية","desc":"فرشاة مزدوجة لفك التشابك","price":50,"cost":22,"icon":"🪮","stock":20,"unit":"قطعة","brand":"Grooming Pro","country":"الصين","features":["أسنان ناعمة","مقبض مريح","للفراء الطويل والقصير"],"badges":["recommended"]},
            {"id":31,"name":"مقص أظافر احترافي","desc":"مقص آمن بحماية من القص الزائد","price":75,"cost":35,"icon":"✂️","stock":15,"unit":"قطعة","brand":"Nail Clipper","country":"ألمانيا","features":["شفرة حادة","واقي أمان","مقبض مطاطي"],"badges":["premium"]},
            {"id":32,"name":"مناديل تنظيف معطرة","desc":"مناديل مبللة للتنظيف السريع","price":45,"cost":22,"icon":"🧻","stock":35,"unit":"علبة 80 منديل","brand":"Fresh Wipes","country":"مصر","features":["آمنة 100%","معطرة","مضادة للبكتيريا"],"badges":["popular"]},
        ],
        "الفيتامينات_والمكملات": [
            {"id":34,"name":"مالتي فيتامين للقطط","desc":"فيتامينات متعددة لصحة أفضل","price":160,"cost":90,"icon":"💊","stock":15,"unit":"علبة 60 قرص","brand":"Pet Vitamin","country":"أمريكا","features":["فيتامينات متكاملة","تقوية المناعة","طعم سمك"],"badges":["vet"]},
        ],
    }

if "packages" not in st.session_state:
    st.session_state.packages = {
        "الباقة البرونزية": {
            "price":200,"duration":"شهرياً","desc":"باقة أساسية للرعاية الشهرية",
            "icon":"🥉","color":"#CD7F32",
            "features":["استشارتان هاتفيتان","استشارة واتساب","خصم 10% على الأدوية"]
        },
        "الباقة الفضية": {
            "price":400,"duration":"شهرياً","desc":"رعاية متقدمة مع فحوصات دورية",
            "icon":"🥈","color":"#C0C0C0",
            "features":["4 استشارات","فحص شامل مجاني","خصم 20% على المنتجات"]
        },
        "الباقة الذهبية": {
            "price":700,"duration":"شهرياً","desc":"رعاية VIP شاملة",
            "icon":"🥇","color":"#FFD700",
            "features":["استشارات غير محدودة","زيارة منزلية","خصم 30% على المنتجات"]
        },
        "الباقة الماسية": {
            "price":1200,"duration":"شهرياً","desc":"الأشمل - رعاية ملكية",
            "icon":"💎","color":"#B9F2FF",
            "features":["كل مميزات الذهبية","زيارتان منزليتان","خصم 40% على كل شيء"]
        },
    }

# =============================================
# بطاقة المنتج (بدون سلة - فقط واتساب)
# =============================================
def display_product_card(product):
    if product["stock"] > 10:
        sc, st_txt = "in-stock",  f"✅ متوفر ({product['stock']})"
    elif product["stock"] > 0:
        sc, st_txt = "low-stock", f"⚠️ محدود ({product['stock']})"
    else:
        sc, st_txt = "out-stock", "❌ نفذ المخزون"

    st.markdown(f"""
    <div class="product-card">
        <div class="product-image">{product['icon']}</div>
        <div class="product-name">{product['name']}</div>
        <div>{get_badge_html(product.get('badges', []))}</div>
        <div class="product-description">{product['desc']}</div>
        <div class="product-price">{product['price']} ج.م</div>
        <div style="font-size:0.8rem;color:#718096;margin-top:5px;">
            📦 {product['unit']} | 🏷️ {product['brand']} | 🌍 {product['country']}
        </div>
        <div class="stock-badge {sc}" style="margin-top:10px;">{st_txt}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 التفاصيل والمميزات"):
        for f in product["features"]:
            st.write(f"✓ {f}")

    # ===== زر الواتساب مباشرة =====
    if product["stock"] > 0:
        st.link_button(
            f"📱 اطلب عبر الواتساب - {product['price']} ج.م",
            product_wa_msg(product),
            use_container_width=True
        )
    else:
        st.button("❌ نفذ من المخزون", disabled=True, use_container_width=True)

    # عرض التكلفة والربح للمدير فقط
    if st.session_state.is_logged_in:
        profit = product["price"] - product["cost"]
        c1, c2 = st.columns(2)
        with c1: st.caption(f"💰 التكلفة: {product['cost']} ج")
        with c2: st.caption(f"📈 الربح: {profit} ج (+{profit/product['cost']*100:.0f}%)")


def render_item(name, price, desc, is_medical=False):
    ac  = "#d9534f" if is_medical else "#28a745"
    msg = urllib.parse.quote(f"مرحباً VetFamily 🐾\nأود طلب: {name}\nالسعر: {price}\nبرجاء التواصل لتأكيد الطلب 🙏")
    st.markdown(f"""
    <div class="item-box" style="border-right:8px solid {ac};">
        <div class="item-title">{name}</div>
        <div class="item-desc">{desc}</div>
        <div class="item-price" style="color:{ac};">السعر: {price}</div>
    </div>""", unsafe_allow_html=True)
    st.link_button(
        f"📱 اطلب عبر الواتساب",
        f"https://wa.me/{WHATSAPP_NUMBER}?text={msg}",
        use_container_width=True
    )

# =============================================
# الهيدر الرئيسي
# =============================================
st.markdown("""
<div class="main-header">
    <h1>🐾 VetFamily Alexandria 🐾</h1>
    <p>مركز الرعاية البيطرية المتكاملة - الإسكندرية</p>
    <p style="font-size:0.95rem;">
        🩺 أطباء متخصصون &nbsp;|&nbsp;
        🍖 منتجات أصلية &nbsp;|&nbsp;
        📱 اطلب عبر الواتساب مباشرة
    </p>
</div>
""", unsafe_allow_html=True)

# ===== شريط الأزرار =====
t1, t2, t3 = st.columns(3)

with t1:
    if st.button("❤️ أعجبني", use_container_width=True):
        st.balloons()
        st.success("شكراً لدعمك! 🙏")

with t2:
    if st.button("🏠 تبني الآن", use_container_width=True):
        st.session_state.show_adoption_form = not st.session_state.show_adoption_form
        st.rerun()

with t3:
    if st.button("🔐 المدير", use_container_width=True):
        st.session_state.show_login = not st.session_state.show_login
        st.rerun()

# ===== دخول المدير =====
if st.session_state.show_login and not st.session_state.is_logged_in:
    with st.expander("🔐 دخول لوحة التحكم", expanded=True):
        lc1, lc2, lc3 = st.columns([2, 2, 1])
        with lc1: lu = st.text_input("اسم المستخدم", key="lu")
        with lc2: lp = st.text_input("كلمة المرور", type="password", key="lp")
        with lc3:
            st.write("")
            if st.button("دخول 🔓", use_container_width=True):
                if check_login(lu, lp):
                    st.session_state.is_logged_in = True
                    st.session_state.show_login   = False
                    st.success("✅ تم الدخول")
                    st.rerun()
                else:
                    st.error("❌ خطأ في البيانات")

if st.session_state.is_logged_in:
    im1, im2, im3, im4 = st.columns(4)
    with im1: st.metric("📱 طلبات الواتساب", len(st.session_state.db.get("whatsapp_orders",[])))
    with im2: st.metric("💳 الاشتراكات",     len(st.session_state.db["subscriptions"]))
    with im3: st.metric("🏠 التبني",          len(st.session_state.db["adoption"]))
    with im4:
        if st.button("🔓 خروج", use_container_width=True):
            st.session_state.is_logged_in = False
            st.rerun()

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =============================================
# التبويبات
# =============================================
if st.session_state.is_logged_in:
    tabs = st.tabs([
        "🏪 المتجر","💎 الباقات","🩺 الاستشارات",
        "📊 لوحة التحكم","💳 الاشتراكات","🏠 التبني"
    ])
    tab_shop, tab_pkg, tab_con, tab_dash, tab_sub, tab_ado = tabs
else:
    tabs = st.tabs([
        "🏪 المتجر","💎 الباقات","🩺 الاستشارات","ℹ️ من نحن"
    ])
    tab_shop, tab_pkg, tab_con, tab_about = tabs

# ===== المتجر =====
with tab_shop:
    st.write("## 🛒 متجر المستلزمات البيطرية")
    st.markdown("""
    <div style="background:linear-gradient(135deg,#25d366,#128c7e);
                padding:15px;border-radius:15px;text-align:center;color:white;margin-bottom:20px;">
        <h3 style="margin:0;color:white;">📱 اطلب أي منتج عبر الواتساب مباشرة!</h3>
        <p style="margin:5px 0 0;font-size:0.95rem;">اضغط على زر الواتساب تحت أي منتج وسيتم التواصل معك فوراً</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="offers-title">🔥 عروض اليوم الحصرية</div>', unsafe_allow_html=True)
    daily_offers = [
        {"name":"📦 رويال كانين قطط 2 كجم", "price":"550 ج.م بدلاً من 650","desc":"عرض خاص لدعم صحة أليفك."},
        {"name":"🐱 رمل قطط كربون 5 لتر",   "price":"180 ج.م بدلاً من 220","desc":"أفضل حماية من الروائح."},
    ]
    oc = st.columns(len(daily_offers))
    for i, o in enumerate(daily_offers):
        with oc[i]: render_item(o["name"], o["price"], o["desc"])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns([2, 2, 1])
    with sc1: srch = st.text_input("🔍 ابحث:", placeholder="اسم المنتج أو الماركة...")
    with sc2: scat = st.selectbox("📂 الفئة:", ["الكل"] + list(st.session_state.products.keys()))
    with sc3: ssrt = st.selectbox("ترتيب:", ["الأحدث","السعر: الأقل","السعر: الأعلى"])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    for ck, prods in st.session_state.products.items():
        if scat != "الكل" and ck != scat: continue
        st.markdown(f"### 📦 {ck.replace('_',' ')}")
        fp = [p for p in prods if not srch or
              srch.lower() in p["name"].lower() or
              srch.lower() in p["brand"].lower()]
        if not fp: continue
        if ssrt == "السعر: الأقل":    fp = sorted(fp, key=lambda x: x["price"])
        elif ssrt == "السعر: الأعلى": fp = sorted(fp, key=lambda x: x["price"], reverse=True)
        cols = st.columns(3)
        for idx, prod in enumerate(fp):
            with cols[idx % 3]: display_product_card(prod)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ===== الباقات =====
with tab_pkg:
    st.write("## 💎 الباقات الطبية")
    st.markdown("""
    <div style="background:linear-gradient(135deg,#25d366,#128c7e);
                padding:15px;border-radius:15px;text-align:center;color:white;margin-bottom:20px;">
        <h3 style="margin:0;color:white;">📱 اشترك الآن عبر الواتساب مباشرة!</h3>
        <p style="margin:5px 0 0;font-size:0.95rem;">اضغط على زر الاشتراك وسيتم التواصل معك فوراً</p>
    </div>
    """, unsafe_allow_html=True)

    for pn, pd in st.session_state.packages.items():
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{pd['color']}22,{pd['color']}44);
                    padding:25px;border-radius:18px;margin:15px 0;
                    border:3px solid {pd['color']};text-align:center;">
            <h2 style="font-weight:900;">{pd['icon']} {pn}</h2>
            <p style="color:#555;">{pd['desc']}</p>
            <h1 style="color:{pd['color']};font-weight:900;">{pd['price']} ج.م / {pd['duration']}</h1>
        </div>""", unsafe_allow_html=True)

        pc1, pc2 = st.columns([2, 1])
        with pc1:
            st.write("#### ✨ المميزات:")
            for f in pd["features"]:
                st.write(f"✅ {f}")
        with pc2:
            st.markdown("<br>", unsafe_allow_html=True)
            # زر الواتساب للاشتراك
            st.link_button(
                f"📱 اشترك في {pn} عبر الواتساب",
                package_wa_msg(pn, pd),
                use_container_width=True
            )
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ===== الاستشارات =====
with tab_con:
    st.write("## 🩺 الاستشارات البيطرية")
    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:25px;border-radius:18px;color:white;">
            <h3 style="color:white;">👨‍⚕️ فريقنا الطبي</h3>
            <ul style="line-height:2;">
                <li>أطباء بيطريون معتمدون</li>
                <li>خبرة واسعة في جميع التخصصات</li>
                <li>استشارات على مدار الساعة</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with cc2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#f093fb,#f5576c);padding:25px;border-radius:18px;color:white;">
            <h3 style="color:white;">📋 خدماتنا</h3>
            <ul style="line-height:2;">
                <li>الكشف والفحص الشامل</li>
                <li>التطعيمات والتحصينات</li>
                <li>العمليات الجراحية</li>
                <li>التحاليل الطبية</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # أسعار الخدمات مع زر واتساب لكل خدمة
    svcs = [
        ("📞","استشارة هاتفية","مجاني"),
        ("🏥","استشارة بالعيادة","100 ج.م"),
        ("💉","كشف + تطعيم","150 ج.م"),
        ("🏠","زيارة منزلية","250 ج.م"),
        ("🔬","فحص شامل","300 ج.م"),
        ("⚕️","عملية صغرى","500 ج.م+"),
    ]
    sv_cols = st.columns(3)
    for idx, (ico, nm, pr) in enumerate(svcs):
        with sv_cols[idx % 3]:
            st.markdown(f"""
            <div style="background:white;padding:18px;border-radius:14px;
                        text-align:center;border:2px solid #667eea;margin:8px 0;">
                <div style="font-size:2.5rem;">{ico}</div>
                <h4 style="color:#2d3748;margin:8px 0;">{nm}</h4>
                <h3 style="color:#667eea;margin:0;">{pr}</h3>
            </div>""", unsafe_allow_html=True)
            msg = urllib.parse.quote(f"مرحباً VetFamily 🐾\nأود حجز: {nm}\nالسعر: {pr}\nبرجاء التواصل 🙏")
            st.link_button(
                "📱 احجز عبر الواتساب",
                f"https://wa.me/{WHATSAPP_NUMBER}?text={msg}",
                use_container_width=True
            )

# ===== لوحة التحكم للمدير =====
if st.session_state.is_logged_in:
    with tab_dash:
        st.write("## 📊 لوحة التحكم")
        ct = get_now()
        st.info(f"🕐 {ct.strftime('%Y-%m-%d %H:%M:%S')}")

        dm1, dm2, dm3 = st.columns(3)
        with dm1: st.metric("💳 الاشتراكات", len(st.session_state.db["subscriptions"]))
        with dm2: st.metric("🏠 طلبات التبني", len(st.session_state.db["adoption"]))
        with dm3:
            st.download_button(
                label="📥 تحميل قاعدة البيانات",
                data=json.dumps(st.session_state.db, ensure_ascii=False, indent=2),
                file_name=f"vetfamily_{ct.strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

        st.markdown("""
        <div style="background:#fff3cd;border:2px solid #ffc107;border-radius:15px;padding:20px;margin:20px 0;">
            <h4 style="color:#856404;">📱 ملاحظة هامة</h4>
            <p style="color:#856404;margin:0;">
                جميع الطلبات تصلك مباشرة على الواتساب من العملاء.<br>
                الاشتراكات وطلبات التبني مسجلة هنا للأرشيف.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab_sub:
        st.write("## 💳 الاشتراكات المسجلة")
        if st.session_state.db["subscriptions"]:
            for s in reversed(st.session_state.db["subscriptions"]):
                with st.expander(f"{s['package_name']} - {s['customer_name']} | {s['price']} ج.م | {s['date']}"):
                    st.write(f"**📞** {s['customer_phone']}")
                    st.write(f"**💰** {s['price']} ج.م / {s['duration']}")
                    st.write(f"**📅** {s['start_date']} ← {s['end_date']}")
                    st.write(f"**📍** {s.get('customer_address','')}")
        else:
            st.info("لا توجد اشتراكات مسجلة بعد")

    with tab_ado:
        st.write("## 🏠 طلبات التبني المسجلة")
        if st.session_state.db["adoption"]:
            for r in reversed(st.session_state.db["adoption"]):
                with st.expander(f"#{r['id']} - {r['customer_name']} | {r['pet_type']} | {r['date']}"):
                    st.write(f"**📞** {r['customer_phone']}")
                    st.write(f"**📍** {r['customer_address']}")
                    st.write(f"**🐾** {r['pet_type']} | **🎂** {r.get('pet_age','')}")
                    st.write(f"**🏡** {r.get('home_type','')} | **📚** {r.get('experience','')}")
                    if r.get("notes"): st.write(f"**📝** {r['notes']}")
        else:
            st.info("لا توجد طلبات تبني مسجلة بعد")

else:
    with tab_about:
        st.write("## ℹ️ عن VetFamily Alexandria")
        st.markdown("""
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                    padding:35px;border-radius:20px;color:white;text-align:center;">
            <h2 style="color:white;">🐾 عائلتك البيطرية في الإسكندرية</h2>
            <p style="font-size:1.1rem;">مركز متكامل للرعاية البيطرية والمستلزمات</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        ab_cols = st.columns(3)
        for col, (ico, ttl, dsc) in zip(ab_cols, [
            ("👨‍⚕️","أطباء متخصصون","خبرة واسعة في جميع التخصصات"),
            ("🏆","منتجات أصلية","100% أصلية من أفضل العلامات العالمية"),
            ("📱","طلب سهل وسريع","اطلب عبر الواتساب مباشرة بضغطة واحدة"),
        ]):
            with col:
                st.markdown(f"""
                <div style="text-align:center;padding:25px;background:white;
                            border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,0.08);">
                    <div style="font-size:3.5rem;">{ico}</div>
                    <h3 style="font-weight:900;">{ttl}</h3>
                    <p>{dsc}</p>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        ac1, ac2 = st.columns(2)
        with ac1:
            st.markdown("- **📍** محرم بك - الإسكندرية\n- **📞** 01022395878")
        with ac2:
            st.markdown("- **🕐** يومياً 9 ص - 9 م\n- **💬** واتساب متاح دائماً")
        st.link_button("👍 تابعنا على فيسبوك", FACEBOOK_URL, use_container_width=True)

# =============================================
# نموذج التبني (مع زر الواتساب)
# =============================================
if st.session_state.show_adoption_form:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#38ef7d,#11998e);
                padding:20px;border-radius:18px;text-align:center;color:white;margin-bottom:15px;">
        <h2 style="color:white;margin:0;">🏠 طلب التبني 🐾</h2>
        <p style="color:white;margin:8px 0 0;">ساعد حيوان أليف في إيجاد منزل دافئ</p>
    </div>""", unsafe_allow_html=True)

    # اختيار نوع الحيوان أولاً لبناء رسالة الواتساب
    pet_types = ["قطة 🐱","كلب 🐕","طائر 🐦","أرنب 🐰","أخرى"]
    selected_pet = st.selectbox("🐾 ما نوع الحيوان الذي تريد تبنيه؟", pet_types)

    # زر الواتساب المباشر
    st.link_button(
        f"📱 تواصل معنا الآن عبر الواتساب لتبني {selected_pet}",
        adoption_wa_msg(selected_pet),
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**أو أترك بياناتك وسنتواصل معك:**")

    with st.form("adoption_form"):
        af1, af2 = st.columns(2)
        with af1:
            an = st.text_input("الاسم الكامل *")
            ap = st.text_input("رقم الواتساب *")
        with af2:
            aa = st.text_input("العنوان *")
            ah = st.selectbox("نوع السكن:", ["شقة","فيلا","منزل مستقل","آخر"])
        af3, af4 = st.columns(2)
        with af3: pa = st.selectbox("العمر المفضل:", ["صغير","متوسط","كبير","لا يهم"])
        with af4: ae = st.radio("خبرة سابقة؟", ["نعم","لا","خبرة بسيطة"])
        ano = st.text_area("ملاحظات إضافية:")

        af5, af6 = st.columns(2)
        with af5: sub = st.form_submit_button("📝 إرسال البيانات", use_container_width=True, type="primary")
        with af6: can = st.form_submit_button("❌ إغلاق", use_container_width=True)

        if sub:
            if an and ap and aa:
                if save_adoption({
                    "name":an,"phone":ap,"address":aa,"home_type":ah,
                    "pet_type":selected_pet,"pet_age":pa,
                    "experience":ae,"notes":ano
                }):
                    st.markdown("""
                    <div class="success-message">
                        🎉 تم تسجيل طلبك بنجاح!<br>
                        سيتم التواصل معك قريباً على الواتساب 💚<br>
                        أو تواصل معنا مباشرة الآن عبر الزر أعلاه
                    </div>""", unsafe_allow_html=True)
                    st.balloons()
                    st.session_state.show_adoption_form = False
                    st.rerun()
            else:
                st.error("⚠️ أدخل الاسم والهاتف والعنوان")
        if can:
            st.session_state.show_adoption_form = False
            st.rerun()

# =============================================
# الفوتر
# =============================================
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;padding:25px;
            background:linear-gradient(135deg,#1e3c72,#2a5298);
            border-radius:18px;color:white;margin-top:20px;">
    <h3 style="color:white;font-weight:900;">🐾 VetFamily Alexandria 🐾</h3>
    <p style="margin:5px 0;">مركز الرعاية البيطرية المتكاملة</p>
    <p style="font-size:0.85rem;margin-top:10px;color:rgba(255,255,255,0.8);">
        📍 محرم بك - الإسكندرية &nbsp;|&nbsp;
        📞 01022395878 &nbsp;|&nbsp;
        📱 اطلب عبر الواتساب<br>
        🕐 يومياً من 9 ص إلى 9 م<br>
        © 2024 VetFamily Alexandria
    </p>
</div>""", unsafe_allow_html=True)
