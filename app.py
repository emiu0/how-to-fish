import random
import time
import streamlit as st

st.set_page_config(page_title="How to Fish - Trò chơi câu cá", page_icon="🎣", layout="centered")

# --- 1. KHỞI TẠO TRẠNG THÁI GAME (SESSION STATE) ---
if "money" not in st.session_state:
    st.session_state.money = 100
    st.session_state.rod_level = 1  # Cấp độ cần câu
    st.session_state.inventory = []  # Danh sách cá đã bắt
    st.session_state.game_state = "IDLE"  # IDLE, CASTING, BITE, REELING
    st.session_state.current_fish = None
    st.session_state.tension = 50  # Độ căng dây câu (0 - 100)

# Danh sách các loại cá tương ứng với cấp độ cần câu
FISH_DATABASE = {
    1: [
        {"name": "🐟 Cá Rô Phi", "value": 20, "difficulty": 30, "rarity": "Thường"},
        {"name": "🐠 Cá Cảnh Nhỏ", "value": 35, "difficulty": 45, "rarity": "Thường"},
        {"name": "🦐 Tôm Sông", "value": 15, "difficulty": 20, "rarity": "Thường"}
    ],
    2: [
        {"name": "🐟 Cá Rô Phi", "value": 20, "difficulty": 30, "rarity": "Thường"},
        {"name": "🦈 Cá Hồi", "value": 80, "difficulty": 60, "rarity": "Hiếm"},
        {"name": "🐙 Bạch Tuộc Nhỏ", "value": 120, "difficulty": 75, "rarity": "Hiếm"}
    ],
    3: [
        {"name": "🦈 Cá Hồi", "value": 80, "difficulty": 60, "rarity": "Hiếm"},
        {"name": "🐋 Cá Ngừ Đại Dương", "value": 300, "difficulty": 85, "rarity": "Cực Hiếm"},
        {"name": "🐉 Cá Mập Trắng", "value": 600, "difficulty": 95, "rarity": "Huyền Thoại"}
    ]
}

# --- 2. GIAO DIỆN CHÍNH (HEADER & THÔNG SỐ) ---
st.title("🎣 HOW TO FISH - Game Câu Cá Ảo")
st.markdown("Hành trình trở thành vua câu cá từ bờ hồ đến đại dương!")

# Hiển thị thông tin người chơi ở sidebar hoặc khung trên
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💰 Tiền (Vàng)", f"{st.session_state.money} 🪙")
with col2:
    st.metric("🎣 Cấp Cần Câu", f"Cấp {st.session_state.rod_level}")
with col3:
    st.metric("🎒 Số cá trong kho", len(st.session_state.inventory))

st.markdown("---")

# --- 3. KHU VỰC ĐIỀU KHIỂN & GAMEPLAY ---

# Trạng thái 1: Đang ở bờ hồ / chờ quăng cần
if st.session_state.game_state == "IDLE":
    st.subheader("🌅 Bạn đang đứng ở bờ hồ yên bình...")
    st.write("Hãy nhấn nút bên dưới để quăng cần câu xuống nước và chờ cá cắn câu nhé!")
    
    if st.button("🎣 Quăng Cần Ngay!", use_container_width=True):
        st.session_state.game_state = "BITE"
        st.rerun()

# Trạng thái 2: Chờ cá cắn câu
elif st.session_state.game_state == "BITE":
    st.info("🌊 Phao đang nổi trên mặt nước... Đang đợi cá cắn câu...")
    
    # Giả lập thời gian chờ cá cắn ngẫu nhiên
    time.sleep(1.5)
    
    # Chọn ngẫu nhiên loại cá dựa trên cấp cần câu hiện tại
    available_fish = FISH_DATABASE.get(st.session_state.rod_level, FISH_DATABASE[1])
    st.session_state.current_fish = random.choice(available_fish)
    
    st.session_state.game_state = "REELING"
    st.rerun()

# Trạng thái 3: Kéo cá lên (Reeling Minigame)
elif st.session_state.game_state == "REELING":
    fish = st.session_state.current_fish
    st.warning(f"⚠️ **CÓ CÁ CẮN CÂU!** Đây là **{fish['name']}** (Độ hiếm: {fish['rarity']})")
    st.write("Hãy điều chỉnh lực kéo để giữ dây không bị đứt hoặc để cá sổng mất!")
    
    # Thanh trượt mô phỏng độ căng dây (Người chơi phải giữ ở khoảng an toàn từ 40 đến 70)
    pull_force = st.slider("Độ kéo dây (Cố gắng giữ vùng an toàn 40-70):", 0, 100, 50)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🎯 Giữ & Kéo!", use_container_width=True):
            # Kiểm tra độ căng dây so với độ khó của cá
            target_diff = fish["difficulty"]
            if abs(pull_force - target_diff) <= 15:
                st.success(f"🎉 Chúc mừng! Bạn đã kéo thành công **{fish['name']}**!")
                st.session_state.money += fish["value"]
                st.session_state.inventory.append(fish["name"])
                st.session_state.game_state = "IDLE"
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("💥 Dây câu bị căng quá hoặc chùng quá! Cá đã xổng mất rồi!")
                st.session_state.game_state = "IDLE"
                time.sleep(1)
                st.rerun()
                
    with col_b:
        if st.button("❌ Cắt dây chạy trốn", use_container_width=True):
            st.warning("Bạn đã cắt dây để bảo toàn lực.")
            st.session_state.game_state = "IDLE"
            st.rerun()

# --- 4. CỬA HÀNG NÂNG CẤP (SHOP) ---
st.markdown("---")
st.subheader("🛒 Cửa Hàng Nâng Cấp Cần Câu")

col_shop1, col_shop2 = st.columns(2)

with col_shop1:
    st.write("**Cần câu Cấp 2** (Mở khóa cá Hiếm)")
    st.write("Giá: **150 🪙**")
    if st.session_state.rod_level < 2:
        if st.button("Nâng cấp Cần Cấp 2"):
            if st.session_state.money >= 150:
                st.session_state.money -= 150
                st.session_state.rod_level = 2
                st.success("Nâng cấp thành công cần câu Cấp 2!")
                st.rerun()
            else:
                st.error("Bạn không đủ tiền!")
    else:
        st.info("Đã sở hữu")

with col_shop2:
    st.write("**Cần câu Cấp 3** (Mở khóa cá Huyền Thoại)")
    st.write("Giá: **500 🪙**")
    if st.session_state.rod_level < 3:
        if st.button("Nâng cấp Cần Cấp 3"):
            if st.session_state.money >= 500:
                st.session_state.money -= 500
                st.session_state.rod_level = 3
                st.success("Nâng cấp thành công cần câu Cấp 3!")
                st.rerun()
            else:
                st.error("Bạn không đủ tiền!")
    else:
        st.info("Đã sở hữu")
