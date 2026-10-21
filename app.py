import random
import time
import streamlit as st

st.set_page_config(page_title="How to Fish - Phiên bản Bá Đạo", page_icon="🎣", layout="centered")

# --- 1. KHỞI TẠO TRẠNG THÁI GAME ---
if "money" not in st.session_state:
    st.session_state.money = 150
    st.session_state.gear_level = 1  # 1: Cần câu tre, 2: Súng lục săn cá, 3: Súng ngắm đại dương
    st.session_state.inventory = []
    st.session_state.game_state = "IDLE"  # IDLE, FISHING, ACTION
    st.session_state.current_target = None

# Danh sách trang bị và vũ khí câu cá
GEARS = {
    1: {"name": "🎋 Cần câu tre truyền thống", "cost": 0, "power": 1},
    2: {"name": "🔫 Súng lục săn cá (Pistol)", "cost": 300, "power": 3},
    3: {"name": "🎯 Súng ngắm săn cá mập (Sniper)", "cost": 1000, "power": 5}
}

# Cơ sở dữ liệu cá và quái vật biển
FISH_DB = [
    {"name": "🐟 Cá Rô Phi ngơ ngác", "value": 30, "chance": 50, "type": "Thường"},
    {"name": "🐠 Cá hề đột biến", "value": 60, "chance": 35, "type": "Hiếm"},
    {"name": "🦈 Cá mập hung tợn", "value": 200, "chance": 12, "type": "Cực Hiếm"},
    {"name": "🐉 Thủy quái hồ sâu (Boss)", "value": 600, "chance": 3, "type": "Huyền Thoại"}
]

# --- 2. GIAO DIỆN CHÍNH ---
st.title("🎣 HOW TO FISH: Bản Săn Cá Bá Đạo")
st.markdown("*(Không chỉ là câu cá, đây là sinh tồn!)*")

# Bảng thông tin người chơi
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💰 Tiền thưởng", f"{st.session_state.money} 🪙")
with col2:
    current_gear = GEARS[st.session_state.gear_level]["name"]
    st.metric("🛠️ Trang bị hiện tại", current_gear)
with col3:
    st.metric("🎒 Kho chiến lợi phẩm", len(st.session_state.inventory))

st.markdown("---")

# --- 3. KHU VỰC HÀNH ĐỘNG ---

if st.session_state.game_state == "IDLE":
    st.subheader("🌅 Bạn đã sẵn sàng ra khơi chưa?")
    st.write("Chọn phương thức tác chiến bên dưới để bắt đầu kiếm tiền và săn những con cá độc lạ:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🎣 Đi câu cá thư giãn", use_container_width=True):
            st.session_state.game_state = "FISHING"
            st.rerun()
    with col_b:
        if st.session_state.gear_level > 1:
            if st.button("💥 Dùng vũ khí săn cá tốc độ cao", use_container_width=True):
                st.session_state.game_state = "ACTION"
                st.rerun()
        else:
            st.info("🔒 Cần nâng cấp lên Súng để mở khóa chế độ hành động!")

elif st.session_state.game_state == "FISHING":
    st.info("🌊 Đang thả mồi chờ cá cắn câu...")
    time.sleep(1.2)
    
    # Random tỷ lệ bắt cá dựa trên cấp độ trang bị
    roll = random.randint(1, 100)
    gear_bonus = GEARS[st.session_state.gear_level]["power"] * 3
    
    if roll <= 50 - gear_bonus:
        fish = FISH_DB[0]
    elif roll <= 85 - gear_bonus:
        fish = FISH_DB[1]
    elif roll <= 97:
        fish = FISH_DB[2]
    else:
        fish = FISH_DB[3]
        
    st.session_state.current_target = fish
    st.session_state.game_state = "RESULT"
    st.rerun()

elif st.session_state.game_state == "ACTION":
    st.warning("🎯 Phát hiện động tĩnh lớn dưới mặt nước! Ngắm và bóp cò ngay!")
    time.sleep(1)
    
    # Chế độ dùng súng dễ bắt cá to hơn
    fish = random.choice(FISH_DB[1:]) # Ưu đãi cá to
    st.session_state.current_target = fish
    st.session_state.game_state = "RESULT"
    st.rerun()

elif st.session_state.game_state == "RESULT":
    fish = st.session_state.current_target
    st.success(f"🎉 Bạn đã tóm gọn: **{fish['name']}** (Loại: {fish['type']})!")
    st.write(f"Giá trị quy đổi: **+{fish['value']} 🪙**")
    
    st.session_state.money += fish["value"]
    st.session_state.inventory.append(fish["name"])
    
    if st.button("🔄 Tiếp tục hành trình", use_container_width=True):
        st.session_state.game_state = "IDLE"
        st.rerun()

# --- 4. CỬA HÀNG NÂNG CẤP VŨ KHÍ & CẦN CÂU ---
st.markdown("---")
st.subheader("🛒 Cửa Hàng Vũ Khí & Dụng Cụ")

c1, c2 = st.columns(2)

with c1:
    st.write("**🔫 Súng lục săn cá (Cấp 2)**")
    st.write("Giá: **300 🪙** - Tăng tỷ lệ gặp cá lớn.")
    if st.session_state.gear_level < 2:
        if st.button("Mua Súng Lục"):
            if st.session_state.money >= 300:
                st.session_state.money -= 300
                st.session_state.gear_level = 2
                st.success("Đã mua Súng Lục thành công!")
                st.rerun()
            else:
                st.error("Không đủ tiền!")
    else:
        st.info("Đã sở hữu ✅")

with c2:
    st.write("**🎯 Súng ngắm đại dương (Cấp 3)**")
    st.write("Giá: **1000 🪙** - Săn boss và cá khổng lồ.")
    if st.session_state.gear_level < 3:
        if st.button("Mua Súng Ngắm"):
            if st.session_state.money >= 1000:
                st.session_state.money -= 1000
                st.session_state.gear_level = 3
                st.success("Đã mua Súng Ngắm thành công!")
                st.rerun()
            else:
                st.error("Không đủ tiền!")
    else:
        st.info("Đã sở hữu ✅")
