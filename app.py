import random
import time
import streamlit as st

# Cấu hình trang web
st.set_page_config(page_title="How to Fish - Island Adventure", page_icon="🎣", layout="centered")

# Giao diện CSS tùy chỉnh
st.markdown("""
    <style>
    .banner-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    .island-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1E88E5;
        padding: 12px 15px;
        border-radius: 6px;
        margin-bottom: 12px;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. DỮ LIỆU CÁC ĐẢO & BOSS ---
ISLANDS = {
    1: {
        "name": "🏝️ Đảo Tân Thủ (Green Lake)",
        "difficulty": "Dễ",
        "desc": "Vùng hồ yên bình, thích hợp cho người mới học câu cá.",
        "fishes": ["🐟 Cá Rô Phi", "🐠 Cá Bảy Màu", "🦐 Tôm Sông"],
        "boss": "🦈 Cá Trê Khổng Lồ",
        "key_needed": None,
        "key_reward": "Chìa khóa Đảo San Hò 🗝️"
    },
    2: {
        "name": "🪸 Đảo San Hò (Coral Atoll)",
        "difficulty": "Trung bình",
        "desc": "Vùng biển sâu với các loài sinh vật ngầm nguy hiểm.",
        "fishes": ["🐟 Cá Hồi Đại Dương", "🐙 Bạch Tuộc Nhỏ", "🦀 Cua Hoàng Gia"],
        "boss": "🐊 Cá Sấu Nước Mặn",
        "key_needed": "Chìa khóa Đảo San Hò 🗝️",
        "key_reward": "Chìa khóa Đảo Quái Vật 🔑"
    },
    3: {
        "name": "🌋 Đảo Quái Vật (Volcano Isle)",
        "difficulty": "Khó",
        "desc": "Vùng biển dung nham nóng rực, sào huyệt của thủy quái.",
        "fishes": ["🦈 Cá Mập Xám", "🦑 Mực Ống Khổng Lồ", "🐍 Rắn Biển Độc"],
        "boss": "🐉 Thủy Quái Leviathan",
        "key_needed": "Chìa khóa Đảo Quái Vật 🔑",
        "key_reward": "Chìa khóa Đảo Băng Giá 🗝️✨"
    }
}

# --- 2. KHỞI TẠO SESSION STATE ---
if "gold" not in st.session_state:
    st.session_state.gold = 150
    st.session_state.hp = 100
    st.session_state.current_island = 1
    st.session_state.keys = []
    st.session_state.inventory = []
    st.session_state.boat_level = 1
    st.session_state.menu = "FISHING"

# --- 3. BANNER TIÊU ĐỀ ---
st.markdown("""
    <div class="banner-box">
        <h1 style='margin:0; font-size: 28px;'>🎣 HOW TO FISH: ISLAND ADVENTURE</h1>
        <p style='margin-top:5px; font-style: italic;'>Khám phá đảo • Săn Boss cá lớn • Thu thập chìa khóa lái thuyền!</p>
    </div>
""", unsafe_allow_html=True)

# Thanh chỉ số trên cùng
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Vàng", f"{st.session_state.gold} 🪙")
with col2:
    st.metric("❤️ HP", f"{st.session_state.hp}/100")
with col3:
    st.metric("🚤 Thuyền", f"Cấp {st.session_state.boat_level}")
with col4:
    st.metric("🔑 Chìa khóa", len(st.session_state.keys))

st.markdown("---")

# --- 4. MENU ĐIỀU HƯỚNG CHÍNH ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    if st.button("🎣 Hồ Câu", use_container_width=True):
        st.session_state.menu = "FISHING"
        st.rerun()
with m2:
    if st.button("🗺️ Bản Đồ Đảo", use_container_width=True):
        st.session_state.menu = "MAP"
        st.rerun()
with m3:
    if st.button("🛒 Cửa Hàng", use_container_width=True):
        st.session_state.menu = "SHOP"
        st.rerun()
with m4:
    if st.button("🎒 Kho Đồ", use_container_width=True):
        st.session_state.menu = "INVENTORY"
        st.rerun()

st.markdown("---")

current_map = ISLANDS[st.session_state.current_island]

# --- 5. MÀN HÌNH CÂU CÁ & SĂN BOSS ---
if st.session_state.menu == "FISHING":
    st.subheader(f"📍 Đang ở: {current_map['name']}")
    st.write(f"_{current_map['desc']}_")
    
    st.info(f"🎯 **Mục tiêu Boss trên đảo này:** Săn **{current_map['boss']}** để nhận **{current_map['key_reward']}**!")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        if st.button("🎣 Thả cần câu cá thường", use_container_width=True):
            with st.spinner("Đang chờ cá cắn câu..."):
                time.sleep(0.8)
                fish = random.choice(current_map["fishes"])
                earned = random.randint(25, 50) * st.session_state.current_island
                st.session_state.gold += earned
                st.session_state.inventory.append(fish)
                st.success(f"🎉 Bạn bắt được **{fish}** và bán được **+{earned} 🪙**!")

    with col_f2:
        if st.button(f"⚔️ Săn Boss ({current_map['boss']})", use_container_width=True):
            with st.spinner("Giao chiến căng thẳng với cá lớn..."):
                time.sleep(1.2)
                win_chance = 45 + (st.session_state.boat_level * 15)
                roll = random.randint(1, 100)
                
                if roll <= win_chance:
                    reward = current_map["key_reward"]
                    st.balloons()
                    st.success(f"💥 THẮNG LỢI! Bạn đã hạ gục thành công **{current_map['boss']}**!")
                    
                    if reward not in st.session_state.keys:
                        st.session_state.keys.append(reward)
                        st.info(f"🗝️ Bạn nhận được phần thưởng quan trọng: **{reward}**!")
                    else:
                        st.session_state.gold += 300
                        st.write("Nhận thêm thưởng **+300 🪙** vàng!")
                else:
                    dmg = random.randint(15, 30)
                    st.session_state.hp -= dmg
                    st.error(f"💥 Boss phản đòn quá mạnh! Bạn bị mất **-{dmg} HP**!")
                    if st.session_state.hp <= 0:
                        st.error("💀 Bạn đã ngất xỉu vì hết máu! Hãy vào cửa hàng hồi phục ngay.")

# --- 6. MÀN HÌNH BẢN ĐỒ LÁI THUYỀN SANG ĐẢO ---
elif st.session_state.menu == "MAP":
    st.subheader("🗺️ Bản Đồ Hàng Hải & Chọn Đảo")
    st.write("Sử dụng chìa khóa thu thập được để lái thuyền sang các vùng đất mới:")
    
    for island_id, data in ISLANDS.items():
        st.markdown(f"""
            <div class="island-card">
                <b>{data['name']}</b> ({data['difficulty']})<br>
                <small>{data['desc']}</small>
            </div>
        """, unsafe_allow_html=True)
        
        c_m1, c_m2 = st.columns([2, 1])
        with c_m1:
            if data["key_needed"] is None:
                st.caption("✅ Vùng biển tự do")
            else:
                if data["key_needed"] in st.session_state.keys:
                    st.caption(f"🔓 Đã có điều kiện mở khóa ({data['key_needed']})")
                else:
                    st.caption(f"🔒 Cần: {data['key_needed']}")
                    
        with c_m2:
            if st.session_state.current_island == island_id:
                st.button("📍 Đang đứng đây", key=f"btn_pos_{island_id}", disabled=True)
            else:
                can_travel = (data["key_needed"] is None) or (data["key_needed"] in st.session_state.keys)
                if st.button("⛵ Lái thuyền", key=f"btn_travel_{island_id}", disabled=not can_travel):
                    st.session_state.current_island = island_id
                    st.success(f"Đã lái thuyền cập bến **{data['name']}** thành công!")
                    st.rerun()

# --- 7. MÀN HÌNH CỬA HÀNG ---
elif st.session_state.menu == "SHOP":
    st.subheader("🛒 Cửa Hàng Nâng Cấp & Hồi Phục")
    
    s1, s2 = st.columns(2)
    with s1:
        st.write("**🚤 Nâng cấp Thuyền**")
        boat_cost = st.session_state.boat_level * 250
        st.write(f"Cấp: {st.session_state.boat_level} | Giá: **{boat_cost} 🪙**")
        if st.button("Nâng cấp Thuyền ngay"):
            if st.session_state.gold >= boat_cost:
                st.session_state.gold -= boat_cost
                st.session_state.boat_level += 1
                st.success("Thuyền đã được nâng cấp vững chắc hơn!")
                st.rerun()
            else:
                st.error("Không đủ tiền vàng!")
                
    with s2:
        st.write("**❤️ Hồi phục HP (+50)**")
        st.write("Giá: **70 🪙**")
        if st.button("Mua bình máu"):
            if st.session_state.gold >= 70:
                st.session_state.gold -= 70
                st.session_state.hp = min(100, st.session_state.hp + 50)
                st.success("Đã hồi phục 50 HP thành công!")
                st.rerun()
            else:
                st.error("Không đủ tiền vàng!")

# --- 8. MÀN HÌNH KHO ĐỒ ---
elif st.session_state.menu == "INVENTORY":
    st.subheader("🎒 Kho Đồ & Chìa Khóa Hành Trình")
    
    st.markdown("#### 🗝️ Chìa Khóa Đảo:")
    if st.session_state.keys:
        for k in st.session_state.keys:
            st.write(f"- {k}")
    else:
        st.write("Chưa sở hữu chìa khóa nào. Hãy đi săn Boss ở Hồ Câu!")
        
    st.markdown("---")
    st.markdown("#### 🐟 Bộ Sưu Tập Cá Đã Câu Được:")
    if st.session_state.inventory:
        st.write(", ".join(set(st.session_state.inventory)))
    else:
        st.write("Kho cá đang trống.")
