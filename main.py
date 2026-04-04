import streamlit as st

# إضافة عنوان للتطبيق
st.title("مرحباً بك في تطبيقي الأول! 👋")

# إضافة نص عادي
st.write("هذا التطبيق تم بناؤه باستخدام Streamlit و VS Code.")

# إضافة حقل إدخال نصي
name = st.text_input("ما هو اسمك؟")

# إضافة زر تفاعلي
if st.button("تأكيد"):
    if name:
        st.success(f"أهلاً بك يا {name}! يسعدنا انضمامك.")
    else:
        st.warning("يرجى إدخال اسمك أولاً.")

# إضافة شريط جانبي (Sidebar)
st.sidebar.header("إعدادات")
st.sidebar.info("يمكنك إضافة أدوات هنا أيضاً!")
