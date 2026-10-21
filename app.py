import random
import time
import streamlit as st

st.set_page_config(page_title="How to Fish - Sinh Tồn Căng Thẳng", page_icon="🎣", layout="centered")

# --- 1. KHỞI TẠO TRẠNG THÁI GAME ---
if "gold" not in st.session_state:
    st.session_state.gold = 100
    st.session_state.hp = 100
    st.session_state.ammo = 5          # Đạn để tự vệ khi gặp quái
    st.session_state.rod_tier = 1      # Cấp độ cần câu
    st.session_state.inventory = []
    st.session_state.state = "DOCK"    # DOCK, FISHING, ENCOUNTER, SHOP

# Danh sách sự kiện câu cá & sinh tồn
ENCOUNTERS = [
    {"name": "🐟 Cá Rô Phi hiền lành", "type": "fish", "value": 30, "dmg": 0, "rate": 50},
    {"name": "🐠 Cá Ngừ đại dương lớn", "type": "fish", "value": 80, "dmg": 0, "rate": 25},
    {"name": "🦈 Cá Mập hung dữ bất ngờ tấn công!", "type": "danger", "value": 200, "dmg": 30, "rate": 15},
    {"name": "🦑 Thủy quái xúc tu khổng lồ kéo dây!", "type": "danger", "value": 500, "dmg": 55, "rate": 10}
]

# --- 2. GIAO DIỆN CHÍNH ---
st.title("🎣 HOW TO FISH: Phiên bản Sinh Tồn & Hành Động")
st.markdown("*Đừng lơ là! Dưới làn nước sâu kia không chỉ có cá, mà còn có những mối nguy hiểm chết người...*")

# Thanh thông số nhân vật
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Vàng", f"{st.session_state.gold} 🪙")
with col2:
    st.metric("❤️ HP", f"{st.session_state.hp}/100")
with col3:
    st.metric("🔫 Đạn tự vệ", f"{st.session_state.ammo} viên")
with col4:
    st.metric("🎒 Kho đồ", len(st.session_state.inventory))

st.markdown("---")

# --- 3. CÁC TRẠNG THÁI TRÒ CHƠI ---

# Màn hình chính tại bến tàu / bờ hồ
if st.session_state.state == "DOCK":
    st.subheader("🌅 Bến tàu yên bình (nhưng đầy rẫy hiểm nguy)")
    st.write("Bạn muốn làm gì tiếp theo?")
    
    c_btn1, c_btn2, c_btn3 = st.columns(3)
    with c_btn1:
        if st.button("🎣 Quăng cần câu", use_container_width=True):
            st.session_state.state = "FISHING"
            st.rerun()
    with c_btn2:
        if st.button("🛒 Cửa hàng sinh tồn", use_container_width=True):
            st.session_state.state = "SHOP"
            st.rerun()
    with c_btn3:
        if st.button("🔄 Chơi lại từ đầu", use_container_width=True):
            st.session_state.gold = 100
            st.session_state.hp = 100
            st.session_state.ammo = 5
            st.session_state.inventory = []
            st.rerun()

# Trạng thái đang câu cá / chờ đợi
elif st.session_state.state == "FISHING":
    st.info("🌊 Phao đang nổi bập bềnh trên mặt nước... Đang đợi cá cắn câu...")
    time.sleep(1.5)
    
    # Random sự kiện
    roll = random.randint(1, 100)
    cumulative = 0
    selected = ENCOUNTERS[0]
    for item in ENCOUNTERS:
        cumulative += item["rate"]
        if roll <= cumulative:
            selected = item
            break
            
    st.session_state.current_event = selected
    
    if selected["type"] == "fish":
        st.success(f"🎉 Kéo lên thành công! Bạn bắt được **{selected['name']}** (+{selected['value']} vàng)!")
        st.session_state.gold += selected["value"]
        st.session_state.inventory.append(selected["name"])
        st.session_state.state = "DOCK"
        time.sleep(1)
        st.rerun()
    else:
        # Gặp nguy hiểm / quái vật tấn công
        st.warning(f"⚠️ **NGUY HIỂM!** {selected['name']}")
        st.session_state.state = "ENCOUNTER"
        st.rerun()

# Trạng thái chiến đấu / xử lý tình huống nguy hiểm khi câu trúng quái
elif st.session_state.state == "ENCOUNTER":
    event = st.session_state.current_event
    st.error(f"Quái vật đang lao thẳng vào bạn! Gây ra **{event['dmg']} sát thương** nếu không chống trả kịp thời!")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        if st.button("🔫 Bắn hạ quái vật (Dùng 1 đạn)", use_container_width=True):
            if st.session_state.ammo > 0:
                st.session_state.ammo -= 1
                st.success(f"💥 BẮP TRÚNG! Bạn đã tiêu diệt gọn gàng quái vật và thu về **+{event['value']} vàng**!")
                st.session_state.gold += event["value"]
                st.session_state.inventory.append(f"Chiến lợi phẩm: {event['name']}")
                st.session_state.state = "DOCK"
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Bạn đã hết đạn! Không thể bắn hạ quái vật!")
    with col_e2:
        if st.button("🏃 Cố gắng cắt dây tháo chạy", use_container_width=True):
            st.warning(f"Bạn cắt dây tháo chạy nhưng bị dính **{event['dmg']} sát thương**!")
            st.session_state.hp -= event["dmg"]
            st.session_state.state = "DOCK"
            
            if st.session_state.hp <= 0:
                st.error("💀 Bạn đã cạn kiệt HP và ngất xỉu! Game Over.")
            time.sleep(1)
            st.rerun()

# Cửa hàng mua sắm vật phẩm
elif st.session_state.state == "SHOP":
    st.subheader("🛒 Cửa Hàng Trang Bị & Sinh Tồn")
    
    s1, s2 = st.columns(2)
    with s1:
        st.write("**Hộp đạn tự vệ (5 viên)**")
        st.write("Giá: **60 🪙**")
        if st.button("Mua đạn"):
            if st.session_state.gold >= 60:
                st.session_state.gold -= 60
                st.session_state.ammo += 5
                st.success("Đã mua thành công 5 viên đạn!")
                st.rerun()
            else:
                st.error("Không đủ tiền vàng!")
                
    with s2:
        st.write("**Bình cứu thương (+50 HP)**")
        st.write("Giá: **50 🪙**")
        if st.button("Mua máu"):
            if st.session_state.gold >= 50:
                st.session_state.gold -= 50
                st.session_state.hp = min(100, st.session_state.hp + 50)
                st.success("Đã hồi phục 50 HP!")
                st.rerun()
            else:
                st.error("Không đủ tiền vàng!")
                
    st.markdown("---")
    if st.button("🏠 Quay lại bến tàu", use_container_width=True):
        st.session_state.state = "DOCK"
        st.rerun()
