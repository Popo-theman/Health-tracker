import streamlit as st
import math

# ตั้งค่าหน้าแอปให้ดูสวยงาม
st.set_page_config(page_title="Pond's Health Tracker", page_icon="🏥")

st.title("🏥 My Personal Health & Diet")
st.subheader("บันทึกสุขภาพประจำวันของคุณปอน")

# ส่วนที่ 1: ข้อมูลร่างกาย (Sidebar ด้านข้าง)
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
    sleep = st.slider("เวลานอน (ชั่วโมง)", 0, 12, 7)

# ส่วนที่ 2: บันทึกอาหาร
st.header("🍽️ บันทึกการกินวันนี้")
col1, col2 = st.columns(2)

with col1:
    bf_food = st.text_input("มื้อเช้า", "น้ำเปล่า + น้ำมันมะกอก + กาแฟดำดริป")
    lunch_food = st.text_input("มื้อเที่ยง")
    dinner_food = st.text_input("มื้อเย็น")

with col2:
    bf_cal = st.number_input("แคลอรี่ (เช้า)", value=130)
    lunch_cal = st.number_input("แคลอรี่ (เที่ยง)", value=0)
    dinner_cal = st.number_input("แคลอรี่ (เย็น)", value=0)

# คำนวณผลลัพธ์
height_m = height / 100
bmi = weight / (height_m ** 2)

# คำนวณ BMR & TDEE
bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
activity_map = {"ไม่ออกกำลังกายเลย": 1.2, "ออกกำลังกายเบาๆ (1-3 วัน/สัปดาห์)": 1.375, 
                "ออกกำลังกายปานกลาง (3-5 วัน/สัปดาห์)": 1.55, "ออกกำลังกายหนัก (6-7 วัน/สัปดาห์)": 1.725}
tdee = bmr * activity_map[activity]

total_in = bf_cal + lunch_cal + dinner_cal
diff = tdee - total_in

# แสดงผลรายงาน
st.divider()
st.header("📊 รายงานวิเคราะห์")
c1, c2, c3 = st.columns(3)
c1.metric("BMI", f"{bmi:.1f}")
c2.metric("เผาผลาญ (TDEE)", f"{int(tdee)} kcal")
c3.metric("กินเข้าไป", f"{int(total_in)} kcal")

if diff > 0:
    st.success(f"วันนี้ทำได้ดีมากครับ! ร่างกายติดลบไป {int(diff)} แคลอรี่ (ดึงไขมันมาใช้แล้ว)")
else:
    st.warning(f"วันนี้กินเกินไป {int(abs(diff))} แคลอรี่ ต้องขยับร่างกายเพิ่มขึ้นนะครับ")
