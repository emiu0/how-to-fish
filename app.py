import random
import time
import streamlit as st

# Cấu hình trang web
st.set_page_config(page_title="How to Fish - Phiêu Lưu Khám Phá Đảo", page_icon="🎣", layout="centered")

# CSS tùy chỉnh hình nền và giao diện Banner Game
st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        text-shadow: 2px 2px 4px #00000033;
    }
    .banner-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
    }
    .island-card {
        background-color: #f0f2f6;
        border-left: 5px solid #1E88E5;
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. DỮ LIỆU CÁC ĐẢO VÀ CÁ MỤC TIÊU (MAPS & BOSSES) ---
ISLANDS = {
    1: {
        "name": "🏝️ Đảo Tân Thủ (Green Lake)",
        "bg_color": "🟢 Map Dễ",
        "description": "Vùng nước nông yên bình, thích hợp cho người mới bắt đầu.",
        "fishes": ["🐟 Cá Rô Phi", "🐠 Cá Bảy Màu", "🦐 Tôm Sông"],
        "boss": "🦈 Cá Trê Khổng Lồ",
        "key_needed": None,
        "key_reward": "Chìa khóa Đảo San Hò 🗝️"
    },
    2: {
        "name": "🪸 Đảo San Hò (Coral Atoll)",
        "bg_color": "🔵 Map Trung Bình",
        "description": "Vùng biển xanh thẫm với nhiều loài cá ngầm hung dữ.",
        "fishes": ["🐟 Cá Hồi Đại Dương", "🐙 Bạch Tuộc Nhỏ", "🦀 Cua Hoàng Gia"],
        "boss": "🐊 Cá Sấu Đầm Lầy",
        "key_needed": "Chìa khóa Đảo San Hò 🗝️",
        "key_reward": "Chìa khóa Đảo Quái Vật 🔑"
    },
    3: {
        "name": "🌋 Đảo Quái Vật (Volcano Isle)",
        "bg_color": "🔴 Map Khó",
        "description": "Vùng biển núi lửa nóng rực, sinh sống bởi các loài thủy quái biến dị.",
        "fishes": ["🦈 Cá Mập Xám", "🦑 Mực Ống Đại Dương", "🐍 Rắn Biển Độc"],
        "boss": "🐉 Thủy Quái Leviathan",
        "key_needed": "Chìa khóa Đảo Quái Vật 🔑",
        "key_reward": "Chìa khóa Đảo Băng Giá 🗝️✨"
    }
}

# --- 2. KHỜI TẠO STATE GAME ---
if "gold" not in st.session_state:
    st.session_state.gold = 100
    st.session_state.hp = 100
    st.session_state.current_island = 1
    st.session_state.keys = []            # Chìa khóa sở hữu
    st.session_state.inventory = []       # Cá đã bắt
    st.session_state.boat_level = 1       # Cấp thuyền
    st.session_state.game_menu = "FISHING"# MENU: FISHING, MAP, SHOP, INVENTORY

# --- 3. BANNER HÌNH NỀN CHÍNH & TIÊU ĐỀ GAME ---
st.markdown("""
    <div class="banner-box">
        <h1 style='margin:0;'>🎣 HOW TO FISH: ISLAND ADVENTURE</h1>
        <p style='margin-top:5px; font-style: italic;'>Khám phá đảo mới • Săn cá mục tiêu • Tìm chìa khóa lái thuyền!</p>
    </div>
""", unsafe_allow_html=True)

# Hiển thị thông số trên cùng
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💰 Tiền vàng", f"{st.session_state.gold} 🪙")
with c2:
    st.metric("❤️ HP Sinh tồn", f"{st.session_state.hp}/100")
with c3:
    st.metric("🚤 Cấp Thuyền", f"Cấp {st.session_state.boat_level}")
with c4:
    st.metric("🔑 Số chìa khóa", len(st.session_state.keys))

st.markdown("---")

# --- 4. THANH MENU ĐIỀU HƯỚNG GAME ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    if st.button("🎣 Hồ Câu Cá", use_container_width=True):
        st.session_state.game_menu = "FISHING"
        st.rerun()
with m2:
    if st.button("🗺️ Lái Thuyền Sang Đảo", use_container_width=True):
        st.session_state.game_menu = "MAP"
        st.rerun()
with m3:
    if st.button("🛒 Cửa Hàng Nâng Cấp", use_container_width=True):
        st.session_state.game_menu = "SHOP"
        st.rerun()
with m4:
    if st.button("🎒 Kho Đồ & Chìa Khóa", use_container_width=True):
        st.session_state.game_menu = "INVENTORY"
        st.rerun()

st.markdown("---")

current_map = ISLANDS[st.session_state.current_island]

# --- 5. MÀN HÌNH MỤC CÂU CÁ (FISHING) ---
if st.session_state.game_menu == "FISHING":
    st.subheader(f"📍 Đang ở: {current_map['name']}")
    st.info(f"ℹ️ {current_map['description']} | Mức độ: **{current_map['bg_color']}**")
    
    st.markdown("#### 🎯 Mục tiêu hiện tại:")
    st.write(f"- Săn cá lớn Boss: **{current_map['boss']}** để nhận **{current_map['key_reward']}**!")
    
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        if st.button("🎣 Thả cần câu cá thường", use_container_width=True):
            with st.spinner("Đang đợi cá cắn câu..."):
                time.sleep(1)
                caught = random.choice(current_map["fishes"])
                earned = random.randint(20, 60) * st.session_state.current_island
                st.session_state.gold += earned
                st.session_state.inventory.append(caught)
                st.success(f"🎉 Bạn đã bắt được **{caught}** và bán được **+{earned} 🪙**!")

    with col_act2:
        if st.button(f"⚔️ Tấn công Boss ({current_map['boss']})", use_container_width=True):
            with st.spinner("Đang giao chiến nảy lửa với cá lớn mục tiêu..."):
                time.sleep(1.5)
                # Tỷ lệ thắng dựa trên cấp thuyền
                win_rate = 40 + (st.session_state.boat_level * 20)
                roll = random.randint(1, 100)
                
                if roll <= win_rate:
                    reward_key = current_map["key_reward"]
                    st.balloons()
                    st.success(f"💥 XUẤT SẮC! Bạn đã hạ gục **{current_map['boss']}**!")
                    
                    if reward_key not in st.session_state.keys:
                        st.session_state.keys.append(reward_key)
                        st.info(f"🗝️ Bạn nhận được: **{reward_key}**! Bây giờ bạn có thể lái thuyền sang đảo tiếp theo!")
                    else:
                        st.session_state.gold += 300
                        st.write("Bạn nhận được thêm +300 🪙 tiền thưởng!")
                else:
                    dmg = random.randint(15, 30)
                    st.session_state.hp -= dmg
                    st.error(f"💥 Boss phản công dữ dội! Bạn thất bại và bị trừ **-{dmg} HP**!")

# --- 6. MÀN HÌNH BẢN ĐỒ LÁI THUYỀN SANG ĐẢO (MAP) ---
elif st.session_state.game_menu == "MAP":
    st.subheader("🗺️ Bản Đồ Bãi Biển & Lái Thuyền Sang Đảo")
    st.write("Chọn hòn đảo bạn muốn lái thuyền di chuyển đến:")
    
    for island_id, data in ISLANDS.items():
        st.markdown(f"""
            <div class="island-card">
                <h4>{data['name']} ({data['bg_color']})</h4>
                <p>{data['description']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        c_map1, c_map2 = st.columns([2, 1])
        with c_map1:
            if data["key_needed"] is None:
                st.caption("✅ Đảo tự do (Tân thủ)")
            else:
                if data["key_needed"] in st.session_state.keys:
                    st.caption(f"🔓 Đã mở khóa (Sở hữu: {data['key_needed']})")
                else:
                    st.caption(f"🔒 Yêu cầu: {data['key_needed']}")
        
        with c_map2:
            if st.session_state.current_island == island_id:
                st.button("📍 Đang ở đây", key=f"is_{island_id}", disabled=True)
            else:
                # Kiểm tra điều kiện có chìa khóa chưa
                can_go = (data["key_needed"] is None) or (data["key_needed"] in st.session_state.keys)
                if st.button("⛵ Lái thuyền đến", key=f"is_{island_id}", disabled=not can_go):
                    st.session_state.current_island = island_id
                    st.success(f"Đã di chuyển thuyền đến **{data['name']}**!")
                    st.rerun()

# --- 7. MÀN HÌNH CỬA HÀNG (SHOP) ---
elif st.session_state.game_menu == "SHOP":
    st.subheader("🛒 Cửa Hàng Nâng Cấp Thuyền & Vật Phẩm")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("**🚤 Nâng Cấp Thuyền (Tăng % thắng Boss)**")
        cost = st.session_state.boat_level * 200
        st.write(f"Cấp hiện tại: **{st.session_state.boat_level}** | Giá nâng cấp: **{cost} 🪙**")
        if st.button("Nâng Cấp Thuyền"):
            if st.session_state.gold >= cost:
                st.session_state.gold -= cost
                st.session_state.boat_level += 1
                st.success("Thuyền đã được gia cố vững chắc hơn!")
                st.rerun()
            else:
                st.error("Không đủ vàng!")

    with col_s2:
        st.write("**❤️ Hồi Phục Máu Sinh Tồn (+50 HP)**")
        st.write("Giá: **60 🪙**")
        if st.button("Mua Bình Hồi Máu"):
            if st.session_state.gold >= 60:
                st.session_state.gold -= 60
                st.session_state.hp = min(100, st.session_state.hp + 50)
                st.success("Đã hồi phục máu thành công!")
                st.rerun()
            else:
                st.error("Không đủ vàng!")

# --- 8. MÀN HÌNH KHO ĐỒ & CHÌA KHÓA (INVENTORY) ---
elif st.session_state.game_menu == "INVENTORY":
    st.subheader("🎒 Kho Vật Phẩm & Chìa Khóa Hành Trình")
    
    st.markdown("#### 🗝️ Chìa Khóa Sở Hữu:")
    if st.session_state.keys:
        for k in st.session_state.keys:
            st.write(f"- {k}")
    else:
        st.write("Chưa có chìa khóa nào. Hãy đi săn cá Boss ở mục Hồ Câu để kiếm chìa khóa!")
        
    st.markdown("---")
    st.markdown("#### 🐟 Bộ Sưu Tập Cá Đã Bắt:")
    if st.session_state.inventory:
        st.write(", ".join(set(st.session_state.inventory)))
    else:
        st.write("Kho cá đang trống.")
