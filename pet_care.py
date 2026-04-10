import streamlit as st
from PIL import Image
from datetime import datetime
import pytz
import io
import csv
import hashlib

# إعداد الصفحة
st.set_page_config(page_title="pet care", layout="wide", page_icon="🐾")

# تحديد منطقة القاهرة الزمنية
CAIRO_TZ = pytz.timezone('Africa/Cairo')

def get_cairo_time():
    return datetime.now(CAIRO_TZ)

# CSS الكامل
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');

    * {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        text-align: right !important;
        background: linear-gradient(135deg, #a1ebdb 0%, #ffdca2 100%);
        background-attachment: fixed;
    }

    .block-container {
        padding: 3rem 2.5rem;
        max-width: 1200px;
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-top: 30px;
        margin-bottom: 30px;
    }

    .stImage img {
        border-radius: 50%; 
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); 
        border: 4px solid #ffffff;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #1a365d !important;
        font-weight: 800 !important;
        text-align: right !important;
        direction: rtl !important;
    }

    div.stButton > button {
        width: 100%;
        height: 55px;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 14px;
        background: linear-gradient(45deg, #10b981, #059669);
        color: white !important;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(5, 150, 105, 0.2);
    }
    
    input, textarea, select {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stTextInput > label > div[data-testid="stMarkdownContainer"] > p,
    .stTextArea > label > div[data-testid="stMarkdownContainer"] > p,
    .stNumberInput > label > div[data-testid="stMarkdownContainer"] > p {
        display: none !important;
    }
    
    .stTextInput small, .stTextArea small, .stNumberInput small {
        display: none !important;
    }
    
    .price-tag {
        font-size: 24px;
        color: #2e7d32;
        font-weight: bold;
    }
    
    .notification-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }

    .subscription-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border-right: 6px solid #10b981;
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    .thank-you-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# دالة تشفير
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("admin123")

def check_login(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH

if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# تهيئة البيانات
if 'packages' not in st.session_state:
    st.session_state.packages = {
        "الباقة الماسية": {
            "price": 5000,
            "description": "رعاية شاملة + جهاز تتبع + نظام غذائي",
            "icon": "💎",
            "features": [
                "زيارات منزلية غير محدودة",
                "جهاز تتبع GPS متطور",
                "نظام غذائي مخصص",
                "استشارات على مدار الساعة",
                "تطعيمات شاملة"
            ]
        },
        "الباقة الذهبية": {
            "price": 2500,
            "description": "4 استشارات شهرياً + اللقاحات الأساسية",
            "icon": "✨",
            "features": [
                "4 استشارات شهرياً",
                "اللقاحات الأساسية",
                "فحص دوري شهري",
                "خصم 20% على الخدمات الإضافية"
            ]
        },
        "الباقة الاقتصادية": {
            "price": 1000,
            "description": "استشارة شهرية + جدول تطعيمات",
            "icon": "🛡️",
            "features": [
                "استشارة شهرية واحدة",
                "جدول تطعيمات سنوي",
                "خصم 10% على الخدمات الإضافية"
            ]
        }
    }

if 'subscriptions' not in st.session_state:
    st.session_state.subscriptions = []

if 'package_notifications' not in st.session_state:
    st.session_state.package_notifications = []

if 'shopping_cart' not in st.session_state:
    st.session_state.shopping_cart = []

# دالة حفظ الاشتراك
def save_subscription(package_name, package_price, customer_info):
    try:
        cairo_time = get_cairo_time()
        subscription = {
            "id": len(st.session_state.subscriptions) + 1,
            "package_name": str(package_name),
            "price": int(package_price),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "time": cairo_time.strftime("%H:%M:%S"),
            "customer_name": str(customer_info["name"]),
            "customer_phone": str(customer_info["phone"]),
            "status": "جديد - في انتظار التواصل"
        }
        
        st.session_state.subscriptions.append(subscription)
        
        notification = {
            "message": f"اشتراك جديد في {package_name}",
            "timestamp": cairo_time.strftime("%H:%M:%S"),
            "date": cairo_time.strftime("%Y-%m-%d"),
            "details": subscription
        }
        st.session_state.package_notifications.insert(0, notification)
        
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الاشتراك: {e}")
        return False

# الهيدر
col_text, col_img = st.columns([5, 1]) 

with col_text:
    st.markdown("<h1>pet care🐾</h1>", unsafe_allow_html=True)

with col_img:
    try:
        image = Image.open('cat.png')
        st.image(image, width=300) 
    except:
        pass

st.markdown("---")


col1, col2 = st.columns(2)
with col1:
    if st.button("أعجبني ❤️"):
        st.balloons()
        st.success("شكراً على حبك للأليف 🐱")

with col2:
    if st.button("تبني الآن 🏠"):
        st.info("سجل بياناتك")

st.write("# مركز الرعاية المتكاملة البيطرية 🐾")
st.write("## تحت اشراف نخبة من الأطباء والمهندسين")

# التبويبات
if st.session_state.is_logged_in:
    tabs = st.tabs([
        "الباقات المتاحة 💳",
        "الاستشارات واللقاحات",
        "المتجر والمستلزمات 🛒",
        "التكنولوجيا والأجهزة",
        "لوحة التحكم 📊",
        "إدارة الباقات ⚙️"
    ])
    tab1, tab2, tab3, tab4, tab5, tab6 = tabs
else:
    tabs = st.tabs([
        "الباقات المتاحة 💳",
        "الاستشارات واللقاحات",
        "المتجر والمستلزمات 🛒",
        "التكنولوجيا والأجهزة"
    ])
    tab1, tab2, tab3, tab4 = tabs

# تبويب الباقات
with tab1:
    st.write("## اختر باقتك المفضلة 💳")
    
    for idx, (package_name, package_data) in enumerate(st.session_state.packages.items()):
        st.markdown("---")
        
        st.write(f"## {package_name} {package_data['icon']}")
        st.write(f"**{package_data['description']}**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### التفاصيل:")
            for feature in package_data['features']:
                st.write(f"✓ {feature}")
        
        with col2:
            st.markdown(f"<p class='price-tag'>{package_data['price']} ج.م / سنة</p>", unsafe_allow_html=True)
        
        st.write("### بيانات التفعيل 📝")
        
        col_name, col_phone = st.columns(2)
        
        with col_name:
            customer_name = st.text_input(
                "الاسم الكامل",
                key=f"name_{package_name}_{idx}",
                placeholder="أدخل اسمك الكامل",
                label_visibility="collapsed"
            )
            st.caption("الاسم الكامل")
        
        with col_phone:
            customer_phone = st.text_input(
                "رقم الواتساب",
                key=f"phone_{package_name}_{idx}",
                placeholder="01xxxxxxxxx",
                label_visibility="collapsed"
            )
            st.caption("رقم الواتساب")
        
        if st.button(f"تفعيل {package_name} ✅", key=f"btn_{package_name}_{idx}"):
            if customer_name.strip() and customer_phone.strip():
                customer_info = {
                    "name": customer_name.strip(),
                    "phone": customer_phone.strip()
                }
                
                if save_subscription(package_name, package_data['price'], customer_info):
                    # رسالة الشكر والتأكيد
                    st.markdown("""
                    <div class='thank-you-message'>
                        ✅ شكراً لك! 🎉<br>
                        سيتم تنفيذ الطلب والتواصل للتوصيل 📞<br>
                        تم حفظ بيانات: {} - {} 🔔
                    </div>
                    """.format(customer_name, customer_phone), unsafe_allow_html=True)
                    
                    st.balloons()
                    st.success(f"تم تفعيل {package_name} ��نجاح ✅")
                    st.rerun()
                else:
                    st.error("فشل في حفظ الاشتراك ❌")
            else:
                st.error("برجاء إدخال الاسم ورقم الهاتف ⚠️")
    
    st.markdown("---")
    st.write("## باقة من اختيارك (حسب الطلب) 🎨")
    
    services_db = {
        "استشارة طبية منزلية": 400,
        "لقاح السعار الدوري": 450,
        "جهاز تتبع GPS (تركيب مهندس)": 1800,
        "تصميم نظام غذائي (مهندس سلامة)": 600
    }
    
    selected_items = st.multiselect("اختر من الخدمات التالية:", list(services_db.keys()))
    
    if selected_items:
        custom_total = sum(services_db[item] for item in selected_items)
        st.success(f"**إجمالي الباقة الحرة: {custom_total} ج.م**")
        
        st.write("### بيانات التفعيل 📝")
        
        col_name2, col_phone2 = st.columns(2)
        
        with col_name2:
            custom_name = st.text_input("الاسم", key="c_name", placeholder="أدخل اسمك", label_visibility="collapsed")
            st.caption("الاسم الكامل")
        
        with col_phone2:
            custom_phone = st.text_input("الواتساب", key="c_phone", placeholder="01xxxxxxxxx", label_visibility="collapsed")
            st.caption("رقم الواتساب")
        
        if st.button("تفعيل الباقة الحرة ✅"):
            if custom_name.strip() and custom_phone.strip():
                if save_subscription("باقة حرة (مخصصة)", custom_total, {"name": custom_name, "phone": custom_phone}):
                    # رسالة الشكر والتأكيد للباقة الحرة
                    st.markdown("""
                    <div class='thank-you-message'>
                        ✅ شكراً لك! 🎉<br>
                        سيتم تنفيذ الطلب والتواصل للتوصيل 📞<br>
                        تم حفظ بيانات: {} - {} 🔔
                    </div>
                    """.format(custom_name, custom_phone), unsafe_allow_html=True)
                    
                    st.balloons()
                    st.success("تم التفعيل ✅")
                    st.rerun()

# تبويب الاستشارات
with tab2:
    st.write("## الخدمات الطبية والوقائية 🩺")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### الأدوية واللقاحات")
        st.info("نوفر أحدث اللقاحات الدورية والبروتوكولات العلاجية المعتمدة")
    with col2:
        st.write("### إرشادات طبية")
        st.write("- جدول التطعيمات السنوي")
        st.write("- الإسعافات الأولية للحيوانات الأليفة")

# تبويب المتجر
with tab3:
    st.write("## متجر المستلزمات 🛒")

# تبويب التكنولوجيا
with tab4:
    st.write("## الحلول التقنية ⚙️")

# لوحة التحكم
if st.session_state.is_logged_in:
    with tab5:
        st.write("## لوحة التحكم - الاشتراكات والإشعارات 📊")
        
        cairo_now = get_cairo_time()
        st.info(f"الوقت الحالي: {cairo_now.strftime('%Y-%m-%d %H:%M:%S')} 🕐")
        
        if st.button("تسجيل الخروج 🔓"):
            st.session_state.is_logged_in = False
            st.rerun()
        
        # الإحصائيات
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إجمالي الاشتراكات 📦", len(st.session_state.subscriptions))
        with col2:
            total_revenue = sum(sub["price"] for sub in st.session_state.subscriptions)
            st.metric("إجمالي الإيرادات 💰", f"{total_revenue:,} ج.م")
        with col3:
            st.metric("الإشعارات 🔔", len(st.session_state.package_notifications))
        
        st.markdown("---")
        
        # الإشعارات
        st.write("### الإشعارات الفورية 🔔")
        
        if st.session_state.package_notifications:
            for notif in st.session_state.package_notifications:
                st.markdown(f"""
                <div class='notification-box'>
                    <h4>🔔 {notif['message']}</h4>
                    <p>📅 التاريخ: {notif['date']} | ⏰ الوقت: {notif['timestamp']}</p>
                    <p>👤 العميل: {notif['details']['customer_name']}</p>
                    <p>📞 الهاتف: {notif['details']['customer_phone']}</p>
                    <p>💰 المبلغ: {notif['details']['price']} ج.م | 📦 الباقة: {notif['details']['package_name']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد إشعارات")
        
        st.markdown("---")
        
        # جدول الاشتراكات
        st.write("### جدول الاشتراكات التفصيلي 📋")
        
        total_subs = len(st.session_state.subscriptions)
        st.success(f"إجمالي الاشتراكات: {total_subs} اشتراك ✅")
        
        if st.session_state.subscriptions:
            for sub in reversed(st.session_state.subscriptions):
                st.markdown(f"""
                <div class='subscription-card'>
                    <h2 style='color: #10b981; margin-bottom: 15px;'>
                        اشتراك رقم {sub['id']} - {sub['package_name']} 🆔
                    </h2>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**بيانات العميل 👤**")
                    st.write(f"**الاسم:** {sub['customer_name']}")
                    st.write(f"**الهاتف:** {sub['customer_phone']}")
                
                with col2:
                    st.write("**بيانات الباقة 📦**")
                    st.write(f"**الباقة:** {sub['package_name']}")
                    st.write(f"**السعر:** {sub['price']:,} ج.م")
                
                with col3:
                    st.write("**التوقيت 📅**")
                    st.write(f"**التاريخ:** {sub['date']}")
                    st.write(f"**الوقت:** {sub['time']}")
                
                st.markdown("---")
                status_options = ["جديد - في انتظار التواصل", "تم التواصل", "جاري التنفيذ", "مكتمل", "ملغي"]
                current_status = sub.get('status', 'جديد - في انتظار التواصل')
                
                col_status, col_btn = st.columns([4, 1])
                
                with col_status:
                    new_status = st.selectbox(
                        "تحديث حالة الاشتراك:",
                        status_options,
                        index=status_options.index(current_status) if current_status in status_options else 0,
                        key=f"status_select_{sub['id']}"
                    )
                
                with col_btn:
                    if st.button("حفظ 💾", key=f"save_btn_{sub['id']}"):
                        for s in st.session_state.subscriptions:
                            if s['id'] == sub['id']:
                                s['status'] = new_status
                        st.success("تم التحديث ✅")
                        st.rerun()
                
                st.markdown("---")
                st.markdown("<br>", unsafe_allow_html=True)
        
        else:
            st.warning("لا توجد اشتراكات حتى الآن ⚠️")
            st.info("سجل في باقة من تبويب 'الباقات المتاحة' لتظهر البيانات هنا 💡")
        
        # تنزيل تقرير CSV
        if st.session_state.subscriptions:
            st.markdown("---")
            st.markdown("---")
            if st.button("تنزيل تقرير CSV 📥"):
                output = io.StringIO()
                # إضافة UTF-8 BOM للتأكد من عرض العربية بشكل صحيح في Excel
                output.write('\ufeff')
                writer = csv.writer(output)
                writer.writerow(['الرقم', 'العميل', 'الهاتف', 'الباقة', 'السعر', 'التاريخ', 'الوقت', 'الحالة'])
                
                for sub in st.session_state.subscriptions:
                    writer.writerow([
                        sub['id'],
                        sub['customer_name'],
                        sub['customer_phone'],
                        sub['package_name'],
                        sub['price'],
                        sub['date'],
                        sub['time'],
                        sub.get('status', 'جديد')
                    ])
                
                st.download_button(
                    "تحميل الملف 📄",
                    output.getvalue().encode('utf-8-sig'),
                    f"subscriptions_{cairo_now.strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                    key='download-csv'
                )

    # إدارة الباقات
    with tab6:
        st.write("## إدارة الباقات ⚙️")
        if st.button("تسجيل الخروج 🔓", key="logout2"):
            st.session_state.is_logged_in = False
            st.rerun()

# الشريط الجانبي
st.sidebar.write("# فريق العمل 👨‍⚕️")
st.sidebar.markdown("""
* **الفريق الطبي:** استشارات وأدوية
* **سلامة الغذاء:** طعام صحي
* **الهندسة الطبية:** أجهزة تتبع
---
📞 **للدعم:** 00000
""")

st.sidebar.markdown("---")

if not st.session_state.is_logged_in:
    st.sidebar.write("### تسجيل دخول المدير 🔐")
    with st.sidebar.form("login_form"):
        username = st.text_input("اسم المستخدم", label_visibility="collapsed", placeholder="admin")
        password = st.text_input("كلمة المرور", type="password", label_visibility="collapsed", placeholder="admin123")
        
        if st.form_submit_button("دخول 🔓"):
            if check_login(username, password):
                st.session_state.is_logged_in = True
                st.success("تم الدخول ✅")
                st.rerun()
            else:
                st.error("خطأ في البيانات ❌")
else:
    st.sidebar.success("مسجل دخول كمدير ✅")
    cairo_now = get_cairo_time()
    st.sidebar.info(f"🕐 {cairo_now.strftime('%H:%M')}\n📅 {cairo_now.strftime('%Y-%m-%d')}")
    st.sidebar.metric("الاشتراكات ✅", len(st.session_state.subscriptions))
    
    # عرض آخر 3 مشتركين
    if st.session_state.subscriptions:
        st.sidebar.write("### آخر المشتركين:")
        for sub in reversed(st.session_state.subscriptions[-3:]):
            st.sidebar.info(f"👤 {sub['customer_name']}\n📞 {sub['customer_phone']}\n📦 {sub['package_name']}")