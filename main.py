import streamlit as st

# إعداداتالصفحة
st.set_page_config(page_title="العنايةالذكيةبالحيواناتالأليفة", page_icon="🐾")

# القائمةالجانبيةللتنقل
page = st.sidebar.selectbox("انتقلإلى:", ["الرئيسية", "قائمةالمنتجات", "تواصلمعنا"])

if page == "الرئيسية":
st.title("🐾مرحباًبكفيمشروعالعنايةالذكية")
st.subheader("نقدمأفضلالمستلزماتالطبيةوالغذائيةللحيواناتالأليفةفيالإسكندرية")
st.write("هدفناهوتوفيرمتطلباتأصحابالعياداتوالمربينبأفضلجودةوأسرعخدمةتوصيل.")
st.image("https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60", caption="خدمتكمهيغايتنا")

elif page == "قائمةالمنتجات":
st.title("📦كتالوجالمنتجات")
st.write("استكشفمجموعتناالمختارةمنالمستلزمات:")

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

elif page == "تواصلمعنا":
st.title("📞اطلبالآن")
st.write("نحنمتواجدونلخدمتكمفيمنطقةمحرمبكوكرموز.")

with st.form("contact_form"):
name = st.text_input("الاسم:")
order = st.text_area("المنتجاتالمطلوبة:")
phone = st.text_input("رقمالهاتف:")
submit = st.form_submit_button("إرسالالطلب")

if submit:
st.success(f"شكراًيا {name}،تماستلامطلبكوسنتواصلمعكفوراً!")

# تذييلالصفحة
st.sidebar.write("---")
st.sidebar.write("📍الإسكندرية - محرمبك / كرموز")
