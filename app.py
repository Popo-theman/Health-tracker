import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Pond's Health Tracker V3.1", page_icon="📊")

# --- ส่วนการดึงข้อมูลจาก Google Sheets ---
sheet_url = "https://docs.google.com/spreadsheets/d/1tOHQx1UyqpZPdoExF89EZQq_-p8xaTBk0plXAzwQKQM/edit?usp=drivesdk "

def get_csv_url(url):
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    if match:
        return f"https://docs.google.com/spreadsheets/d/{match.group(1)}/export?format=csv"
    return url

@st.cache_data
def load_food_data(url):
    df = pd.read_csv(get_csv_url(url))
    return pd.Series(df.Calories.values, index=df.Menu).to_dict()

try:
    food_db = load_food_data(sheet_url)
    food_options = list(food_db.keys())
except:
    st.error("เชื่อมต่อข้อมูลไม่ได้ ตรวจสอบการแชร์ลิงก์ Sheets นะครับ")
    food_db = {}
    food_options = []

st.title("📊 Health Tracker (Multi-Select)")

# ส่วนที่ 1: ข้อมูลร่างกาย
with st.sidebar:
    st.header("👤 ข้อมูลส่วนตัว")
    weight = st.number_input("น้ำหนัก (กก.)", value=89.0)
    height = st.number_input("ส่วนสูง (ซม.)", value=167)
    age = st.number_input("อายุ (ปี)", value=45)

# ส่วนที่ 2: บันทึกอาหารแบบเลือกได้หลายอย่าง
st.header("🍽️ บันทึกการกินวันนี้")

def meal_box(label, key_name):
    st.subheader(label)
    # เปลี่ยนจาก selectbox เป็น multiselect
    selected_foods = st.multiselect(f"เลือกเมนูสำหรับ {label}", food_options, key=key_name)
    # คำนวณผลรวมแคลอรี่ของรายการที่เลือก
    total_cal = sum(food_db.get(food, 0) for food in selected_foods)
    st.info(f"แคลอรี่รวม {label}: {total_cal} kcal")
    return total_cal

bf_total = meal_box("มื้อเช้า", "bf")
lunch_total = meal_box("มื้อเที่ยง", "lh")
dinner_total = meal_box("มื้อเย็น", "dn")

# --- ส่วนคำนวณผลลัพธ์ ---
tdee = ((10 * weight) + (6.25 * height) - (5 * age) + 5) * 1.2
total_in = bf_total + lunch_total + dinner_total
diff = tdee - total_in

st.divider()
st.header("📊 รายงานวิเคราะห์")
c1, c2, c3 = st.columns(3)
c1.metric("TDEE (เผาผลาญ)", f"{int(tdee)}")
c2.metric("กินเข้าไปรวม", f"{total_in}")
c3.metric("สถานะ", "ลดไขมัน" if diff > 0 else "กินเกิน", delta=f"{int(diff)} kcal")
