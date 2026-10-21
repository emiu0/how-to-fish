import streamlit as st
import streamlit.components.v1 as components

# Cấu hình giao diện Streamlit full màn hình
st.set_page_config(
    page_title="How to Fish - 3D Survival Edition",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn hoàn toàn header và footer mặc định của Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0rem !important;}
    body { overflow: hidden; background-color: #040914; }
    </style>
""", unsafe_allow_html=True)

# Mã nguồn HTML5 + Three.js 3D Game mô phỏng chính xác tựa game How to Fish
game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>How to Fish 3D</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body, html { width: 100%; height: 100%; overflow: hidden; font-family: 'Courier New', Courier, monospace; background: #040914; }
        #webgl-container { width: 100vw; height: 100vh; display: block; }
        
        /* MÀN HÌNH CHÍNH (MAIN MENU) */
        #mainMenu {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(90deg, rgba(4,9,20,0.95) 0%, rgba(4,9,20,0.5) 50%, rgba(4,9,20,0) 100%);
            display: flex; flex-direction: column; justify-content: center; padding-left: 8%;
            z-index: 100;
        }
        .game-subtitle { font-size: 13px; letter-spacing: 4px; color: #94a3b8; margin-bottom: 5px; border-left: 3px solid #f6ad55; padding-left: 10px; }
        .game-title { font-size: 64px; font-weight: 900; line-height: 0.92; color: #f6ad55; text-transform: uppercase; margin-bottom: 30px; text-shadow: 4px 4px 12px rgba(0,0,0,0.9); }
        .menu-btn {
            width: 240px; padding: 14px 22px; margin-bottom: 12px; background: rgba(15, 23, 42, 0.85); color: #e2e8f0;
            border: 1px solid #334155; border-radius: 4px; font-weight: bold; font-size: 16px; text-align: left;
            cursor: pointer; transition: all 0.2s ease; backdrop-filter: blur(6px);
        }
        .menu-btn:hover { background: #f6ad55; color: #040914; border-color: #f6ad55; transform: translateX(10px); }

        /* HUD THÔNG SỐ TRONG GAME */
        #hud {
            position: absolute; top: 15px; left: 15px; right: 15px; display: none; justify-content: space-between;
            background: rgba(11, 19, 30, 0.85); padding: 12px 25px; border-radius: 8px; border: 1px solid #1e293b; color: white;
            font-weight: bold; z-index: 10; backdrop-filter: blur(8px);
        }
        .hud-item { display: flex; align-items: center; gap: 8px; font-size: 16px; }

        /* BẢNG HÀNH ĐỘNG / TƯƠNG TÁC */
        #actionPrompt {
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.9); color: #38bdf8; padding: 12px 30px; border-radius: 30px;
            border: 2px solid #00d2ff; font-weight: bold; display: none; z-index: 20; text-align: center;
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.4); animation: pulse 1.5s infinite;
        }
        @keyframes pulse { 0% { transform: translateX(-50%) scale(1); } 50% { transform: translateX(-50%) scale(1.05); } 100% { transform: translateX(-50%) scale(1); } }

        /* KHUNG THÔNG BÁO */
        #msgBox {
            position: absolute; top: 100px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.95); color: #f8fafc; padding: 12px 30px; border-radius: 20px;
            border: 1px solid #f6ad55; font-weight: bold; display: none; z-index: 30; text-align: center;
        }
    </style>
    <!-- THƯ VIỆN THREE.JS 3D -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="webgl-container"></div>

    <!-- MÀN HÌNH CHÍNH -->
    <div id="mainMenu">
        <div class="game-subtitle">A SURVIVAL FISHING ADVENTURE</div>
        <div class="game-title">HOW TO<br>FISH</div>
        <button class="menu-btn" onclick="startGame()">▶ NEW GAME</button>
        <button class="menu-btn" onclick="startGame()">★ CONTINUE</button>
        <button class="menu-btn" onclick="alert('Hướng dẫn: Dùng phím W, A, S, D hoặc Mũi Tên để lái thuyền trên biển 3D. Lái sát vào Đảo và bấm [SPACE] để câu cá hoặc bắn quái vật lấy chìa khóa!')">⚙ SETTINGS</button>
    </div>

    <!-- HUD TRONG GAME -->
    <div id="hud">
        <div class="hud-item">💰 Vàng: <span id="goldVal">250</span></div>
        <div class="hud-item">❤️ HP: <span id="hpVal">100</span></div>
        <div class="hud-item">🔫 Vũ Khí: <span id="weaponVal">Cần Câu / Súng</span></div>
        <div class="hud-item">🔑 Chìa Khóa: <span id="keyVal">1/3</span></div>
        <div class="hud-item">📍 Đảo: <span id="islandVal">Đảo Tân Thủ</span></div>
    </div>

    <div id="actionPrompt">Bấm [SPACE] để thả cần câu / Tấn công Boss!</div>
    <div id="msgBox"></div>

<script>
let scene, camera, renderer;
let boat3D, ocean;
let islands = [];
let inMenu = true;

// Trò chơi state
let gold = 250, hp = 100, boatLevel = 1;
let keysOwned = [1];
let currentIslandIdx = 0;

const boatState = { x: 0, z: 0, angle: 0, speed: 0, maxSpeed: 0.5, accel: 0.02, friction: 0.95 };
const keys = {};

window.addEventListener('keydown', e => keys[e.code] = true);
window.addEventListener('keyup', e => keys[e.code] = false);

// --- DỮ LIỆU ĐẢO & BOSS ---
const islandList = [
    { name: "Đảo Tân Thủ", x: -50, z: -50, color: 0x15803d, boss: "🦈 Cá Trê Khổng Lồ", keyReq: null, rewardKey: 2 },
    { name: "Đảo San Hò", x: 60, z: -60, color: 0x0284c7, boss: "🐊 Cá Sấu Nước Mặn", keyReq: 2, rewardKey: 3 },
    { name: "Đảo Quái Vật", x: 10, z: 80, color: 0xb91c1c, boss: "🐉 Thủy Quái Leviathan", keyReq: 3, rewardKey: 4 }
];

function init3D() {
    const container = document.getElementById('webgl-container');

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x040914);
    scene.fog = new THREE.FogExp2(0x040914, 0.006);

    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 25, 40);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // Ánh sáng
    const ambientLight = new THREE.AmbientLight(0x94a3b8, 0.7);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xf8fafc, 1.0);
    dirLight.position.set(100, 150, 50);
    scene.add(dirLight);

    // Mặt nước biển 3D
    const oceanGeo = new THREE.PlaneGeometry(600, 600, 32, 32);
    const oceanMat = new THREE.MeshPhongMaterial({ color: 0x0f172a, shininess: 90, flatShading: true });
    ocean = new THREE.Mesh(oceanGeo, oceanMat);
    ocean.rotation.x = -Math.PI / 2;
    scene.add(ocean);

    // Tạo các hòn đảo 3D low-poly
    islandList.forEach((islData, idx) => {
        const islandGroup = new THREE.Group();
        islandGroup.position.set(islData.x, 0, islData.z);

        // Đất đảo
        const landGeo = new THREE.CylinderGeometry(28, 35, 10, 16);
        const landMat = new THREE.MeshLambertMaterial({ color: islData.color });
        const land = new THREE.Mesh(landGeo, landMat);
        land.position.y = 3;
        islandGroup.add(land);

        // Cây cối low-poly trên đảo
        for(let i=0; i<6; i++) {
            const treeGeo = new THREE.ConeGeometry(3, 10, 5);
            const treeMat = new THREE.MeshLambertMaterial({ color: 0x14532d });
            const tree = new THREE.Mesh(treeGeo, treeMat);
            const angle = Math.random() * Math.PI * 2;
            const r = Math.random() * 18;
            tree.position.set(Math.cos(angle)*r, 10, Math.sin(angle)*r);
            islandGroup.add(tree);
        }

        scene.add(islandGroup);
        islands.push({ group: islandGroup, data: islData, radius: 32 });
    });

    // Tạo Thuyền 3D & Nhân vật Low-poly (phong cách How to Fish)
    boat3D = new THREE.Group();
    
    // Thân thuyền
    const boatGeo = new THREE.BoxGeometry(4, 2, 10);
    const boatMat = new THREE.MeshLambertMaterial({ color: 0x7c2d12 });
    const boatMesh = new THREE.Mesh(boatGeo, boatMat);
    boatMesh.position.y = 1;
    boat3D.add(boatMesh);

    // Nhân vật hình nộm (Puppet character trên thuyền)
    const bodyGeo = new THREE.CylinderGeometry(0.8, 0.8, 4);
    const bodyMat = new THREE.MeshLambertMaterial({ color: 0x1e3a8a }); // Áo xanh đặc trưng
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.set(0, 3.5, 0);
    boat3D.add(body);

    // Đầu nhân vật
    const headGeo = new THREE.SphereGeometry(1, 8, 8);
    const headMat = new THREE.MeshLambertMaterial({ color: 0xfde047 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.set(0, 6, 0);
    boat3D.add(head);

    boat3D.position.set(0, 0, 0);
    scene.add(boat3D);

    window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function startGame() {
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById('hud').style.display = 'flex';
    inMenu = false;
    showMsg("⛵ Lái thuyền đến các hòn đảo và tiêu diệt Boss để lấy chìa khóa!");
}

function showMsg(txt, duration = 3500) {
    const box = document.getElementById('msgBox');
    box.innerText = txt;
    box.style.display = 'block';
    setTimeout(() => { box.style.display = 'none'; }, duration);
}

// --- GAME LOOP 3D ---
function animate() {
    requestAnimationFrame(animate);

    if (inMenu) {
        // Camera xoay quanh cảnh đại dương 3D ở Menu
        const t = Date.now() * 0.0004;
        camera.position.x = Math.sin(t) * 70;
        camera.position.z = Math.cos(t) * 70;
        camera.position.y = 35;
        camera.lookAt(0, 0, 0);
    } else {
        // Điều khiển lái thuyền 3D
        if (keys['KeyW'] || keys['ArrowUp']) boatState.speed = Math.min(boatState.speed + boatState.accel, boatState.maxSpeed);
        else if (keys['KeyS'] || keys['ArrowDown']) boatState.speed = Math.max(boatState.speed - boatState.accel, -boatState.maxSpeed / 2);
        else boatState.speed *= boatState.friction;

        if (keys['KeyA'] || keys['ArrowLeft']) boatState.angle += 0.035;
        if (keys['KeyD'] || keys['ArrowRight']) boatState.angle -= 0.035;

        boatState.x += Math.sin(boatState.angle) * boatState.speed;
        boatState.z += Math.cos(boatState.angle) * boatState.speed;

        boat3D.position.x = boatState.x;
        boat3D.position.z = boatState.z;
        boat3D.rotation.y = boatState.angle;

        // Camera đi theo thuyền góc nhìn thứ ba
        camera.position.x = boatState.x - Math.sin(boatState.angle) * 30;
        camera.position.z = boatState.z - Math.cos(boatState.angle) * 30;
        camera.position.y = 18;
        camera.lookAt(boatState.x, 2, boatState.z);

        // Kiểm tra va chạm gần đảo để câu cá/săn boss
        let nearIsland = false;
        islands.forEach((isl, idx) => {
            const dx = boatState.x - isl.data.x;
            const dz = boatState.z - isl.data.z;
            const dist = Math.sqrt(dx*dx + dz*dz);

            if (dist < isl.radius + 6) {
                nearIsland = true;
                currentIslandIdx = idx;
                
                const promptBox = document.getElementById('actionPrompt');
                promptBox.style.display = 'block';
                promptBox.innerText = "⚓ Bấm [SPACE] để săn Boss " + isl.data.boss + " tại " + isl.data.name + "!";

                if (keys['Space']) {
                    if (isl.data.keyReq && !keysOwned.includes(isl.data.keyReq)) {
                        showMsg("🔒 Đảo này đã bị khóa! Cần đánh bại Boss ở đảo trước để mở.");
                    } else {
                        triggerBossBattle(isl.data);
                    }
                }
            }
        });

        if (!nearIsland) {
            document.getElementById('actionPrompt').style.display = 'none';
        }
    }

    // Cập nhật thông số HUD
    document.getElementById('goldVal').innerText = gold;
    document.getElementById('hpVal').innerText = hp;
    document.getElementById('keyVal').innerText = keysOwned.length + "/3";
    document.getElementById('islandVal').innerText = islandList[currentIslandIdx].name;

    renderer.render(scene, camera);
}

function triggerBossBattle(isl) {
    if (Math.random() < 0.75) {
        if (!keysOwned.includes(isl.rewardKey)) {
            keysOwned.push(isl.rewardKey);
            showMsg("🎉 CHIẾN THẮNG! Bạn đã bắn hạ " + isl.boss + " và nhận được Chìa Khóa mới!", 4500);
        } else {
            gold += 300;
            showMsg("🎉 Tiêu diệt Boss thành công! Nhận thêm +300 🪙 Vàng!", 3500);
        }
    } else {
        hp -= 25;
        showMsg("💥 Boss phản công dữ dội! Thuyền bị hư hại mất -25 HP!", 3500);
        if (hp <= 0) {
            alert("Bạn đã cạn kiệt HP! Trò chơi kết thúc.");
            location.reload();
        }
    }
    keys['Space'] = false; // Chống lặp phím liên tục
}

// Khởi chạy 3D Engine
init3D();
animate();
</script>
</body>
</html>
"""

# Nhúng game vào Streamlit qua component HTML
components.html(game_code, height=780, scrolling=False)
