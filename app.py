import streamlit as st

st.set_page_config(page_title="Pond's Health Tracker V2.1", page_icon="🏥")

st.title("🏥 My Personal Health & Diet (V2.1)")
st.subheader("ระบบบันทึกสุขภาพพร้อมระบบคำนวณอัตโนมัติ")

# 1. ฐานข้อมูลอาหาร
food_db = {
    "--- เลือกเมนู หรือ กำหนดเอง ---": 0,
    "น้ำเปล่า + น้ำมันมะกอก + กาแฟดำดริป": 130,
    "ข้าวราดกะเพราไก่ไข่ดาว": 600,
    "ข้าวมันไก่": 596,
    "ก๋วยเตี๋ยวหมูน้ำตก": 350,
    "ผัดไทยกุ้งสด": 550,
    "ข้าวไข่เจียว": 450,
    "สลัดผักไก่ย่าง": 150,
    "ส้มตำไทย": 60,
    "ผลไม้ตามฤดูกาล (1 จานเล็ก)": 100,
}

# ส่วนที่ 1: ข้อมูลร่างกาย (Sidebar)
with st.sidebar:
    st.header("👤 ข้อมูลส่วนตัว")
    age = st.number_input("อายุ (ปี)", value=45)
    weight = st.number_input("น้ำหนักปัจจุบัน (กก.)", value=89.0)
    height = st.number_input("ส่วนสูง (ซม.)", value=167)
    activity = st.selectbox(
        "กิจกรรมในแต่ละวัน",
        ["ไม่ออกกำลังกายเลย", "ออกกำลังกายเบาๆ (1-3 วัน/สัปดาห์)", 
         "ออกกำลังกายปานกลาง (3-5 วัน/สัปดาห์)", "ออกกำลังกายหนัก (6-7 วัน/สัปดาห์)"]
    )

# ส่วนที่ 2: บันทึกอาหาร
st.header("🍽️ บันทึกการกินวันนี้")

col1, col2 = st.columns(2)
with col1:
    bf_select = st.selectbox("มื้อเช้า", list(food_db.keys()), index=1, key="bf_s")
with col2:
    bf_cal = st.number_input("แคลอรี่ (เช้า)", value=food_db[bf_select])

col3, col4 = st.columns(2)
with col3:
    lunch_select = st.selectbox("มื้อเที่ยง", list(food_db.keys()), index=0, key="lh_s")
with col4:
    lunch_cal = st.number_input("แคลอรี่ (เที่ยง)", value=food_db[lunch_select])

col5, col6 = st.columns(2)
with col5:
    dinner_select = st.selectbox("มื้อเย็น", list(food_db.keys()), index=0, key="dn_s")
with col6:
    dinner_cal = st.number_input("แคลอรี่ (เย็น)", value=food_db[dinner_select])

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
    st.success(f"วันนี้ทำได้ดีมากครับ! ร่างกายติดลบไป {int(diff)} แคลอรี่ (ดึงไขมันมาใช้แล้ว)")
else:
    st.warning(f"วันนี้กินเกินไป {int(abs(diff))} แคลอรี่ ต้องขยับร่างกายเพิ่มขึ้นนะครับ")
