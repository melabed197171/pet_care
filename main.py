importstreamlitas st
importpandasas pd

# إعداد الصفحة
st.set_page_config(page_title="VetSmart Pro | الرعاية الذكية", page_icon="🐾", layout="wide")

# --- التنسيق البصري ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; }
    .price-box { padding: 15px; background-color: #e8f5e9; border-radius: 10px; border: 1px solid #2e7d32; }
</style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (فريق العمل) ---
with st.sidebar:
    st.header("🩺 فريق VetSmart")
    st.info("نخبة من الأطباء البيطريين ومهندسي سلامة الغذاء لخدمة أليفك.")
    st.divider()
    st.write("📍 الرياض، المملكة العربية السعودية")

# --- العنوان الرئيسي ---
st.title("🐾 منصة VetSmart Pro للرعاية المتكاملة")
st.subheader("إشراف طبي وهندسي عالمي المستوى")

# --- أقسام الخدمات ---
tabs = st.tabs(["🏥 الخدمات والعيادة", "🍱 التغذية الذكية", "🛍️ المتجر والمستلزمات", "💳 إتمام الطلب"])

# القسم 1: الخدمات الطبية والإرشادات
with tabs[0]:
col1, col2 = st.columns(2)
with col1:
        st.markdown("### 🩺 استشارات وتطعيمات")
        st.write("- استشارات طبية فورية.\n- جدول تطعيمات ذكي.\n- متابعة دورية للأدوية.")
with col2:
        st.markdown("### 📚 إرشادات بيطرية")
        st.success("نصيحة الطبيب: تأكد من جدول التطعيمات الرباعي لقطتك في موعده.")

# القسم 2: التغذية الذكية (إشراف مهندس سلامة الغذاء)
with tabs[1]:
    st.header("⚖️ حاسبة التغذية ومعايير السلامة")
c1, c2 = st.columns(2)
with c1:
weight = st.number_input("وزن الأليف (كجم):", min_value=0.5, value=5.0)
