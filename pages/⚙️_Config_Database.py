import streamlit as st
from database import add_device, get_all_devices, delete_device

st.set_page_config(page_title="Manage Devices", layout="wide")
st.title("⚙️ จัดการอุปกรณ์ (Add / Delete)")

# สร้าง 2 คอลัมน์ แบ่งซ้าย-ขวา
col_add, col_del = st.columns(2)

# --- ส่วนที่ 1: ฟอร์มเพิ่มอุปกรณ์ ---
with col_add:
    st.subheader("➕ เพิ่มอุปกรณ์ใหม่")
    with st.form("device_form", clear_on_submit=True):
        device_name = st.text_input("ชื่ออุปกรณ์")
        owner = st.text_input("ชื่อผู้ถือครอง")
        device_type = st.selectbox("ประเภทอุปกรณ์", ["Laptop", "PC"])
        sn = st.text_input("Serial Number / Key")
        status = st.select_slider("สถานะ", options=["Active", "In Storage", "Repair"])
        
        submit = st.form_submit_button("บันทึกข้อมูล")
        if submit:
            if device_name and owner:
                add_device(device_name, owner, device_type, sn, status)
                st.success(f"บันทึก {device_name} เรียบร้อยแล้วครับ!")
                st.rerun() # เพื่อให้ Dropdown ในส่วนลบข้อมูลอัปเดตทันที
            else:
                st.error("กรุณากรอกชื่อและเจ้าของครับ")

# --- ส่วนที่ 2: ฟอร์มลบอุปกรณ์ ---
with col_del:
    st.subheader("🗑️ ลบอุปกรณ์")
    df = get_all_devices()
    
    if not df.empty:
        # สร้างตัวเลือกจาก DataFrame
        options = df['id'].tolist()
        
        # ฟังก์ชันช่วยจัดรูปแบบข้อความใน Dropdown
        def format_label(id_val):
            row = df[df['id'] == id_val].iloc[0]
            return f"ID: {id_val} | {row['device_name']} ({row['owner']})"

        device_to_delete = st.selectbox(
            "เลือกอุปกรณ์ที่ต้องการนำออก", 
            options=options,
            format_func=format_label
        )
        
        # เพิ่มปุ่มยืนยันการลบ
        if st.button("ยืนยันการลบอุปกรณ์"):
            # บรรทัดนี้สำคัญมากครับ ต้องมีตัวแปร success มารับค่า
            success = delete_device(device_to_delete) 
            
            if success:
                st.success("ลบสำเร็จแล้วครับ!")
                st.rerun()
            else:
                st.error("ไม่สามารถลบได้ หรือไม่พบข้อมูลอุปกรณ์นี้")
