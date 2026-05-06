import streamlit as st
from database import create_db, get_all_devices, delete_device # เพิ่ม delete_device
import plotly.express as px

# สร้าง DB ครั้งแรกถ้ายังไม่มี
create_db()

st.set_page_config(page_title="Asset Dashboard", layout="wide")
st.title("📊 สรุปรายการอุปกรณ์สำนักงาน")

df = get_all_devices()

if not df.empty:
    # ส่วนของ Metrics สรุปตัวเลข
    c1, c2, c3 = st.columns(3)
    c1.metric("อุปกรณ์ทั้งหมด", len(df))
    c2.metric("Laptop", len(df[df['device_type'] == 'Laptop']))
    c3.metric("License", len(df[df['device_type'] == 'License']))

    # กราฟวงกลมแสดงสัดส่วนอุปกรณ์
    st.subheader("สัดส่วนอุปกรณ์ตามประเภท")
    fig = px.pie(df, names='device_type', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    # ตารางข้อมูลทั้งหมดพร้อมตัวกรอง (Filter)
    st.subheader("รายการอุปกรณ์ทั้งหมด")
    search = st.text_input("🔍 ค้นหาชื่ออุปกรณ์หรือผู้ถือครอง")
    if search:
        df = df[df['device_name'].str.contains(search, case=False) | 
                df['owner'].str.contains(search, case=False)]
    
    st.dataframe(df, use_container_width=True)
else:
    st.info("ยังไม่มีข้อมูลอุปกรณ์ในระบบ เริ่มเพิ่มข้อมูลได้ที่เมนูด้านซ้ายครับ")
    
st.subheader("จัดการอุปกรณ์")
if not df.empty:
    # สร้าง List ของ ID และชื่อ เพื่อเอามาใส่ในตัวเลือกการลบ
    device_to_delete = st.selectbox("เลือกอุปกรณ์ที่ต้องการลบ", 
                                    options=df['id'].tolist(),
                                    format_func=lambda x: f"ID: {x} - {df[df['id']==x]['device_name'].values[0]}")
    
    if st.button("🗑️ ยืนยันการลบอุปกรณ์"):
        delete_device(device_to_delete)
        st.warning(f"ลบอุปกรณ์ ID {device_to_delete} เรียบร้อยแล้ว")
        st.rerun() # สั่งให้หน้าเว็บโหลดข้อมูลใหม่ทันที