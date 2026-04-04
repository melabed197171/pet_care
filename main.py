import streamlit as st

# إعداداتالصفحة
st.set_page_config(page_title="العناية الذكية بالحيوانات الأليفة", page_icon="🐾")

# القائمةالجانبيةللتنقل
page = st.sidebar.selectbox("انتقل إلى:", ["الرئيسية", "قائمة المنتجات", "تواصل معنا"])

if page == " الرئيسية", "العناية الذكية"):
    st.subheader("نقدم أفضل المستلزمات الطبية والغذائية للحيوانات الأليفة في الإسكندرية")
    st.write("هدفنا هو توفير متطلبات أصحاب العيادات والمربين بأفضل جودة وأسرع خدمة توصيل.")
    st.image("https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60", caption="خدمتكمهيغايتنا")

elif page == "قائمة المنتجات":
    st.title("📦كتالوج المنتجات")
    st.write("استكشف مجموعتنا المختارة من المستلزمات:")

col1, col2 = st.columns(2)

with col1:
 st.info("💊 **مستلزماتطبية**")
 st.write("- حقنطبيةمقاساتمختلفة")
 st.write("- مطهراتوشاشمعقم")
 st.write("- فيتاميناتومكملاتغذائية")

with col2:
 st.success("🥣 **أغذيةواكسسوارات**")
 st.write("- درايفود (Dry Food) متميز")
 st.write("- أطواقوسلاسلمتينة")
 st.write("- أدواتالعنايةبالشعر (فرش)")
