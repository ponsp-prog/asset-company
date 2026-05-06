import sqlite3
import pandas as pd

def create_db():
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS devices
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  device_name TEXT, 
                  owner TEXT, 
                  device_type TEXT, 
                  serial_number TEXT,
                  status TEXT)''')
    conn.commit()
    conn.close()

def add_device(name, owner, dtype, sn, status):
    try:
        conn = sqlite3.connect('assets.db')
        c = conn.cursor()
        c.execute("INSERT INTO devices (device_name, owner, device_type, serial_number, status) VALUES (?,?,?,?,?)",
                  (name, owner, dtype, sn, status))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding device: {e}")
        return False

def get_all_devices():
    conn = sqlite3.connect('assets.db')
    try:
        # ใช้ดึงข้อมูลและจัดการเรื่องถ้าตารางยังไม่มี Column
        df = pd.read_sql_query("SELECT * FROM devices", conn)
        if df.empty:
             df = pd.DataFrame(columns=['id', 'device_name', 'owner', 'device_type', 'serial_number', 'status'])
    except:
        df = pd.DataFrame(columns=['id', 'device_name', 'owner', 'device_type', 'serial_number', 'status'])
    finally:
        conn.close()
    return df

def delete_device(device_id):
    try:
        conn = sqlite3.connect('assets.db')
        c = conn.cursor()
        c.execute("DELETE FROM devices WHERE id = ?", (device_id,))
        conn.commit()
        # ตรวจสอบว่ามีการลบแถวออกไปจริงไหม
        rows_affected = c.rowcount
        conn.close()
        return rows_affected > 0
    except Exception as e:
        print(f"Error deleting device: {e}")
        return False