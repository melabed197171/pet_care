import streamlit as st
from PIL import Image
st.set_page_config(page_title="منصة أصدقاء الحيوان", page_icon="🐾", layout="centered")
try:
    image = Image.open('cat.png')
    st.image(image, width=300)
except FileNotFoundError:
    st.warning("cat.png")
# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="مركز العناية المتكاملة بالحيوانات", page_icon="🐾", layout="wide")

# العنوان الرئيسي والتعريف بالفريق
st.title("🐾 مركز العناية المتكاملة البيطرية ")
st.markdown("""
    **تحت إشراف نخبة من:**
    * 🩺 أطباء بيطريين متخصصين
    * 🍎 مهندسي سلامة غذاء
    * ⚙️ مهندسي أجهزة طبية
""")

# إنشاء تبويبات (Tabs) لتنظيم الخدمات
tab1, tab2, tab3, tab4 = st.tabs(["الاستشارات واللقاحات", "الغذاء والمستلزمات", "التكنولوجيا والأجهزة", "طلب خدمة"])

# القسم الأول: الاستشارات والطب البيطري
with tab1:
    st.header("🩺 الخدمات الطبية والوقائية")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("الأدوية واللقاحات")
        st.info("نوفر أحدث اللقاحات الدورية والبروتوكولات العلاجية المعتمدة.")
    with col2:
        st.subheader("إرشادات طبية")
        st.write("- جدول التطعيمات السنوي.")
        st.write("- الإسعافات الأولية للحيوانات الأليفة.")

# القسم الثاني: سلامة الغذاء والمستلزمات
with tab2:
    st.header("🍎 التغذية والمستلزمات")
    st.write("نركز على تقديم **طعام صحي** خاضع لرقابة مهندسي سلامة الغذاء.")
    items = ["طعام جاف (Dry Food)", "مكملات غذائية", "أدوات العناية الشخصية", "ألعاب ترفيهية"]
    st.multiselect("تصفح الأصناف المتاحة:", items)

# القسم الثالث: التكنولوجيا (تحت إشراف مهندس الأجهزة)
with tab3:
    st.header("⚙️ الحلول التقنية والأجهزة")
    st.success("أجهزة تتبع وحماية متطورة بإشراف هندسي طبي.")
    col_a, col_b = st.columns(2)
    col_a.metric("أجهزة التتبع (GPS)", "دقة عالية")
    col_b.metric("أجهزة مراقبة الصحة", "تنبيه فوري")
    st.image("https://placeholder.com", caption="أحدث تقنيات حماية الحيوانات")

# القسم الرابع: التواصل وطلب الاستشارة
with tab4:
    st.header("📅 احجز استشارتك الآن")
    with st.form("consultation_form"):
        name = st.text_input("الاسم ")
        pet_type = st.selectbox("نوع الحيوان", ["قطط", "كلاب", "طيور", "أخرى"])
        service = st.radio("نوع الخدمة المطلوبة", ["استشارة طبية", "طلب دواء/لقاح", "جهاز تتبع", "تنسيق نظام غذائي"])
        details = st.text_area("تفاصيل الحالة أو الطلب")
        
        submitted = st.form_submit_button("إرسال الطلب")
        if submitted:
            st.balloons()
            st.success(f"شكراً أستاذ {name}، سيقوم المختص (طبيب أو مهندس) بالتواصل معك قريباً.")

# تذييل الصفحة
st.sidebar.markdown("---")
st.sidebar.write("📞 **للطوارئ:** 000-000-000")
st.sidebar.write("📍 **موقعنا:** متاحون لخدمتكم أينما كنتم.")
import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="منصة الرعاية المتكاملة", page_icon="🐾", layout="wide")

# تنسيق واجهة المستخدم (CSS)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
    }
    .price-tag {
        font-size: 24px;
        color: #2e7d32;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🐾 مركز العناية المتكاملة البيطرية ")
st.subheader("إشراف نخبة من الأطباء والمهندسين لخدمة أليفك")

# 1. قسم اختيار الباقات الجاهزة
st.header("💳 اختر باقتك المفضلة")
col1, col2, col3 = st.columns(3)

# تعريف متغير في 'session_state' لحفظ الاختيار
if 'final_plan' not in st.session_state:
    st.session_state.final_plan = "لم يتم الاختيار بعد"
if 'total_price' not in st.session_state:
    st.session_state.total_price = 0

with col1:
    st.info("### 💎 الباقة الماسية")
    st.write("رعاية شاملة + جهاز تتبع + نظام غذائي")
    st.markdown("<p class='price-tag'>5000 ج.م / سنة</p>", unsafe_allow_html=True)
    if st.button("تفعيل الباقة الماسية"):
        st.session_state.final_plan = "الماسية"
        st.session_state.total_price = 5000

with col2:
    st.warning("### ✨ الباقة الذهبية")
    st.write("4 استشارات شهرياً + اللقاحات الأساسية")
    st.markdown("<p class='price-tag'>2500 ج.م / سنة</p>", unsafe_allow_html=True)
    if st.button("تفعيل الباقة الذهبية"):
        st.session_state.final_plan = "الذهبية"
        st.session_state.total_price = 2500

with col3:
    st.error("### 🛡️ الباقة الاقتصادية")
    st.write("استشارة شهرية + جدول تطعيمات")
    st.markdown("<p class='price-tag'>1000 ج.م / سنة</p>", unsafe_allow_html=True)
    if st.button("تفعيل الباقة الاقتصادية"):
        st.session_state.final_plan = "الاقتصادية"
        st.session_state.total_price = 1000

st.divider()

# 2. قسم الباقة الحرة (من اختيار العميل)
st.header("🎨 باقة من اختيارك (حسب الطلب)")
st.write("حدد الخدمات التي تحتاجها وسيقوم النظام بحساب التكلفة فوراً:")

services_db = {
    "استشارة طبية منزلية": 400,
    "لقاح السعار الدوري": 450,
    "جهاز تتبع GPS (تركيب مهندس)": 1800,
    "تصميم نظام غذائي (مهندس سلامة)": 600,
    "فحص دوري للأجهزة الطبية": 350,
    "صندوق مستلزمات عناية": 900
}

col_a, col_b = st.columns([2, 1])

with col_a:
    selected_items = st.multiselect("اختر من الخدمات التالية:", list(services_db.keys()))

with col_b:
    custom_total = sum(services_db[item] for item in selected_items)
    st.metric("إجمالي الباقة الحرة", f"{custom_total} ج.م")
    if st.button("تفعيل اختياراتي"):
        st.session_state.final_plan = "باقة حرة (مخصصة)"
        st.session_state.total_price = custom_total

st.divider()

# 3. نموذج إرسال الطلب النهائي
st.header("📝 إتمام الحجز")
with st.form("checkout_form"):
    st.write(f"📌 الباقة المختارة: **{st.session_state.final_plan}**")
    st.write(f"💰 التكلفة الإجمالية: **{st.session_state.total_price} ج.م**")
    
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("الاسم بالكامل")
        phone = st.text_input("رقم الواتساب")
    with c2:
        pet_type = st.text_input("نوع الحيوان (قط، كلب، إلخ)")
        address = st.text_input("العنوان (للمقابلات المنزلية)")
        
    submitted = st.form_submit_button("تأكيد وإرسال للمختصين")
    
    if submitted:
        if name and phone:
            st.success(f"تم إرسال طلبك بنجاح! سيتواصل معك أحد الأطباء أو المهندسين لتأكيد باقة: {st.session_state.final_plan}")
            st.balloons()
        else:
            st.error("برجاء إدخال الاسم ورقم الهاتف.")

# شريط جانبي للمعلومات
st.sidebar.title("👨‍⚕️ فريق العمل")
st.sidebar.markdown("""
* **الفريق الطبي:** استشارات وأدوية.
* **سلامة الغذاء:** طعام صحي ومضمون.
* **الهندسة الطبية:** أجهزة تتبع وحماية.
---
📞 **للدعم الفني:** 01xxxxxxxxx
""")
