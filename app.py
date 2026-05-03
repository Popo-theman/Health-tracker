import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pond's Health Tracker V3.0", page_icon="📊")

# --- ส่วนการดึงข้อมูลจาก Google Sheets ของคุณ ---
sheet_url = "https://docs.google.com/spreadsheets/d/1tOHQx1UyqpZPdoExF89EZQq_-p8xaTBk0plXAzwQKQM/edit?usp=sharing"
# เปลี่ยนท้ายลิงก์ให้เป็นรูปแบบ CSV เพื่อให้โปรแกรมอ่านง่าย
csv_url = sheet_url.replace('/edit?usp=sharing', '/gviz/tq?tqx=out:csv')

@st.cache_data(ttl=600) # ให้รีเฟรชข้อมูลทุก 10 นาที หรือเมื่อกด Rerun
def load_food_data(url):
    df = pd.read_csv(url)
    # สร้าง Dictionary จาก Sheets: โดยใช้คอลัมน์ Menu เป็นชื่อ และ Calories เป็นค่า
    return pd.Series(df.Calories.values, index=df.Menu).to_dict()

try:
    food_db = load_food_data(csv_url)
    food_list = ["--- เลือกเมนู หรือ กำหนดเอง ---"] + list(food_db.keys())
except Exception as e:
    st.error("ไม่สามารถเชื่อมต่อ Google Sheets ได้ ตรวจสอบว่าตั้งค่า 'ทุกคนที่มีลิงก์มีสิทธิ์อ่าน' แล้วหรือยัง")
    food_db = {"--- เลือกเมนู หรือ กำหนดเอง ---": 0}
    food_list = list(food_db.keys())

st.title("📊 Health Tracker V3.0")
st.subheader("จัดการเมนูอาหารผ่าน Google Sheets")

# ส่วนที่ 1: ข้อมูลร่างกาย (Sidebar)
with st.sidebar:
    st.header("👤 ข้อมูลส่วนตัว")
    age = st.number_input("อายุ (ปี)", value=45)
    weight = st.number_input("น้ำหนัก (กก.)", value=89.0)
    height = st.number_input("ส่วนสูง (ซม.)", value=167)
    activity = st.selectbox(
        "กิจกรรมในแต่ละวัน",
        ["ไม่ออกกำลังกายเลย", "ออกกำลังกายเบาๆ (1-3 วัน/สัปดาห์)", 
         "ออกกำลังกายปานกลาง (3-5 วัน/สัปดาห์)", "ออกกำลังกายหนัก (6-7 วัน/สัปดาห์)"]
    )

# ส่วนที่ 2: บันทึกอาหาร
st.header("🍽️ บันทึกการกินวันนี้")

def food_section(label, key_s, key_n):
    col_a, col_b = st.columns(2)
    with col_a:
        sel = st.selectbox(label, food_list, key=key_s)
    with col_b:
        # ดึงค่าแคลอรี่จากฐานข้อมูล ถ้าไม่เจอก็ให้เป็น 0
        val = food_db.get(sel, 0)
        return st.number_input(f"แคลอรี่ ({label})", value=int(val), key=key_n)

bf_cal = food_section("มื้อเช้า", "s1", "n1")
lunch_cal = food_section("มื้อเที่ยง", "s2", "n2")
dinner_cal = food_section("มื้อเย็น", "s3", "n3")

# --- ส่วนคำนวณตัวเลข ---
height_m = height / 100
bmi = weight / (height_m ** 2)
bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
activity_map = {"ไม่ออกกำลังกายเลย": 1.2, "ออกกำลังกายเบาๆ (1-3 วัน/สัปดาห์)": 1.375, 
                "ออกกำลังกายปานกลาง (3-5 วัน/สัปดาห์)": 1.55, "ออกกำลังกายหนัก (6-7 วัน/สัปดาห์)": 1.725}
tdee = bmr * activity_map[activity]

total_in = bf_cal + lunch_cal + dinner_cal
diff = tdee - total_in

st.divider()
st.header("📊 รายงานวิเคราะห์")
c1, c2, c3 = st.columns(3)
c1.metric("BMI", f"{bmi:.1f}")
c2.metric("เผาผลาญ (TDEE)", f"{int(tdee)} kcal")
c3.metric("กินเข้าไปรวม", f"{int(total_in)} kcal")

if diff > 0:
    st.success(f"วันนี้ติดลบไป {int(diff)} แคลอรี่ (ดึงไขมันมาใช้)")
else:
    st.warning(f"วันนี้เกินไป {int(abs(diff))} แคลอรี่")

st.info("💡 ทริค: หากเพิ่มเมนูใน Google Sheets แล้วไม่ขึ้น ให้กดปุ่ม R (Rerun) หรือรอประมาณ 10 นาทีครับ")
