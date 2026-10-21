import random
import time
import streamlit as st

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="How to Fish - Island Explorer", page_icon="🎣", layout="centered")

# CSS tùy chỉnh hình nền Banner chính
st.markdown("""
    <style>
    .banner-container {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #00d2ff;
        box-shadow: 0px 4px 15px rgba(0, 210, 255, 0.3);
        margin-bottom: 20px;
    }
    .island-box {
        background-color: #1e293b;
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #00d2ff;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. DỮ LIỆU BẢN ĐỒ CÁC ĐẢO & CHÌA KHÓA ---
# Mỗi đảo có 'key_id_needed' (ID chìa khóa cần để vào) và 'key_id_reward' (ID chìa khóa nhận được khi thắng Boss)
ISLAND_DATA = {
    1: {
        "name": "🏝️ Đảo Tân Thủ (Green Lake)",
        "difficulty": "Dễ 🟢",
        "desc": "Vùng nước nông yên bình, nơi lý tưởng để bắt đầu sự nghiệp câu cá.",
        "fishes": ["🐟 Cá Rô Phi", "🐠 Cá Bảy Màu", "🦐 Tôm Biển"],
        "boss": "🦈 Cá Trê Khổng Lồ",
        "key_id_needed": None,       # Không cần chìa khóa
        "key_id_reward": 2,          # Thắng Boss đảo 1 sẽ nhận Chìa Khóa vào Đảo 2
        "reward_name": "🗝️ Chìa Khóa San Hò"
    },
    2: {
        "name": "🪸 Đảo San Hò (Coral Reef)",
        "difficulty": "Trung Bình 🔵",
        "desc": "Vùng biển xanh thẫm ẩn chứa nhiều sinh vật săn mồi hung hãn.",
        "fishes": ["🐟 Cá Hồi Đại Dương", "🐙 Bạch Tuộc Nhỏ", "🦀 Cua Hoàng Gia"],
        "boss": "🐊 Cá Sấu Nước Mặn",
        "key_id_needed": 2,          # Cần chìa khóa ID 2
        "key_id_reward": 3,          # Thắng Boss đảo 2 sẽ nhận Chìa Khóa vào Đảo 3
        "reward_name": "🔑 Chìa Khóa Quái Vật"
    },
    3: {
        "name": "🌋 Đảo Quái Vật (Volcano Isle)",
        "difficulty": "Khó 🔴",
        "desc": "Vùng biển núi lửa nóng rực, sào huyệt của các thủy quái dị biến.",
        "fishes": ["🦈 Cá Mập Xám", "🦑 Mực Khổng Lồ", "🐍 Rắn Biển Biến Dị"],
        "boss": "🐉 Thủy Quái Leviathan",
        "key_id_needed": 3,          # Cần chìa khóa ID 3
        "key_id_reward": 4,
        "reward_name": "🗝️✨ Chìa Khóa Huyền Thoại"
    }
}

# --- 2. KHỞI TẠO KHÔNG GIAN LƯU TRỮ (SESSION STATE) ---
if "gold" not in st.session_state:
    st.session_state.gold = 200
    st.session_state.hp = 100
    st.session_state.current_island = 1
    st.session_state.owned_keys = [1]      # Mặc định sở hữu Chìa khóa Đảo 1
    st.session_state.inventory = []
    st.session_state.boat_level = 1
    st.session_state.nav_menu = "FISHING"  # FISHING, MAP, SHOP, INVENTORY

# --- 3. BANNER HÌNH NỀN CHÍNH DÀNH CHO GAME ---
st.markdown("""
    <div class="banner-container">
        <h1 style='margin:0; font-size: 32px;'>🎣 HOW TO FISH: BẢN ĐỒ VÀ ĐẢO</h1>
        <p style='margin-top:8px; font-style: italic; color: #cbd5e1;'>
            Câu cá tích vàng • Săn Boss nhận chìa khóa • Lái thuyền khám phá đại dương!
        </p>
    </div>
""", unsafe_allow_html=True)

# Thanh hiển thị chỉ số nhân vật
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💰 Vàng", f"{st.session_state.gold} 🪙")
with c2:
    st.metric("❤️ Sinh Lực", f"{st.session_state.hp}/100")
with c3:
    st.metric("🚤 Thuyền", f"Cấp {st.session_state.boat_level}")
with c4:
    st.metric("🔑 Số Chìa Khóa", len(st.session_state.owned_keys))

st.markdown("---")

# --- 4. THANH MENU CHÍNH ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    if st.button("🎣 Hồ Câu", key="nav_fish", use_container_width=True):
        st.session_state.nav_menu = "FISHING"
        st.rerun()
with m2:
    if st.button("🗺️ Chọn Đảo", key="nav_map", use_container_width=True):
        st.session_state.nav_menu = "MAP"
        st.rerun()
with m3:
    if st.button("🛒 Cửa Hàng", key="nav_shop", use_container_width=True):
        st.session_state.nav_menu = "SHOP"
        st.rerun()
with m4:
    if st.button("🎒 Kho Đồ", key="nav_inv", use_container_width=True):
        st.session_state.nav_menu = "INVENTORY"
        st.rerun()

st.markdown("---")

current_island_data = ISLAND_DATA[st.session_state.current_island]

# --- 5. MÀN HÌNH MỤC CÂU CÁ & SĂN BOSS ---
if st.session_state.nav_menu == "FISHING":
    st.subheader(f"📍 Vị trí: {current_island_data['name']}")
    st.write(f"_{current_island_data['desc']}_")
    
    st.info(f"🎯 **Nhiệm vụ Đảo này:** Đánh bại Boss **{current_island_data['boss']}** để đoạt lấy **{current_island_data['reward_name']}**!")
    
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        if st.button("🎣 Câu cá kiếm tiền", key="btn_fish_normal", use_container_width=True):
            with st.spinner("Đang chờ cá cắn câu..."):
                time.sleep(0.7)
                caught_fish = random.choice(current_island_data["fishes"])
                earned_gold = random.randint(30, 70) * st.session_state.current_island
                
                st.session_state.gold += earned_gold
                st.session_state.inventory.append(caught_fish)
                st.success(f"🎉 Bạn câu được **{caught_fish}** và bán được **+{earned_gold} 🪙**!")

    with col_act2:
        if st.button(f"⚔️ Giao chiến với Boss", key="btn_fight_boss", use_container_width=True):
            with st.spinner("Đang chiến đấu kịch liệt với Boss..."):
                time.sleep(1.2)
                # Tỷ lệ chiến thắng phụ thuộc vào cấp thuyền
                win_chance = 40 + (st.session_state.boat_level * 15)
                roll = random.randint(1, 100)
                
                if roll <= win_chance:
                    st.balloons()
                    st.success(f"💥 XUẤT SẮC! Bạn đã đánh bại **{current_island_data['boss']}**!")
                    
                    target_key_id = current_island_data["key_id_reward"]
                    if target_key_id not in st.session_state.owned_keys:
                        st.session_state.owned_keys.append(target_key_id)
                        st.info(f"🗝️ Bạn đã nhặt được: **{current_island_data['reward_name']}**! Giờ bạn đã có thể lái thuyền sang đảo tiếp theo trên Bản Đồ!")
                    else:
                        st.session_state.gold += 300
                        st.write("Bạn nhận được tiền thưởng thêm **+300 🪙** vàng!")
                else:
                    damage = random.randint(15, 30)
                    st.session_state.hp -= damage
                    st.error(f"💥 Boss phản đòn quá mạnh! Bạn bị mất **-{damage} HP**!")

# --- 6. MÀN HÌNH BẢN ĐỒ LÁI THUYỀN SANG ĐẢO (ĐÃ SỬA SẠCH LỖI KEY) ---
elif st.session_state.nav_menu == "MAP":
    st.subheader("🗺️ Bản Đồ Đại Dương & Bến Tàu")
    st.write("Chọn hòn đảo muốn lái thuyền cập bến:")
    
    for island_id, data in ISLAND_DATA.items():
        st.markdown(f"""
            <div class="island-box">
                <h4 style='margin:0;'>{data['name']} ({data['difficulty']})</h4>
                <p style='margin:5px 0 0 0; font-size: 14px;'>{data['desc']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_m1, col_m2 = st.columns([2, 1])
        
        # Kiểm tra điều kiện mở khóa đảo
        req_key = data["key_id_needed"]
        has_access = (req_key is None) or (req_key in st.session_state.owned_keys)
        
        with col_m1:
            if req_key is None:
                st.caption("✅ Đảo Tân Thủ (Đã mở sẵn)")
            elif has_access:
                st.caption("🔓 Đã có chìa khóa mở cổng đảo!")
            else:
                st.caption(f"🔒 Cần chìa khóa: **{ISLAND_DATA[req_key - 1]['reward_name']}** (Đánh bại Boss Đảo {req_key - 1} để lấy)")
                
        with col_m2:
            if st.session_state.current_island == island_id:
                st.button("📍 Đang ở đây", key=f"island_curr_{island_id}", disabled=True, use_container_width=True)
            else:
                # Tạo key duy nhất cho nút bấm lái thuyền
                if st.button("⛵ Lái thuyền đến", key=f"island_goto_{island_id}", disabled=not has_access, use_container_width=True):
                    st.session_state.current_island = island_id
                    st.success(f"Đã di chuyển thuyền đến **{data['name']}**!")
                    st.rerun()

# --- 7. MÀN HÌNH CỬA HÀNG ---
elif st.session_state.nav_menu == "SHOP":
    st.subheader("🛒 Cửa Hàng Bến Tàu")
    
    shop_col1, shop_col2 = st.columns(2)
    with shop_col1:
        st.write("**🚤 Nâng cấp Thuyền**")
        upgrade_cost = st.session_state.boat_level * 200
        st.write(f"Cấp thuyền: {st.session_state.boat_level} ➔ Tăng % thắng Boss")
        st.write(f"Giá: **{upgrade_cost} 🪙**")
        
        if st.button("Nâng cấp ngay", key="btn_upgrade_boat"):
            if st.session_state.gold >= upgrade_cost:
                st.session_state.gold -= upgrade_cost
                st.session_state.boat_level += 1
                st.success("Thuyền đã được gia cố kiên cố hơn!")
                st.rerun()
            else:
                st.error("Không đủ vàng!")

    with shop_col2:
        st.write("**❤️ Hồi Phục Sinh Lực (+50 HP)**")
        st.write("Giá: **60 🪙**")
        
        if st.button("Mua Bình Máu", key="btn_buy_hp"):
            if st.session_state.gold >= 60:
                st.session_state.gold -= 60
                st.session_state.hp = min(100, st.session_state.hp + 50)
                st.success("Đã hồi phục 50 HP!")
                st.rerun()
            else:
                st.error("Không đủ vàng!")

# --- 8. MÀN HÌNH KHO ĐỒ & CHÌA KHÓA ---
elif st.session_state.nav_menu == "INVENTORY":
    st.subheader("🎒 Kho Đồ & Chìa Khóa Hành Trình")
    
    st.markdown("#### 🔑 Danh Sách Chìa Khóa Đã Sở Hữu:")
    if st.session_state.owned_keys:
        for k_id in st.session_state.owned_keys:
            if k_id == 1:
                st.write("- 🗝️ Chìa Khóa Tân Thủ (Mở Đảo 1)")
            else:
                st.write(f"- {ISLAND_DATA[k_id - 1]['reward_name']} (Mở Đảo {k_id})")
    else:
        st.write("Chưa có chìa khóa nào.")
        
    st.markdown("---")
    st.markdown("#### 🐟 Bộ Sưu Tập Cá Đã Câu:")
    if st.session_state.inventory:
        st.write(", ".join(set(st.session_state.inventory)))
    else:
        st.write("Kho cá đang trống.")
