import random
import time
import streamlit as st

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="How to Catch Fish", page_icon="🎣", layout="wide")

# --- CSS TÙY CHỈNH GIAO DIỆN CHUẨN NHƯ ẢNH ---
st.markdown("""
    <style>
    /* Ẩn header mặc định của streamlit để giống game full màn hình */
    header {visibility: hidden;}
    .stApp {
        background: linear-gradient(135deg, #0b1d28 0%, #162636 50%, #13222d 100%);
        color: #e2e8f0;
    }
    
    /* Giao diện màn hình chính (Main Menu) */
    .menu-container {
        position: absolute;
        top: 15%;
        left: 8%;
        z-index: 10;
        width: 300px;
    }
    .game-title {
        font-family: 'Courier New', Courier, monospace;
        font-size: 52px;
        font-weight: 900;
        line-height: 0.95;
        color: #f6ad55;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
        margin-bottom: 5px;
    }
    .game-subtitle {
        font-size: 11px;
        letter-spacing: 3px;
        color: #cbd5e1;
        text-transform: uppercase;
        margin-bottom: 25px;
        border-left: 2px solid #f6ad55;
        padding-left: 8px;
    }
    
    /* Hiển thị hòn đảo / đại dương minh họa bên phải */
    .island-view-box {
        background: radial-gradient(circle, #2d5a6f 0%, #0d212c 70%);
        border: 2px solid #2d4a5c;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.6);
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. DỮ LIỆU ĐẢO VÀ CHÌA KHÓA ---
ISLAND_DATA = {
    1: {
        "name": "🏝️ Đảo Tân Thủ (Green Lake)",
        "difficulty": "Dễ 🟢",
        "desc": "Vùng nước nông yên bình, nơi bắt đầu cuộc hành trình.",
        "fishes": ["🐟 Cá Rô Phi", "🐠 Cá Bảy Màu", "🦐 Tôm Sông"],
        "boss": "🦈 Cá Trê Khổng Lồ",
        "key_id_needed": None,
        "key_id_reward": 2,
        "reward_name": "🗝️ Chìa Khóa San Hò"
    },
    2: {
        "name": "🪸 Đảo San Hò (Coral Reef)",
        "difficulty": "Trung Bình 🔵",
        "desc": "Vùng biển xanh thẫm ẩn chứa sinh vật nguy hiểm.",
        "fishes": ["🐟 Cá Hồi Đại Dương", "🐙 Bạch Tuộc Nhỏ", "🦀 Cua Hoàng Gia"],
        "boss": "🐊 Cá Sấu Nước Mặn",
        "key_id_needed": 2,
        "key_id_reward": 3,
        "reward_name": "🔑 Chìa Khóa Quái Vật"
    },
    3: {
        "name": "🌋 Đảo Quái Vật (Volcano Isle)",
        "difficulty": "Khó 🔴",
        "desc": "Vùng biển núi lửa nóng rực, sào huyệt của thủy quái.",
        "fishes": ["🦈 Cá Mập Xám", "🦑 Mực Khổng Lồ", "🐍 Rắn Biển Biến Dị"],
        "boss": "🐉 Thủy Quái Leviathan",
        "key_id_needed": 3,
        "key_id_reward": 4,
        "reward_name": "🗝️✨ Chìa Khóa Huyền Thoại"
    }
}

# --- 2. KHỞI TẠO STATE ---
if "game_state" not in st.session_state:
    st.session_state.game_state = "MENU"  # MENU, PLAYING, SETTINGS, CREDITS
    st.session_state.gold = 200
    st.session_state.hp = 100
    st.session_state.current_island = 1
    st.session_state.owned_keys = [1]
    st.session_state.inventory = []
    st.session_state.boat_level = 1
    st.session_state.nav_menu = "FISHING"

# =========================================================================
# GIAO DIỆN 1: MÀN HÌNH CHÍNH (MAIN MENU GIỐNG ẢNH MẪU)[cite: 3]
# =========================================================================
if st.session_state.game_state == "MENU":
    col_menu, col_scene = st.columns([1, 1.5])
    
    with col_menu:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="game-subtitle">A SURVIVAL FISHING ADVENTURE</div>
            <div class="game-title">HOW TO<br>CATCH<br>FISH</div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Các nút menu chính
        if st.button("▶ CONTINUE", key="btn_continue", use_container_width=True):
            st.session_state.game_state = "PLAYING"
            st.rerun()
            
        if st.button("★ NEW GAME", key="btn_newgame", use_container_width=True):
            st.session_state.gold = 200
            st.session_state.hp = 100
            st.session_state.current_island = 1
            st.session_state.owned_keys = [1]
            st.session_state.inventory = []
            st.session_state.boat_level = 1
            st.session_state.game_state = "PLAYING"
            st.rerun()
            
        if st.button("⚙ SETTINGS", key="btn_settings", use_container_width=True):
            st.session_state.game_state = "SETTINGS"
            st.rerun()
            
        if st.button("ℹ CREDITS", key="btn_credits", use_container_width=True):
            st.session_state.game_state = "CREDITS"
            st.rerun()
            
    with col_scene:
        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="island-view-box">
                <h1 style='font-size: 70px; margin: 0;'>🏝️</h1>
                <h3 style='color: #63b3ed; margin-top: 10px;'>Đại Dương Bao La & Đảo Hoang</h3>
                <p style='color: #a0aec0; font-size: 14px;'>Sẵn sàng giương buồm, câu cá và chinh phục các bí ẩn ngoài khơi xa.</p>
            </div>
        """, unsafe_allow_html=True)

# =========================================================================
# GIAO DIỆN 2: SETTINGS (CÀI ĐẶT)
# =========================================================================
elif st.session_state.game_state == "SETTINGS":
    st.title("⚙ Cài Đặt Trò Chơi")
    st.write("Tùy chỉnh âm thanh và đồ họa:")
    st.slider("Âm lượng nhạc nền", 0, 100, 80)
    st.slider("Độ phân giải / Hiệu ứng", 1, 3, 2)
    
    if st.button("⬅ Trở về Menu Chính"):
        st.session_state.game_state = "MENU"
        st.rerun()

# =========================================================================
# GIAO DIỆN 3: CREDITS (THÔNG TIN TÁC GIẢ)
# =========================================================================
elif st.session_state.game_state == "CREDITS":
    st.title("ℹ Thông Tin Nhà Phát Triển")
    st.markdown("""
    * **Tựa game:** How to Catch Fish[cite: 3]
    * **Thể loại:** Sinh tồn, Câu cá, Phiêu lưu khám phá đảo.
    * **Phát triển bởi:** Trí tuệ nhân tạo & Bạn.
    """)
    if st.button("⬅ Trở về Menu Chính"):
        st.session_state.game_state = "MENU"
        st.rerun()

# =========================================================================
# GIAO DIỆN 4: TRONG TRÒ CHƠI (GAMEPLAY CHÍNH)
# =========================================================================
elif st.session_state.game_state == "PLAYING":
    # Thanh tiêu đề phụ trong game & nút quay về menu
    c_head1, c_head2 = st.columns([4, 1])
    with c_head1:
        st.markdown("### 🎣 HOW TO CATCH FISH: ISLAND EXPLORER")
    with c_head2:
        if st.button("🏠 Thoát về Menu", use_container_width=True):
            st.session_state.game_state = "MENU"
            st.rerun()

    # Thanh thông số nhân vật
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 Vàng", f"{st.session_state.gold} 🪙")
    with c2:
        st.metric("❤️ Sinh Lực", f"{st.session_state.hp}/100")
    with c3:
        st.metric("🚤 Thuyền", f"Cấp {st.session_state.boat_level}")
    with c4:
        st.metric("🔑 Chìa Khóa", len(st.session_state.owned_keys))

    st.markdown("---")

    # Thanh menu điều hướng trong game
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

    # 1. Hồ câu cá & Săn Boss lấy chìa khóa
    if st.session_state.nav_menu == "FISHING":
        st.subheader(f"📍 Vị trí: {current_island_data['name']}")
        st.write(f"_{current_island_data['desc']}_")
        
        st.info(f"🎯 **Nhiệm vụ Đảo này:** Đánh bại Boss **{current_island_data['boss']}** để nhận **{current_island_data['reward_name']}**!")
        
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
                    win_chance = 40 + (st.session_state.boat_level * 15)
                    roll = random.randint(1, 100)
                    
                    if roll <= win_chance:
                        st.balloons()
                        st.success(f"💥 XUẤT SẮC! Bạn đã đánh bại **{current_island_data['boss']}**!")
                        target_key_id = current_island_data["key_id_reward"]
                        if target_key_id not in st.session_state.owned_keys:
                            st.session_state.owned_keys.append(target_key_id)
                            st.info(f"🗝️ Bạn đã nhặt được: **{current_island_data['reward_name']}**! Giờ bạn có thể lái thuyền sang đảo tiếp theo!")
                        else:
                            st.session_state.gold += 300
                            st.write("Nhận thêm phần thưởng **+300 🪙** vàng!")
                    else:
                        damage = random.randint(15, 30)
                        st.session_state.hp -= damage
                        st.error(f"💥 Boss phản đòn! Bạn bị mất **-{damage} HP**!")

    # 2. Bản đồ lái thuyền sang đảo
    elif st.session_state.nav_menu == "MAP":
        st.subheader("🗺️ Bản Đồ Đại Dương & Bến Tàu")
        st.write("Chọn hòn đảo muốn lái thuyền cập bến:")
        
        for island_id, data in ISLAND_DATA.items():
            st.markdown(f"""
                <div style='background-color: #1e293b; color: white; padding: 15px; border-radius: 10px; border-left: 6px solid #00d2ff; margin-bottom: 15px;'>
                    <h4 style='margin:0;'>{data['name']} ({data['difficulty']})</h4>
                    <p style='margin:5px 0 0 0; font-size: 14px;'>{data['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_m1, col_m2 = st.columns([2, 1])
            req_key = data["key_id_needed"]
            has_access = (req_key is None) or (req_key in st.session_state.owned_keys)
            
            with col_m1:
                if req_key is None:
                    st.caption("✅ Đảo Tân Thủ (Đã mở sẵn)")
                elif has_access:
                    st.caption("🔓 Đã có chìa khóa mở cổng đảo!")
                else:
                    st.caption(f"🔒 Cần chìa khóa: **{ISLAND_DATA[req_key - 1]['reward_name']}**")
                    
            with col_m2:
                if st.session_state.current_island == island_id:
                    st.button("📍 Đang ở đây", key=f"island_curr_{island_id}", disabled=True, use_container_width=True)
                else:
                    if st.button("⛵ Lái thuyền đến", key=f"island_goto_{island_id}", disabled=not has_access, use_container_width=True):
                        st.session_state.current_island = island_id
                        st.success(f"Đã di chuyển thuyền đến **{data['name']}**!")
                        st.rerun()

    # 3. Cửa hàng
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
                    st.success("Thuyền đã được nâng cấp!")
                    st.rerun()
                else:
                    st.error("Không đủ tiền vàng!")

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
                    st.error("Không đủ tiền vàng!")

    # 4. Kho đồ
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
