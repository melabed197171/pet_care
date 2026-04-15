import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pytz

# 1. إعدادات الصفحة
st.set_page_config(page_title="VetFamily Alexandria", layout="wide")

# 2. رابط الجدول (تأكد من الصلاحية لـ Editor)
URL = "https://docs.google.com/spreadsheets/d/1kQ1junWnmyfwKPYj-Jm2QeCLlJ4dwmiMXkystV8dc7k/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def save_order(name, phone, product):
    try:
        df = conn.read(spreadsheet=URL)
        new_data = pd.DataFrame([{
            "التاريخ": datetime.now(pytz.timezone('Africa/Cairo')).strftime("%Y-%m-%d %H:%M"),
            "اسم العميل": name,
            "المنتج": product,
            "رقم الهاتف": phone
        }])
        updated_df = pd.concat([df, new_data], ignore_index=True)
        conn.update(spreadsheet=URL, data=updated_df)
        return True
    except:
        return False

# 3. الهيدر (العنوان)
st.markdown("<h1 style='text-align: center; color: #1e3c72;'>VetFamily Alexandria</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>مركز الرعاية المتكاملة للحيوانات الأليفة</p>", unsafe_allow_html=True)
st.write("---")

# 4. قسم عروض اليوم الحصرية
st.subheader("عروض اليوم الحصرية")
c1, c2 = st.columns(2)

with c1:
    st.info("رويال كانين قطط 2 كجم - 450 ج.م")
    with st.expander("اطلب الان"):
        n1 = st.text_input("الاسم", key="n1")
        p1 = st.text_input("الموبايل", key="p1")
        if st.button("تأكيد طلب رويال", key="b1"):
            if n1 and p1:
                if save_order(n1, p1, "رويال كانين 2 كجم"): st.success("تم الحجز")

with c2:
    st.info("رمل قطط كربون 5 لتر - 180 ج.م")
    with st.expander("اطلب الان"):
        n2 = st.text_input("الاسم", key="n2")
        p2 = st.text_input("الموبايل", key="p2")
        if st.button("تأكيد طلب الرمل", key="b2"):
            if n2 and p2:
                if save_order(n2, p2, "رمل كربون"): st.success("تم الحجز")

st.write("---")

# 5. قسم طعام القطط الجاف (باقي الصفحة)
st.subheader("طعام القطط الجاف")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://via.placeholder.com/150", caption="بريميوم كات - 1 كجم")
    st.write("**السعر: 70 ج.م**")
    with st.expander("حجز المنتج"):
        un = st.text_input("الاسم", key="u1")
        up = st.text_input("الموبايل", key="ph1")
        if st.button("طلب بريميوم", key="bt1"):
            save_order(un, up, "بريميوم كات")

with col2:
    st.image("https://via.placeholder.com/150", caption="رويال كانين كيتن - 1.5 كجم")
    st.write("**السعر: 400 ج.م**")
    with st.expander("حجز المنتج"):
        un2 = st.text_input("الاسم", key="u2")
        up2 = st.text_input("الموبايل", key="ph2")
        if st.button("طلب كيتن", key="bt2"):
            save_order(un2, up2, "رويال كيتن")

with col3:
    st.image("https://via.placeholder.com/150", caption="رويال كانين بالغ - 2 كجم")
    st.write("**السعر: 450 ج.م**")
    with st.expander("حجز المنتج"):
        un3 = st.text_input("الاسم", key="u3")
        up3 = st.text_input("الموبايل", key="ph3")
        if st.button("طلب بالغ", key="bt3"):
            save_order(un3, up3, "رويال بالغ")
